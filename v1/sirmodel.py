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
        preparedness_precent=[0.05,0.05,0.25,0.17,0.40,0.60,0.24,0.12,0.12]
        Cv_effectiveness_percent=(1-0.6)
         
        ##################  Without vaccination- S,R, C_diff component to dictionary ###############################################
        
        if len(intervention_state_df.columns)<=9:        
            scenario_dict['t'] = (intervention_state_df.t[3]).tolist()
            scenario_dict['no_intervention_s'] = ( intervention_state_df.S[3]).tolist()
            scenario_dict['no_intervention_r'] = ( intervention_state_df.R1[3]).tolist()
            #scenario_dict['no_intervention_r']=[x + y for (x, y) in zip(( intervention_state_df.R1[3]).tolist(),( intervention_state_df.R2[3]).tolist())]
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
            start_date_x_axis=FirstPeakDate - datetime.timedelta(days=FWP_index)        
            date_xaxis = []
            
            for i in range(0,(len(intervention_state_df.C[3])-1)):
                date_xaxis.append(str(start_date_x_axis + datetime.timedelta(days=int(i))))
            
            scenario_dict['date'] = date_xaxis
        
        elif len(intervention_state_df.columns)>9:
            start_date_x_axis=FirstPeakDate - datetime.timedelta(days=FWP_index)        
            date_xaxis = []
            
            for i in range(0,(len(intervention_state_df.Ct[3])-1)):
                date_xaxis.append(str(start_date_x_axis + datetime.timedelta(days=int(i))))
            
            scenario_dict['date'] = date_xaxis
        
        ################################## getting recovery component ###################################
        R_index=FWP_index-15    
        R1_cases=scenario_dict['no_intervention_r'][R_index]  
        self.FWP_cases=scenario_dict['no_intervention_r'][FWP_index]  
        
        ################################ Remove data point before 2020-01-01###########################
        
        indexJan=scenario_dict['date'].index("2020-01-01")
        
        scenario_dict_final={}
        
        for sub in scenario_dict:      
            # slicing trim before Jan index and reassigning
            scenario_dict_final[sub] = scenario_dict[sub][indexJan:]
            
        all_end_index_final= [item-indexJan if item>0 else item for item in all_end_index]     
            
        R_index_final=R_index-indexJan
        
        return scenario_dict_final,preparedness_list, R1_cases,all_end_index_final,R_index_final
    
    ##################################################################################################################### 
    
    def prep_output_json(self, scenario_dict):
        
        garph_df = pd.DataFrame()       
        garph_df = garph_df.append(scenario_dict, ignore_index=True) 
                
        return garph_df.to_json(orient='records')
    
    
    def run_scenario(self,user_input_dict):
        
        TotalPopulation = 1000000
        R1 = 1.0729 if user_input_dict['R1'] == 0.0 else user_input_dict['R1']
        R2 = 1.782 if user_input_dict['R2'] == 0.0 else user_input_dict['R2']
        R3 = R2 if user_input_dict['R3'] == 0.0 else user_input_dict['R3']
        AverageDurationOfWanning = 0 if user_input_dict['AverageDurationOfWanning'] == 0.0 else 1/user_input_dict['AverageDurationOfWanning'] 
        ThirdWaveImmuneEscape = None if user_input_dict['ThirdWaveImmuneEscape'] == 0.0 else user_input_dict['ThirdWaveImmuneEscape'] 
        LockdownEffectiveness = 0.5 if user_input_dict['LockdownEffectiveness'] == 0.0 else 1-user_input_dict['LockdownEffectiveness'] 
        FirstPeakDate = datetime.datetime.strptime('2020-9-16', '%Y-%m-%d').date() if user_input_dict['FirstPeakDate'] == '' else datetime.datetime.strptime(user_input_dict['FirstPeakDate'], '%Y-%m-%d').date()
        ThirdWaveEmergenceDate =datetime.datetime.strptime('2021-10-1', '%Y-%m-%d').date() if user_input_dict['ThirdWaveEmergenceDate'] == '' else datetime.datetime.strptime(user_input_dict['ThirdWaveEmergenceDate'], '%Y-%m-%d').date()
        LockdownStartDate = None if user_input_dict['LockdownStartDate'] == '' else datetime.datetime.strptime(user_input_dict['LockdownStartDate'], '%Y-%m-%d').date()
        LockdownEndDate =None if user_input_dict['LockdownEndDate'] == '' else datetime.datetime.strptime(user_input_dict['LockdownEndDate'], '%Y-%m-%d').date()
        PopulationDensity = None if user_input_dict['PopulationDensity'] == 0.0 else user_input_dict['PopulationDensity'] 
        VaccinationDuration= None if user_input_dict['VaccinationDuration'] == 0.0 else user_input_dict['VaccinationDuration']
        VaccinationCoverage= 0 if user_input_dict['VaccinationCoverage'] == 0.0 else user_input_dict['VaccinationCoverage']
        
        
       ################## Passing parameter to Sirmodel #########################################################################################
        
        intervention_graph = SirModel(N = [TotalPopulation*0.46,TotalPopulation*0.445,TotalPopulation*0.095],
                                        R1=R1, R2=R2, R3=R3,
                                        AverageDurationOfWanning=AverageDurationOfWanning,
                                        ThirdWaveImmuneEscape=ThirdWaveImmuneEscape,
                                        LockdownEffectiveness=LockdownEffectiveness,                                        
                                        FirstPeakDate=FirstPeakDate,
                                        ThirdWaveEmergenceDate=ThirdWaveEmergenceDate,
                                        LockdownStartDate=LockdownStartDate,
                                        LockdownEndDate=LockdownEndDate,
                                        PopulationDensity=PopulationDensity,
                                        VaccinationDuration=VaccinationDuration,
                                        VaccinationCoverage=VaccinationCoverage)
        
        #Running SIR model
        
        intervention_state_df, FWP_index, all_end_index  = intervention_graph.run_model()
               
       ###############Prepareoutput dictionary #####################################################################################################
                    
       
        scenario_dict_final,self.preparedness_list, self.R1_cases,self.all_end_index_final,self.R_index_final = self.prep_scenario_dict(intervention_state_df,FirstPeakDate,FWP_index, all_end_index )  
        print("sir",self.all_end_index_final)
        return self.prep_output_json(scenario_dict_final)
    
    
        
    
class SirModel:
      
    ########################################Intitial Conditions########################################
    eta =0.25    # rate of developing infectiousness
    gamma = 0.2  # Recovery rate 
    r = 1.0      # Rate of developing symptoms
    k = 5/6      # Relative infectiousness of asymptomatic vs symptomatic infection
    p_sym =0.5   # Proportion developing symptoms    
    d=1/240      # Delay rate from R1 to R2    
    mu = np.array([0.0002, 0.002, 0.024])  #Mortality rate for severe cases 
    age_matrix = np.array([[1.37, 1.43, 0.05], [2.52,2.90,0.10], [0.28,0.34,0.02]]) #Connectivity matrix between age group i with age group j
    
    # mu = np.array([0.0002, 0.0024, 0.0201])
    # age_matrix = np.array([[1.371, 1.4317, 0.05], [2.5175,2.9007,0.0993], [0.2789,0.335,0.016]])
    
    columns = age_matrix.shape[1]
    rows = age_matrix.shape[0]
    
    
    def __init__( self, N, R1, R2, R3, AverageDurationOfWanning,
                 ThirdWaveImmuneEscape,LockdownEffectiveness,
                 ThirdWaveEmergenceDate,FirstPeakDate,LockdownStartDate,LockdownEndDate,
                 PopulationDensity,VaccinationDuration,VaccinationCoverage):
       
        
        self.N = np.array([0,0,0]) if N is None else N               # Population
        
        U1,E1,A1,P1,S1,R11,R21,C1 = N[0], 0, 0, 0, 0, 0, 0 ,0        # initial conditions vector age group 2
        U2,E2,A2,P2,S2,R12,R22,C2 = N[1]-20, 0, 0, 0, 20 , 0, 0, 20  # Initial conditions vector age group 2
        U3,E3,A3,P3,S3,R13,R23,C3 = N[2], 0, 0, 0, 0, 0, 0 , 0       # Initial conditions vector age group 3
        
        self.y0 = np.array([U1,E1,A1,P1,S1,R11,R21,C1,U2,E2,A2,P2,S2,R12,R22,C2,U3,E3,A3,P3,S3,R13,R23,C3])
        
        self.Wa=AverageDurationOfWanning
        self.ThirdWaveImmuneEscape=ThirdWaveImmuneEscape        
        self.ThirdWaveEmergenceDate=ThirdWaveEmergenceDate
        
        #=============================Lockdown inputs==============================================================
        self.LockdownStartDays=50
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
        
        def calc_beta():
            
            size = 12
            F = np.zeros(shape=(size,size))
            V = np.zeros((size,size))
            
            for i in range(0,3):
                for j in range(3,size):
                    if j <= 8:
                        F[i][j] = self.age_matrix[i][j%3] * self.k * self.N[i] / self.N[j%3]
                    elif j > 8:
                        F[i][j] = self.age_matrix[i][j%3] * self.N[i] / self.N[j%3]
                    
            for i in range(0,3):
                V[i][i] = 1.0/self.eta
                V[i+3][i] = (1.0 - self.p_sym) / self.gamma
                V[i+3][i+3] = 1.0/self.gamma
                V[i+6][i+6] = 1.0/self.r
                #V[i+9][i+9] = 1.0/self.gamma
                V[i+9][i] = self.p_sym/(self.gamma+self.mu[i])
                V[i+9][i+9] = 1.0/(self.gamma+self.mu[i])
                V[i+9][i+6] = 1.0/(self.gamma+self.mu[i])
               
            M = max(np.linalg.eigvals(np.dot(F,V)))
            
            return M     
        
        #==========================calculate Reproduction rate and Transmission rate =========================================
        
        self.M =21.2378     # calc_beta()      # max eigen value
        self.R1=R1                # wave 1 Reproduction rate
        self.R2=R2                # wave 2 Reproduction rate
                
        if PopulationDensity==None:   #update wave 3 Reproduction rate w.r.t added population density
            self.R3=R3
        else:
            theta=0.16 * math.log(1 + PopulationDensity)   
            self.R3=R3+theta

        self.Beta_1=self.R1/self.M  # wave 1 Transmission rate
        self.Beta_2=self.R2/self.M  # wave 2 Transmission rate 
        self.Beta_3=self.R3/self.M  # wave 3 Transmission rate
        
        #============================Grid first wave and duration FWP and TWS==================================================
        
        self.end_first_wave=2000          # Time Instant for first wave
        self.t1=np.arange(0,self.end_first_wave,1) # Grid of time points used for first Wave 
        self.Duration_FWP_TWS=(ThirdWaveEmergenceDate-FirstPeakDate).days
        
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
                    self.age_matrix[i][j]* ((state_arr[j][4]) + self.k * (state_arr[j][2] + state_arr[j][3]))
                )/N[j] for j in range(self.columns)
                                       )
            
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
                    (self.age_matrix[i][j]* ((state_arr[j][4]) + self.k * (state_arr[j][2] + state_arr[j][3])))+
                    ((1-C1_v)* self.age_matrix[i][j]* ((state_arr[j][12]) + self.k * (state_arr[j][10] + state_arr[j][11])))
                )/N[j] for j in range(self.columns)
                                       )
           
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
       
    def FirstWavEndindex (self,state_arr, cutoff_percent=None,vaccflag=None):
            
        state_df = pd.DataFrame() 
        
        if vaccflag==None:
        
            for i in range(0, state_arr.shape[0], 8):                                
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7]}                     
                state_df = state_df.append(state_dict,ignore_index=True)
                
        elif vaccflag==1:
            
            for i in range(0, state_arr.shape[0], 17):                                
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7],
                              'Uv':state_arr[i+8],'Ev':state_arr[i+9],'Av':state_arr[i+10],'Pv':state_arr[i+11],
                              'Sv':state_arr[i+12],'R1v':state_arr[i+13],'R2v':state_arr[i+14], 'Cv':state_arr[i+15],
                              'Ct':state_arr[i+16]}                     
                state_df = state_df.append(state_dict,ignore_index=True)
            
        
        state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
       
        state_list=state_df.C[3]
        
        state_list_Cdiff=[state_list[i + 1] - state_list[i] for i in range(len(state_list)-1)] #calculate Cdiff
        
        state_Cdiff_max_index= state_list_Cdiff.index(max(state_list_Cdiff)) 
        
        # print(max(state_list_Cdiff))
        # Getting end index first wave w.r.t Wa
        
        try:
            
            limit_value=max(state_list_Cdiff)*cutoff_percent
        
            first_limit_value = list(filter(lambda i: i < limit_value, state_list_Cdiff[state_Cdiff_max_index:]))[0]
            
        except:
            
            limit_value=max(state_list_Cdiff)*(cutoff_percent+0.20)
            
            first_limit_value = list(filter(lambda i: i < limit_value, state_list_Cdiff[state_Cdiff_max_index:]))[0]
        
        first_limit_value_index=state_list_Cdiff[state_Cdiff_max_index:].index(first_limit_value)
        
        end_index_limit_value=state_Cdiff_max_index + first_limit_value_index
            
        return state_Cdiff_max_index, end_index_limit_value 
    
    #################################Second wave end limit##############################################################
    
    def SecondWaveMinIndex (self,state_arr,vaccflag=None):
    
        state_df = pd.DataFrame()  
        
        if vaccflag==None:
        
            for i in range(0, state_arr.shape[0], 8):
                            
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7]} 
                
                state_df = state_df.append(state_dict,ignore_index=True)
                
        elif vaccflag==1:
            
            for i in range(0, state_arr.shape[0], 17):
                            
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7],
                              'Uv':state_arr[i+8],'Ev':state_arr[i+9],'Av':state_arr[i+10],'Pv':state_arr[i+11],
                              'Sv':state_arr[i+12],'R1v':state_arr[i+13],'R2v':state_arr[i+14], 'Cv':state_arr[i+15],
                              'Ct':state_arr[i+16]} 
                
                state_df = state_df.append(state_dict,ignore_index=True)
        
        state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
    
        state_list=state_df.C[3]
        
        state_list_Cdiff=[state_list[i + 1] - state_list[i] for i in range(len(state_list)-1)] #calculate Cdiff
        
        state_Cdiff_min_index= state_list_Cdiff.index(min(state_list_Cdiff)) 
        
        return state_Cdiff_min_index
    
        
    ############################### Third wave end limit ##############################################################
    
    def ThirdWaveEndlimit (self,state_arr,vaccflag=None, Wa=None, lckdn=None):
        
        state_df = pd.DataFrame()  
        
        if vaccflag==None:
        
            for i in range(0, state_arr.shape[0], 8):
                            
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7]} 
                
                state_df = state_df.append(state_dict,ignore_index=True)
                
                # state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
       
                # state_list=state_df.C[3]
                
                # state_list_Cdiff=[state_list[i + 1] - state_list[i] for i in range(len(state_list)-1)] #calculate Cdiff
                
                # state_Cdiff_max_index= state_list_Cdiff.index(max(state_list_Cdiff)) 
                
        elif vaccflag==1:
            
            for i in range(0, state_arr.shape[0], 17):
                            
                state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                              'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7],
                              'Uv':state_arr[i+8],'Ev':state_arr[i+9],'Av':state_arr[i+10],'Pv':state_arr[i+11],
                              'Sv':state_arr[i+12],'R1v':state_arr[i+13],'R2v':state_arr[i+14], 'Cv':state_arr[i+15],
                              'Ct':state_arr[i+16]} 
                
                state_df = state_df.append(state_dict,ignore_index=True)
        
        state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
       
        state_list=state_df.C[3]
        
        state_list_Cdiff=[state_list[i + 1] - state_list[i] for i in range(len(state_list)-1)] #calculate Cdiff
        
        state_Cdiff_max_index= state_list_Cdiff.index(max(state_list_Cdiff)) 
        
        if vaccflag==None:
            if Wa==0:        
                ThirdDuration=state_Cdiff_max_index*3.5
                
            elif Wa!=0:
                ThirdDuration=state_Cdiff_max_index*8
                
        if vaccflag!=None:
            if lckdn!=None:
                if Wa==0:        
                    ThirdDuration=state_Cdiff_max_index*18
                    
                elif Wa!=0:
                    ThirdDuration=state_Cdiff_max_index*8  
            
            elif lckdn==None:
                if Wa==0:        
                    ThirdDuration=state_Cdiff_max_index*3.5
                    
                elif Wa!=0:
                    ThirdDuration=state_Cdiff_max_index*8
        return ThirdDuration

    ############################## run model function ######################################################
        
    def run_model(self):
       
        #==============================No vaccination scenario ============================================
        
        if self.VaccinationDuration==None:
            
        #========================No intervation(include R0, Wa, Thies effect)=========================
            
            if self.LockdownStartDate==None:
               
                state_df = pd.DataFrame() 
                
                #----------------------First wave-------------------------------------------
                
                #First wave- getting peak, slice range based on days after firstpeak
                
                ret = odeint(self.deriv, self.y0, self.t1, args=(self.Beta_1,self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d))
                       
                #Based on Wa getting  First wave end (FWE) index
                
                if self.Wa==0:
                    
                    if self.R1>=1.15:
                    
                        FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.28) 
                    
                    elif self.R1<1.15:
                    
                        FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.75)
                        
                        
                
                elif 1/(30*self.Wa)>0:  
                
                    if 1/(30*self.Wa)>12:  
                    
                        FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.42) 
                    
                    elif 1/(30*self.Wa)<12: 
                    
                        FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.65) 
                
                ret1=ret[0:FWE_index+2,:]  #slice upto first wave end index
                
                y1=np.array(ret1[-1,:]) #initial condition for second wave
                
                #---------------------Second wave-------------------------------------------
                
                # second wave- getting peak, slice range based on days after firstpeak
                
                Duration_SW=self.Duration_FWP_TWS-(FWE_index-FWP_index)  #duration of second wave
                
                # if Duration_SW<0:
                #     FWE_index=FWE_index+(Duration_SW)+Duration_SW
                   
                SWE_index=FWE_index + Duration_SW
                
                t22=np.arange(FWE_index, SWE_index,1)                    # t instant for second wave  
                            
                ret2 = odeint(self.deriv, y1, t22, args=(self.Beta_2,self.N, self.eta, self.gamma, 
                                                               self.p_sym, self.mu, self.r, self.Wa, self.d)) 
                            
                y2=np.array(ret2[-1,:])
                
                #----------------------Third wave -------------------------------------------
                
                #Third wave with immunity escape effect   
                        
                if self.ThirdWaveImmuneEscape!=None:
                    
                    state_arr_2 = np.reshape(y2, (-1,8))           
                
                    for i in [0,1,2]:
                        state_arr_2[i][0]=state_arr_2[i][0]+((state_arr_2[i][5])+(state_arr_2[i][6]))*self.ThirdWaveImmuneEscape  #U
                        state_arr_2[i][5]=(state_arr_2[i][5])*(1-self.ThirdWaveImmuneEscape)                #R1
                        state_arr_2[i][6]=(state_arr_2[i][6])*(1-self.ThirdWaveImmuneEscape)                #R2
                            
                    y3 = np.array((np.reshape(state_arr_2, (-1,24)))[0])  
                    
                    TWE_index_test= SWE_index + 700 
                    
                    t33=np.arange(SWE_index,TWE_index_test,1)
                    
                    ret3 = odeint(self.deriv, y3, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                    self.p_sym, self.mu, self.r, self.Wa, self.d)) 
                # Third wave without immunity escape effect
                else:
                    
                    TWE_index_test=SWE_index+700 
                
                    t33=np.arange(SWE_index,TWE_index_test,1)
                
                    ret3 = odeint(self.deriv, y2, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                               self.p_sym, self.mu, self.r, self.Wa, self.d)) 
                
                # getting duration of third wave
                
                duration_TW=self.ThirdWaveEndlimit(ret3.T,None,self.Wa)
                
                if duration_TW==0.0:
                    
                    #TW_msg='Third wave is not predict'
                    
                    TWE_index_final=SWE_index+100
                    
                    ret33=ret3[0:100,:]
                    
                    result = np.concatenate((ret1, ret2[1:], ret33[1:]), axis=0)
                    
                    all_end_index=[0,FWE_index,SWE_index,SWE_index]
                    
                    #print(TW_msg)
                    
                else:
                
                    ret33=ret3[0:int(duration_TW),:]
                
                    result = np.concatenate((ret1, ret2[1:], ret33[1:]), axis=0)
                    
                    TWE_index_final=SWE_index + duration_TW 
                    
                    SW_minIndex=self.SecondWaveMinIndex(result[int(SWE_index-(Duration_SW/2)):SWE_index].T)
                    
                    SW_minIndex=int(SWE_index-(Duration_SW/2))+ SW_minIndex
                    
                    # SW_minIndex=int(SWE_index-100)+ SW_minIndex
                    
                    if SW_minIndex<SWE_index:                    
                        all_end_index=[0,FWE_index,SW_minIndex,TWE_index_final]                    
                    else:
                        all_end_index=[0,FWE_index,SWE_index,TWE_index_final]
                    
                #----------------------Combining all 3 wave derivative result-------------------------------------------    
                
                state_arr = result.T
         
                for i in range(0, state_arr.shape[0], 8):
                                
                    state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                                  'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7]} 
                    
                    state_df = state_df.append(state_dict,ignore_index=True)
                
                state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
                
                t=np.arange(0,TWE_index_final,1) #time scle of 3 wave
                
                state_df['t'] = [t,t,t,t]  
                
            #===============================Lockdown scenario (include R0, wa, Thies effect) ==========================================    
                    
            if  self.LockdownStartDate!=None:
        
                state_df = pd.DataFrame()  
                
                self.lockdown_duration=(self.LockdownEndDate-self.LockdownStartDate).days
                
                #----------------------First wave-------------------------------------------------------
                
                Lt1=np.arange(0,self.end_first_wave,1)
                        
                ret = odeint(self.deriv, self.y0, Lt1, args=(self.Beta_1,self.N, self.eta, self.gamma, 
                                                            self.p_sym, self.mu, self.r, self.Wa, self.d))  
                
                if self.Wa==0:
                    
                    if self.R1>=1.15:
                    
                        FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.28) 
                    
                    elif self.R1<1.15:
                    
                        FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.75) 
                
                elif 1/(30*self.Wa)>0:  
                
                    if 1/(30*self.Wa)>12:  
                    
                        FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.42) 
                    
                    elif 1/(30*self.Wa)<12: 
                    
                        FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.65) 
                            
                ret1=ret[0:FWE_index+2,:]  #slice upto first wave end index
                
                y1=np.array(ret1[-1,:])    #initial condition for second wave   
            
            #---------------------------Second wave before lockdown start--------------------------------------
                
                Duration_SW=self.Duration_FWP_TWS-(FWE_index-FWP_index)
            
                SWE_index=FWE_index + Duration_SW
            
                Lt2=np.arange(0,self.LockdownStartDays,1)
                                
                ret2 = odeint(self.deriv, y1, Lt2, args=(self.Beta_2,self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d))  
                
                y2=np.array(ret2[-1,:]) 
                
            #----------------------------Second wave Lockdown first Phase -------------------------------------
                #Lockdown duration days divide into two phase 
                
                L_phase_1_days=int(0.45*self.lockdown_duration)    
                
                L_phase_2_days=int(0.55*self.lockdown_duration)
                
                Lt_phase_1=np.arange(0,L_phase_1_days,1)
                
                #In first phase of lockdown transmission rate decreases
                beta_phase_1=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2,L_phase_1_days)).tolist()
                
                beta_phase_1.reverse()    
                
                self.finterp_phase_1 = interp1d(Lt_phase_1,beta_phase_1,fill_value='extrapolate')  
                
                ret2_1 = odeint(self.deriv, y2, Lt_phase_1, args=(None, self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d,1))  
                
                y2_1 =np.array(ret2_1[-1,:])            
            
            #--------------------------Second wave Lockdown Second  Phase ---------------------------------- 
                #In second phase of lockdown transmission rate is reduce constant value
                
                Lt_phase_2=np.arange(0,L_phase_2_days,1)
                
                beta_phase_2=self.Beta_2*self.LockdownEffectiveness
                
                ret2_2 = odeint(self.deriv, y2_1, Lt_phase_2, args=(beta_phase_2,self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d))        
                
                y2_2=np.array(ret2_2[-1,:])
            
            #----------------------Second wave after Lockdown release ---------------------------
            
                #  After Lockdown release reduce transmission rate increase to previous value
                
                SW_LR_Days=Duration_SW-self.lockdown_duration-self.LockdownStartDays
                
                Lt_phase_3=np.arange(0, SW_LR_Days,1)
                
                beta_Phase_3=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2, SW_LR_Days)).tolist()
                
                self.finterp_phase_3 = interp1d(Lt_phase_3, beta_Phase_3,fill_value='extrapolate') 
                
                ret2_3 = odeint(self.deriv, y2_2, Lt_phase_3, args=(None,self.N,self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d,2)) 
                
                y2_3=np.array(ret2_3[-1,:])

            #----------------------Third wave -------------------------------------------
                
                #Third wave with immunity escape effect   
                   
                if self.ThirdWaveImmuneEscape!=None:
                    
                    state_arr_2_3 = np.reshape(y2_3, (-1,8))           
                
                    for i in [0,1,2]:
                            state_arr_2_3[i][0]=state_arr_2_3[i][0]+((state_arr_2_3[i][5])+(state_arr_2_3[i][6]))*self.ThirdWaveImmuneEscape  #U
                            state_arr_2_3[i][5]=(state_arr_2_3[i][5])*(1-self.ThirdWaveImmuneEscape)                #R1
                            state_arr_2_3[i][6]=(state_arr_2_3[i][6])*(1-self.ThirdWaveImmuneEscape)                #R2
                            
                    y2_4 = np.array((np.reshape(state_arr_2_3, (-1,24)))[0])  
                    
                    TWE_index_test= SWE_index + 700
                    
                    t33=np.arange(SWE_index,TWE_index_test,1)
                    
                    ret3 = odeint(self.deriv, y2_4, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                    self.p_sym, self.mu, self.r, self.Wa, self.d)) 
                #Third wave without immune escape effect
                else:
                    
                    TWE_index_test= SWE_index + 700
                    
                    t33=np.arange(SWE_index,TWE_index_test,1)
                    
                    ret3 = odeint(self.deriv, y2_3, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                   self.p_sym, self.mu, self.r, self.Wa, self.d)) 
                
                # getting duration of third wave
                
                duration_TW=self.ThirdWaveEndlimit(ret3.T,None,self.Wa)
                
                if duration_TW==0.0:
                    
                    #TW_msg='Third wave is not predict'
                    
                    TWE_index_final=SWE_index+100
                    
                    ret33=ret3[0:100,:]
                    
                    result = np.concatenate((ret1,ret2[1:], ret2_1[1:], ret2_2[1:], ret2_3[1:],ret33[1:]), axis=0)
                    
                    all_end_index=[0,FWE_index,SWE_index,SWE_index]
                    
                    #print(TW_msg)
                    
                else:
                
                    ret33=ret3[0:int(duration_TW),:]
                
                    result = np.concatenate((ret1,ret2[1:], ret2_1[1:], ret2_2[1:], ret2_3[1:],ret33[1:]), axis=0)
                    
                    TWE_index_final=SWE_index + duration_TW
                    
                    SW_minIndex=self.SecondWaveMinIndex(result[int(SWE_index-(Duration_SW/2)):SWE_index].T)
                    
                    SW_minIndex=int(SWE_index-(Duration_SW/2))+ SW_minIndex
                    
                    # SW_minIndex=int(SWE_index-100)+ SW_minIndex
                    
                    if SW_minIndex<SWE_index:                    
                        all_end_index=[0,FWE_index,SW_minIndex,TWE_index_final]                    
                    else:
                        all_end_index=[0,FWE_index,SWE_index,TWE_index_final]
    
                    
            
             #-------------------------------Combine all 3 wave derivative---------------------------
            
                state_arr = result.T
                
                for i in range(0, state_arr.shape[0], 8):
                    
                                
                    state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                                    'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7]} 
                    
                    state_df = state_df.append(state_dict,ignore_index=True)
                    
                                        
                state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
                
                t=np.arange(0,TWE_index_final,1)
                
                state_df['t'] = [t,t,t,t]
                
            all_end_index_int = [int(item) for item in all_end_index]
        
            return state_df, FWP_index, all_end_index_int 
                
##################################### Vaccination Scenario ##################################################################                
        
        if self.VaccinationDuration!=None:    
            
            self.VaccinationRate= -(1/(self.VaccinationDuration))*math.log(1-self.VaccinationCoverage)
            
            state_df = pd.DataFrame() 
            
            state_df_v =  pd.DataFrame() 
            
            state_df_nv =  pd.DataFrame() 
            
        #========================Vaccination scenario (include R0, wa, Thies effect) =================================
            
            for vaccRate in [self.VaccinationRate,0]:
                
                if self.VaccinationDuration!=None and self.LockdownStartDate==None:                     
                    
                    ret = odeint(self.deriv_vacc, self.y0_v, self.t1, args=(self.Beta_1,self.N, self.eta, self.gamma, 
                                                                        self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0))
                        
                    if self.Wa==0:
                    
                        if self.R1>=1.15:
                        
                            FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.28,1) 
                        
                        elif self.R1<1.15:
                        
                            FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.75,1) 
                
                    elif 1/(30*self.Wa)>0:  
                
                        if 1/(30*self.Wa)>12:  
                        
                            FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.42,1) 
                        
                        elif 1/(30*self.Wa)<12: 
                        
                            FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.65,1)           
                    
                    
                    ret1=ret[0:FWE_index+2,:]  #slice upto first wave end index
                    
                    y1=np.array(ret1[-1,:]) #initial condition for second wave
                    
                #---------------------Second wave-------------------------------------------
                    
                    Duration_SW=self.Duration_FWP_TWS-(FWE_index-FWP_index)
                    
                    SWE_index=FWE_index + Duration_SW
                    
                    t22=np.arange(FWE_index, SWE_index,1) 
                                
                    ret2 = odeint(self.deriv_vacc, y1, t22, args=(self.Beta_2,self.N, self.eta, self.gamma, 
                                                                   self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0)) 
                                
                    y2=np.array(ret2[-1,:])
                    
                            
                #----------------------Third wave ----------------------------------------------------------------------
                    # Third wave with immunity escape effect
                    
                    if self.ThirdWaveImmuneEscape!=None:
                        
                        state_arr_2 = np.reshape(y2, (-1,17))           
                    
                        for i in [0,1,2]:
                                state_arr_2[i][0]=state_arr_2[i][0]+((state_arr_2[i][5])+(state_arr_2[i][6]))*self.ThirdWaveImmuneEscape  #U
                                state_arr_2[i][5]=(state_arr_2[i][5])*(1-self.ThirdWaveImmuneEscape)                #R1
                                state_arr_2[i][6]=(state_arr_2[i][6])*(1-self.ThirdWaveImmuneEscape)                #R2
                                
                        y3 = np.array((np.reshape(state_arr_2, (-1,51)))[0])  
                        
                        TWE_index_test= SWE_index + 700
                        
                        t33=np.arange(SWE_index,TWE_index_test,1)
                        
                        ret3 = odeint(self.deriv_vacc, y3, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                        self.p_sym, self.mu, self.r, self.Wa, self.d,vaccRate,self.C1_v,self.C2_v)) 
                    # Third wave without immune escape effect
                    else:
                        
                        TWE_index_test= SWE_index + 700
                        
                        t33=np.arange(SWE_index,TWE_index_test,1)
                        
                        ret3 = odeint(self.deriv_vacc, y2, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                       self.p_sym, self.mu, self.r, self.Wa, self.d,vaccRate,self.C1_v,self.C2_v)) 
                    # getting duration of third wave
                    
                    duration_TW=self.ThirdWaveEndlimit(ret3.T,1,self.Wa)
                    
                    if duration_TW==0.0:
                        
                        #TW_msg='Third wave is not predict'
                        
                        TWE_index_final=SWE_index+100
                        
                        ret33=ret3[0:100,:]
                        
                        result = np.concatenate((ret1, ret2[1:], ret33[1:]), axis=0)
                        
                        all_end_index=[0,FWE_index,SWE_index,SWE_index]
                        
                        #print(TW_msg)
                        
                    else:
                    
                        ret33=ret3[0:int(duration_TW),:]
                        
                        result = np.concatenate((ret1, ret2[1:], ret33[1:]), axis=0)
                        
                        TWE_index_final=SWE_index + duration_TW 
                        
                        SW_minIndex=self.SecondWaveMinIndex(result[int(SWE_index-(Duration_SW/2)):SWE_index].T,1)
                        
                        SW_minIndex=int(SWE_index-(Duration_SW/2))+ SW_minIndex
                        
                        if SW_minIndex<SWE_index:                    
                            all_end_index=[0,FWE_index,SW_minIndex,TWE_index_final]                    
                        else:
                            all_end_index=[0,FWE_index,SWE_index,TWE_index_final]
                        
                    #----------------------Combining all 3 wave derivative-------------------------------------------    
                    
                    state_arr = result.T
                     
                    if vaccRate!=0:
                        
                        for i in range(0, state_arr.shape[0], 17):
                                        
                            state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                                          'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7],
                                          'Uv':state_arr[i+8],'Ev':state_arr[i+9],'Av':state_arr[i+10],'Pv':state_arr[i+11],
                                          'Sv':state_arr[i+12],'R1v':state_arr[i+13],'R2v':state_arr[i+14], 'Cv':state_arr[i+15],
                                          'Ct':state_arr[i+16]} 
                            
                            state_df_v = state_df_v.append(state_dict,ignore_index=True)
                            
                            
                    elif vaccRate==0:
                        
                        for i in range(0, state_arr.shape[0], 17):
                            
                            state_dict_temp={'Ct0':state_arr[i+16]}
                                                    
                            state_df_nv = state_df_nv.append(state_dict_temp,ignore_index=True)
                            
                        state_df= pd.concat([state_df_v,state_df_nv],axis=1)
                            
                #=============================== Lockdown Scenario and Vaccination Scenario (include R0, wa, Thies effect) ==========================================    
                        
                if  self.LockdownStartDate!=None and self.VaccinationDuration!=None:
                    
                    
                    self.lockdown_duration=(self.LockdownEndDate-self.LockdownStartDate).days
                    
                    #----------------------First wave-------------------------------------------------------
                    
                    Lt1=np.arange(0,self.end_first_wave,1)
                            
                    ret = odeint(self.deriv_vacc, self.y0_v, Lt1, args=(self.Beta_1,self.N, self.eta, self.gamma, 
                                                                self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0))  
                    
                    if self.Wa==0:
                    
                        if self.R1>=1.15:
                        
                            FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.28,1) 
                        
                        elif self.R1<1.15:
                        
                            FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.75,1) 
                
                    elif 1/(30*self.Wa)>0:  
                
                        if 1/(30*self.Wa)>12:  
                        
                            FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.42,1) 
                        
                        elif 1/(30*self.Wa)<12: 
                        
                            FWP_index,FWE_index=self.FirstWavEndindex(ret.T,0.65,1) 
                                
                    ret1=ret[0:FWE_index+2,:]  #slice upto first wave end index
                    
                    y1=np.array(ret1[-1,:]) #initial condition for second wave   
                    
                    #---------------------------Second wave before lockdown start--------------------------------------
                 
                    # second wave- getting peak, slice range based on days after firstpeak
                    
                    Duration_SW=self.Duration_FWP_TWS-(FWE_index-FWP_index)
                
                    SWE_index=FWE_index + Duration_SW
                
                    Lt2=np.arange(0,self.LockdownStartDays,1)
                                    
                    ret2 = odeint(self.deriv_vacc, y1, Lt2, args=(self.Beta_2,self.N, self.eta, self.gamma, 
                                                                    self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0))  
                    
                    y2=np.array(ret2[-1,:]) 
                    
                    #----------------------------Second wave Lockdown first Phase -------------------------------------
                    
                    #Lockdown duration days divide into two phase            
                    
                    L_phase_1_days=int(0.45*self.lockdown_duration)    
                    
                    L_phase_2_days=int(0.55*self.lockdown_duration)
                    
                    Lt_phase_1=np.arange(0,L_phase_1_days,1)
                    
                    #In first phase of lockdown transmission rate decreases
                    
                    beta_phase_1=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2,L_phase_1_days)).tolist()
                    
                    beta_phase_1.reverse()    
                    
                    self.finterp_phase_1 = interp1d(Lt_phase_1,beta_phase_1,fill_value='extrapolate')  
                    
                    ret2_1 = odeint(self.deriv_vacc, y2, Lt_phase_1, args=(None, self.N, self.eta, self.gamma, 
                                                                    self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0,1))  
                    
                    y2_1 =np.array(ret2_1[-1,:])            
                    
                    #--------------------------Second wave Lockdown Second  Phase ---------------------------------- 
                    
                    Lt_phase_2=np.arange(0,L_phase_2_days,1)
                    
                    beta_phase_2=self.Beta_2*self.LockdownEffectiveness
                    
                    ret2_2 = odeint(self.deriv_vacc, y2_1, Lt_phase_2, args=(beta_phase_2,self.N, self.eta, self.gamma, 
                                                                    self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0))        
                    
                    y2_2=np.array(ret2_2[-1,:])
                    
                    #----------------------Second wave after Lockdown release ---------------------------
                    
                    SW_LR_Days=Duration_SW-self.lockdown_duration-self.LockdownStartDays
                    
                    Lt_phase_3=np.arange(0, SW_LR_Days,1)
                    
                    beta_Phase_3=(np.linspace(self.Beta_2*self.LockdownEffectiveness,self.Beta_2, SW_LR_Days)).tolist()
                    
                    self.finterp_phase_3 = interp1d(Lt_phase_3, beta_Phase_3,fill_value='extrapolate') 
                    
                    ret2_3 = odeint(self.deriv_vacc, y2_2, Lt_phase_3, args=(None,self.N,self.eta, self.gamma, 
                                                                    self.p_sym, self.mu, self.r, self.Wa, self.d,0,0,0,2)) 
                    
                    y2_3=np.array(ret2_3[-1,:])
        
                    #----------------------Third wave-------------------------------------------
                    
                    # Third wave with immunity escape effect
                    
                    if self.ThirdWaveImmuneEscape!=None:
                        
                        state_arr_2_3 = np.reshape(y2_3, (-1,17))           
                    
                        for i in [0,1,2]:
                                state_arr_2_3[i][0]=state_arr_2_3[i][0]+((state_arr_2_3[i][5])+(state_arr_2_3[i][6]))*self.ThirdWaveImmuneEscape  #U
                                state_arr_2_3[i][5]=(state_arr_2_3[i][5])*(1-self.ThirdWaveImmuneEscape)                #R1
                                state_arr_2_3[i][6]=(state_arr_2_3[i][6])*(1-self.ThirdWaveImmuneEscape)                #R2
                                
                        y2_4 = np.array((np.reshape(state_arr_2_3, (-1,51)))[0])  
                        
                        TWE_index_test= SWE_index + 700
                        
                        t33=np.arange(SWE_index,TWE_index_test,1)
                        
                        ret3 = odeint(self.deriv_vacc, y2_4, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                        self.p_sym, self.mu, self.r, self.Wa, self.d,vaccRate,self.C1_v,self.C2_v)) 
                    # Third wave without immune escape effect
                    else:
                        
                        TWE_index_test= SWE_index + 700
                        
                        t33=np.arange(SWE_index,TWE_index_test,1)
                        
                        ret3 = odeint(self.deriv_vacc, y2_3, t33, args=(self.Beta_3,self.N, self.eta, self.gamma, 
                                                                       self.p_sym, self.mu, self.r, self.Wa, self.d,vaccRate,self.C1_v,self.C2_v)) 
                    
                    # getting duration of third wave
                    
                    # if vaccRate==0:
                        
                    #     duration_TW=self.ThirdWaveEndlimit(ret3.T,1,self.Wa)
                        
                    # else:
                        
                    #     duration_TW= SWE_index + 700
                        
                    duration_TW=self.ThirdWaveEndlimit(ret3.T,1,self.Wa,1)
                    if duration_TW==0.0:
                        
                        #TW_msg='Third wave is not predict'
                        
                        TWE_index_final=SWE_index+100
                        
                        ret33=ret3[0:100,:]
                        
                        result = np.concatenate((ret1,ret2[1:], ret2_1[1:], ret2_2[1:], ret2_3[1:],ret33[1:]), axis=0)
                        
                        all_end_index=[0,FWE_index,SWE_index,SWE_index]
                        
                        #print(TW_msg)
                        
                    else:
                    
                        ret33=ret3[0:int(duration_TW),:]
                    
                        result = np.concatenate((ret1,ret2[1:], ret2_1[1:], ret2_2[1:], ret2_3[1:],ret33[1:]), axis=0)
                        
                        TWE_index_final=SWE_index + duration_TW
                        
                        SW_minIndex=self.SecondWaveMinIndex(result[int(SWE_index-(Duration_SW/2)):SWE_index].T,1)
                        
                        SW_minIndex=int(SWE_index-(Duration_SW/2))+ SW_minIndex
                        
                        if SW_minIndex<SWE_index:                    
                            all_end_index=[0,FWE_index,SW_minIndex,TWE_index_final]                    
                        else:
                            all_end_index=[0,FWE_index,SWE_index,TWE_index_final]
                    
                #-------------------------------Combine all 3 wave derivative---------------------------
                    
                    state_arr = result.T
                     
                    if vaccRate!=0:
                        
                        for i in range(0, state_arr.shape[0], 17):
                                        
                            state_dict = {'U':state_arr[i],'E':state_arr[i+1],'A':state_arr[i+2],'P':state_arr[i+3],
                                          'S':state_arr[i+4],'R1':state_arr[i+5],'R2':state_arr[i+6], 'C':state_arr[i+7],
                                          'Uv':state_arr[i+8],'Ev':state_arr[i+9],'Av':state_arr[i+10],'Pv':state_arr[i+11],
                                          'Sv':state_arr[i+12],'R1v':state_arr[i+13],'R2v':state_arr[i+14], 'Cv':state_arr[i+15],
                                          'Ct':state_arr[i+16]} 
                            
                            state_df_v = state_df_v.append(state_dict,ignore_index=True)
                            
                            
                    elif vaccRate==0:
                        
                        for i in range(0, state_arr.shape[0], 17):
                            
                            state_dict_temp={'Ct0':state_arr[i+16]}
                                                    
                            state_df_nv = state_df_nv.append(state_dict_temp,ignore_index=True)
                            
                        state_df= pd.concat([state_df_v,state_df_nv],axis=1)
                            #state_df = state_df_v
                    
            state_df.loc[3] = state_df.loc[0] + state_df.loc[1] + state_df.loc[2] 
            
            t=np.arange(0,TWE_index_final,1) #time scle of 3 wave
            
            state_df['t'] = [t,t,t,t]           
                
            all_end_index_int = [int(item) for item in all_end_index]
            
            return state_df, FWP_index, all_end_index_int 
    
