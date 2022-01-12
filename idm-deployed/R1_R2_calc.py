# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 18:21:21 2021

@author: admin
"""

import pandas as pd
import numpy as np
import datetime

# FWP_date=datetime.datetime.strptime("2020-09-16", '%Y-%m-%d').date()
# SWP_date=datetime.datetime.strptime("2021-05-6", '%Y-%m-%d').date()
# sero=7.5
# SW_cases=2000
# FW_cases=500

    
def get_R_1(sero):    
    df_sero_R1=pd.read_csv("./data/sero_R0.csv")
    closest_index_sero = df_sero_R1['Sero_peak'].sub(sero).abs().idxmin()
    R0=df_sero_R1.at[closest_index_sero,'R0']
    return R0

def get_FW_cutoff_percent(FWP_date,SWP_date):
    peak_duration=(SWP_date-FWP_date).days
    df_cutoff=pd.read_csv("./data/FW_cutoff_percent.csv")
    closest_index_duration = df_cutoff['Duration'].sub(peak_duration).abs().idxmin()
    cutoff_percent=df_cutoff.at[closest_index_duration,'Cutoff_percent']
    # print(cutoff_percent)
    return cutoff_percent
    
    
# cutoff_percent=get_FW_cutoff_percent(FWP_date,SWP_date)   
     
# ind=get_R_1(sero)




