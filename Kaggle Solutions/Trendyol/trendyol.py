import numpy as np
import pandas as pd
import time
import math
import csv

def writeToCSV(filename, productID, sales): 
	productID = str(productID)
	sales = str(sales)
	with open(filename, mode='a', newline='') as file: 
		writer = csv.writer(file)
		writer.writerow([productID, sales]) 

def average(array): 
	return np.average(array)

def weighted_average(array):
	weights = []
	for i in range(len(array)): 
		weights.append(i+1)
	return np.average(array, weights=weights)

def ultraweighted_average(array):
	helper = []
	for i in range(len(array)):
		helper.append(i+1)

	weights = []
	for i in range(len(array)): 
		weights.append((i+1) * helper[i])
	return np.average(array, weights=weights)


similars = pd.read_csv("product.csv", sep=",", names=["productID", "gender", "color", "categoryID", "brandID", "subcategoryID", "price"])
similars = similars.iloc[1:]
similars["gender"] = similars["gender"].astype(int)
similars["productID"] = similars["productID"].astype(int)
similars["categoryID"] = similars["categoryID"].astype(int)
similars["subcategoryID"] = similars["subcategoryID"].astype(int)
similars["brandID"] = similars["brandID"].astype(int)
similars["price"] = similars["price"].astype(int)
similars["color"] = similars["color"].astype(int)

train = pd.read_csv("dailyProductActions.csv", sep=",", names=["productID", "date", "soldquantity", "stock", "clickcount", "favoredcount"])
train = train.iloc[1:]
train["productID"] = train["productID"].astype(int)
train["soldquantity"] = train["soldquantity"].astype(int)
train["date"] = pd.to_datetime(train["date"])
train["clickcount"] = train["clickcount"].fillna(0).astype(int)
train["favoredcount"] = train["favoredcount"].fillna(0).astype(int)
train = train.sort_values(["productID", "date"])
products = train.groupby("productID")

submit = pd.read_csv("SampleSubmission.csv", sep=",", names=["productID", "sales"])
submit = submit.iloc[1:]
submit["productID"] = submit["productID"].astype(int)
submit = submit["productID"].tolist()


def calculateAverages(productIDs): 
	averageofweightedaverages = []
	averageofultraweightedaverages = []
	averagelast7 = []
	averageweightedlast7 = []
	for productID in productIDs: 
		product = train.loc[train["productID"] == productID]
		sales = product["soldquantity"].tolist()

		if len(sales) < 7:
			averageofweightedaverages.append(average(sales))
			averageofultraweightedaverages.append(average(sales))
			averagelast7.append(average(sales))
			averageweightedlast7.append(average(sales))
		else: 
			averageofweightedaverages.append(weighted_average(sales))
			averageofultraweightedaverages.append(ultraweighted_average(sales))
			averagelast7.append(average(sales[-7:]))
			averageweightedlast7.append(weighted_average(sales[-7:]))

	return average(averageofweightedaverages), average(averageofultraweightedaverages), average(averagelast7), average(averageweightedlast7)


def getSimilars(productID):
	mProduct = similars.loc[similars['productID'] == productID]
	mGender = mProduct["gender"].tolist()[0]
	mCategoryID = mProduct["categoryID"].tolist()[0]
	mBrandID = mProduct["brandID"].tolist()[0]
	mSubCategoryID = mProduct["subcategoryID"].tolist()[0]

	similarProducts = similars.loc[(similars["gender"] == mGender) & (similars["categoryID"] == mCategoryID) & (similars["brandID"] == mBrandID) & (similars["subcategoryID"] == mSubCategoryID)]["productID"].tolist()
	similarProducts.append(productID)

	print (similarProducts)
	return similarProducts





count = 0
for productID in submit: 
	count += 1
	
	similarProducts = getSimilars(productID)

	similarWeightedAverage, similarUltraWeightedAverage, similarLast7Average, similarLast7WeightedAverage = calculateAverages(similarProducts)

	weightedSimilarValue = int(similarWeightedAverage*7)
	ultraweightedSimilarValue = int(similarUltraWeightedAverage*7)
	similarLast7Value = int(similarLast7Average*7)
	similarLast7WeightedValue = int(similarLast7WeightedAverage*7)


	writeToCSV("SampleSubmission1.csv", productID, weightedSimilarValue)
	writeToCSV("SampleSubmission2.csv", productID, ultraweightedSimilarValue)
	writeToCSV("SampleSubmission3.csv", productID, similarLast7Value)
	writeToCSV("SampleSubmission4.csv", productID, similarLast7WeightedValue)


	print (str(count) + " - " + str(productID))
