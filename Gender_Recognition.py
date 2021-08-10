#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('Desktop'):
    for filename in filenames:
        print(os.path.join(archive, voice.csv))

# Any results you write to the current directory are saved as output.


# In[2]:


data = pd.read_csv(r'C:\Users\Mukul\OneDrive\Desktop\archive\voice.csv')


# In[3]:


data.info()


# In[4]:


data.head()


# In[5]:


# We need to classificate to genders, so we have to make labels integer rather than object. I decided to make 1 as man, 0 as woman. (I'm not sexist, it is only for implementation, no offense :) )
data.label = [1 if each == 'male' else 0 for each in data.label]


# In[6]:


# Our new data
data.label.head() # 1's are for male


# In[7]:


data.label.tail() # 0's are for females


# In[8]:


y = data.label.values # set y as our genders
x_data = data.drop(['label'],axis=1) # other features in x_data


# In[9]:


# Normalization process is important for making data relevant, 
# which means it is kind of a protection of small datas for avoiding pressure of big datas. (Ex: 0.01 cannot be observed due to 1024.92)  
# This process makes all values between 0 and 1

x = (x_data - np.min(x_data)) / (np.max(x_data)-np.min(x_data)).values


# In[10]:


# train test split
# import necessary libraries
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# we have to transpoze our arrays in order to set features and samples correctly
x_train = x_train.T
y_train = y_train.T
x_test = x_test.T
y_test = y_test.T

print("x train: ",x_train.shape)
print("x test: ",x_test.shape)
print("y train: ",y_train.shape)
print("y test: ",y_test.shape)
# As it can be seen below, it became [total feature,total sample]


# In[11]:


# Initializing parameters
def initialize_weights_and_bias(dimension):
    w = np.full((dimension,1),0.01) # weight
    b = 0.0 # bias
    return w, b


# In[12]:


# Sigmoid function
# Calculation of z
def sigmoid(z):
    y_head = 1/(1+np.exp(-z))
    return y_head


# In[13]:


# Forward and Backward Propagations 
def forward_backward_propagation(w,b,x_train,y_train):
    
    # Forward propagation
    z = np.dot(w.T,x_train) + b
    y_head = sigmoid(z)
    loss = -y_train*np.log(y_head)-(1-y_train)*np.log(1-y_head)
    cost = (np.sum(loss))/x_train.shape[1]
    
    # Backward propagation
    derivative_weight = (np.dot(x_train,((y_head-y_train).T)))/x_train.shape[1] 
    derivative_bias = np.sum(y_head-y_train)/x_train.shape[1]
    gradients = {"derivative_weight": derivative_weight,"derivative_bias": derivative_bias}
    return cost,gradients


# In[14]:


# Updating parameters
def update(w, b, x_train, y_train, learning_rate,number_of_iterarion):
    cost_list = [] # for storing all costs
    cost_list2 = [] # for storing once every 10 costs
    index = [] # for storing index in order to show on plot
    
    # Updating(learning) parameters is number_of_iterarion times
    for i in range(number_of_iterarion):
        # make forward and backward propagation and find cost and gradients
        cost,gradients = forward_backward_propagation(w,b,x_train,y_train)
        cost_list.append(cost)
        # lets update
        w = w - learning_rate * gradients["derivative_weight"]
        b = b - learning_rate * gradients["derivative_bias"]
        if i % 10 == 0:
            cost_list2.append(cost)
            index.append(i)
            print ("Cost after iteration %i: %f" %(i, cost))
            
    # We update(learn) parameters weights and bias
    parameters = {"weight": w,"bias": b}
    plt.plot(index,cost_list2)
    plt.xticks(index,rotation='vertical')
    plt.xlabel("Number of Iterarion")
    plt.ylabel("Cost")
    plt.show()
    return parameters, gradients, cost_list


# In[15]:


# Prediction
def predict(w,b,x_test):
    
    # x_test is a input for Forward Propagation
    z = sigmoid(np.dot(w.T,x_test)+b)
    Y_prediction = np.zeros((1,x_test.shape[1]))
    # if z is bigger than 0.5, our prediction is sign one (y_head=1),
    # if z is smaller than 0.5, our prediction is sign zero (y_head=0),
    for i in range(z.shape[1]):
        if z[0,i]<= 0.5:
            Y_prediction[0,i] = 0
        else:
            Y_prediction[0,i] = 1

    return Y_prediction


# In[16]:


# Let's gather all the classes
def logistic_regression(x_train, y_train, x_test, y_test, learning_rate ,  num_iterations):
    # Initialize
    dimension =  x_train.shape[0] # It's 20 because samples of our data has 20 features 
    w,b = initialize_weights_and_bias(dimension)
    # do not change learning rate
    parameters, gradients, cost_list = update(w, b, x_train, y_train, learning_rate,num_iterations)
    
    y_prediction_test = predict(parameters["weight"],parameters["bias"],x_test)
    y_prediction_train = predict(parameters["weight"],parameters["bias"],x_train)

    # Print train/test Errors
    print("train accuracy: {} %".format(100 - np.mean(np.abs(y_prediction_train - y_train)) * 100))
    print("test accuracy: {} %".format(100 - np.mean(np.abs(y_prediction_test - y_test)) * 100))
    
logistic_regression(x_train, y_train, x_test, y_test,learning_rate = 1, num_iterations = 500) 


# In[17]:


# Let's make the whole thing using sklearn library
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(x_train.T,y_train.T)
print("Test accuracy {}".format(lr.score(x_test.T,y_test.T)))
# As it can be seen, we have better accuracy using sklearn :)


# In[ ]:




