import pandas as pd
import argparse
import numpy as np
import re
import sys
import os
import matplotlib.pyplot as plt
import math

# count the total amount of sports facilities corresponding to postcodes in Melbourne
data = pd.read_csv('dataset 2.csv')
data = data.fillna(0)
condition_list = list(data[' facilitycondition'])
data2 = data[data[" facilitycondition"] != 0]
data2 = data2[data2[" facilitycondition"] != 'Same as above']
data2 = data2[data2[" postcode"] <= 3207.0]
postcode_list = list(set(data2[' postcode']))
postcode_list.sort()
pcode_list = list((data2[' postcode']))
postcode_list.remove(0)

count_list = []
for i in postcode_list:
    count = 0
    for j in pcode_list:
        if j == i:
            count += 1
    count_list.append(count)

# calculate total score
grade_list = []
for i in postcode_list:
    grade = 0
    currdata = data2[data2[" postcode"] == i]
    condition_list = currdata[" facilitycondition"]
    for j in condition_list:
        grade += int(j[0])
    grade_list.append(grade)

# calculate total score
grade_per_f = []
for i in range(len(postcode_list)):
    score = grade_list[i] / count_list[i]
    grade_per_f.append(score)

df_score = pd.DataFrame(postcode_list, columns=['postcode'])
df_score = pd.concat([df_score, pd.DataFrame(grade_per_f, columns=['grade_per_f'])], axis=1)

# get a smaller range of dataframe
less_than_2 = df_score[df_score['grade_per_f'] <= 2]

# plot average grade of sports facilities
plt.figure(figsize=(17,5))
plt.bar(df_score['postcode'], df_score['grade_per_f'])
plt.xlabel("postcode")
plt.ylabel("grade per facility")
plt.title("Distribution of average grade of sports facilities in Melbourne", size=18)
plt.savefig('grade per facility.png')
plt.show()
