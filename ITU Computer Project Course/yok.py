#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from scipy import stats
from numpy import array


ranks = []
math_nets = []

url = "https://yokatlas.yok.gov.tr/lisans-bolum.php?b=10024"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

contents = soup.findAll("div", {"class" : "col-md-6 col-sm-6"}) # contents: left and right column
for content in contents: 
	a = content.findAll("a")
	for one in a: 
		rank_url = "https://yokatlas.yok.gov.tr/content/lisans-dynamic/1000_1.php" + one["href"][10:]
		page = requests.get(rank_url)
		soup = BeautifulSoup(page.content, "html.parser")
		rank = soup.find("td", text="0,12 Katsayı ile Yerleşen Son Kişinin Başarı Sırası").find_next_sibling().get_text()
		rank = rank.replace(".", "")

		net_math = ""
		if rank != "Dolmadı": 
			ranks.append(int(rank))
			math_url = "https://yokatlas.yok.gov.tr/content/lisans-dynamic/1210a.php" + one["href"][10:]
			page = requests.get(math_url)
			soup = BeautifulSoup(page.content, "html.parser")
			net_math = soup.find("td", text="TYT Temel Matematik (40 soruda)").find_next_sibling().get_text()
			net_math = net_math.replace(",", ".")
			math_nets.append(float(net_math))

		print (rank + " - " + net_math)
		


ranks = array(ranks) # necessary for plotting regression line
math_nets = array(math_nets) # necessary for plotting regression line


slope, intercept, r_value, p_value, std_err = stats.linregress(ranks, math_nets)
print ("r-squared metric: %f" % r_value**2)

plt.plot(ranks, intercept + slope * ranks, 'r', label='regression line')
plt.scatter(ranks, math_nets)
plt.xlabel("ranks")
plt.ylabel("net math questions")
plt.legend()
plt.show()

