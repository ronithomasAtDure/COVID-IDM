##### IMPORTS #####

#libraries
from flask import Flask, app, render_template, request, send_file, redirect, url_for
import pandas as pd
import sqlite3
import plotly
import plotly.express as px
import json
import hashlib

#dependencies
from responsejson import createoutputjson

#### PLOT FUNCTION ####

def plot(place, r1, r2, r3, wa, thie, FirstPeaktDate,ThirdWaveEmergenceDate, LockdownStartDate, LockdownEndDate, effLck, popdens, vaccDays, vaccCover):

    #to be reflected below plot
    values={
        "R<sub>0</sub>(1)":r1, "R(2)":r2, "R(3)":r3,
        "Waning Duration":int(wa/30), "Immune Escape":str(thie*100)+"%",
        "First Peak Date":FirstPeaktDate, "Future Variant Date":ThirdWaveEmergenceDate,
        "Lockdown Start Date":LockdownStartDate, "Lockdown End Date":LockdownEndDate,
        "Lockdown Effectiveness":str(effLck*100)+"%", "Vaccine Coverage (Full Dose)":str(vaccCover*100)+"%"
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

    #calling the function from sirmodel.py
    plotData,R1_cases,R1_index,all_end_index,preparedness = createoutputjson(r1, r2, r3, wa, thie, FirstPeaktDate, ThirdWaveEmergenceDate, LockdownStartDate, LockdownEndDate, effLck, popdens, vaccDays, vaccCover)
    print(all_end_index)
    #plot for non vaccine scenario
    if vaccDays == 0.0:
        c_diff, date = plotData[0]['no_intervention_c_diff'], plotData[0]['date']
        #plotly df
        df = pd.DataFrame({
        "Time (Days)": date[:len(c_diff)],
        "Daily symptomatic cases (numbers/million)": [int(item) for item in c_diff]
            })
        #graph
        fig = px.line(df, x="Time (Days)", y="Daily symptomatic cases (numbers/million)", height=500)
        fig.update_yaxes(tickfont_family="Roboto Medium")

        #limiting x-axis quarterly
        fig.update_xaxes(
            dtick="M3", tickfont_family="Roboto Medium", tickfont_size=13, tickangle=-45)
    
    #plot for vaccine scenario
    else:
        ct_diff, ct0_diff, date = plotData[0]['no_intervention_ct_diff'], plotData[0]['no_intervention_ct0_diff'], plotData[0]['date']
        lim = min([len(ct_diff), len(ct0_diff), len(date)])
        #plotly df
        df = pd.DataFrame({
        "Time (Days)": date[:lim],
        "Daily symptomatic With Vaccine cases (numbers/million)": [int(item) for item in ct_diff[:lim]],
        "Daily symptomatic Vaccine cases (numbers/million)": [int(item) for item in ct0_diff[:lim]]
            })
        #graph
        fig = px.line(df, x="Time (Days)", y="Daily symptomatic Vaccine cases (numbers/million)", height=500)
        fig.add_scatter(x=df['Time (Days)'], y=df['Daily symptomatic With Vaccine cases (numbers/million)'], mode='lines', line_color="#ef553b", name="Vaccine")
        fig.add_scatter(x=df['Time (Days)'], y=df['Daily symptomatic Vaccine cases (numbers/million)'], mode='lines', line_color="#636efa", name="No Vaccine")
        fig.update_yaxes(tickfont_family="Roboto Medium")
        fig.update_xaxes(
            dtick="M3",
            tickfont_family="Roboto Medium", tickfont_size=13, tickangle=-45)

    #seroprevalence date
    SeroDate = date[R1_index]

    #adding place name to plot
    fig.update_layout(title_text= f"Location: {place}",
        title_xref="container")

    #adding x-axis data to plot
    fig.update_xaxes(title_text=f"""Time (Days)
        <br>
        {', '.join(ValuesPlot[:4])}
        <br>
        {', '.join(ValuesPlot[4:6])}
        <br>
        {', '.join(ValuesPlot[6:8])}
        <br>
        {', '.join(ValuesPlot[8:])}
        """)

    #displaying wanning message
    if all_end_index[1]>600:
        waMsg=""
    else: waMsg="hide"

    #shaded region for wave 1, 2 & 3
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

    #adding all graph data to a json
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON, round(R1_cases/10000, 2), SeroDate, wavestatus, waMsg, preparedness

##### FLASK APP STARTS HERE #####
app = Flask(__name__)

#jinja zip for multiple iteration in html table
app.jinja_env.filters['zip'] = zip

##### ROUTES #####

### SIGNIN/INDEX ###
@app.route("/", methods=['POST', 'GET'])
@app.route("/index/", methods=['POST', 'GET'])
def signin():
    if request.method == "POST":
        username = str(request.form['username'])
        password = request.form['password']
        #hashing the passowrd with md5
        password= hashlib.md5(password.encode()).hexdigest()

        #connect to db
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        #check if user exists
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

        #### USER DETAILS #####
        #making DB of users
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        #creating table
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
        #inserting data
        cur.execute('''
        INSERT INTO users(name, orgname, email, username, password) VALUES(?,?,?,?,?)''',
        (name, orgname, email, username, password))

        #commit changes and close connection
        conn.commit()
        cur.close()

        return redirect("/")
    else:
        return render_template("register.html")

### DASHBOARD ###
@app.route("/dashboard/", methods=['POST', 'GET'])
def dashboard():
    if request.method == "POST":
        place = str(request.form['place'])
        r1 = 0.0 if request.form['r1'] == "" else float(request.form['r1'])
        r2 = 0.0 if request.form['r2'] == "" else float(request.form['r2'])
        r3 = r2 if request.form['r3'] == "" else float(request.form['r3'])
        #checking for checkbox
        try:
            check = request.form['wanning']
            wa = float(request.form['wa'])*30
        except:
            check = ""
            wa = 0
        thie = 0.0 if request.form['thie'] == "" else float(request.form['thie'])/100
        FirstPeaktDate = str(request.form['FirstPeaktDate'])
        ThirdWaveEmergenceDate = str(request.form['ThirdWaveEmergenceDate'])
        try:
            checkpop = request.form['checkpop']
            popdens = float(request.form['popdens'])/100
        except:
            checkpop = ""
            popdens = 0.0
        LockdownStartDate = str(request.form['LockdownStartDate'])
        LockdownEndDate = str(request.form['LockdownEndDate'])
        effLck = 0 if request.form['effLck'] == "" else float(request.form['effLck'])/100
        vaccDays = 0 if request.form['vaccDays'] == "" else float(request.form['vaccDays'])*30
        vaccCover = 0.0 if request.form['vaccCover'] == "" else float(request.form['vaccCover'])/100

        #plot function
        graphJSON, R1_cases, seroDate, wavestatus, waMsg, preparedness = plot(place, r1, r2, r3, wa, thie, FirstPeaktDate, ThirdWaveEmergenceDate, LockdownStartDate, LockdownEndDate, effLck, popdens, vaccDays, vaccCover)
        
        #passing all the details to the html
        return render_template("dashboard.html", graphJSON=graphJSON, place=place, r1=r1, r2=r2, r3=r3, wa=wa/30, thie=thie*100,
                FirstPeaktDate=FirstPeaktDate, ThirdWaveEmergenceDate=ThirdWaveEmergenceDate, LockdownStartDate=LockdownStartDate,
                LockdownEndDate=LockdownEndDate, effLck=effLck*100, popdens=popdens*100, vaccDays=vaccDays/30,
                vaccCover=vaccCover*100, recoveryCases=R1_cases, preparedness=preparedness, wavestatus=wavestatus, waMsg=waMsg, check=check, checkpop=checkpop, seroDate=seroDate)

    else:
        #default values
        place = "India"
        r1 = 1.19
        r2 = 1.995
        r3 = r2
        check = ""
        wa = 0
        thie = 0
        FirstPeaktDate = "2020-09-16"
        ThirdWaveEmergenceDate = ""
        checkpop =""
        popdens = 0.0
        LockdownStartDate = ""
        LockdownEndDate = ""
        effLck = 0
        vaccDays = 0
        vaccCover = 0

        #plot function
        graphJSON, R1_cases, seroDate, wavestatus, waMsg, preparedness = plot(place, r1, r2, r3, wa, thie, FirstPeaktDate, ThirdWaveEmergenceDate, LockdownStartDate, LockdownEndDate, effLck, popdens, vaccDays, vaccCover)
        
        return render_template("dashboard.html", graphJSON=graphJSON, place=place, r1=r1, r2=r2, r3=r3, wa=wa/30, thie=thie*100,
                        FirstPeaktDate=FirstPeaktDate, ThirdWaveEmergenceDate=ThirdWaveEmergenceDate, LockdownStartDate=LockdownStartDate,
                        LockdownEndDate=LockdownEndDate, effLck=effLck*100, popdens=popdens*100, vaccDays=vaccDays/30,
                        vaccCover=vaccCover*100, recoveryCases=R1_cases, preparedness=preparedness, wavestatus=wavestatus, waMsg=waMsg, check=check, checkpop=checkpop, seroDate=seroDate)

### ABOUT ###
@app.route("/about/")
def about():
    return render_template("about.html")

### SERO TABLE ###
@app.route("/seroprevalence-table/")
def serotable():
    #reading data from csv
    data = pd.read_csv("static/r0-sero.csv")
    #converting dataframe to list
    r0s = data['R0'].tolist()
    peaks = data['peak'].tolist()
    daysprior = data['15 days before peak'].tolist()

    return render_template("seroprevalence-table.html", r0s=r0s, peaks=peaks, daysprior=daysprior)

### DOWNLOAD CODE FILE ###
@app.route('/download/')
def downloadCode():
    return send_file("sirmodel.py", as_attachment=True)

##### FLASK APP ENDS HERE #####
if __name__ == "__main__":
    app.run(debug=True, port=5001)