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

import sirmodel

#popsize, beta3, wa, thie, r2p, seroprevalence, d2p,FirstPeaktDate, LockdownStartDate, LockdownEndDate, effLck, vaccRate, vaccDays
# popsize, beta3, wa, thie, r2p, sterilePrev, d2p, LockdownStartDate, LockdownEndDate, effLck, vaccRate, vaccDays
def createoutputjson(r1=0.0, r2=0.0,  r3=0.0, wa=0.0,thie=0.0, FirstPeaktDate="", ThirdWaveEmergenceDate='' , LockdownStartDate="", LockdownEndDate="", effLck="",PopulationDensity=0.0, vaccDuration=0.0,vaccCoverage=0.0):
    input = {}
    input = {"R1": r1, "R2": r2, "R3": r3, "AverageDurationOfWanning":wa, "ThirdWaveImmuneEscape":thie, "FirstPeakDate":FirstPeaktDate,'ThirdWaveEmergenceDate':ThirdWaveEmergenceDate, "LockdownStartDate":LockdownStartDate, "LockdownEndDate":LockdownEndDate, "LockdownEffectiveness":effLck,"PopulationDensity":PopulationDensity, "VaccinationDuration":vaccDuration,"VaccinationCoverage":vaccCoverage}
    runmd = sirmodel.CovidApp(input)
    #print(input)
    
    data, R1_cases,R1_index, all_end_index,preparedness_list = runmd.get_json()
    #covid_model_v5_2.plotsir(data)
    
    data1=json.loads(data)
    # print(data1)
    return data1, R1_cases, R1_index, all_end_index,preparedness_list
