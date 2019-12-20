
/**
 * @file A simple WebGL example for viewing meshes read from OBJ files
 * @author Eric Shaffer <shaffer1@illinois.edu>  
 */

/** @global The WebGL context */
var gl;

/** @global The HTML5 canvas we draw on */
var canvas;

/** @global A simple GLSL shader program */
var shaderProgram;

/** @global Shader program from skybox */
var shaderProgramSB; 

/** @global The Modelview matrix */
var mvMatrix = mat4.create();

/** @global The View matrix */
var vMatrix = mat4.create();

/** @global The Projection matrix */
var pMatrix = mat4.create();

/** @global The Normal matrix */
var nMatrix = mat3.create();

/** @global The matrix stack for hierarchical modeling */
var mvMatrixStack = [];

/** @global An object holding the geometry for a 3D mesh */
var myMesh;


// View parameters
/** @global Location of the camera in world coordinates */
var eyePt = vec3.fromValues(0.0,0.0,2.0);
/** @global Direction of the view in world coordinates */
var viewDir = vec3.fromValues(0.0,0.0,-1.0);
/** @global Up vector for view matrix creation, in world coordinates */
var up = vec3.fromValues(0.0,1.0,0.0);
/** @global Location of a point along viewDir in world coordinates */
var viewPt = vec3.fromValues(0.0,0.0,0.0);



//Light parameters
/** @global Light position in VIEW coordinates */
var lightPosition = [10,10,10];
/** @global Ambient light color/intensity for Phong reflection */
var lAmbient = [0,0,0];
/** @global Diffuse light color/intensity for Phong reflection */
var lDiffuse = [1,1,1];
/** @global Specular light color/intensity for Phong reflection */
var lSpecular =[0,0,0];

//Material parameters
/** @global Ambient material color/intensity for Phong reflection */
var kAmbient = [1.0,1.0,1.0];
/** @global Diffuse material color/intensity for Phong reflection */
var kTerrainDiffuse = [205.0/255.0,163.0/255.0,63.0/255.0];
/** @global Specular material color/intensity for Phong reflection */
var kSpecular = [0.0,0.0,0.0];
/** @global Shininess exponent for Phong reflection */
var shininess = 23;
/** @global Edge color fpr wireframeish rendering */
var kEdgeBlack = [0.0,0.0,0.0];
/** @global Edge color for wireframe rendering */
var kEdgeWhite = [1.0,1.0,1.0];


//Model parameters
//Orbit angle
var eulerY=0;
/** Teapot Rotation Angle */
var rotY = 0;

// Create a place to store cube geometry
var cubeVertexBuffer;

//Texture Parameters

var cubeImage;
var cubeTexture;



//Buffer Locations

var vertexLocation;
var skyboxLocation;
var invVdpLocation;


var reflectOn= true;

//-------------------------------------------------------------------------
/**
 * Asynchronously read a server-side text file
 */
function asyncGetFile(url) {
  //Your code here
    console.log("Getting text file");
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open("GET", url);
      xhr.onload = () => resolve(xhr.responseText);
      xhr.onerror = () => reject(xhr.statusText);
      xhr.send();
      console.log("Made promise");
    });
}

//-------------------------------------------------------------------------
/**
 * Sends Modelview matrix to shader
 */
function uploadModelViewMatrixToShader() {
  gl.uniformMatrix4fv(shaderProgram.mvMatrixUniform, false, mvMatrix);
}

//-------------------------------------------------------------------------
/**
 * Sends projection matrix to shader
 */
function uploadProjectionMatrixToShader() {
  gl.uniformMatrix4fv(shaderProgram.pMatrixUniform, 
                      false, pMatrix);
}

//-------------------------------------------------------------------------
/**
 * Generates and sends the normal matrix to the shader
 */
function uploadNormalMatrixToShader() {
  mat3.fromMat4(nMatrix,mvMatrix);
  mat3.transpose(nMatrix,nMatrix);
  mat3.invert(nMatrix,nMatrix);
  gl.uniformMatrix3fv(shaderProgram.nMatrixUniform, false, nMatrix);
}

//-------------------------------------------------------------------------
/**
* Sends Modelview matrix to shader
*/
function uploadModelViewMatrixToShaderSB() {
gl.uniformMatrix4fv(shaderProgramSB.mvMatrixUniform, false, mvMatrix);
}
  
//-------------------------------------------------------------------------
/**
* Sends projection matrix to shader
*/
function uploadProjectionMatrixToShaderSB() {
gl.uniformMatrix4fv(shaderProgramSB.pMatrixUniform, 
                    false, pMatrix);
}
  
//-------------------------------------------------------------------------
/**
* Generates and sends the normal matrix to the shader
*/
function uploadNormalMatrixToShaderSB() {
mat3.fromMat4(nMatrix,mvMatrix);
mat3.transpose(nMatrix,nMatrix);
mat3.invert(nMatrix,nMatrix);
gl.uniformMatrix3fv(shaderProgramSB.nMatrixUniform, false, nMatrix);
}


//----------------------------------------------------------------------------------
/**
* Pushes matrix onto modelview matrix stack
*/
function mvPushMatrix() {
    var copy = mat4.clone(mvMatrix);
    mvMatrixStack.push(copy);
}


//----------------------------------------------------------------------------------
/**
 * Pops matrix off of modelview matrix stack
 */
function mvPopMatrix() {
    if (mvMatrixStack.length == 0) {
      throw "Invalid popMatrix!";
    }
    mvMatrix = mvMatrixStack.pop();
}

//----------------------------------------------------------------------------------
/**
 * Sends projection/modelview matrices to shader
 */
function setMatrixUniforms() {
    uploadModelViewMatrixToShader();
    uploadNormalMatrixToShader();
    uploadProjectionMatrixToShader();
}

//----------------------------------------------------------------------------------
/**
 * Sends projection/modelview matrices to shader
 */
function setMatrixUniformsSB() {
    uploadModelViewMatrixToShaderSB();
    uploadProjectionMatrixToShaderSB();
}

//----------------------------------------------------------------------------------
/**
 * Translates degrees to radians
 * @param {Number} degrees Degree input to function
 * @return {Number} The radians that correspond to the degree input
 */
function degToRad(degrees) {
        return degrees * Math.PI / 180;
}

//----------------------------------------------------------------------------------
/**
 * Creates a context for WebGL
 * @param {element} canvas WebGL canvas
 * @return {Object} WebGL context
 */
function createGLContext(canvas) {
  var names = ["webgl", "experimental-webgl"];
  var context = null;
  for (var i=0; i < names.length; i++) {
    try {
      context = canvas.getContext(names[i]);
    } catch(e) {}
    if (context) {
      break;
    }
  }
  if (context) {
    context.viewportWidth = canvas.width;
    context.viewportHeight = canvas.height;
  } else {
    alert("Failed to create WebGL context!");
  }
  return context;
}

//----------------------------------------------------------------------------------
/**
 * Loads Shaders
 * @param {string} id ID string for shader to load. Either vertex shader/fragment shader
 */
function loadShaderFromDOM(id) {
  var shaderScript = document.getElementById(id);
  
  // If we don't find an element with the specified id
  // we do an early exit 
  if (!shaderScript) {
    return null;
  }
  
  // Loop through the children for the found DOM element and
  // build up the shader source code as a string
  var shaderSource = "";
  var currentChild = shaderScript.firstChild;
  while (currentChild) {
    if (currentChild.nodeType == 3) { // 3 corresponds to TEXT_NODE
      shaderSource += currentChild.textContent;
    }
    currentChild = currentChild.nextSibling;
  }
 
  var shader;
  if (shaderScript.type == "x-shader/x-fragment") {
    shader = gl.createShader(gl.FRAGMENT_SHADER);
  } else if (shaderScript.type == "x-shader/x-vertex") {
    shader = gl.createShader(gl.VERTEX_SHADER);
  } else {
    return null;
  }
 
  gl.shaderSource(shader, shaderSource);
  gl.compileShader(shader);
 
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    alert(gl.getShaderInfoLog(shader));
    return null;
  } 
  return shader;
}

//----------------------------------------------------------------------------------
/**
 * Setup the fragment and vertex shaders for teapot
 */
function setupShaders() {
  vertexShader = loadShaderFromDOM("shader-vs");
  fragmentShader = loadShaderFromDOM("shader-fs");
  
  shaderProgram = gl.createProgram();
  gl.attachShader(shaderProgram, vertexShader);
  gl.attachShader(shaderProgram, fragmentShader);
  gl.linkProgram(shaderProgram);

  if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    alert("Failed to setup shaders");
  }

  gl.useProgram(shaderProgram);

  shaderProgram.vertexPositionAttribute = gl.getAttribLocation(shaderProgram, "aVertexPosition");
  gl.enableVertexAttribArray(shaderProgram.vertexPositionAttribute);

  shaderProgram.vertexNormalAttribute = gl.getAttribLocation(shaderProgram, "aVertexNormal");
  gl.enableVertexAttribArray(shaderProgram.vertexNormalAttribute);

  shaderProgram.mvMatrixUniform = gl.getUniformLocation(shaderProgram, "uMVMatrix");
  shaderProgram.pMatrixUniform = gl.getUniformLocation(shaderProgram, "uPMatrix");
  shaderProgram.nMatrixUniform = gl.getUniformLocation(shaderProgram, "uNMatrix");
  shaderProgram.uniformLightPositionLoc = gl.getUniformLocation(shaderProgram, "uLightPosition");    
  shaderProgram.uniformAmbientLightColorLoc = gl.getUniformLocation(shaderProgram, "uAmbientLightColor");  
  shaderProgram.uniformDiffuseLightColorLoc = gl.getUniformLocation(shaderProgram, "uDiffuseLightColor");
  shaderProgram.uniformSpecularLightColorLoc = gl.getUniformLocation(shaderProgram, "uSpecularLightColor");
  shaderProgram.uniformShininessLoc = gl.getUniformLocation(shaderProgram, "uShininess");    
  shaderProgram.uniformAmbientMaterialColorLoc = gl.getUniformLocation(shaderProgram, "uKAmbient");  
  shaderProgram.uniformDiffuseMaterialColorLoc = gl.getUniformLocation(shaderProgram, "uKDiffuse");
  shaderProgram.uniformSpecularMaterialColorLoc = gl.getUniformLocation(shaderProgram, "uKSpecular");

  shaderProgram.uniformTextureLoc = gl.getUniformLocation(shaderProgram, "utexture");
  shaderProgram.uniformEyePtLoc = gl.getUniformLocation(shaderProgram, "uEyePt");

  shaderProgram.uniformReflectOnLoc = gl.getUniformLocation(shaderProgram, "uReflectOn");
}


/**
 * Setup the fragment and vertex shaders for skybox
 */
function setupShadersSB() {
    vertexShader = loadShaderFromDOM("shader-vs_SB");
    fragmentShader = loadShaderFromDOM("shader-fs_SB");
    
    shaderProgramSB = gl.createProgram();
    gl.attachShader(shaderProgramSB, vertexShader);
    gl.attachShader(shaderProgramSB, fragmentShader);
    gl.linkProgram(shaderProgramSB);
  
    if (!gl.getProgramParameter(shaderProgramSB, gl.LINK_STATUS)) {
      alert("Failed to setup shaders");
    }
  
    gl.useProgram(shaderProgramSB);
  
    
    
    shaderProgramSB.mvMatrixUniform = gl.getUniformLocation(shaderProgramSB, "uMVMatrix");
    shaderProgramSB.pMatrixUniform = gl.getUniformLocation(shaderProgramSB, "uPMatrix");
  
    vertexPositionLocation = gl.getAttribLocation(shaderProgramSB, "aVertexPositionSB");
  
    // lookup uniforms
    skyboxLocation = gl.getUniformLocation(shaderProgramSB, "uskybox");
    invVdpLocation = gl.getUniformLocation(shaderProgramSB, "uinvVdp");
  }


//-------------------------------------------------------------------------
/**
 * Sends material information to the shader
 * @param {Float32} alpha shininess coefficient
 * @param {Float32Array} a Ambient material color
 * @param {Float32Array} d Diffuse material color
 * @param {Float32Array} s Specular material color
 */
function setMaterialUniforms(alpha,a,d,s) {
  gl.uniform1f(shaderProgram.uniformShininessLoc, alpha);
  gl.uniform3fv(shaderProgram.uniformAmbientMaterialColorLoc, a);
  gl.uniform3fv(shaderProgram.uniformDiffuseMaterialColorLoc, d);
  gl.uniform3fv(shaderProgram.uniformSpecularMaterialColorLoc, s);
}

//-------------------------------------------------------------------------
/**
 * Sends light information to the shader
 * @param {Float32Array} loc Location of light source
 * @param {Float32Array} a Ambient light strength
 * @param {Float32Array} d Diffuse light strength
 * @param {Float32Array} s Specular light strength
 */
function setLightUniforms(loc,a,d,s) {
  gl.uniform3fv(shaderProgram.uniformLightPositionLoc, loc);
  gl.uniform3fv(shaderProgram.uniformAmbientLightColorLoc, a);
  gl.uniform3fv(shaderProgram.uniformDiffuseLightColorLoc, d);
  gl.uniform3fv(shaderProgram.uniformSpecularLightColorLoc, s);
}

//----------------------------------------------------------------------------------
/**
 * Populate buffers with data
 */
function setupMesh(filename) {
   //Your code here
   myMesh = new TriMesh();
   myPromise = asyncGetFile(filename);
   myPromise.then((retrievedText) =>{
    myMesh.loadFromOBJ(retrievedText);
    //myMesh.printBuffers();
    console.log("Yay! got the file");
  })

  .catch(
    (reason) => {
      console.log('Handle rejected promis ('+reason+') here');
    });
}

//----------------------------------------------------------------------------------
/**
 * Draw call that applies matrix transformations to model and draws model in frame
 */
function draw() { 
    //console.log("function draw()")
  
    gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // We'll use perspective 
    mat4.perspective(pMatrix,degToRad(45), 
                     gl.viewportWidth / gl.viewportHeight,
                     5, 500.0);

    // We want to look down -z, so create a lookat point in that direction    
    //vec3.add(viewPt, eyePt, viewDir);
    //console.log("eyePt: ", eyePt);
    // Then generate the lookat matrix and initialize the view matrix to that view
    mat4.lookAt(vMatrix,eyePt,viewPt,up);
    
    viewPt = [0,0,0];
    eyePt = [8*Math.sin(degToRad(eulerY)),1,8*Math.cos(degToRad(eulerY))];

    gl.useProgram(shaderProgram);
    //Set uniform for EyePt
    gl.uniform3fv(shaderProgram.uniformEyePtLoc, eyePt);
    //Draw Teapot
    //ADD an if statement to prevent early drawing of myMesh
        gl.useProgram(shaderProgram);
        mvPushMatrix();
        
        mat4.rotateY(mvMatrix, mvMatrix, degToRad(rotY));;
        //mat4.multiply(mvMatrix,vMatrix,mvMatrix);
        mat4.lookAt(mvMatrix,eyePt,viewPt,up);
        
        setMatrixUniforms();
        setLightUniforms(lightPosition,lAmbient,lDiffuse,lSpecular);
    
        if ((document.getElementById("polygon").checked) || (document.getElementById("wirepoly").checked))
        {
            setMaterialUniforms(shininess,kAmbient,
                                kTerrainDiffuse,kSpecular); 
            myMesh.drawTriangles();
        }
    
        if(document.getElementById("wirepoly").checked)
        {   
            setMaterialUniforms(shininess,kAmbient,
                                kEdgeBlack,kSpecular);
            myMesh.drawEdges();
        }   

        if(document.getElementById("wireframe").checked)
        {
            setMaterialUniforms(shininess,kAmbient,
                                kEdgeWhite,kSpecular);
            myMesh.drawEdges();
        }
        
        if(document.getElementById("reflectOn").checked)
        {
          reflectOn=true;
        }

        if (document.getElementById("reflectOff").checked)
        {
          reflectOn=false;
        }

        gl.uniform1i(shaderProgram.uniformReflectOnLoc, reflectOn);

        //Set texture uniforms
        gl.uniform1i(shaderProgram.uniformTextureLoc,0);


        mvPopMatrix();

    //Draw skybox
    gl.useProgram(shaderProgramSB);

 
    //Draw 
    mvPushMatrix();
    
    
    //mat4.rotateX(mvMatrix,mvMatrix,modelYRotationRadians);
    mat4.rotateY(mvMatrix,mvMatrix,degToRad(-eulerY));
    
    setMatrixUniformsSB();    
    drawCube();
    mvPopMatrix();
    
  
}

//----------------------------------------------------------------------------------
//Code to handle user interaction
var currentlyPressedKeys = {};

function handleKeyDown(event) {
        //console.log("Key down ", event.key, " code ", event.code);
        currentlyPressedKeys[event.key] = true;
          if (currentlyPressedKeys["a"]) {
            // key A
            eulerY-= 1;
        } else if (currentlyPressedKeys["d"]) {
            // key D
            eulerY+= 1;
        } 
    
        if (currentlyPressedKeys["ArrowUp"]){
            // Up cursor key
            event.preventDefault();
            rotY+= 1;
        } else if (currentlyPressedKeys["ArrowDown"]){
            event.preventDefault();
            // Down cursor key
            rotY-= 1;
        } 
    
}

function handleKeyUp(event) {
        //console.log("Key up ", event.key, " code ", event.code);
        currentlyPressedKeys[event.key] = false;
}

//----------------------------------------------------------------------------------
/**
 * Startup function called from html code to start program.
 */
 function startup() {
  canvas = document.getElementById("myGLCanvas");
  gl = createGLContext(canvas);
  gl.clearColor(0.0, 0.0, 0.0, 1.0);
  gl.enable(gl.DEPTH_TEST);
  
  

  setupShaders();
  setupMesh("teapot_0.obj");
  
  setupShadersSB();
  setupBuffers();
  setupTextures();
  
  document.onkeydown = handleKeyDown;
  document.onkeyup = handleKeyUp;
  tick();
}


//----------------------------------------------------------------------------------
/**
  * Update any model transformations
  */
function animate() {
   //console.log(eulerX, " ", eulerY, " ", eulerZ); 
   document.getElementById("eY").value=eulerY;
  //  document.getElementById("rY").value=rotY;
   lightPosition=eyePt;
   lightPosition[1]=5;   
}


//----------------------------------------------------------------------------------
/**
 * Keeping drawing frames....
 */
function tick() {
    requestAnimFrame(tick);
    animate();
    draw();
}


//Draw a cube based on buffers.
 
function drawCube(){

  

  gl.useProgram(shaderProgramSB);
  gl.enableVertexAttribArray(vertexLocation);

  // Draw the cube by binding the array buffer to the cube's vertices
  // array, setting attributes, and pushing it to GL.

  //gl.bindBuffer(gl.ARRAY_BUFFER, cubeVertexBuffer);
  gl.bindBuffer(gl.ARRAY_BUFFER, cubeVertexBuffer);

  gl.vertexAttribPointer(vertexLocation, 2, gl.FLOAT, false, 0, 0);

  
  var vdpMatrix= mat4.create();
  mat4.mul(vdpMatrix, pMatrix, mvMatrix);
  var invVdpMatrix= mat4.create();
  mat4.invert(invVdpMatrix, vdpMatrix);

 // Set the uniforms
  gl.uniformMatrix4fv(invVdpLocation, false,  invVdpMatrix);

  // Use texture unit 0 for u_skybox
  gl.uniform1i(skyboxLocation, 0);

  // Draw the cube.
  
  setMatrixUniformsSB();
  //gl.drawElements(gl.TRIANGLES, 36, gl.UNSIGNED_SHORT, 0);
  gl.drawArrays(gl.TRIANGLES, 0, 6);

}

/**
 * Translates degrees to radians
 * @param {Number} degrees Degree input to function
 * @return {Number} The radians that correspond to the degree input
 */
function degToRad(degrees) {
    return degrees * Math.PI / 180;
}

function setupBuffers() {

    // Create a buffer for the cube's vertices.
  
    cubeVertexBuffer = gl.createBuffer();
    // Bind buffer
    gl.bindBuffer(gl.ARRAY_BUFFER, cubeVertexBuffer);
    // Put the vertices in the buffer
    var vertices = new Float32Array(
      [
        -10, -10, 
         10, -10, 
        -10,  10, 
        -10,  10,
         10, -10,
         10,  10,
      ]);
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
  
   }


   
/**
 * Creates texture for application to cube.
 */
function setupTextures() {
    // Create a texture.
  var texture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_CUBE_MAP, texture);
   
  const faceInfos = [
    {
      target: gl.TEXTURE_CUBE_MAP_POSITIVE_X, 
      file: 'Skybox/posx.jpg',
    },
    {
      target: gl.TEXTURE_CUBE_MAP_NEGATIVE_X, 
      file: 'Skybox/negx.jpg',
    },
    {
      target: gl.TEXTURE_CUBE_MAP_POSITIVE_Y, 
      file: 'Skybox/posy.jpg',
    },
    {
      target: gl.TEXTURE_CUBE_MAP_NEGATIVE_Y, 
      file: 'Skybox/negy.jpg',
    },
    {
      target: gl.TEXTURE_CUBE_MAP_POSITIVE_Z, 
      file: 'Skybox/posz.jpg',
    },
    {
      target: gl.TEXTURE_CUBE_MAP_NEGATIVE_Z, 
      file: 'Skybox/negz.jpg',
    },
  ];
  faceInfos.forEach((faceInfo) => {
    const {target, file} = faceInfo;
   
    // setup faces
    
    gl.texImage2D(target, 0, gl.RGBA, 2048, 2048, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
   
    // Asynchronously load an image
    const image = new Image();
    image.src = file;
    image.onload = function() {
      // Now that the image has loaded make copy it to the texture.
      gl.bindTexture(gl.TEXTURE_CUBE_MAP, texture);
      gl.texImage2D(target, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
      gl.generateMipmap(gl.TEXTURE_CUBE_MAP);
    };
  });
  gl.generateMipmap(gl.TEXTURE_CUBE_MAP);
  gl.texParameteri(gl.TEXTURE_CUBE_MAP, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
  }