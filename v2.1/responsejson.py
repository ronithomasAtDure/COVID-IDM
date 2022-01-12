# -*- coding: utf-8 -*-
"""
Created on Fri May 15 20:08:31 2020

@author: Garima
"""

import json
import sys
import re
from typing import Pattern
#import covid_model_v5_2 

import pandas as pd
import numpy as np

import sirmodel as srmb

from datetime import datetime
start_time = datetime.now()

def createoutputjson(Sero=0, FWP_date="",  FWP_cases=0.0, SWP_date="", SWP_cases=0.0, R3=0, wa=0.0, thie=0.0, TW_Emergence_date='' , LockdownStartDate="", LockdownEndDate="", effLck="",PopulationDensity=0.0, vaccDuration=0.0,vaccCoverage=0.0):
    input = {}
    input = {"Sero": Sero, "FWP_date":FWP_date , "FWP_cases": FWP_cases, "SWP_date":SWP_date, "SWP_cases":SWP_cases, "R3":R3, "AverageDurationOfWanning":wa, "ThirdWaveImmuneEscape":thie,'TW_Emergence_date':TW_Emergence_date, "LockdownStartDate":LockdownStartDate, "LockdownEndDate":LockdownEndDate, "LockdownEffectiveness":effLck,"PopulationDensity":PopulationDensity, "VaccinationDuration":vaccDuration,"VaccinationCoverage":vaccCoverage}
    runmd = srmb.CovidApp(input)
    # print(input)
    
    data, R1_cases,R1_index, all_end_index,preparedness_list,seroAlert = runmd.get_json()
    # print("rj",all_end_index)
    #covid_model_v5_2.plotsir(data)
    
    data1=json.loads(data)
    # print(data1)
    return data1, R1_cases, R1_index, all_end_index,preparedness_list, seroAlert


#data,R1_cases,R1_index,all_end_index,preparedness_list=createoutputjson(r1=1.115, r2=1.64, r3=1.64, wa=0.0,thie=0.0, FirstPeaktDate="2020-11-30", ThirdWaveEmergenceDate="" , LockdownStartDate="2021-04-18", LockdownEndDate="2021-06-25", effLck=0.3, PopulationDensity=0.0, vaccDuration=90, vaccCoverage=0.3)

# data,R1_cases,R1_index,all_end_index,preparedness_list=createoutputjson(Sero=8.115, FWP_date="2020-9-13",  FWP_cases=100, SWP_date="2021-5-6", SWP_cases=420, R3=0.0, wa=0.0,thie=0.0, TW_Emergence_date="2021-09-01" , LockdownStartDate="2020-04-18", LockdownEndDate="2021-05-25", effLck=0.7, PopulationDensity=0.0, vaccDuration=3, vaccCoverage=0.8)

#data,R1_cases,R1_index,all_end_index,preparedness_list=createoutputjson(Sero=4, FWP_date="2020-11-30",  FWP_cases=180, SWP_date="2021-05-6", SWP_cases=1000, R3=0.0, wa=0.0,thie=0.0, TW_Emergence_date="" , LockdownStartDate="", LockdownEndDate="2021-05-20", effLck=0.5, PopulationDensity=0.0, vaccDuration=0, vaccCoverage=0.3)
