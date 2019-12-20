# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019

"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math
import copy

class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.lambda_mixture = 0.0
        self.num_class=0
        self.likelihood=[[]]
        self.prior=[]
        self.vocab= [[]]


    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """

        # TODO: Write your code here
        self.num_class=max(train_label)

        frequency = [0]*self.num_class

        for i in train_label:
            frequency[i-1]+=1
        
        self.prior = [x / len(train_set) for x in frequency]

        vocab= [[] for _ in range(self.num_class)] #Initialist list of all words
    

        
        for c in range(self.num_class):
            for i in range (len(train_set)):
                if (train_label[i]==c+1):
                    for j in range (len(train_set[i])):
                        if (train_set[i][j] not in vocab[c]):
                            vocab[c].append(train_set[i][j])
       


        self.vocab=copy.deepcopy(vocab)
        self.likelihood=copy.deepcopy(vocab)


        for i in range(self.num_class):
            for j in range(len(self.likelihood[i])):
                self.likelihood[i][j]=0
        


        for c in range(self.num_class):
            #print ("c: ", c)
            for i in range(len(train_set)):
                if (train_label[i]==c+1):
                    for w in range(len(vocab[c])):
                        if vocab[c][w] in train_set[i]:
                            self.likelihood[c][w]+=1
 

        for c in range (self.num_class):
            for w in range(len(vocab[c])):
                self.likelihood[c][w]=(1+self.likelihood[c][w])/((frequency[c])+len(vocab[c]))
        #print (self.likelihood)
        

        pass

    def predict(self, x_set, dev_label,lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """

        accuracy = 0.0
        result = [0]*len(x_set)

        for i in range(len(x_set)): #For every text
            print ("i: ", i)
            products=[0]*self.num_class
            for c in range(self.num_class): #For everyclass
                products[c]+=math.log(self.prior[c]) #Add log of prior
                for w in range(len(self.vocab[c])): #For every word in vocab list
                    #print ("vocab cw: ", self.vocab[c][w])
                    if self.vocab[c][w] in x_set[i]:
                        products[c]+=math.log(self.likelihood[c][w])
                        #print (self.likelihood[c][w])
                        
                    # else :
                    #     products[c]+=math.log(1-(self.likelihood[c][w]))
        
            
            result[i]=products.index(max(products))+1
            if (result[i]==dev_label[i]):
                accuracy+=1	

        accuracy/=len(x_set)

        print (result)

        # TODO: Write your code here
        pass

        return accuracy,result

