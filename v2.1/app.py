##### IMPORTS #####

#libraries
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import sqlite3
import plotly
import plotly.express as px
import json
import hashlib


##### DEPENDENCIES #####
from responsejson import createoutputjson


##### PLOT FUNCTION #####

def plot(place, seropeak, FirstPeaktDate,  fCases, SecondPeaktDate, sCases,
                trans, wa, thie, ThirdWaveEmergenceDate , LockdownStartDate, LockdownEndDate, rm, popdens, vaccDays, vaccCover):
    
    #Data to print below the chart
    values={
        "Restriction Start Date":LockdownStartDate, "Restriction End Date":LockdownEndDate,
        "Restrictive Measures":str(rm*100)+"%",
        "Increase in Population":str(popdens*100)+"%", "Vaccine Coverage (Full Dose)":str(vaccCover*100)+"%", "Waning Duration":int(wa/30),
        "Date of Future Variant":ThirdWaveEmergenceDate, "Increase in Transmissibility":str(trans*100)+"%", "Immune Escape":str(thie*100)+"%"
    }
    
    ValuesPlot=[]
    for k,v in values.items():
        if v == 0 or v == "0" or v == "0.0":
            continue
        if v == "0%" or v == "0.0%":
            continue
        elif v == '':
            continue
        else:
           ValuesPlot.append("%s: %s" % (k,v))

    #Calling tehe createoutputjson function
    plotData,R1_cases,R1_index,all_end_index,preparedness, seromsg = createoutputjson(seropeak, FirstPeaktDate,  fCases, SecondPeaktDate, sCases,
                trans, wa, thie, ThirdWaveEmergenceDate , LockdownStartDate, LockdownEndDate, rm, popdens, vaccDays, vaccCover)
    
    if seromsg == "no":
        seroAlert = "hide"
    else:
        seroAlert = ""
        # preparedness=[0,0,0,0,0,0,0,0,0,0,0,0]


    # print(seroAlert)
    
    if seromsg=="no":

        #Plot for Non-Vaccine scenario
        if vaccDays == 0.0:
            c_diff, date = plotData[0]['no_intervention_c_diff'], plotData[0]['date']
            
            #DF for the plot
            df = pd.DataFrame({
            "Time (Days)": date[:len(c_diff)],
            "Daily symptomatic cases (numbers/million)": [int(item) for item in c_diff]
                })
    
            #Ploting the data
            fig = px.line(df, x="Time (Days)", y="Daily symptomatic cases (numbers/million)", height=500)
            fig.update_yaxes(tickfont_family="Roboto Medium")
    
            #Limit X-axis scale quarterly
            fig.update_xaxes(
                dtick="M3", tickfont_family="Roboto Medium", tickfont_size=13, tickangle=-45)
        
        #Plot for Vaccine scenario
        else:
            ct_diff, ct0_diff, date = plotData[0]['no_intervention_ct_diff'], plotData[0]['no_intervention_ct0_diff'], plotData[0]['date']
            lim = min([len(ct_diff), len(ct0_diff), len(date)])
    
            df = pd.DataFrame({
            "Time (Days)": date[:lim],
            "Daily symptomatic With Vaccine cases (numbers/million)": [int(item) for item in ct_diff[:lim]],
            "Daily symptomatic Vaccine cases (numbers/million)": [int(item) for item in ct0_diff[:lim]]
                })
    
            fig = px.line(df, x="Time (Days)", y="Daily symptomatic Vaccine cases (numbers/million)", height=500)
            fig.add_scatter(x=df['Time (Days)'], y=df['Daily symptomatic With Vaccine cases (numbers/million)'], mode='lines', line_color="#ef553b", name="Vaccine")
            fig.add_scatter(x=df['Time (Days)'], y=df['Daily symptomatic Vaccine cases (numbers/million)'], mode='lines', line_color="#636efa", name="No Vaccine")
            fig.update_yaxes(tickfont_family="Roboto Medium")
            fig.update_xaxes(
                dtick="M3",
                tickfont_family="Roboto Medium", tickfont_size=13, tickangle=-45)
    
        #Appending Location Name 
        fig.update_layout(title_text= f"Location: {place}",
            title_xref="container")
    
        #Appending Values to the plot
        fig.update_xaxes(title_text=f"""
            {', '.join(ValuesPlot[:2])}
            <br>
            {', '.join(ValuesPlot[2:4])}
            <br>
            {', '.join(ValuesPlot[4:6])}
            <br>
            {', '.join(ValuesPlot[6:8])}
            <br>
            {', '.join(ValuesPlot[8:])}
            """)
    
        #Determine shaded area for the plot for wave 1, 2 & 3
        fig.add_vrect(x0=date[all_end_index[0]], x1=date[all_end_index[1]], annotation_text="First Wave", annotation_position="top left",
                        annotation=dict(font_size=14), fillcolor="yellow", opacity=0.10, line_width=0)
    
        if all_end_index[2] == all_end_index[3]:
            fig.add_vrect(x0=date[all_end_index[1]], x1=date[-1], annotation_text="Second Wave", annotation_position="top left",
                        annotation=dict(font_size=14), fillcolor="green", opacity=0.10, line_width=0)
    
            #Third wave prediction status
            wavestatus = 0
        else:
            fig.add_vrect(x0=date[all_end_index[1]], x1=date[all_end_index[2]], annotation_text="Second Wave", annotation_position="top left",
                        annotation=dict(font_size=14), fillcolor="green", opacity=0.10, line_width=0)
            fig.add_vrect(x0=date[all_end_index[2]], x1=date[-1], annotation_text="Third Wave", annotation_position="top right",
                        annotation=dict(font_size=14), fillcolor="red", opacity=0.10, line_width=0)
            wavestatus = 1
    
        #Creating JSON of the plot
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        preparedness = [round(item, 3) for item in preparedness]
        return graphJSON, wavestatus, preparedness, seroAlert
    
    else:
        
        return None,"",preparedness,seroAlert



#Defining defaults for the plot
class defaultPlot():
    place = "India"
    seropeak = 8.1
    FirstPeaktDate = "2020-09-17"
    fCases = 93180
    SecondPeaktDate = "2021-05-06"
    sCases = 391232
    checktrans = ""
    trans = 0
    # check = ""
    wa = 0
    thie = 0
    ThirdWaveEmergenceDate = ""
    checkpop =""
    popdens = 0.0
    LockdownStartDate = ""
    LockdownEndDate = ""
    rm = 0
    vaccDays = 0
    vaccCover = 0

    #Calling the plot function
    graphJSON, wavestatus, preparedness, seroAlert= plot(place, seropeak, FirstPeaktDate,  fCases, SecondPeaktDate, sCases,
            trans, wa, thie, ThirdWaveEmergenceDate , LockdownStartDate, LockdownEndDate, rm, popdens, vaccDays, vaccCover)

#Storing the default values in a generator to reuse    
default = defaultPlot()

##### FLASK APP STARTS HERE #####
app = Flask(__name__)

##### ROUTES #####

### SIGNIN/INDEX ###
@app.route("/", methods=['POST', 'GET'])
@app.route("/index/", methods=['POST', 'GET'])
def signin():
    if request.method == "POST":
        username = str(request.form['username'])
        password = request.form['password']
        #Hashing the passowrd with md5
        password= hashlib.md5(password.encode()).hexdigest()

        #Making a connection to the database
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        #Check if user exists
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        data = cur.fetchone()
        if data is None:
            return render_template("index.html", error="Incorrect Username or Password")
        else:
            return redirect(url_for('about'))

    else:
        return render_template("index.html")

### REGISTER ###
@app.route("/register/", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        orgname = request.form['orgname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password= hashlib.md5(password.encode()).hexdigest()

        #making DB of new users
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        #creating table if not exists
        cur.executescript('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                orgname TEXT,
                email TEXT UNIQUE,
                username TEXT UNIQUE,
                password TEXT
            )

        ''')

        #Inserting data
        cur.execute('''
        INSERT INTO users(name, orgname, email, username, password) VALUES(?,?,?,?,?)''',
        (name, orgname, email, username, password))

        #Commit changes and close the connection
        conn.commit()
        cur.close()

        return redirect("/")
    else:
        return render_template("register.html")

### ADVANCED DASHBOARD ###
@app.route("/advanced-dashboard/", methods=['POST', 'GET'])
def advanced_dashboard():
    if request.method == "POST":
        place = str(request.form['place'])
        seropeak = 0.0 if request.form['seropeak'] == "" else float(request.form['seropeak'])
        FirstPeaktDate = str(request.form['FirstPeaktDate'])
        fCases = 0.0 if request.form['fCases'] == "" else int(request.form['fCases'])
        SecondPeaktDate = str(request.form['SecondPeaktDate'])
        sCases = 0.0 if request.form['sCases'] == "" else int(request.form['sCases'])

        #Checking if the user has selected the population checkbox
        try:
            checkpop = request.form['checkpop']
            popdens = float(request.form['popdens'])/100
        except:
            checkpop = ""
            popdens = 0.0

        #Checking if the user has selected the advanced checkbox
        try:
            checkadvanced = request.form['checkadvanced']
            try: check = request.form['wanning']
            except: check = ""
            try: wa = float(request.form['wa'])*30 if request.form['wanning'] else 0
            except: wa = 0.0
            try: checktrans = request.form['checktrans']
            except: checktrans = ""
            try: trans = float(request.form['trans'])/100 if request.form['checktrans'] else 0
            except: trans = 0
            try: thie = float(request.form['thie'])/100
            except: thie = 0
            try: ThirdWaveEmergenceDate = str(request.form['ThirdWaveEmergenceDate'])
            except: ThirdWaveEmergenceDate = ""

        except:
            checkadvanced = ""
            check = ""
            wa = 0.0
            checktrans = ""
            trans = 0
            thie = 0
            ThirdWaveEmergenceDate = ""

        LockdownStartDate = str(request.form['LockdownStartDate'])
        LockdownEndDate = str(request.form['LockdownEndDate'])
        rm = 0 if request.form['rm'] == "" else float(request.form['rm'])/100
        vaccDays = 0 if request.form['vaccDays'] == "" else float(request.form['vaccDays'])*30
        vaccCover = 0.0 if request.form['vaccCover'] == "" else float(request.form['vaccCover'])/100

        #Calling the plot function
        graphJSON, wavestatus, preparedness,seroAlert = plot(place, seropeak, FirstPeaktDate,  fCases, SecondPeaktDate, sCases,
                trans, wa, thie, ThirdWaveEmergenceDate , LockdownStartDate, LockdownEndDate, rm, popdens, vaccDays, vaccCover)
        
        #Passing all the values to the html
        return render_template("advanced.html", graphJSON=graphJSON, place=place,
                        seropeak=seropeak, FirstPeaktDate=FirstPeaktDate, fCases=fCases, SecondPeaktDate=SecondPeaktDate, sCases=sCases, check=check, wa=wa/30,
                        LockdownStartDate=LockdownStartDate, LockdownEndDate=LockdownEndDate, rm=rm*100,
                        ThirdWaveEmergenceDate=ThirdWaveEmergenceDate, trans=trans*100, checktrans=checktrans, thie=thie*100,checkpop=checkpop, popdens=popdens*100,
                        vaccDays=vaccDays/30, vaccCover=vaccCover*100, checkadvanced = checkadvanced,
                        preparedness=preparedness, wavestatus=wavestatus, seroAlert=seroAlert)

    else:
        return render_template("advanced.html", graphJSON=default.graphJSON, place=default.place,
                        seropeak=default.seropeak, FirstPeaktDate=default.FirstPeaktDate, fCases=default.fCases, SecondPeaktDate=default.SecondPeaktDate, sCases=default.sCases,  wa=default.wa/30,
                        LockdownStartDate=default.LockdownStartDate, LockdownEndDate=default.LockdownEndDate, rm=default.rm,
                        ThirdWaveEmergenceDate=default.ThirdWaveEmergenceDate, trans=default.trans, checktrans=default.checktrans, thie=default.thie*100, popdens=default.popdens*100,
                        vaccDays=default.vaccDays/30, vaccCover=default.vaccCover*100, seroAlert=default.seroAlert,
                        preparedness=default.preparedness, wavestatus=default.wavestatus)


### ABOUT ###
@app.route("/about/")
def about():
    return render_template("about.html")

##### FLASK APP ENDS HERE #####
if __name__ == "__main__":
    app.run(debug=True, port=5021)