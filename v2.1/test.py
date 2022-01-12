from flask import Flask, app, render_template

app = Flask(__name__)

#jinja zip for multiple iteration in html table
app.jinja_env.filters['zip'] = zip


@app.route("/advanced-dashboard/", methods=['POST', 'GET'])
def advanced_dashboard():
    place = "India"
    # r1 = 1.19
    # r2 = 1.995
    # r3 = r2
    seropeak = 0.0
    FirstPeaktDate = "2020-09-16"
    fCases = 0.0
    SecondPeaktDate = ""
    sCases = 0.0
    checktrans = ""
    trans = 0
    # check = ""
    # wa = 0
    # thie = 0
    ThirdWaveEmergenceDate = ""
    checkpop =""
    popdens = 0.0
    LockdownStartDate = ""
    LockdownEndDate = ""
    effLck = 0
    vaccDays = 0
    vaccCover = 0
    print("INPUT", place, seropeak, FirstPeaktDate, fCases, SecondPeaktDate, sCases, checktrans, trans,
            ThirdWaveEmergenceDate, checkpop, popdens, LockdownStartDate, LockdownEndDate, effLck, vaccDays, vaccCover)

        #plot function
        # graphJSON, R1_cases, seroDate, wavestatus, waMsg, preparedness, selectefflck = plot(place, r1, r2, r3, wa, thie, FirstPeaktDate, ThirdWaveEmergenceDate, LockdownStartDate, LockdownEndDate, effLck, popdens, vaccDays, vaccCover)
        
    return render_template("advanced-dashboard.html", place=place, effLck=effLck, preparedness=0,
                    FirstPeaktDate=FirstPeaktDate, ThirdWaveEmergenceDate=ThirdWaveEmergenceDate, LockdownStartDate=LockdownStartDate,
                    LockdownEndDate=LockdownEndDate,  popdens=popdens*100, vaccDays=vaccDays/30,
                    vaccCover=vaccCover*100)


@app.route("/basic-dashboard/", methods=['POST', 'GET'])
def basic_dashboard():
    place = "India"
    # r1 = 1.19
    # r2 = 1.995
    # r3 = r2
    seropeak = 0.0
    FirstPeaktDate = "2020-09-16"
    fCases = 0.0
    SecondPeaktDate = ""
    sCases = 0.0
    checktrans = ""
    trans = 0
    # check = ""
    # wa = 0
    # thie = 0
    ThirdWaveEmergenceDate = ""
    checkpop =""
    popdens = 0.0
    LockdownStartDate = ""
    LockdownEndDate = ""
    effLck = 0
    vaccDays = 0
    vaccCover = 0
    print("INPUT", place, seropeak, FirstPeaktDate, fCases, SecondPeaktDate, sCases, checktrans, trans,
            ThirdWaveEmergenceDate, checkpop, popdens, LockdownStartDate, LockdownEndDate, effLck, vaccDays, vaccCover)

        #plot function
        # graphJSON, R1_cases, seroDate, wavestatus, waMsg, preparedness, selectefflck = plot(place, r1, r2, r3, wa, thie, FirstPeaktDate, ThirdWaveEmergenceDate, LockdownStartDate, LockdownEndDate, effLck, popdens, vaccDays, vaccCover)
        
    return render_template("basic-dashboard.html", place=place, effLck=effLck, preparedness=0,
                    FirstPeaktDate=FirstPeaktDate, ThirdWaveEmergenceDate=ThirdWaveEmergenceDate, LockdownStartDate=LockdownStartDate,
                    LockdownEndDate=LockdownEndDate,  popdens=popdens*100, vaccDays=vaccDays/30,
                    vaccCover=vaccCover*100)


##### FLASK APP ENDS HERE #####
if __name__ == "__main__":
    app.run(debug=True, port=5021)