import datetime as dt
import sqlite3
import sys
import json
import urllib.request

con=sqlite3.connect("C:/Users/skyle/Documents/sqlite3_NHL2019.db")
con.isolation_level = None
cur=con.cursor()

TodayDt = dt.date.today()

selDate = str(TodayDt + dt.timedelta(days=-1))
print (selDate)

cur.execute("SELECT gmid FROM HCKYSCHED where gmdate = ?", (selDate,))

gamedata = cur.fetchall()
print (gamedata)

for index, dat in enumerate(gamedata):
    sv_gmid = dat[0]
    data = urllib.request.urlopen('https://statsapi.web.nhl.com/api/v1/game/'+str(sv_gmid)+'/linescore')
    print (sv_gmid)
    gmOTSOIND = 'N'
    awayshootout = 0
    homeshootout = 0
    response = data.read()
    json_response = json.loads(response)
    ###print response
    print (json_response)
    GmStateInd = (json_response["currentPeriod"])
    ###currentPeriod, once game is completed --- 3 --> regular game, 4 --> OT game, 5 --> SO game
    awayGoals = (json_response["teams"]["away"]["goals"])
    homeGoals = (json_response["teams"]["home"]["goals"])
    awaySOG = (json_response["teams"]["away"]["shotsOnGoal"])
    homeSOG = (json_response["teams"]["home"]["shotsOnGoal"])
    var_periods = (json_response["periods"])

    away_pergoals = []
    home_pergoals = []
    away_perSOG = []
    home_perSOG = []
    period_num = []

    ## shootouts don't count as a period, so -1 if SO
    period_range = GmStateInd
    if period_range == 4:
        gmOTSOIND = 'OT'

    if period_range == 5:
        gmOTSOIND = 'SO'
        period_range = 4
        if awayGoals > homeGoals:
            awayshootout = 1
            homeshootout = 0

        if awayGoals < homeGoals:
            homeshootout = 1
            awayshootout = 0

    if period_range > 0:
        gmDONEIND = 'Y'

    for i in range(period_range):
           period_num.insert(i, var_periods[i]["num"])
           away_pergoals.insert(i, var_periods[i]["away"]["goals"])
           away_perSOG.insert(i, var_periods[i]["away"]["shotsOnGoal"])
           home_pergoals.insert(i, var_periods[i]["home"]["goals"])
           home_perSOG.insert(i, var_periods[i]["home"]["shotsOnGoal"])

    if period_range < 4:
           period_num.insert(i, 4)
           away_pergoals.insert(i, 0)
           away_perSOG.insert(i, 0)
           home_pergoals.insert(i, 0)
           home_perSOG.insert(i, 0)

    ##### sample #### sqlite_update_query = """Update new_developers set salary = ?, email = ? where id = ?"""
    params = (int(awayGoals), int(homeGoals), int(awaySOG), int(homeSOG), int(away_pergoals[0]), int(away_perSOG[0]), int(home_pergoals[0]), int(home_perSOG[0]), int(away_pergoals[1]), int(away_perSOG[1]), int(home_pergoals[1]), int(home_perSOG[1]), int(away_pergoals[2]), int(away_perSOG[2]), int(home_pergoals[2]), int(home_perSOG[2]), int(away_pergoals[3]), int(away_perSOG[3]), int(home_pergoals[3]), int(home_perSOG[3]), int(awayshootout), int(homeshootout), str(gmOTSOIND), str(gmDONEIND), sv_gmid)
    cur.execute(
       "UPDATE HCKYSCHED set VTMSCORE = ?, HTMSCORE = ?, VTMSOG = ?, HTMSOG = ?, VTMSP1 = ?, VTMP1SOG = ?, HTMSP1 = ?, HTMP1SOG = ?, VTMSP2 = ?, VTMP2SOG = ?, HTMSP2 = ?, HTMP2SOG = ?, VTMSP3 = ?, VTMP3SOG = ?, HTMSP3 = ?, HTMP3SOG = ?, VTMSOT = ?, VTMOTSOG = ?, HTMSOT = ?, HTMOTSOG = ?, VTMSSO = ?, HTMSSO = ?, GMOTSOIND = ?, GMDONEIND = ? where GMID = ?", params)
