#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import json
import urllib.request
import sqlite3
import datetime as dt
import calendar
import config

fieldnames = ("IN_GmDate", "IN_VTM", "IN_VNN", "IN_VSCR", "IN_HTM", "IN_HNN", "IN_HSCR", "IN_OTSO_IND", "FLD9")

TodayDt = dt.date.today().strftime("%Y%m%d")
var_year = 2019

con=sqlite3.connect(config.dbpath)
con.isolation_level = None
cur=con.cursor()

cur.execute('''DROP TABLE HCKYTEAM''')
cur.execute('''CREATE TABLE HCKYTEAM
               (SCHEDYR INTEGER(4), TIMEZONE TEXT(3), CONFID INTEGER(3), CONFNAME TEXT(30), DIVID INTEGER(3), DIVNAME TEXT(30), LOCATENAME TEXT(30), TEAMNAME TEXT(50), TEAMABBR TEXT(3), TEAMNNAME TEXT(30), TEAMID INTEGER(3), FRANCHISEID INTEGER(3))''')

# create a simple JSON array
response = urllib.request.urlopen('https://statsapi.web.nhl.com/api/v1/teams')

json_html = json.load(response)
teams = json_html["teams"]
for conference in teams:
    team_id = conference["id"]
    time_zone = conference["venue"]["timeZone"]["tz"]
    conf_id = conference["conference"]["id"]
    conf_name = conference["conference"]["name"]
    div_id = conference["division"]["id"]
    div_name = conference["division"]["name"]
    location_name = conference["locationName"]
    team_name = conference["name"]
    team_abbr = conference["abbreviation"]
    team_nickname = conference["teamName"]
    franchise_id = conference["franchiseId"]
    ###RowCnt = RowCnt + 1
    params = (int(var_year), time_zone, int(conf_id), conf_name, int(div_id), div_name, location_name, team_name, team_abbr, team_nickname, int(team_id), int(franchise_id))
    cur.execute("INSERT INTO HCKYTEAM VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

cur.execute("SELECT * FROM HCKYTEAM")

tmdata = cur.fetchall()

print(tmdata)

cur.execute('''DROP TABLE HCKYSCHED''')
cur.execute('''CREATE TABLE HCKYSCHED
               (SCHEDYR INTEGER(4), GMID INTEGER(5), GMDT TEXT(20), GMDATE TEXT(10), GMTIME TEXT(5), GMDOW TEXT(3),  VTMID INTEGER(3), VTMABBR TEXT(3), VTMSCORE INTEGER(2), VTMSOG INTEGER(2), VTMSP1 INTEGER(2), VTMP1SOG INTEGER(2), VTMSP2 INTEGER(2), VTMP2SOG INTEGER(2), VTMSP3 INTEGER(2), VTMP3SOG INTEGER(2), VTMSOT INTEGER(2), VTMOTSOG INTEGER(2), VTMSSO INTEGER(2), HTMID INTEGER(3), HTMABBR TEXT(3), HTMSCORE INTEGER(2), HTMSOG INTEGER(2), HTMSP1 INTEGER(2), HTMP1SOG INTEGER(2), HTMSP2 INTEGER(2), HTMP2SOG INTEGER(2), HTMSP3 INTEGER(2), HTMP3SOG INTEGER(2), HTMSOT INTEGER(2), HTMOTSOG INTEGER(2), HTMSSO INTEGER(2), GMOTSOIND TEXT(2), GMDONEIND TEXT(1))''')

# create a simple JSON array
data = urllib.request.urlopen('https://statsapi.web.nhl.com/api/v1/schedule?startDate=2019-10-02&endDate=2020-04-04')

response = data.read()

urlresp_dict = json.loads(response)

resp_dates = (urlresp_dict["dates"])
var_zero = 0
var_NO = ''

datesLength = len(resp_dates)
for i in range(datesLength):
    gmDate = resp_dates[i], ["gameDate"]
    gameDate = gmDate[0]["games"]
    gmLength = len(gmDate[0]["games"])
    for i in range(gmLength):
        var_gmid = gameDate[i]["gamePk"]
        var_gmdate = gameDate[i]["gameDate"]
        dbmem = sqlite3.connect(":memory:")
        cmem = dbmem.cursor()
        cmem.execute("SELECT strftime('%s', ?)", (var_gmdate,))
        converted = cmem.fetchone()[0]
        dtconv = dt.datetime.fromtimestamp(int(converted))
        print("datetime is %s" % dt)
        var_dow = calendar.day_abbr[dtconv.weekday()]
        var_date = dtconv.date()
        var_time = dtconv.time().strftime("%H:%M")
        print("DOW   = " + str(var_dow))
        print("DATE  = " + str(var_date))
        print("TIME  = " + str(var_time))
        print("var_gmdate type  ---" + str(type(var_gmdate)))
        var_gmhomeid = gameDate[i]["teams"]["home"]["team"]["id"]
        var_gmawayid = gameDate[i]["teams"]["away"]["team"]["id"]
        cur.execute("SELECT TEAMABBR FROM HCKYTEAM WHERE TEAMID = ? ", (var_gmhomeid,))
        var_hometmabbr = cur.fetchone()
        if var_hometmabbr:
            print("HOME ABBR = " + str(var_hometmabbr))

        var_gmawayid = gameDate[i]["teams"]["away"]["team"]["id"]
        cur.execute("SELECT TEAMABBR FROM HCKYTEAM WHERE TEAMID = ? ", (var_gmawayid,))
        var_awaytmabbr = cur.fetchone()
        if var_awaytmabbr:
            print("AWAY ABBR = " + str(var_awaytmabbr))

        print("GmId = " + str(var_gmid) + "  GmDt = " + str(var_gmdate) + "  HomeId = " + str(var_gmhomeid) + "  AwayId = " + str(var_gmawayid))
        params = (int(var_year), int(var_gmid), str(var_gmdate), str(var_date), str(var_time), str(var_dow), str(var_gmawayid), str(var_awaytmabbr), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), str(var_gmhomeid), str(var_hometmabbr), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), int(var_zero), str(var_NO), str(var_NO))
        cur.execute("INSERT INTO HCKYSCHED VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)


cur.execute("UPDATE hckysched SET vtmabbr = substr(vtmabbr,4,3), htmabbr = substr(htmabbr,4,3)")

cur.execute("SELECT * FROM HCKYSCHED")

scheddata = cur.fetchall()

print(scheddata)
