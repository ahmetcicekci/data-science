import numpy as np
import pandas as pd
import csv
np.set_printoptions(threshold=10000)

df_train = pd.read_csv("armut/armut_challenge_training.csv", sep=",", names=["id", "user_id", "service_id", "timestamp"])
df_train = df_train.iloc[2:]
df_train = df_train.drop("id", 1)
df_train["user_id"] = df_train["user_id"].astype(int)
df_train["service_id"] = df_train["service_id"].astype(int)
df_train["timestamp"] = pd.to_datetime(df_train["timestamp"])
df_train = df_train.sort_values(["user_id", "timestamp"])

grouped = df_train.groupby("user_id")
groups = []

for group in grouped: 
	groups.append(group)



def similarity(l1,l2):
        l2_copy=list(l2)
        counter=0
        for i in l1:
            if i in l2_copy:
                counter+=1
                l2_copy.remove(i)
        return counter


def writeToCSV(filename, user_id, service_id): 
	user_id = str(user_id)
	service_id = str(service_id)
	with open(filename, mode='a', newline='') as file: 
		writer = csv.writer(file)
		writer.writerow([user_id, service_id]) 


def predictNext(user_id): 
	mGroupList = df_train.loc[df_train['user_id'] == user_id]["service_id"].tolist()
	lastElement = mGroupList[-1]

	firstPostValues = []
	secondPostValues = []
	thirdPostValues = []

	for group in groups: 
			groupList = group[1]["service_id"].tolist()
			for index, item in enumerate(groupList[:-1]):
				if item == lastElement:
					firstPostValues.append(groupList[index + 1])
					similarityLevel = similarity(mGroupList, groupList)
					for x in range(similarityLevel):
						secondPostValues.append(groupList[index + 1])
					for x in range(similarityLevel ** 2):
						thirdPostValues.append(groupList[index + 1])

	if len(firstPostValues) == 0: #tebrikler bu hizmeti senden başka alan yok
		firstPostValues.append(group[1]["service_id"].tolist()[-2]) # bir önceki hizmet
		secondPostValues.append(group[1]["service_id"].tolist()[-2])
		thirdPostValues.append(group[1]["service_id"].tolist()[-2])
	
	firstPostValues = np.array(firstPostValues)
	secondPostValues = np.array(secondPostValues)
	thirdPostValues = np.array(thirdPostValues)

	firstMostFreq = np.argmax(np.bincount(firstPostValues))
	secondMostFreq = np.argmax(np.bincount(secondPostValues))
	thirdMostFreq = np.argmax(np.bincount(thirdPostValues))


	writeToCSV("armutsubmit0.csv", user_id, firstMostFreq)
	writeToCSV("armutsubmit1.csv", user_id, secondMostFreq)
	writeToCSV("armutsubmit2.csv", user_id, thirdMostFreq)
	print (str(user_id) + " --- " + str(firstMostFreq) + " - " + str(secondMostFreq) + " - " + str(thirdMostFreq))








df_submit = pd.read_csv("armut/ArmutSampleSubmission.csv", sep=",", names=["user_id", "service_id"])
df_submit = df_submit.iloc[1:] # delete header
df_submit["user_id"] = df_submit["user_id"].astype(int)
df_submit["service_id"] = df_submit["service_id"].astype(int)
submitUsers = df_submit["user_id"].tolist()




for user in submitUsers: 
	predictNext(user)
