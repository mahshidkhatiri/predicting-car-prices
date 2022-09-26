import requests
from bs4 import BeautifulSoup
import mysql.connector
from sklearn.preprocessing import OneHotEncoder
import csv
import pandas as pd
from itertools import zip_longest
import numpy as np
from sklearn.linear_model import LinearRegression
import os
def info():
    cnx = mysql.connector.connect(user='root', password='', database='cars')
    cursor = cnx.cursor()
    sql_Delete_query = "DELETE FROM carsinfo"
    cursor.execute(sql_Delete_query)
    cnx.commit()

    for n in range(1,21):

        r= requests.get("https://www.truecar.com/used-cars-for-sale/listings/?page=%i" % n)
        soup=BeautifulSoup(r.text,"html.parser")
        years=soup.find_all("span",attrs={"class":"vehicle-card-year font-size-1"})
        names=soup.find_all("span",attrs={"class":"vehicle-header-make-model text-truncate"})
        prices=soup.find_all("div",attrs={"data-test":"vehicleListingPriceAmount"})
        mileage=soup.find_all("div",attrs={"data-test":"vehicleMileage"})
        colors=soup.find_all("div",attrs={"class":"vehicle-card-location font-size-1 margin-top-1 text-truncate"})
        for i in range(0, len(names)):
            x=mileage[i].text.split()
            z=x[0].split(",")
            s=z[0]+z[1]
            mileage_n=int(s)
            w=prices[i].text.split("$")
            z=w[1].split(",")
            s=z[0]+z[1]
            price_n=int(s)
            year=int(years[i].text)
            color=colors[i].text.split()
            cursor.execute("INSERT INTO  carsinfo VALUES (\'%s\',\'%s\',%d,%d,%d)"%(names[i].text,color[0],year,mileage_n,price_n))
    cnx.commit()
    cnx.close()
    
    
    
    
def ml(l_for_predict):
    cnx = mysql.connector.connect(user='root', password='', database='cars')
    sql = "SELECT * FROM carsinfo"
    cursor = cnx.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    data=[[],[],[],[],[]]
    for i in result:
        x=list(i)
        data[0].append(x[0])
        data[1].append(x[1])
        data[2].append(x[2])
        data[3].append(x[3])
        data[4].append(x[4])
    export_data = zip_longest(*data, fillvalue = '')
    with open('carinfo.csv', 'w', encoding="ISO-8859-1", newline='') as file:
          write = csv.writer(file)
          write.writerow(("name","color", "year","mileage","price"))
          write.writerows(export_data)
    cnx.close()
    df = pd.read_csv('carinfo.csv')
    os.remove('carinfo.csv')
    x=df[["name","color"]]
    enc = OneHotEncoder(handle_unknown='ignore')
    x = enc.fit_transform(x).toarray()
    df2=df[["year","mileage"]]
    xx=df2.to_numpy()
    X = np.concatenate((x, xx), axis=1)
    y=df['price']
    reg = LinearRegression().fit(X, y)
    my_array = np.array([l_for_predict])
    df3 = pd.DataFrame(my_array, columns = ["name","color", "year","mileage"])
    x_n=df3[["name","color"]]
    x_n = enc.transform(x_n).toarray()
    df4=df3[["year","mileage"]]
    xx_n=df4.to_numpy()
    X_n = np.concatenate((x_n, xx_n), axis=1)
    print(reg.predict(X_n)[0],"$")
    
def predict():
    z=input("enter ur input like this : name,color,year,mileage\n")
    z=z.split(",")
    z[2]=int(z[2])
    z[3]=int(z[3])
    ml(z)
info()
predict()