#Created by alecio on Sun May  9 19:06:39 CEST 2021

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

    return float(value.replace('%','').replace(',','.'))
def toInt(value):
    return int(value.replace('.' , '').replace('-','0'))

def dayofyear(date) :
    return date.timetuple().tm_yday

if __name__ == "__main__" :

    usage = "[USAGE] python3 main.py"

    for arg in sys.argv :
        if ( arg == "-h" or arg == "--help" ): 
            print(usage)
            exit()

    FILE = sys.argv[1]

    df = pd.read_csv(FILE,header="infer",converters={"CODICEIDENTIFICATIVOFARMACIA":toInt,"DATAINIZIOVALIDITA":dateconverter})

    #FOR DEBUG
    #df = df.sample(n=100, replace=False, random_state=1)

    df = df[['CODICEIDENTIFICATIVOFARMACIA','DESCRIZIONEREGIONE','DATAINIZIOVALIDITA']]

    df = df[df['DATAINIZIOVALIDITA'].map(giveYear) != 2005]
    
    id = -1
    min_year = 0
    good_index = 0

    pd.set_option('display.max_rows', 100)

    df.reset_index(inplace=True,drop=True)

    for i1,row in df.iterrows() : 
        if(row['CODICEIDENTIFICATIVOFARMACIA'] != id ):
            id = row['CODICEIDENTIFICATIVOFARMACIA']
            min_year = row['DATAINIZIOVALIDITA'].year
            good_index = i1
        else :
            current = row['DATAINIZIOVALIDITA'].year
            if current >= min_year :
                df = df.drop(index=[i1])
            else : 
                try:
                    df = df.drop(index=[(good_index)])
                    good_index=i1
                except KeyError : 
                    print("Current index = "+str(i1))
                    print("Dataframe = ")
                    
                    print(df.head(30))
                    exit()
    
    #print(df)

    #print(len( np.unique( df["DESCRIZIONEREGIONE"].to_numpy() ) ) ) 

    m_regions = np.unique( df["DESCRIZIONEREGIONE"].to_numpy() )
    region2num = {}
    dict_index = 0
    for el in  m_regions : 
        region2num[el]=dict_index
        dict_index+=1
    #print(region2num)

    m_years = np.unique( df['DATAINIZIOVALIDITA'].map(giveYear).to_numpy() )
    dict_index=0
    date2num = {}
    for el in m_years :
        date2num[el]=dict_index
        dict_index+=1
    #print(date2num)

    count_table = np.zeros(shape=(len(region2num),len(date2num)),dtype=np.int64,order='C')

    for i2, r1 in df.iterrows() :
        pos = (
            region2num[r1['DESCRIZIONEREGIONE']],
            date2num[r1['DATAINIZIOVALIDITA'].year]
            )
        count_table[pos] += 1

    #ROWS ARE REGIONS - COLUMNS ARE YEARS
    #print(count_table)

    m_rows = count_table.shape[0]
    m_cols = count_table.shape[1]

    print("REGIONI:",end="")
    for i in range(0,m_cols):
        print(", "+str(m_years[i]),end="")
    print("")

    for m_y in range(0, m_rows):
        print(m_regions[m_y],end="\t\t\t")
        for m_x in range(0, m_cols):
            print(", "+str(count_table[m_y,m_x]),end="")
        print("")



        

