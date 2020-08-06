# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 18:56:03 2020

@author: Rohit Mehta
"""


from Plot_AQI import avg_data
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv 

def met_data(month,year):
    
    # opening & storing html code in plain text format
    file_html = open('Data/Html_Data/{}/{}.html'.format(year,month),'rb')
    plain_text = file_html.read()
    
    tempD = []
    finalD = []
    
    # data scrapping using BeautifulSoup
    soup = BeautifulSoup(plain_text,'lxml')
    for table in soup.findAll('table',{ 'class': 'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a=tr.get_text()
                tempD.append(a)
     
    # finding no. of rows in the original table           
    rows = len(tempD)/15
    
    # identifying rows from text & stored in finalD
    for times in range(round(rows)):
        newtempD = []
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        finalD.append(newtempD)    
    
    length = len(finalD)     
    
    # removing unnecessary first & last row
    finalD.pop(length-1)
    finalD.pop(0)
    
    # removing unnecessary columns
    for a in range(len(finalD)):
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)
       
    return finalD
    # after removal finalD contains clean data

# return csv file in list format
def data_combine(year,cs):
    for a in pd.read_csv('Data/Real-Data/real_' + str(year) + '.csv', chunksize=cs):
        df=pd.DataFrame(data = a)
        mylist = df.values.tolist()
    return mylist    

if __name__=="__main__":
    
    # creating new folder real-data which will contain cleaned data in csv files.
    if not os.path.exists("Data/Real-Data"):
        os.makedirs("Data/Real-Data")
    for year in range(2013,2017):
        final_data = []
        with open('Data/Real-Data/real_' + str(year) + '.csv', 'w') as csvfile:
            wr=csv.writer(csvfile,dialect='excel')
            # first row
            wr.writerow(['T','TM','Tm','SLP','H','W','V','VM','PM2.5'])
        # data added to final_data monthwise
        for month in range(1,13):
            temp = met_data(month,year)
            final_data=final_data + temp
        
        # dependent feature
        pm=avg_data(year)
        
        if len(pm)==364:
            pm.insert(364,'-')
            
        # combing independent features from final_data & dependent features from pm to form a complete dataset
        for i in range(len(final_data)-1):
            final_data[i].insert(8,pm[i])
            
        # storing complete dataset for a year in csv file & cleanind the data   
        with open ('Data/Real-Data/real_' + str(year) + '.csv', 'a') as csvfile:
            wr=csv.writer(csvfile,dialect='excel')        
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == '-':
                        flag = 1
                if flag !=1:
                    wr.writerow(row)
                     

    data_2013 = data_combine(2013,600)
    data_2014 = data_combine(2014,600)
    data_2015 = data_combine(2015,600)
    data_2016 = data_combine(2016,600)
    
    # complete dataset
    total = data_2013 + data_2014 + data_2015 + data_2016
    
    # storing complete dataset
    with open('Data/Real-Data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile,dialect = 'excel')
        wr.writerow(['T','TM','Tm','SLP','H','W','V','VM','PM2.5'])
        wr.writerows(total)


df=pd.read_csv('Data/Real-Data/Real_Combine.csv')



        
                
            
    
    
    


