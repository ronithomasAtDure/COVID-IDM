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

def createoutputjson(Sero=0, FWP_date="",  FWP_cases=0.0, SWP_date="", SWP_cases=0.0, R3=0, wa=0.0, thie=0.0, TW_Emergence_date='' , LockdownStartDate="", LockdownEndDate="", effLck="",PopulationDensity=0.0, vaccDuration=0.0,vaccCoverage=0.0, proportionHospital=1, proportionOxygen=1, homecare=None):
    input = {}
    input = {"Sero": Sero, "FWP_date":FWP_date , "FWP_cases": FWP_cases, "SWP_date":SWP_date, "SWP_cases":SWP_cases, "R3":R3, "AverageDurationOfWanning":wa, "ThirdWaveImmuneEscape":thie,'TW_Emergence_date':TW_Emergence_date, "LockdownStartDate":LockdownStartDate, "LockdownEndDate":LockdownEndDate, "LockdownEffectiveness":effLck,"PopulationDensity":PopulationDensity, "VaccinationDuration":vaccDuration,"VaccinationCoverage":vaccCoverage, "proportionHospital":proportionHospital, "proportionOxygen":proportionOxygen, "homeCare": homecare}
    runmd = srmb.CovidApp(input)
    # print(input)
    
    data, R1_cases,R1_index, all_end_index,preparedness_list,seroAlert = runmd.get_json()
    # print("rj",all_end_index)
    #covid_model_v5_2.plotsir(data)
    
    data1=json.loads(data)
    # print(data1)
    return data1, R1_cases, R1_index, all_end_index,preparedness_list, seroAlert

# data,R1_cases,R1_index,all_end_index,preparedness_list,serowarning=createoutputjson(Sero=14.2, FWP_date="29-8-2020",  FWP_cases=178, SWP_date="31-5-2021", SWP_cases=270, R3=0.0, wa=0.0,thie=0.0, TW_Emergence_date="" , LockdownStartDate="16-05-2021", LockdownEndDate="15-07-2021", effLck=0.5, PopulationDensity=0.0, vaccDuration=0.0, vaccCoverage=0.0, proportionHospital=0.2, proportionOxygen=0.6, homecare=1)
# data,R1_cases,R1_index,all_end_index,preparedness_list,serowarning=createoutputjson(Sero=8.1, FWP_date="17-09-2020",  FWP_cases=93180, SWP_date="06-5-2021", SWP_cases=391232, R3=0.0, wa=0.0,thie=0.0, TW_Emergence_date="" , LockdownStartDate="19-04-2021", LockdownEndDate="29-05-2021", effLck=0.5, PopulationDensity=0.0, vaccDuration=0.0, vaccCoverage=0.0, proportionHospital=1, proportionOxygen=1, homecare=None)
# print(preparedness_list)