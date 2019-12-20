import numpy as np
import matplotlib.pyplot as plt


class MultiClassPerceptron(object):
	def __init__(self,num_class,feature_dim):
		"""Initialize a multi class perceptron model. 

		This function will initialize a feature_dim weight vector,
		for each class. 

		The LAST index of feature_dim is assumed to be the bias term,
			self.w[:,0] = [w1,w2,w3...,BIAS] 
			where wi corresponds to each feature dimension,
			0 corresponds to class 0.  

		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example 
		"""

		self.w = np.zeros((feature_dim+1,num_class))

	def train(self,train_set,train_label):
		""" Train perceptron model (self.w) with training dataset. 

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		
		# YOUR CODE HERE
		

		#Set bias vector

		bias = np.ones((1,self.w.shape[1]))
		self.w[-1] = bias

		# Make copy of training set and append 1 to columns 
		train_set_Cpy = np.append(train_set,np.ones([len(train_set),1]),1)

		#Calculate product of 
		#product=np.matmul(train_set_Cpy,self.w)

		
		for i in range(train_set_Cpy.shape[0]): #for each image in the training set	
			products=np.matmul(train_set_Cpy[i],self.w) #Multiply weight with each image and get vecctor of products
			prediction=np.argmax(products) #Prediction is the index with the max element, this is the predicted lable
			groundTruth=train_label[i] #Actually lable of image
			if (prediction!=groundTruth): #if our prediction correct, do nothing. If it is incorrect, we must update the corresponding weights
				self.w[:,groundTruth]=self.w[:,groundTruth]+train_set_Cpy[i]
				self.w[:,prediction]=self.w[:,prediction]-train_set_Cpy[i]

				


		pass

	def test(self,test_set,test_label):
		""" Test the trained perceptron model (self.w) using testing dataset. 
			The accuracy is computed as the average of correctness 
			by comparing between predicted label and true label. 
			
		Args:
		    test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
		    test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

		Returns:
			accuracy(float): average accuracy value 
			pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
		"""    


		maxProd=np.zeros(self.w.shape[1])
		minProd=np.zeros(self.w.shape[1])
		currMaxProd=np.zeros(self.w.shape[1])
		currMinProd=np.zeros(self.w.shape[1])
		
		for i in range(self.w.shape[1]):
			currMaxProd[i]=-10000
		

		for i in range(self.w.shape[1]):
			currMinProd[i]=10000
		# YOUR CODE HERE
		accuracy = 0 
		pred_label = np.zeros((len(test_set)))

		test_set_Cpy = np.append(test_set,np.ones([len(test_set),1]),1)

		for i in range(test_set.shape[0]): #for each image in the training set
			products=np.matmul(test_set_Cpy[i],self.w) #Multiply weight with each image and get vecctor of products
			prediction=np.argmax(products) #Prediction is the index with the max element, this is the predicted lable
			pred_label[i]=prediction
			if (pred_label[i]==test_label[i]):
				accuracy+=1
			
			if (products[test_label[i]]>currMaxProd[test_label[i]]):
				currMaxProd[test_label[i]]=products[test_label[i]]
				maxProd[test_label[i]]=i
			
			if (products[test_label[i]]<currMinProd[test_label[i]]):
				currMinProd[test_label[i]]=products[test_label[i]]
				minProd[test_label[i]]=i

				

		accuracy/=len(test_set)

		print(1.2)
		print (maxProd)
		print (minProd)

		pass
		
		

		#print ("accuracy: ",accuracy)

		# currImage=self.w[:,0]
		# currImage = np.delete (currImage,-1)
		# currImage = np.reshape(currImage,(28,28))
		# plt.imshow(currImage)
		# plt.show()
		return accuracy, pred_label

	def save_model(self, weight_file):
		""" Save the trained model parameters 
		""" 

		np.save(weight_file,self.w)

	def load_model(self, weight_file):
		""" Load the trained model parameters 
		""" 

		self.w = np.load(weight_file)

