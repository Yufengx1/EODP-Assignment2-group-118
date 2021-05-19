import pandas as pd
import argparse
import numpy as np
import re
import sys
import os
import matplotlib.pyplot as plt
import math

# count the total amount of sports facilities corresponding to postcodes in Melbourne
data1 = pd.read_csv('dataset 1.csv')
data1 = data1.fillna(0)
postcode_list = list(set(data1['Pcode']))
postcode_list.sort()
pcode_list = list((data1['Pcode']))
postcode_list.remove(0)

count_list = []
for i in postcode_list:
    count = 0
    for j in pcode_list:
        if j == i:
            count += 1
    count_list.append(count)
for i in range(len(postcode_list)):
    if postcode_list[i] > 3207.0:
        postcode_list = postcode_list[:i]
        count_list = count_list[:i]
        break
        
df_pcode_num = pd.DataFrame(postcode_list, columns=['postcode_list'])
df_pcode_num = pd.concat([df_pcode_num, pd.DataFrame(count_list, columns=['count_list'])], axis=1)

# plot 1
plt.figure(figsize=(13,10))
plt.bar(df_pcode_num['postcode_list'], df_pcode_num['count_list'])
plt.xlim(2995,3215)
plt.xlabel("postcode")
plt.ylabel("total amount")
plt.title("Total amount of sports facilities in Melbourne", size=18)
plt.savefig('Total amount of sports facilities.png')
plt.show()

# sort the population by postcode
pop = pd.read_csv('population dataset.csv')
postcode_list2 = pop['POA_CODE_2016']
pcode_list = []
pop_list = pop['Tot_P_P']
for i in postcode_list2:
    pcode = ''
    curr_list = list(i)[3:]
    for j in curr_list:
        pcode += j
    
    pcode_list.append(int(pcode))
    
for i in range(len(pcode_list)):
    if pcode_list[i] > 3207:
        pcode_list = pcode_list[:i]
        pop_list = pop_list[:i]
        break    
pop_list1 = list(pop_list)

df_pop_num = pd.DataFrame(pcode_list, columns=['pcode_list'])
df_pop_num = pd.concat([df_pop_num, pd.DataFrame(pop_list1, columns=['pop_list'])], axis=1)

# plot 2
plt.figure(figsize=(13,10))
plt.scatter(df_pop_num['pcode_list'], df_pop_num['pop_list'], marker = '.')
plt.xlabel("postcode")
plt.ylabel("population")
plt.title("Distribution of population in Melbourne", size=18)
plt.savefig('Distribution of population.png')
plt.show()

# caculate average amount of facilities by log_person
for i in range(len(postcode_list)):
    postcode_list[i] = int(postcode_list[i])
    
pcode_new = []
log_list = []
count_new = []
for i in range(3000,3208):
    if i in pcode_list and i in postcode_list:
        pcode_new.append(i)
        
for i in pcode_new:
    for j in range(len(postcode_list)):
        if i == postcode_list[j]:
            count_new.append(count_list[j])
    
    for j in range(len(pcode_list)):
        if i == pcode_list[j]:
            log_list.append(pop_list1[j])
            
for i in range(len(log_list)):
    if log_list[i] != 0:
        log_list[i] = math.log(log_list[i])
        
num_per_p = []
for i in range(len(count_new)):
    if log_list[i] == 0:
        num_per_p.append(0)
    else:
        num_per_p.append(count_new[i] / log_list[i])
        
mean = sum(num_per_p)/len(num_per_p)
df_npp = pd.DataFrame(pcode_new, columns=['pcode_list'])
df_npp = pd.concat([df_npp, pd.DataFrame(num_per_p, columns=['num_per_p'])], axis=1)

# get a smaller range of dataframe
less_than_2 = df_npp[df_npp['num_per_p'] < mean]
less_than_half = df_npp[df_npp['num_per_p'] < 0.5]

# plot amount of facilities per log_person
plt.figure(figsize=(13,10))
plt.bar(df_npp['pcode_list'], df_npp['num_per_p'])
plt.xlim(2995, 3215)
plt.xlabel("postcode")
plt.ylabel("amount per log_person")
plt.title("amount per log_person of sports facilities in Melbourne", size=18)
plt.savefig('amount per log_person.png')
plt.show()