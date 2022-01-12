#!/usr/bin/env python
# coding: utf-8

from scipy.integrate import odeint
import datetime
import json
import numpy as np
import pandas as pd
from itertools import repeat
from scipy.interpolate import interp1d
import math
import R1_R2_calc 
from scipy.optimize import least_squares
import scipy.optimize as optimize

class CovidApp:

    def __init__(self, string):
        
        self.string = string

    def get_json(self):        
        # req_data = request.get_json()
        #a = json.loads(self.string)        
        data=self.run_scenario(self.string)        
        return data,self.R1_cases, self.R_index_final, self.all_end_index_final, self.preparedness_list
        

    def prep_scenario_dict(self,intervention_state_df,FirstPeakDate,FWP_index, all_end_index ):
         
        scenario_dict = dict()  
        preparedness_list=[] 
        # preparedness_precent=[0.05,0.05,0.25,0.17,0.40,0.60,0.24,0.12,0.12]
        preparedness_precent=[0.05,0.05,0.25,0.217,0.415,0.621,0.237,0.129,0.142]
        Cv_effectiveness_percent=(1-0.6)
         
        ##################  Without vaccination- S,R, C_diff component to dictionary ###############################################
        
        if len(intervention_state_df.columns)<=9:        
            scenario_dict['t'] = (intervention_state_df.t[3]).tolist()
            scenario_dict['no_intervention_s'] = ( intervention_state_df.S[3]).tolist()
            scenario_dict['no_intervention_r'] = ( intervention_state_df.R1[3]).tolist()
            scenario_dict['no_intervention_c'] = ( intervention_state_df.C[3]).tolist()
            
            #scenario_dict['no_intervention_r']=[x + y for (x, y) in zip(( intervention_state_df.R1[3]).tolist(),( intervention_state_df.R2[3]).tolist())]
            #state_list=intervention_state_df.C[3]
            #scenario_dict['no_intervention_c_diff']=[state_list[i + 1] - state_list[i] for i in range(len(state_list)-1)] 
            scenario_dict['no_intervention_c_diff'] = [j - i for i, j in zip((intervention_state_df.C[3]).tolist()[:-1], (intervention_state_df.C[3]).tolist()[1:])]        # rate of change(diff) of C value
            if all_end_index[2]== all_end_index[3]:
                scenario_dict['no_intervention_c_diff'][0:all_end_index[2]]=list(filter(lambda x : x > 0, scenario_dict['no_intervention_c_diff'][0:all_end_index[2]])) #keep diff vaue is 3rd wave not occur
            else:    
                scenario_dict['no_intervention_c_diff']=list(filter(lambda x : x > 0, scenario_dict['no_intervention_c_diff']))   # remove negative value after diff
            
            #----------------------Hospital system preparedness without vaccination----------------------------------------------------------------------------------
            scenario_dict['no_intervention_c1_diff'] = [j - i for i, j in zip((intervention_state_df.C[0]).tolist()[:-1], (intervention_state_df.C[0]).tolist()[1:])] # diff value
            scenario_dict['no_intervention_c2_diff'] = [j - i for i, j in zip((intervention_state_df.C[1]).tolist()[:-1], (intervention_state_df.C[1]).tolist()[1:])] # diff value
            scenario_dict['no_intervention_c3_diff'] = [j - i for i, j in zip((intervention_state_df.C[2]).tolist()[:-1], (intervention_state_df.C[2]).tolist()[1:])] # diff value
            
            if all_end_index[2]!= all_end_index[3]:
                
                #Age group wise hospitalization count
                preparedness_list.append((max(list(scenario_dict['no_intervention_c1_diff'][all_end_index[2]:all_end_index[3]]))*preparedness_precent[0])*10)
                preparedness_list.append((max(list(scenario_dict['no_intervention_c2_diff'][all_end_index[2]:all_end_index[3]]))*preparedness_precent[1])*10)
                preparedness_list.append((max(list(scenario_dict['no_intervention_c3_diff'][all_end_index[2]:all_end_index[3]]))*preparedness_precent[2])*10)
                
                #Age group wise oxygen bed and ventilation bed count
                for i in range (0,6):                     
                    preparedness_list.append(preparedness_list[i]*preparedness_precent[i+3])
                
                #Total count of each requirement
                for i in range (0,3):
                    j=3*i
                    preparedness_list.append(preparedness_list[j]+preparedness_list[j+1]+preparedness_list[j+2])
            
            else:                 
                preparedness_list=[0]*12  #third not occur 
                    
            preparedness_list=[round(item,2) for item in preparedness_list] 
      
         ################### Vaccination- get S,R, C_diff component to dictionary ###############################################
        
        if len(intervention_state_df.columns)>9: 
            scenario_dict['t'] = (intervention_state_df.t[3]).tolist()
            scenario_dict['no_intervention_s'] = ( intervention_state_df.S[3]).tolist()
            scenario_dict['no_intervention_r'] = ( intervention_state_df.R1[3]).tolist()
            scenario_dict['no_intervention_c'] = ( intervention_state_df.C[3]).tolist()
            scenario_dict['no_intervention_ct_diff'] = [j - i for i, j in zip((intervention_state_df.Ct[3]).tolist()[:-1], (intervention_state_df.Ct[3]).tolist()[1:])] # diff value with vaccination
            scenario_dict['no_intervention_ct0_diff'] = [j - i for i, j in zip((intervention_state_df.Ct0[3]).tolist()[:-1], (intervention_state_df.Ct0[3]).tolist()[1:])] # diff value without vaccination
            
            if all_end_index[2]== all_end_index[3]:
                scenario_dict['no_intervention_ct_diff'][0:all_end_index[2]]=list(filter(lambda x : x > 0, scenario_dict['no_intervention_ct_diff'][0:all_end_index[2]])) 
                scenario_dict['no_intervention_ct0_diff'][0:all_end_index[2]]=list(filter(lambda x : x > 0, scenario_dict['no_intervention_ct0_diff'][0:all_end_index[2]])) 
            else:    
                scenario_dict['no_intervention_ct_diff']=list(filter(lambda x : x > 0, scenario_dict['no_intervention_ct_diff']))   # remove negative value after diff
                scenario_dict['no_intervention_ct0_diff']=list(filter(lambda x : x > 0, scenario_dict['no_intervention_ct0_diff']))   # remove negative value after diff   
            
            ########################Hospital system preparedness#####################################################
            scenario_dict['no_intervention_c1_diff'] = [j - i for i, j in zip((intervention_state_df.C[0]).tolist()[:-1], (intervention_state_df.C[0]).tolist()[1:])] # diff value
            scenario_dict['no_intervention_c2_diff'] = [j - i for i, j in zip((intervention_state_df.C[1]).tolist()[:-1], (intervention_state_df.C[1]).tolist()[1:])] # diff value
            scenario_dict['no_intervention_c3_diff'] = [j - i for i, j in zip((intervention_state_df.C[2]).tolist()[:-1], (intervention_state_df.C[2]).tolist()[1:])] # diff value
            
            scenario_dict['no_intervention_cv1_diff'] = [j - i for i, j in zip((intervention_state_df.Cv[0]).tolist()[:-1], (intervention_state_df.Cv[0]).tolist()[1:])] # diff value
            scenario_dict['no_intervention_cv2_diff'] = [j - i for i, j in zip((intervention_state_df.Cv[1]).tolist()[:-1], (intervention_state_df.Cv[1]).tolist()[1:])] # diff value
            scenario_dict['no_intervention_cv3_diff'] = [j - i for i, j in zip((intervention_state_df.Cv[2]).tolist()[:-1], (intervention_state_df.Cv[2]).tolist()[1:])]
            
            #Third wave occured preparedness
            if all_end_index[2]!=all_end_index[3]:
                preparedness_temp_C=[]
                preparedness_temp_Cv=[]
                
                #without hospital requirement
                preparedness_temp_C.append((max(list(scenario_dict['no_intervention_c1_diff'][all_end_index[2]:all_end_index[3]]))*preparedness_precent[0])*10)
                preparedness_temp_C.append((max(list(scenario_dict['no_intervention_c2_diff'][all_end_index[2]:all_end_index[3]]))*preparedness_precent[1])*10)
                preparedness_temp_C.append((max(list(scenario_dict['no_intervention_c3_diff'][all_end_index[2]:all_end_index[3]]))*preparedness_precent[2])*10)
                
                #without vaccine oxygen and ventilator requirement
                for i in range(0,6):
                    preparedness_temp_C.append(preparedness_temp_C[i]*preparedness_precent[i+3])
                
                #with vaccine reduce hospital requirement by (1-0.6) 
                preparedness_temp_Cv.append(((max(list(scenario_dict['no_intervention_cv1_diff'][all_end_index[2]:all_end_index[3]]))*preparedness_precent[0])*Cv_effectiveness_percent)*10)
                preparedness_temp_Cv.append(((max(list(scenario_dict['no_intervention_cv2_diff'][all_end_index[2]:all_end_index[3]]))*preparedness_precent[1])*Cv_effectiveness_percent)*10)
                preparedness_temp_Cv.append(((max(list(scenario_dict['no_intervention_cv3_diff'][all_end_index[2]:all_end_index[3]]))*preparedness_precent[2])*Cv_effectiveness_percent)*10)
                
                #with vaccine reduce oxygen and ventilator requirement by (1-0.6) 
                for i in range (0,6):
                    preparedness_temp_Cv.append((preparedness_temp_Cv[i]*preparedness_precent[i+3])*Cv_effectiveness_percent)
                
                #calculating ct i.e c+cv requirment
                preparedness_list = [x + y for (x, y) in zip(preparedness_temp_C,preparedness_temp_Cv)]
                
                # Calculating total for each requirement
                for i in range (0,3):
                    j=3*i
                    preparedness_list.append(preparedness_list[j]+preparedness_list[j+1]+preparedness_list[j+2])
            
            #Third wave not occur no preparedness       
            else:   
                preparedness_list=[0]*12
                    
            preparedness_list=[round(item,2) for item in preparedness_list] 
            
        #################################### Embedding dates array on x Axis #################################### 
        if len(intervention_state_df.columns)<=9:
            start_date_x_axis=FirstPeakDate - datetime.timedelta(days=int(FWP_index))       
            date_xaxis = []
            
            for i in range(0,(len(intervention_state_df.C[3])-1)):
                date_xaxis.append(str(start_date_x_axis + datetime.timedelta(days=int(i))))
            
            scenario_dict['date'] = date_xaxis
        
        elif len(intervention_state_df.columns)>9:
            start_date_x_axis=FirstPeakDate - datetime.timedelta(days=int(FWP_index))        
            date_xaxis = []
            
            for i in range(0,(len(intervention_state_df.Ct[3])-1)):
                date_xaxis.append(str(start_date_x_axis + datetime.timedelta(days=int(i))))
            
            scenario_dict['date'] = date_xaxis
        
        ################################## getting recovery component ###################################
        R_index=int(FWP_index)
        R1_cases=scenario_dict['no_intervention_r'][R_index]  
        self.FWP_cases=scenario_dict['no_intervention_r'][int(FWP_index)]  
        
        ################################ Remove data point before 2020-01-01###########################
        try:
            indexJan=scenario_dict['date'].index("2020-01-01")
            
            scenario_dict_final={}
            
            for sub in scenario_dict:      
                # slicing trim before Jan index and reassigning
                scenario_dict_final[sub] = scenario_dict[sub][indexJan:]
                
            all_end_index_final= [item-indexJan if item>0 else item for item in all_end_index]     
                
            R_index_final=R_index-indexJan
            
            return scenario_dict_final,preparedness_list, R1_cases,all_end_index_final,R_index_final
        except:
            return scenario_dict,preparedness_list, R1_cases,all_end_index,R_index
    
    ##################################################################################################################### 
    
    def prep_output_json(self, scenario_dict):
        
        garph_df = pd.DataFrame()       
        garph_df = garph_df.append(scenario_dict, ignore_index=True) 
                
        return garph_df.to_json(orient='records')
    
    
    def run_scenario(self,user_input_dict):
        
        self.TotalPopulation = 1000000
        Sero = 1.0729 if user_input_dict['Sero'] == 0.0 else user_input_dict['Sero']
        FirstPeakDate = datetime.datetime.strptime('2020-9-16', '%Y-%m-%d').date() if user_input_dict['FWP_date'] == '' else datetime.datetime.strptime(user_input_dict['FWP_date'], '%Y-%m-%d').date()
        self.SecondPeakDate = datetime.datetime.strptime('2020-9-16', '%Y-%m-%d').date() if user_input_dict['SWP_date'] == '' else datetime.datetime.strptime(user_input_dict['SWP_date'], '%Y-%m-%d').date()
        FWP_cases = 1.782 if user_input_dict['FWP_cases'] == 0.0 else user_input_dict['FWP_cases']
        SWP_cases = 1.782 if user_input_dict['SWP_cases'] == 0.0 else user_input_dict['SWP_cases']
        Ratio_peak=round((SWP_cases/FWP_cases),1)        
        self.R1=R1_R2_calc.get_R_1(Sero)
        R2 = self.R1
        #self.R3 = R2 if user_input_dict['R3'] == 0.0 else user_input_dict['R3']
        self.PeakDuration=(self.SecondPeakDate-FirstPeakDate).days
        self.PeakRatio=(SWP_cases/FWP_cases)
        self.R3_percent = None if user_input_dict['R3'] == 0.0 else user_input_dict['R3']
        self.AverageDurationOfWanning = 0 if user_input_dict['AverageDurationOfWanning'] == 0.0 else 1/user_input_dict['AverageDurationOfWanning'] 
        self.ThirdWaveImmuneEscape = None if user_input_dict['ThirdWaveImmuneEscape'] == 0.0 else user_input_dict['ThirdWaveImmuneEscape'] 
        self.LockdownEffectiveness = 1 if user_input_dict['LockdownEffectiveness'] == 0.0 else 1-user_input_dict['LockdownEffectiveness'] 
        self.ThirdWaveEmergenceDate =None if user_input_dict['TW_Emergence_date'] == '' else datetime.datetime.strptime(user_input_dict['TW_Emergence_date'], '%Y-%m-%d').date()
        self.LockdownStartDate = None if user_input_dict['LockdownStartDate'] == '' else datetime.datetime.strptime(user_input_dict['LockdownStartDate'], '%Y-%m-%d').date()
        self.LockdownEndDate =None if user_input_dict['LockdownEndDate'] == '' else datetime.datetime.strptime(user_input_dict['LockdownEndDate'], '%Y-%m-%d').date()
        self.PopulationDensity = None if user_input_dict['PopulationDensity'] == 0.0 else user_input_dict['PopulationDensity'] 
        self.VaccinationDuration= None if user_input_dict['VaccinationDuration'] == 0.0 else user_input_dict['VaccinationDuration']
        self.VaccinationCoverage= 0 if user_input_dict['VaccinationCoverage'] == 0.0 else user_input_dict['VaccinationCoverage']
        # self.populationPercent=[0.46,0.445,0.095]
        self.populationPercent=[0.328, 0.573, 0.099]
        # FWEindextemp=400
        
        # self.model_input=([self.TotalPopulation*0.46,self.TotalPopulation*0.445,self.TotalPopulation*0.095],
        #                    self.R1, R2, R2, self.PeakDuration, self.PeakRatio, self.AverageDurationOfWanning,
        #                    self.ThirdWaveImmuneEscape, self.LockdownEffectiveness,self.ThirdWaveEmergenceDate,
        #                    self.LockdownStartDate,self.LockdownEndDate,self.PopulationDensity,
        #                    self.VaccinationDuration,self.VaccinationCoverage,FWEindextemp)
        
       ################## Passing parameter to Sirmodel #########################################################################################
        def optimize_FWE_R2(x):
            
            FWEindex=x[1]
            R2=x[0]
            
            intervention_graph = SirModel(N=[self.TotalPopulation*self.populationPercent[0],self.TotalPopulation*self.populationPercent[1],self.TotalPopulation*self.populationPercent[2]],
                                        R1=self.R1, R2=R2, R3_percent=self.R3_percent, PeakDuration=self.PeakDuration, PeakRatio=self.PeakRatio,
                                        SecondPeakDate=self.SecondPeakDate,
                                       AverageDurationOfWanning=self.AverageDurationOfWanning,
                                        ThirdWaveImmuneEscape=self.ThirdWaveImmuneEscape,
                                        LockdownEffectiveness=self.LockdownEffectiveness,    
                                        ThirdWaveEmergenceDate=self.ThirdWaveEmergenceDate,
                                        LockdownStartDate=self.LockdownStartDate,
                                        LockdownEndDate=self.LockdownEndDate,
                                        PopulationDensity=self.PopulationDensity,
                                        VaccinationDuration=self.VaccinationDuration,
                                        VaccinationCoverage=self.VaccinationCoverage,FWEindex=FWEindex)
        
            result  = intervention_graph.run_model_optimize()
            
            return result
        
        result = optimize.minimize(optimize_FWE_R2, (2,500),method='nelder-mead')
        
        R2=result.x[0]
        
        FWEindex=result.x[1]
        
        # print(self.R1)
        
        # print(result)
        
        # R2=1.32240973  #result.x[0]1.32240973, 640.48119427
        
        # FWEindex=640.48119427         #result.x[1]
        
        #self.R3 = R2            #if user_input_dict['R3'] == 0.0 else user_input_dict['R3']
        
        intervention_graph_1 = SirModel(N = [self.TotalPopulation*self.populationPercent[0],self.TotalPopulation*self.populationPercent[1],self.TotalPopulation*self.populationPercent[2]],
                                        R1=self.R1, R2=R2, R3_percent=self.R3_percent, PeakDuration=self.PeakDuration, PeakRatio=self.PeakRatio,
                                        SecondPeakDate=self.SecondPeakDate,
                                        AverageDurationOfWanning=self.AverageDurationOfWanning,
                                        ThirdWaveImmuneEscape=self.ThirdWaveImmuneEscape,
                                        LockdownEffectiveness=self.LockdownEffectiveness,    
                                        ThirdWaveEmergenceDate=self.ThirdWaveEmergenceDate,
                                        LockdownStartDate=self.LockdownStartDate,
                                        LockdownEndDate=self.LockdownEndDate,
                                        PopulationDensity=self.PopulationDensity,
                                        VaccinationDuration=self.VaccinationDuration,
                                        VaccinationCoverage=self.VaccinationCoverage,FWEindex=FWEindex)
        #Running SIR model
        
        intervention_state_df, FWP_index, all_end_index  = intervention_graph_1.run_model_1()
               
       ###############Prepareoutput dictionary #####################################################################################################
                    
       
        scenario_dict_final,self.preparedness_list, self.R1_cases,self.all_end_index_final,self.R_index_final = self.prep_scenario_dict(intervention_state_df,FirstPeakDate,FWP_index, all_end_index )  
        
        return self.prep_output_json(scenario_dict_final)
               
       ###############Prepareoutput dictionary #####################################################################################################
                    
       
        # scenario_dict_final,self.preparedness_list, self.R1_cases,self.all_end_index_final,self.R_index_final = self.prep_scenario_dict(intervention_state_df,FirstPeakDate,FWP_index, all_end_index )  
        # print("sir",self.all_end_index_final)
        # return self.prep_output_json(scenario_dict_final)
    
    
        
    
class SirModel:
      
    ########################################Intitial Conditions########################################
    eta =0.25    # rate of developing infectiousness
    gamma = 0.2  # Recovery rate 
    r = 1.0      # Rate of developing symptoms
    k = 5/6      # Relative infectiousness of asymptomatic vs symptomatic infection
    p_sym =0.5   # Proportion developing symptoms    
    d=1/240      # Delay rate from R1 to R2    
    #mu = np.array([0.0002, 0.002, 0.024])  #Previous Mortality rate for severe cases 
    mu = np.array([0.0002, 0.0025, 0.0189])  #latest value Mortality rate for severe cases  
    age_matrix = np.array([[1.37, 1.43, 0.05], [2.52,2.90,0.10], [0.28,0.34,0.02]]) #Connectivity matrix between age group i with age group j
    
    
    # age_matrix = np.array([[0.1030,	0.4862,	0.0111], [1.1355, 6.4962, 0.1382], [0.0970, 0.5169, 0.0160]]) #Connectivity matrix between age group i with age group j
    
    columns = age_matrix.shape[1]
    rows = age_matrix.shape[0]
    
    
    def __init__( self, N, R1, R2, R3_percent,PeakDuration,PeakRatio,SecondPeakDate,AverageDurationOfWanning,
                 ThirdWaveImmuneEscape,LockdownEffectiveness,
                 ThirdWaveEmergenceDate,LockdownStartDate,LockdownEndDate,
                 PopulationDensity,VaccinationDuration,VaccinationCoverage,FWEindex):
       
        
        self.N = np.array([0,0,0]) if N is None else N               # Population
        
        U1,E1,A1,P1,S1,R11,R21,C1 = N[0], 0, 0, 0, 0, 0, 0 ,0        # initial conditions vector age group 2
        U2,E2,A2,P2,S2,R12,R22,C2 = N[1]-20, 0, 0, 0, 20 , 0, 0, 0  # Initial conditions vector age group 2
        U3,E3,A3,P3,S3,R13,R23,C3 = N[2], 0, 0, 0, 0, 0, 0 , 0       # Initial conditions vector age group 3
        
        self.y0 = np.array([U1,E1,A1,P1,S1,R11,R21,C1,U2,E2,A2,P2,S2,R12,R22,C2,U3,E3,A3,P3,S3,R13,R23,C3])
        
        self.SecondPeakDate=SecondPeakDate
        self.Wa=AverageDurationOfWanning
        self.ThirdWaveImmuneEscape=ThirdWaveImmuneEscape        
        self.ThirdWaveEmergenceDate=ThirdWaveEmergenceDate
        self.R3_percent=R3_percent
        self.PopulationDensity=PopulationDensity
        #=============================Lockdown inputs==============================================================
        if LockdownStartDate!=None:
            L_phase_2_days=(LockdownEndDate-LockdownStartDate).days
        else:
            L_phase_2_days=45
            
        #print(L_phase_2_days)
        self.LockdownStartDays=50
        self.L_phase_1_days =20           #int(0.45*self.lockdown_duration) 
        self.L_phase_2_days =L_phase_2_days
        self.LockdownReleaseDays=90 
        self.LockdownEffectiveness=LockdownEffectiveness
        self.LockdownStartDate=LockdownStartDate
        self.LockdownEndDate=LockdownEndDate
        
        
        #=============================Vaccination input, constant and initial condition =============================
        self.VaccinationDuration=VaccinationDuration
        self.C1_v=0                                     # vaccine transmission effectiveness
        self.C2_v=0.6                                   # vaccine seveverity effectiveness
        self.VaccinationCoverage=VaccinationCoverage    # Population vaccinated
        
        
        U1v,E1v,A1v,P1v,S1v,R11v,R21v,C1v,C1t = 0, 0, 0, 0, 0, 0, 0 , 0, 0 # initial conditions: one infected, rest uninfected
        U2v,E2v,A2v,P2v,S2v,R12v,R22v,C2v,C2t = 0, 0, 0, 0, 0 , 0, 0, 0, 0 # Initial conditions vector age group 2
        U3v,E3v,A3v,P3v,S3v,R13v,R23v,C3v,C3t = 0, 0, 0, 0, 0, 0, 0 , 0, 0 # Initial conditions vector age group 3
        
        self.y0_v = np.array([U1,E1,A1,P1,S1,R11,R21,C1,U1v,E1v,A1v,P1v,S1v,R11v,R21v,C1v,C1t,
                              U2,E2,A2,P2,S2,R12,R22,C2,U2v,E2v,A2v,P2v,S2v,R12v, R22v,C2v,C2t,
                              U3,E3,A3,P3,S3,R13,R23,C3,U3v,E3v,A3v,P3v,S3v,R13v,R23v,C3v,C3t])        
        
        #=========================Function to calculate max eigen matrix value ==================================== 
        
        # def calc_beta():
            
        #     size = 12
        #     F = np.zeros(shape=(size,size))
        #     V = np.zeros((size,size))
            
        #     for i in range(0,3):
        #         for j in range(3,size):
        #             if j <= 8:
        #                 F[i][j] = self.age_matrix[i][j%3] * self.k * self.N[i] / self.N[j%3]
        #             elif j > 8:
        #                 F[i][j] = self.age_matrix[i][j%3] * self.N[i] / self.N[j%3]
                    
        #     for i in range(0,3):
        #         V[i][i] = 1.0/self.eta
        #         V[i+3][i] = (1.0 - self.p_sym) / self.gamma
        #         V[i+3][i+3] = 1.0/self.gamma
        #         V[i+6][i+6] = 1.0/self.r
        #         #V[i+9][i+9] = 1.0/self.gamma
        #         V[i+9][i] = self.p_sym/(self.gamma+self.mu[i])
        #         V[i+9][i+9] = 1.0/(self.gamma+self.mu[i])
        #         V[i+9][i+6] = 1.0/(self.gamma+self.mu[i])
               
        #     M = max(np.linalg.eigvals(np.dot(F,V)))
            
        #     return M     
        
        #==========================calculate Reproduction rate and Transmission rate =========================================
        
        self.M =21.2377759915869    # calc_beta() 21.2378      # max eigen value
        self.R1=R1                # wave 1 Reproduction rate
        self.R2=R2        #R2                # wave 2 Reproduction rate
                
        if self.PopulationDensity==None:   #update wave 3 Reproduction rate w.r.t added population density
            self.R3=R2
        elif self.PopulationDensity!=None:            
            theta=0.16 * math.log(1 + self.PopulationDensity)   
            self.R3=R2+theta
            
        if  self.R3_percent==None: 
            self.R4=self.R3
            self.Beta_4=self.R4/self.M
        elif  self.R3_percent!=None:    
            self.R4=self.R3*(1+self.R3_percent)
            self.Beta_4=self.R4/self.M
            
            
    

        self.Beta_1=self.R1/self.M  # wave 1 Transmission rate
        self.Beta_2=self.R2/self.M  # wave 2 Transmission rate 
        self.Beta_3=self.R3/self.M  # wave 3 Transmission rate
        
        #============================Grid first wave and duration FWP and TWS==================================================
        
        self.FWE_index=math.ceil(FWEindex)      # Time Instant for first wave
        
        #self.Duration_FWP_TWS=(ThirdWaveEmergenceDate-FirstPeakDate).days
        
        # self.FW_cutoff_percent=FW_cutoff_percent
        self.PeakRatio=PeakRatio
        # self.FirstPeakDate=FirstPeakDate
        # self.SecondPeakDate=SecondPeakDate
        self.PeakDuration=PeakDuration
        
        
        
        
    ############################## Derivative function  #######################################################################
        
    def deriv (self,y0, t, beta, N, eta, gamma, p_sym, mu, r, Wa, d, L_flag=None):        
              
        state_arr = np.reshape(y0, (-1,8)) 
        
        y0_final= []
        
        if L_flag==None:
            Betac=beta
            Wac=Wa
            
        elif L_flag==1:                        # beta value for lockdown phase 1 (decrease beta) 
            Betac=self.finterp_phase_1(t)
            Wac=Wa
            
        elif L_flag==2:                        # beta value for lockdown phase 2 (increase beta) 
            Betac=self.finterp_phase_3(t)
            Wac=Wa
            
            
        for i in range(3):

            U, E, A, P, S, R1, R2,C = state_arr[i]            

            __lambda = Betac * sum(
                (
                    self.age_matrix[i][j]* ((state_arr[j][4]) + self.k * (state_arr[j][2]) + state_arr[j][3])
                )/N[j] for j in range(self.columns)
                                       )
            #np.sum(state_arr[j][0:7]
    
            dUdt = (-__lambda * U) + (Wac * R1) + (Wac * R2)        #-λ_j U_j+〖w_a  R1〗_j+〖w_a  R2〗_j

            dEdt = (__lambda * U )- (eta * E)            # λ_j U_j-ηE_j

            dAdt = (eta * (1-p_sym) * E) - (gamma * A )    #η (1- p((sym) ) ) E_j-γA_j
            
            dPdt = (eta * p_sym * E) - (r * P )           #η〖 p((sym))  E_j-r P_j            

            dSdt = (r * P)-((gamma + mu[i])* S)    #rP_j-(〖γ+μ〗_j) S_j            
                        
            dR1dt =  (gamma *( A + S))- (d * R1) - (Wac * R1)     #γ〖(A〗_j+S_j)-〖d R1〗_j-〖w_a  R1〗_j
            
            dR2dt =  (d * R1)-(Wac * R2)                                   #〖d R1〗_j-〖w_a  R2〗_j
            
            dCdt=   r*P 
            
            y0_final.extend(np.array([dUdt, dEdt, dAdt, dPdt,dSdt, dR1dt, dR2dt,dCdt])) 
                  
        return y0_final
    
    
    ############################## Vaccination Derivative function ####################################################
        
    def deriv_vacc (self,y0, t, beta, N, eta, gamma, p_sym, mu, r, Wa, d,R_vi,C1_v,C2_v,L_flag=None):        
             
        state_arr = np.reshape(y0, (-1,17)) 
       
        y0_final= []
        
        if L_flag==None:
            Betac=beta
            Wac=Wa
            
        elif L_flag==1:
            Betac=self.finterp_phase_1(t)   # beta value for lockdown phase 1 (decrease beta)
            Wac=Wa
            
        elif L_flag==2:
            Betac=self.finterp_phase_3(t)   # beta value for lockdown phase 2 (increase beta) 
            Wac=Wa
            
       
        for i in range(3):
            
            if i==0:
                R_v=0
            else:
                R_v=R_vi      
   
            U, E, A, P, S, R1, R2,C,Uv, Ev, Av, Pv, Sv, R1v, R2v, Cv, Ct = state_arr[i] 
            
            __lambda = Betac * sum(
                (
                    (self.age_matrix[i][j]* ((state_arr[j][4]) + self.k * (state_arr[j][2]) + state_arr[j][3]))+
                    ((1-C1_v)* self.age_matrix[i][j]* ((state_arr[j][12]) + self.k * (state_arr[j][10]) + state_arr[j][11]))
                )/N[j] for j in range(self.columns)
                                        )
            #print(__lambda)
           
            dUdt = (-__lambda * U) + (Wac * R1) + (Wac * R2)-(R_v*U)        #-λ_j U_j+〖w_a  R1〗_j+〖w_a  R2〗_j  - Rvj Uj
           
            dEdt = (__lambda * U )- (eta * E)                               # λ_j U_j-ηE_j
           
            dAdt = (eta * (1-p_sym) * E) - (gamma * A )                     #η (1- p((sym) ) ) E_j-γA_j
           
            dPdt = (eta * p_sym * E) - (r * P )                             #η〖 p((sym))  E_j-r P_j            
           
            dSdt = (r * P)-((gamma + mu[i])* S)                             #rP_j-(〖γ+μ〗_j) S_j            
           
            dR1dt =  (gamma *( A + S))- (d * R1) - (Wac * R1)               #γ〖(A〗_j+S_j)-〖d R1〗_j-〖w_a  R1〗_j
           
            dR2dt =  (d * R1)-(Wac * R2)                                    #〖d R1〗_j-〖w_a  R2〗_j
           
            dCdt=   r*P 
            
        #--------------------------vaccination-----------------------------------------               
           
            dUvdt = (-__lambda * Uv) + (Wac * R1v) + (Wac * R2v)+(R_v*U)    #-λ_j U_j+〖w_a  R1〗_j+〖w_a  R2〗_j+ Rv Uj
           
            dEvdt = ((1-C1_v)*__lambda * Uv )-(eta * Ev)                    # (1-C1)λ_j U_j-ηE_j
           
            dAvdt = (eta * (1-(1-C2_v)*p_sym) * Ev) - (gamma * Av )         # η (1-(1-c2) p^((sym) ) ) E_j-γA_j
           
            dPvdt = (eta * (1-C2_v)*p_sym * Ev) - (r * Pv )                 # η〖(1-c2) p〗^((sym))  E_j-r P_j        
           
            dSvdt = (r * Pv)-((gamma + mu[i])* Sv)                          #rP_j-(〖γ+μ〗_j) S_j            
           
            dR1vdt =  (gamma *( Av + Sv))- (d * R1v) - (Wac * R1v)          #γ〖(A〗_j+S_j)-〖d R1〗_j-〖w_a  R1〗_j
           
            dR2vdt =  (d * R1v)-(Wac * R2v)                                 #〖d R1〗_j-〖w_a  R2〗_j
           
            dCvdt=   r*Pv 
            
            dCtdt=   r*(P+Pv)
           
            y0_final.extend(np.array([dUdt, dEdt, dAdt, dPdt,dSdt, dR1dt, dR2dt,dCdt, dUvdt, dEvdt, dAvdt, dPvdt,dSvdt, dR1vdt, dR2vdt,dCvdt,dCtdt])) 
         
        return y0_final
    
    ############################## Function to get first wave peak and first wave end index ####################################################    
       
    def FirstWavEndindex (self,state_arr,vaccflag=None):
            
        state_df = pd.DataFrame() 
        
        if vaccflag==None:
        
            for i in range(0, state_arr.shape[0], 8):                                
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7]}                     
                state_df = state_df.append(state_dict,ignore_index=True)
            state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
           
            state_list=state_df.C[3]    
                
                
        elif vaccflag==1:
            
            for i in range(0, state_arr.shape[0], 17):                                
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7],
                              'Uv':state_arr[i+8],'Ev':state_arr[i+9],'Av':state_arr[i+10],'Pv':state_arr[i+11],
                              'Sv':state_arr[i+12],'R1v':state_arr[i+13],'R2v':state_arr[i+14], 'Cv':state_arr[i+15],
                              'Ct':state_arr[i+16]}                     
                state_df = state_df.append(state_dict,ignore_index=True)
            
        
            state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
           
            state_list=state_df.Ct[3]
        
        state_list_Cdiff=[state_list[i + 1] - state_list[i] for i in range(len(state_list)-1)] #calculate Cdiff
        
        Peak_value=max(state_list_Cdiff)
        
        Peak_index= state_list_Cdiff.index(max(state_list_Cdiff)) 
            
        return state_df,Peak_value,Peak_index
    
    #################################Second wave end limit##############################################################
    
    # def SecondWaveMinIndex (self,state_arr,vaccflag=None):
    
    #     state_df = pd.DataFrame()  
        
    #     if vaccflag==None:
        
    #         for i in range(0, state_arr.shape[0], 8):
                            
    #             state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
    #                           'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7]} 
                
    #             state_df = state_df.append(state_dict,ignore_index=True)
                
    #     elif vaccflag==1:
            
    #         for i in range(0, state_arr.shape[0], 17):
                            
    #             state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
    #                           'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7],
    #                           'Uv':state_arr[i+8],'Ev':state_arr[i+9],'Av':state_arr[i+10],'Pv':state_arr[i+11],
    #                           'Sv':state_arr[i+12],'R1v':state_arr[i+13],'R2v':state_arr[i+14], 'Cv':state_arr[i+15],
    #                           'Ct':state_arr[i+16]} 
                
    #             state_df = state_df.append(state_dict,ignore_index=True)
        
    #     state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
    
    #     state_list=state_df.C[3]
        
    #     state_list_Cdiff=[state_list[i + 1] - state_list[i] for i in range(len(state_list)-1)] #calculate Cdiff
        
    #     state_Cdiff_min_index= state_list_Cdiff.index(min(state_list_Cdiff)) 
        
    #     return state_Cdiff_min_index
    
        
    ############################### Third wave end limit ##############################################################
    
    def ThirdWaveEndlimit (self,state_arr,vaccflag=None, Wa=None, lckdn=None):
        
        state_df = pd.DataFrame()  
        
        if vaccflag==None:
        
            for i in range(0, state_arr.shape[0], 8):
                            
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7]} 
                
                state_df = state_df.append(state_dict,ignore_index=True)
                
            state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
           
            state_list=state_df.C[3]
               
                
        elif vaccflag==1:
            
            for i in range(0, state_arr.shape[0], 17):
                            
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7],
                              'Uv':state_arr[i+8],'Ev':state_arr[i+9],'Av':state_arr[i+10],'Pv':state_arr[i+11],
                              'Sv':state_arr[i+12],'R1v':state_arr[i+13],'R2v':state_arr[i+14], 'Cv':state_arr[i+15],
                              'Ct':state_arr[i+16]} 
                
                state_df = state_df.append(state_dict,ignore_index=True)
        
            state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
           
            state_list=state_df.Ct[3]
        
        state_list_Cdiff=[state_list[i + 1] - state_list[i] for i in range(len(state_list)-1)] #calculate Cdiff
        
        state_Cdiff_max_index= state_list_Cdiff.index(max(state_list_Cdiff)) 
        
        if vaccflag==None:
            if Wa==0:        
                ThirdDuration=state_Cdiff_max_index*6
                
            elif Wa!=0:
                ThirdDuration=state_Cdiff_max_index*8
                
        if vaccflag!=None:
            if lckdn!=None:
                if Wa==0:        
                    ThirdDuration=state_Cdiff_max_index*6
                    
                elif Wa!=0:
                    ThirdDuration=state_Cdiff_max_index*8  
            
            elif lckdn==None:
                if Wa==0:        
                    ThirdDuration=state_Cdiff_max_index*6
                    
                elif Wa!=0:
                    ThirdDuration=state_Cdiff_max_index*8
        return ThirdDuration

    ############################## run model function ######################################################
        
    def run_model_optimize(self):
        
        state_df = pd.DataFrame()  
        
        #----------------------First wave-------------------------------------------------------
        
        Lt1=np.arange(0,self.FWE_index,1)
                
        ret = odeint(self.deriv, self.y0, Lt1, args=(self.Beta_1,self.N, self.eta, self.gamma, 
                                                    self.p_sym, self.mu, self.r, self.Wa, self.d))  
         
        state_df_1,FWP_value,FWP_index =self.FirstWavEndindex(ret.T,None)
        
        y1=np.array(ret[-1,:])    #initial condition for second wave   
    
    #---------------------------Second wave before lockdown start--------------------------------------
        
        BeforeLockStart=self.FWE_index+self.LockdownStartDays
        
        Lt2=np.arange(self.FWE_index,BeforeLockStart,1)
                        
        ret2 = odeint(self.deriv, y1, Lt2, args=(self.Beta_2,self.N, self.eta, self.gamma, 
                                                        self.p_sym, self.mu, self.r, self.Wa, self.d))  
        
        y2=np.array(ret2[-1,:]) 
        
    #----------------------------Second wave Lockdown first Phase -------------------------------------
        #Lockdown duration days divide into two phase 
        
        L_phase_1_days=self.L_phase_1_days            #int(0.45*self.lockdown_duration)    
            
        L_phase_2_days=self.L_phase_2_days
        
        L_phase_1_end=L_phase_1_days+BeforeLockStart                 #int((0.45*self.lockdown_duration)+BeforeLockStart)    
        
        L_phase_2_end=L_phase_2_days+BeforeLockStart               #int((0.55*self.lockdown_duration)+L_phase_1_end)
        
        Lt_phase_1=np.arange(BeforeLockStart,L_phase_1_end,1)
        
        #In first phase of lockdown transmission rate decreases
        beta_phase_1=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2,L_phase_1_days)).tolist()
        
        beta_phase_1.reverse()    
        
        self.finterp_phase_1 = interp1d(Lt_phase_1,beta_phase_1,fill_value='extrapolate')  
        
        ret2_1 = odeint(self.deriv, y2, Lt_phase_1, args=(None, self.N, self.eta, self.gamma, 
                                                        self.p_sym, self.mu, self.r, self.Wa, self.d,1))  
        
        y2_1 =np.array(ret2_1[-1,:])            
    
    #--------------------------Second wave Lockdown Second  Phase ---------------------------------- 
        #In second phase of lockdown transmission rate is reduce constant value
        
        Lt_phase_2=np.arange(L_phase_1_end,L_phase_2_end,1)
        
        beta_phase_2=self.Beta_2*self.LockdownEffectiveness
        
        ret2_2 = odeint(self.deriv, y2_1, Lt_phase_2, args=(beta_phase_2,self.N, self.eta, self.gamma, 
                                                        self.p_sym, self.mu, self.r, self.Wa, self.d))        
        
        y2_2=np.array(ret2_2[-1,:])
    
    #----------------------Second wave after Lockdown release ---------------------------
    
        #  After Lockdown release reduce transmission rate increase to previous value
        
        SW_LR_Days=self.LockdownReleaseDays
        
        SW_LR_end=L_phase_2_end+self.LockdownReleaseDays
        
        Lt_phase_3=np.arange(L_phase_2_end, SW_LR_end,1)
        
        beta_Phase_3=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2, SW_LR_Days)).tolist()
        
        self.finterp_phase_3 = interp1d(Lt_phase_3, beta_Phase_3,fill_value='extrapolate') 
        
        ret2_3 = odeint(self.deriv, y2_2, Lt_phase_3, args=(None,self.N,self.eta, self.gamma, 
                                                        self.p_sym, self.mu, self.r, self.Wa, self.d,2)) 
        
        y2_3=np.array(ret2_3[-1,:]) 
        
        ret2_temp = np.concatenate((ret2,ret2_1[1:],ret2_2[1:],ret2_3[1:]), axis=0)
        
        state_df_2,SWP_value,SWP_index_temp=self.FirstWavEndindex(ret2_temp.T,None)
        
        t2=np.arange(self.FWE_index, SW_LR_end,1)
        
        SWP_index=t2[SWP_index_temp]
                
        PeakRatioTemp=SWP_value/FWP_value
        
        PeakDurationTemp=SWP_index-FWP_index
        
        def get_change(current, expected):
        
            return abs(current - expected) / expected
        
        Output=(get_change(PeakRatioTemp,self.PeakRatio) + get_change(PeakDurationTemp,self.PeakDuration))/2
        
        # print(SWP_value,FWP_value,SWP_index,FWP_index)
        
        #print(PeakRatioTemp,self.PeakRatio,PeakDurationTemp,self.PeakDuration)
        
        # print(Output*100, PeakRatioTemp, PeakDurationTemp)
                       
        return  Output*100
    
    
##############################################################################################################    
    
    
        
    def run_model_1(self):
       
        #==============================No vaccination scenario ============================================
        
        if self.VaccinationDuration==None:
            
            state_df = pd.DataFrame()  
            #----------------------First wave-------------------------------------------------------
            
            Lt1=np.arange(0,self.FWE_index,1)
                    
            ret = odeint(self.deriv, self.y0, Lt1, args=(self.Beta_1,self.N, self.eta, self.gamma, 
                                                        self.p_sym, self.mu, self.r, self.Wa, self.d))  
             
            state_df_1,FWP_value,FWP_index =self.FirstWavEndindex(ret.T,None)
            
            y1=np.array(ret[-1,:])    #initial condition for second wave   
        
        #---------------------------Second wave before lockdown start--------------------------------------
            
            BeforeLockStart=self.FWE_index+self.LockdownStartDays
            
            Lt2=np.arange(self.FWE_index,BeforeLockStart,1)
                            
            ret2 = odeint(self.deriv, y1, Lt2, args=(self.Beta_2,self.N, self.eta, self.gamma, 
                                                            self.p_sym, self.mu, self.r, self.Wa, self.d))  
            
            y2=np.array(ret2[-1,:]) 
            
        #----------------------------Second wave Lockdown first Phase -------------------------------------
            #Lockdown duration days divide into two phase 
            
            L_phase_1_days=self.L_phase_1_days            #int(0.45*self.lockdown_duration)    
            
            L_phase_2_days=self.L_phase_2_days             #int(0.55*self.lockdown_duration)
            
            L_phase_1_end=L_phase_1_days+BeforeLockStart                 #int((0.45*self.lockdown_duration)+BeforeLockStart)    
            
            L_phase_2_end=L_phase_2_days+BeforeLockStart               #int((0.55*self.lockdown_duration)+L_phase_1_end)
            
            Lt_phase_1=np.arange(BeforeLockStart,L_phase_1_end,1)
            
            beta_phase_1=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2,L_phase_1_days)).tolist()
            
            beta_phase_1.reverse()    
            
            self.finterp_phase_1 = interp1d(Lt_phase_1,beta_phase_1,fill_value='extrapolate')  
            
            ret2_1 = odeint(self.deriv, y2, Lt_phase_1, args=(None, self.N, self.eta, self.gamma, 
                                                            self.p_sym, self.mu, self.r, self.Wa, self.d,1))  
            
            y2_1 =np.array(ret2_1[-1,:])            
        
        #--------------------------Second wave Lockdown Second  Phase ---------------------------------- 
            #In second phase of lockdown transmission rate is reduce constant value
            
            Lt_phase_2=np.arange(L_phase_1_end,L_phase_2_end,1)
            
            beta_phase_2=self.Beta_2*self.LockdownEffectiveness
            
            ret2_2 = odeint(self.deriv, y2_1, Lt_phase_2, args=(beta_phase_2,self.N, self.eta, self.gamma, 
                                                            self.p_sym, self.mu, self.r, self.Wa, self.d))        
            
            y2_2=np.array(ret2_2[-1,:])
        
        #----------------------Second wave after Lockdown release ---------------------------
        
            #  After Lockdown release reduce transmission rate increase to previous value
            
            SW_LR_Days=self.LockdownReleaseDays
            
            SW_LR_end=L_phase_2_end+self.LockdownReleaseDays
            
            Lt_phase_3=np.arange(L_phase_2_end, SW_LR_end,1)
            
            beta_Phase_3=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2, SW_LR_Days)).tolist()
            
            self.finterp_phase_3 = interp1d(Lt_phase_3, beta_Phase_3,fill_value='extrapolate') 
            
            ret2_3 = odeint(self.deriv, y2_2, Lt_phase_3, args=(None,self.N,self.eta, self.gamma, 
                                                            self.p_sym, self.mu, self.r, self.Wa, self.d,2)) 
            
            y2_3=np.array(ret2_3[-1,:]) 
            
            ret2_temp = np.concatenate((ret2,ret2_1[1:],ret2_2[1:],ret2_3[1:]), axis=0)
            
            state_df_2,SWP_value,SWP_index_temp=self.FirstWavEndindex(ret2_temp.T,None)
            
            t2=np.arange(self.FWE_index, SW_LR_end,1)
            
            SWP_index=t2[SWP_index_temp]
                    
            PeakRatioTemp=SWP_value/FWP_value
            
            PeakDurationTemp=SWP_index-FWP_index
            
            
            
            # #------------------Third wave-----------------------------------------
            
            #Third wave with immunity escape effect or R3_percent effect  
                   
            if self.ThirdWaveImmuneEscape!=None or self.R3_percent!=None:
                
                Duration_SWP_TWEm=(self.ThirdWaveEmergenceDate-self.SecondPeakDate).days
                
                TWEm_Start_index=SWP_index+Duration_SWP_TWEm
                
                t3_1=np.arange(SW_LR_end,TWEm_Start_index,1)
                
                ret3_1 = odeint(self.deriv, y2_3, t3_1, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d)) 
                
                y3_1=np.array(ret3_1[-1,:]) 
                
                if self.ThirdWaveImmuneEscape!=None:
                
                    state_arr_3_1 = np.reshape(y3_1, (-1,8))           
                
                    for i in [0,1,2]:
                            state_arr_3_1[i][0]=state_arr_3_1[i][0]+((state_arr_3_1[i][5])+(state_arr_3_1[i][6]))*self.ThirdWaveImmuneEscape  #U
                            state_arr_3_1[i][5]=(state_arr_3_1[i][5])*(1-self.ThirdWaveImmuneEscape)                #R1
                            state_arr_3_1[i][6]=(state_arr_3_1[i][6])*(1-self.ThirdWaveImmuneEscape)                #R2
                            
                    y3_2 = np.array((np.reshape(state_arr_3_1, (-1,24)))[0]) 
                    
                else:
                    
                    y3_2=np.array(ret3_1[-1,:])
                 
                TWE_index_test= TWEm_Start_index + 1000
                
                t3_2=np.arange(TWEm_Start_index,TWE_index_test,1)
                
                ret3_2 = odeint(self.deriv, y3_2, t3_2, args=(self.Beta_4,self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d)) 
                
                ret3 = np.concatenate((ret3_1,ret3_2[1:]), axis=0)
                
            #Third wave without immune escape effect
            else:
                
                TWE_index_test= SW_LR_end + 1000
                
                t33=np.arange(SW_LR_end,TWE_index_test,1)
                
                ret3 = odeint(self.deriv, y2_3, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                               self.p_sym, self.mu, self.r, self.Wa, self.d)) 
                
                
            
            # getting duration of third wave
            
            duration_TW=self.ThirdWaveEndlimit(ret3.T,None,self.Wa)
            
            if duration_TW<5:
                
                #TW_msg='Third wave is not predict'
                
                TWE_index_final=SW_LR_end+200
                
                ret33=ret3[0:200,:]
                
                result = np.concatenate((ret,ret2[1:], ret2_1[1:], ret2_2[1:], ret2_3[1:],ret33[1:]), axis=0)
                
                all_end_index=[0,self.FWE_index,SW_LR_end,SW_LR_end]
                
                #print(TW_msg)
                
            else:
            
                ret33=ret3[0:int(duration_TW),:]
            
                result = np.concatenate((ret,ret2[1:], ret2_1[1:], ret2_2[1:], ret2_3[1:],ret33[1:]), axis=0)
                
                TWE_index_final=SW_LR_end + duration_TW
                
                all_end_index=[0,self.FWE_index,SW_LR_end,TWE_index_final]
            
            state_arr = result.T
                
            for i in range(0, state_arr.shape[0], 8):                
                            
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                                'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7]} 
                
                state_df = state_df.append(state_dict,ignore_index=True)
            
  #======================================================================================================          
            
        if self.VaccinationDuration!=None:
            
            self.VaccinationRate= -(1/(self.VaccinationDuration))*math.log(1-self.VaccinationCoverage)
            
            #print(self.VaccinationRate)
            
            state_df = pd.DataFrame() 
            
            state_df_v =  pd.DataFrame() 
            
            state_df_nv =  pd.DataFrame() 
            
            Vacccount=0
            
            for vaccRate in [self.VaccinationRate,0]:
                
                Vacccount+=1
                #self.lockdown_duration=(self.LockdownEndDate-self.LockdownStartDate).days
                
                #print(Vacccount)
                
                #----------------------First wave-------------------------------------------------------
                
                Lt1=np.arange(0,self.FWE_index,1)
                        
                ret = odeint(self.deriv_vacc, self.y0_v, Lt1, args=(self.Beta_1,self.N, self.eta, self.gamma, 
                                                            self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0))  
                
                state_df_1,FWP_value,FWP_index =self.FirstWavEndindex(ret.T,1)
                
                y1=np.array(ret[-1,:]) #initial condition for second wave   
                
                #---------------------------Second wave before lockdown start--------------------------------------
             
                # second wave- getting peak, slice range based on days after firstpeak
                
                BeforeLockStart=self.FWE_index+self.LockdownStartDays
            
                Lt2=np.arange(self.FWE_index,BeforeLockStart,1)
                                
                ret2 = odeint(self.deriv_vacc, y1, Lt2, args=(self.Beta_2,self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0))  
                
                y2=np.array(ret2[-1,:]) 
                
                #----------------------------Second wave Lockdown first Phase -------------------------------------
                
                #Lockdown duration days divide into two phase            
                
                L_phase_1_days=self.L_phase_1_days            #int(0.45*self.lockdown_duration)    
            
                L_phase_2_days=self.L_phase_2_days
                
                L_phase_1_end=L_phase_1_days+BeforeLockStart                 #int((0.45*self.lockdown_duration)+BeforeLockStart)    
                
                L_phase_2_end=L_phase_2_days+BeforeLockStart 
                
                Lt_phase_1=np.arange(BeforeLockStart,L_phase_1_end,1)
                
                beta_phase_1=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2,L_phase_1_days)).tolist()
                
                beta_phase_1.reverse()    
                
                self.finterp_phase_1 = interp1d(Lt_phase_1,beta_phase_1,fill_value='extrapolate')  
                
                ret2_1 = odeint(self.deriv_vacc, y2, Lt_phase_1, args=(None, self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0,1))  
                
                y2_1 =np.array(ret2_1[-1,:])            
                
                #--------------------------Second wave Lockdown Second  Phase ---------------------------------- 
                
                Lt_phase_2=np.arange(L_phase_1_end,L_phase_2_end,1)
                
                beta_phase_2=self.Beta_2*self.LockdownEffectiveness
                
                ret2_2 = odeint(self.deriv_vacc, y2_1, Lt_phase_2, args=(beta_phase_2,self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0))        
                
                y2_2=np.array(ret2_2[-1,:])
                
                #----------------------Second wave after Lockdown release ---------------------------
                
                SW_LR_Days=self.LockdownReleaseDays
        
                SW_LR_end=L_phase_2_end+self.LockdownReleaseDays
                
                Lt_phase_3=np.arange(L_phase_2_end, SW_LR_end,1)
                
                beta_Phase_3=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2, SW_LR_Days)).tolist()
                
                self.finterp_phase_3 = interp1d(Lt_phase_3, beta_Phase_3,fill_value='extrapolate') 
                
                ret2_3 = odeint(self.deriv_vacc, y2_2, Lt_phase_3, args=(None,self.N,self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d,vaccRate,self.C1_v,self.C2_v,2)) 
                
                y2_3=np.array(ret2_3[-1,:])
                
                ret2_temp = np.concatenate((ret2,ret2_1[1:],ret2_2[1:],ret2_3[1:]), axis=0)
        
                state_df_2,SWP_value,SWP_index_temp=self.FirstWavEndindex(ret2_temp.T,1)
                
                t2=np.arange(self.FWE_index, SW_LR_end,1)
                
                SWP_index=t2[SWP_index_temp]
                
                #----------------------Third wave-------------------------------------------
                
                # Third wave with immunity escape effect
                
                if self.ThirdWaveImmuneEscape!=None or self.R3_percent!=None:
                
                    Duration_SWP_TWEm=(self.ThirdWaveEmergenceDate-self.SecondPeakDate).days
                    
                    TWEm_Start_index=SWP_index+Duration_SWP_TWEm
                    
                    t3_1=np.arange(SW_LR_end,TWEm_Start_index,1)
                    
                    ret3_1 = odeint(self.deriv_vacc, y2_3, t3_1, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                    self.p_sym, self.mu, self.r, self.Wa, self.d,vaccRate,self.C1_v,self.C2_v)) 
                    
                    y3_1=np.array(ret3_1[-1,:]) 
                    
                    if self.ThirdWaveImmuneEscape!=None:
                    
                        state_arr_3_1 = np.reshape(y3_1, (-1,17))           
                    
                        for i in [0,1,2]:
                                state_arr_3_1[i][0]=state_arr_3_1[i][0]+((state_arr_3_1[i][5])+(state_arr_3_1[i][6]))*self.ThirdWaveImmuneEscape  #U
                                state_arr_3_1[i][5]=(state_arr_3_1[i][5])*(1-self.ThirdWaveImmuneEscape)                #R1
                                state_arr_3_1[i][6]=(state_arr_3_1[i][6])*(1-self.ThirdWaveImmuneEscape)                #R2
                                
                        y3_2 = np.array((np.reshape(state_arr_3_1, (-1,51)))[0]) 
                        
                    else:
                        
                        y3_2=np.array(ret3_1[-1,:])
                     
                    TWE_index_test= TWEm_Start_index + 1000
                    
                    t3_2=np.arange(TWEm_Start_index,TWE_index_test,1)
                    
                    ret3_2 = odeint(self.deriv_vacc, y3_2, t3_2, args=(self.Beta_4,self.N, self.eta, self.gamma, 
                                                                    self.p_sym, self.mu, self.r, self.Wa, self.d,vaccRate,self.C1_v,self.C2_v)) 
                    
                    ret3 = np.concatenate((ret3_1,ret3_2[1:]), axis=0)
                    
                #Third wave without immune escape effect
                else:
                    
                    TWE_index_test= SW_LR_end + 1000
                    
                    t33=np.arange(SW_LR_end,TWE_index_test,1)
                    
                    ret3 = odeint(self.deriv_vacc, y2_3, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                   self.p_sym, self.mu, self.r, self.Wa, self.d,vaccRate,self.C1_v,self.C2_v)) 
                    
                
            
                # getting duration of third wave
                    
                duration_TW=self.ThirdWaveEndlimit(ret3.T,1,self.Wa,1)
                
                if duration_TW==0:
                    
                    #TW_msg='Third wave is not predict'
                    
                    TWE_index_final=SW_LR_end+200
                    
                    ret33=ret3[0:200,:]
                    
                    result = np.concatenate((ret,ret2[1:], ret2_1[1:], ret2_2[1:], ret2_3[1:],ret33[1:]), axis=0)
                    
                    all_end_index=[0,self.FWE_index,SW_LR_end,SW_LR_end]
                    
                else:
                
                    ret33=ret3[0:int(duration_TW),:]
                
                    result = np.concatenate((ret,ret2[1:], ret2_1[1:], ret2_2[1:], ret2_3[1:],ret33[1:]), axis=0)
                    
                    TWE_index_final=SW_LR_end + duration_TW
                    
                    all_end_index=[0,self.FWE_index,SW_LR_end,TWE_index_final]
                    
                    
                
                
            #-------------------------------Combine all 3 wave derivative---------------------------
                
                state_arr = result.T
                 
                if Vacccount==1:
                    
                    for i in range(0, state_arr.shape[0], 17):
                                    
                        state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                                      'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7],
                                      'Uv':state_arr[i+8],'Ev':state_arr[i+9],'Av':state_arr[i+10],'Pv':state_arr[i+11],
                                      'Sv':state_arr[i+12],'R1v':state_arr[i+13],'R2v':state_arr[i+14], 'Cv':state_arr[i+15],
                                      'Ct':state_arr[i+16]} 
                        
                        state_df_v = state_df_v.append(state_dict,ignore_index=True)
                        
                        
                elif Vacccount==2:
                    
                    for i in range(0, state_arr.shape[0], 17):
                        
                        state_dict_temp={'Ct0':state_arr[i+16]}
                                                
                        state_df_nv = state_df_nv.append(state_dict_temp,ignore_index=True)
                        
                    state_df= pd.concat([state_df_v,state_df_nv],axis=1)
                
                
        state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
        
        t=np.arange(0,TWE_index_test,1) #time scle of 3 wave
        
        state_df['t'] = [t,t,t,t]           
            
        all_end_index_int = [int(item) for item in all_end_index]
            
        return state_df, FWP_index, all_end_index_int 
    
