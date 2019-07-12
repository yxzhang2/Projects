import numpy as np

"""
    Minigratch Gradient Descent Function to train model
    1. Format the data
    2. call four_nn function to obtain losses
    3. Return all the weights/biases and a list of losses at each epoch
    Args:
        epoch (int) - number of iterations to run through neural net
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - starting weights
        x_train (np array) - (n,d) numpy array where d=number of features
        y_train (np array) - (n,) all the labels corresponding to x_train
        num_classes (int) - number of classes (range of y_train)
        shuffle (bool) - shuffle data at each epoch if True. Turn this off for testing.
    Returns:
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - resulting weights
        losses (list of ints) - each index should correspond to epoch number
            Note that len(losses) == epoch
    Hints:
        Should work for any number of features and classes
        Good idea to print the epoch number at each iteration for sanity checks!
        (Stdout print will not affect autograder as long as runtime is within limits)
"""


def minibatch_gd(epoch, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, num_classes, shuffle=True):
    batch_size = 200
    # IMPLEMENT HERE

    losses = np.zeros(epoch)

    for e in range(epoch):
        loss = 0# for every epoch
        if (shuffle):  # shuffle x_train and y_train together
            permutation = np.random.permutation(x_train.shape[0])
            x_train = x_train[permutation]
            y_train = y_train[permutation]
        for i in range(int(x_train.shape[0] / batch_size)):
            X, y = x_train[i*200:i*200 + 200], y_train[i*200:i*200 + 200] # multiply by 200
            ret = four_nn(X, w1, w2, w3, w4, b1, b2, b3, b4, y, test=False)
            loss += ret
        losses[e] = loss
        print (loss);
    return w1, w2, w3, w4, b1, b2, b3, b4, losses


"""
    Use the trained weights & biases to see how well the nn performs
        on the test data
    Args:
        All the weights/biases from minibatch_gd()
        x_test (np array) - (n', d) numpy array
        y_test (np array) - (n',) all the labels corresponding to x_test
        num_classes (int) - number of classes (range of y_test)
    Returns:
        avg_class_rate (float) - average classification rate
        class_rate_per_class (list of floats) - Classification Rate per class
            (index corresponding to class number)
    Hints:
        Good place to show your confusion matrix as well.
        The confusion matrix won't be autograded but necessary in report.
"""


def test_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes):
    avg_class_rate = 0.0
    class_rate_per_class = [0.0] * num_classes

    y_pred=four_nn(x_test,w1, w2, w3, w4, b1, b2, b3, b4,y_test,True)

    avg_class_rate=np.sum(y_test==y_pred)/len(y_test)

    cfMatrix=np.zeros((num_classes,num_classes))

    
    for i in range(len(y_test)):
        print (y_test[i])
        print (y_pred[i])
        cfMatrix[y_test[i],int(y_pred[i])]+=1
    
    for i in range(len(cfMatrix)):
        cfMatrix[i,:]/=np.sum(cfMatrix[i])

    print ("avg class rate: ",avg_class_rate)
    print (cfMatrix)

    for i in range(num_classes):
        class_rate_per_class[i]=cfMatrix[i][i]

    return avg_class_rate, class_rate_per_class


"""
    4 Layer Neural Network
    Helper function for minibatch_gd
    Up to you on how to implement this, won't be unit tested
    Should call helper functions below
"""


def four_nn(X, W1, W2, W3, W4, b1, b2, b3, b4, y, test):
    Z1, acache1 = affine_forward(X, W1, b1);
    A1, rcache1 = relu_forward(Z1);
    Z2, acache2 = affine_forward(A1, W2, b2);
    A2, rcache2 = relu_forward(Z2);
    Z3, acache3 = affine_forward(A2, W3, b3);
    A3, rcache3 = relu_forward(Z3);
    F, acache4 = affine_forward(A3, W4, b4);
    if (test):
        classifications = np.zeros(F.shape[0])
        for i in range(F.shape[0]):
            classifications[i] = np.argmax(F[i]); # nupy.argmax
        return classifications;
    loss, dF = cross_entropy(F, y)
    dA3, dW4, db4 = affine_backward(dF, acache4)
    dZ3 = relu_backward(dA3, rcache3)
    dA2, dW3, db3 = affine_backward(dZ3, acache3);
    dZ2 = relu_backward(dA2, rcache2);
    dA1, dW2, db2 = affine_backward(dZ2, acache2);
    dZ1 = relu_backward(dA1, rcache1)
    dX, dW1, db1 = affine_backward(dZ1, acache1);
    # use gradient descent to update parameters ie: W1 = W1 - ndW1
    W1 -= (0.1) * dW1;
    W2 -= (0.1) * dW2;
    W3 -= (0.1) * dW3;
    W4 -= (0.1) * dW4;

    b1 -= (0.1) * db1;
    b2 -= (0.1) * db2;
    b3 -= (0.1) * db3;
    b4 -= (0.1) * db4;

    return loss;




"""
    Next five functions will be used in four_nn() as helper functions.
    All these functions will be autograded, and a unit test script is provided as unit_test.py.
    The cache object format is up to you, we will only autograde the computed matrices.

    Args and Return values are specified in the MP docs
    Hint: Utilize numpy as much as possible for max efficiency.
        This is a great time to review on your linear algebra as well.
"""


def affine_forward(A, W, b):
    cache = (A, W, b)
    Z = np.matmul(A, W) + b

    return Z, cache


def affine_backward(dZ, cache):
    # Get data from cache
    A = cache[0]
    W = cache[1]
    b = cache[2]

    dA = np.matmul(W, dZ.T).T
    dW = np.matmul(A.T, dZ)
    dB = np.sum(dZ, axis=0)

    return dA, dW, dB

def relu_forward(Z):
    cache = Z
    A = np.maximum (Z, 0);
    return A, cache


def relu_backward(dA, cache):
    Z = cache
    dZ = np.where (Z <= 0, 0, dA)
    return dZ


def cross_entropy(F, y):
    sigma_loss = 0;
    shape_arr = F.shape;
    n = shape_arr[0];
    c = shape_arr[1];
    for i in range(0, n):
        sigma_loss = sigma_loss + F[i][int(y[i])];
        sigma_exp = 0;
        for k in range(0, c):
            sigma_exp = sigma_exp + np.exp(F[i][k]);
        sigma_exp = np.log(sigma_exp);
        sigma_loss = sigma_loss - sigma_exp
    loss = (-1 / n) * sigma_loss;
    dF = np.zeros((n, c));
    for i in range(0, n):
        for j in range(0, c):
            bool_int = 0;
            if j == y[i]:
                bool_int = 1;
            exp_fij = np.exp(F[i][j])
            sigma_exp_fik = 0;
            for k in range(0, c):
                sigma_exp_fik = sigma_exp_fik + np.exp(F[i][k])
            dF[i][j] = (-1 / n) * (bool_int - (exp_fij / sigma_exp_fik));
    return loss, dF