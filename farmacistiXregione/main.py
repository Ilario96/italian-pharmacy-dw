import pandas as pd
import numpy as np
import sys
from datetime import datetime
import calendar

def giveYear(obj):
    return obj.year

def dateconverter(value):
    return datetime.strptime(value, '%d/%m/%Y')

def toF(value):

    return float(value)
def toInt(value):
    return int(value)

def dayofyear(date) :
    return date.timetuple().tm_yday

if __name__ == "__main__" :

    usage = "[USAGE] python3 main.py FILE.csv"

    for arg in sys.argv :
        if ( arg == "-h" or arg == "--help" ): 
            print(usage)
            exit()

    FILE = sys.argv[1]

    conv = {}
    num_cols = 15
    for col in range(2,num_cols):
        conv[col]=toInt
    print(conv)
    

    df = pd.read_csv(FILE,header="infer",converters=conv,sep=";")

    #print(len(df.columns))
    #print(df.dtypes)

    #print(df)

    df = df.drop(['Ateneo'], axis=1)

    df = df.groupby(["Regione"],as_index=False).sum()

    df.to_csv("results.csv",index=False)