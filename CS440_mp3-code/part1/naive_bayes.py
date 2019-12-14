import numpy as np

class NaiveBayes(object):
	def __init__(self,num_class,feature_dim,num_value):
		"""Initialize a naive bayes model. 

		This function will initialize prior and likelihood, where 
		prior is P(class) with a dimension of (# of class,)
			that estimates the empirical frequencies of different classes in the training set.
		likelihood is P(F_i = f | class) with a dimension of 
			(# of features/pixels per image, # of possible values per pixel, # of class),
			that computes the probability of every pixel location i being value f for every class label.  

		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example 
		    num_value(int): number of possible values for each pixel 
		"""

		self.num_value = num_value
		self.num_class = num_class
		self.feature_dim = feature_dim

		self.prior = np.zeros((num_class))
		self.likelihood = np.zeros((feature_dim,num_value,num_class))


	def train(self,train_set,train_label):
		""" Train naive bayes model (self.prior and self.likelihood) with training dataset. 
			self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
			self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of 
				(# of features/pixels per image, # of possible values per pixel, # of class).
			You should apply Laplace smoothing to compute the likelihood. 

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE
		for i in range(len(train_label)):
			self.prior[train_label[i]]+=1/len(train_label)

		frequency=self.prior*len(train_set)
		
		for i in range(len(self.likelihood)): #Loop through every pixel per image
			for j in range(len(train_set)): #Loop through every image
				self.likelihood[i][train_set[j][i]][train_label[j]]+=1
			
		for i in range(self.feature_dim): #Laplace smoothing and log
			for j in range (self.num_value):
				for k in range(self.num_class):
					self.likelihood[i][j][k]= np.log((self.likelihood[i][j][k]+1)/(frequency[k]+self.num_value))	

		

		
	
		#print (frequency)
		#print (self.likelihood)
		
		
		pass

	def test(self,test_set,test_label):
		""" Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
			by performing maximum a posteriori (MAP) classification.  
			The accuracy is computed as the average of correctness 
			by comparing between predicted label and true label. 

		Args:
		    test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
		    test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

		Returns:
			accuracy(float): average accuracy value  
			pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
		"""    

		# YOUR CODE HERE

		maxProd=np.zeros(self.num_class)
		minProd=np.zeros(self.num_class)
		currMaxProd=np.zeros(self.num_class)
		currMinProd=np.zeros(self.num_class)

		for i in range(self.num_class):
			currMaxProd[i]=-10000
		

		for i in range(self.num_class):
			currMinProd[i]=10000


		accuracy = 0
		pred_label = np.zeros((len(test_set)))

		for i in range(len(test_set)): #for every sample
			probs=np.zeros(self.num_class)
			for c in range(self.num_class): #For every class
				probs[c]+=np.log(self.prior[c])
				for p in range(self.feature_dim):
					probs[c]+=self.likelihood[p][test_set[i][p]][c]
			
			pred_label[i]=np.argmax(probs)
			if (pred_label[i]==test_label[i]):
				accuracy+=1	
			
			
			if (probs[test_label[i]]>currMaxProd[test_label[i]]):
				currMaxProd[test_label[i]]=probs[test_label[i]]
				maxProd[test_label[i]]=i
			
			if (probs[test_label[i]]<currMinProd[test_label[i]]):
				currMinProd[test_label[i]]=probs[test_label[i]]
				minProd[test_label[i]]=i

		accuracy/=len(test_set)


		print (1.1)	
		print (maxProd)
		print (minProd)
		print (currMaxProd)



		pass

		return accuracy, pred_label


	def save_model(self, prior, likelihood):
		""" Save the trained model parameters 
		"""    

		np.save(prior, self.prior)
		np.save(likelihood, self.likelihood)

	def load_model(self, prior, likelihood):
		""" Load the trained model parameters 
		""" 

		self.prior = np.load(prior)
		self.likelihood = np.load(likelihood)

	def intensity_feature_likelihoods(self, likelihood):
		
		"""
		Get the feature likelihoods for high intensity pixels for each of the classes,
			by sum the probabilities of the top 128 intensities at each pixel location,
			sum k<-128:255 P(F_i = k | c).
			This helps generate visualization of trained likelihood images. 
		
		Args:
			likelihood(numpy.ndarray): likelihood (in log) with a dimension of
				(# of features/pixels per image, # of possible values per pixel, # of class)
		Returns:
			feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
				(# of features/pixels per image, # of class)
		"""
		# YOUR CODE HERE
		feature_likelihoods = np.zeros((likelihood.shape[0],likelihood.shape[2]))
		for i in range(likelihood.shape[0]):
			for j in range(likelihood.shape[2]):
				for k in range(128,256):
					feature_likelihoods[i][j]+=likelihood[i][k][j]

		return feature_likelihoods
