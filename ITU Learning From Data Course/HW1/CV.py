from scipy.io import loadmat
import numpy as np
from sklearn.model_selection import LeaveOneOut, KFold
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix


data = loadmat("data.mat")["data"][0][0]
dataFeatures = data[0]
dataLabels = data[1][:,0]


def getAccuracy(method):
	test_labels_vector = []
	predicted_labels_vector = []

	for train_index, test_index in method.split(dataFeatures):
	    train_data = dataFeatures[train_index]
	    train_labels = dataLabels[train_index]
	    test_data = dataFeatures[test_index]
	    test_labels = dataLabels[test_index]
	    test_labels_vector += test_labels.tolist() # ground truth vector

	    model = LinearSVC()
	    model.fit(train_data, train_labels)

	    predicted_labels = model.predict(test_data)
	    predicted_labels_vector += predicted_labels.tolist()

	
	CM = confusion_matrix(test_labels_vector, predicted_labels_vector)

	true_negative = CM[0][0]
	true_positive = CM[1][1]
	false_negative = CM[1][0]
	false_positive = CM[0][1]

	accuracy = (true_positive + true_negative) / len(dataLabels) * 100

	return accuracy






#---------------------------- MAIN -----------------------------

c = LeaveOneOut() # model: leave one out cross validation
accuracy_loo = getAccuracy(c)

c = KFold(n_splits=5) # model: 5 fold cross validation
accuracy_5_fold = getAccuracy(c) 

c = KFold(n_splits=10) # model: 10 fold cross validation
accuracy_10_fold = getAccuracy(c)


print ("Accuracy for LOO: " + str(accuracy_loo))
print ("Accuracy for 5-fold: " + str(accuracy_5_fold))
print ("Accuracy for 10-fold: " + str(accuracy_10_fold))


