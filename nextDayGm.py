#!/usr/bin/env python
import sqlite3
import datetime as dt
import config

TodayDt = dt.date.today().strftime("%Y-%m-%d")

con = sqlite3.connect(config.dbpath)
con.isolation_level = None
cur = con.cursor()

# get todays games + standings
print(TodayDt)
params: str = TodayDt
cur.execute("select GMDATE, GMTIME, VTMID, HTMID, VTMABBR, HTMABBR from hckysched where GMDATE = ? order by GMTIME", [params])

result = cur.fetchall()

for index, dat in enumerate(result):
    away_name = dat[4]
    home_name = dat[5]
    print('  '  + dat[0] + '  ' + dat[1] + '       ' + '{0: <15}'.format(away_name) + '                                ' + '{0: <15}'.format(home_name))
    params = (dat[2])
    cur.execute("select std_wins, std_loss, std_otl, std_totpoints, std_vwins, std_vloss, std_votl, std_vgms, std_vgoalfor, std_vgoalagnst, std_vsogfor, std_vsogagnst from hckystand where std_id = ?", [params])
    visit_result = cur.fetchall()

    v_goalsforpergame = 0
    v_goalsagnstpergame = 0
    v_sogforpergame = 0
    v_sogagnstpergame = 0

    h_goalsforpergame = 0
    h_goalsagnstpergame = 0
    h_sogforpergame = 0
    h_sogagnstpergame = 0

    for v_index, v_dat in enumerate(visit_result):
        v_twins = v_dat[0]
        v_tlosses = v_dat[1]
        v_totl = v_dat[2]
        v_points = v_dat[3]
        v_wins = v_dat[4]
        v_losses = v_dat[5]
        v_otl = v_dat[6]
        v_percent = 0
        if (float(v_dat[4]) + float(v_dat[5]) + float(v_dat[6])) > 0:
            v_percent = (float(v_dat[4]) / (float(v_dat[4]) + float(v_dat[5]) + float(v_dat[6])) * 100.00)
        v_games = v_dat[7]
        if float(v_dat[7]) > 0:
            v_goalsforpergame = (float(v_dat[8]) / float(v_dat[7]))
            v_goalsagnstpergame = (float(v_dat[9]) / float(v_dat[7]))

        if float(v_dat[7]) > 0:
            v_sogforpergame = (float(v_dat[10]) / float(v_dat[7]))
            v_sogagnstpergame = (float(v_dat[11]) / float(v_dat[7]))

    params = (dat[3])
    cur.execute("select std_wins, std_loss, std_otl, std_totpoints, std_hwins, std_hloss, std_hotl, std_hgms, std_hgoalfor, std_hgoalagnst, std_hsogfor, std_hsogagnst from hckystand where std_id = ?", [params])

    home_result = cur.fetchall()
    for h_index, h_dat in enumerate(home_result):
        h_twins = h_dat[0]
        h_tlosses = h_dat[1]
        h_totl = h_dat[2]
        h_points = h_dat[3]
        h_wins = h_dat[4]
        h_losses = h_dat[5]
        h_otl = h_dat[6]

        h_percent = 0
        if (float(h_dat[4]) + float(h_dat[5]) + float(h_dat[6])) > 0:
            h_percent = (float(h_dat[4]) / (float(h_dat[4]) + float(h_dat[5]) + float(h_dat[6])) * 100.00)
        h_games = h_dat[7]
        if float(h_dat[7]) > 0:
            h_goalsforpergame = (float(h_dat[8]) / float(h_dat[7]))
            h_goalsagnstpergame = (float(h_dat[9]) / float(h_dat[7]))

        if float(h_dat[7]) > 0:
            h_sogforpergame = (float(h_dat[10]) / float(h_dat[7]))
            h_sogagnstpergame = (float(h_dat[11]) / float(h_dat[7]))

        v_GTOTAL = (float(v_goalsforpergame) + float(v_goalsagnstpergame))/2
        h_GTOTAL = (float(h_goalsforpergame) + float(h_goalsagnstpergame))/2
        TOTGOALS = (float(v_GTOTAL) + float(h_GTOTAL))

        v_SOGTOTAL = (float(v_sogforpergame) + float(v_sogagnstpergame))/2
        h_SOGTOTAL = (float(h_sogforpergame) + float(h_sogagnstpergame))/2
        TOTSOGS = (float(v_SOGTOTAL) + float(h_SOGTOTAL))


    if v_points > h_points:
        points_ldr = away_name
    if v_points < h_points:
        points_ldr = home_name
    if v_points == h_points:
        points_ldr = '   ** TIE **'
    print('                           W/L/OTL/Pnts                 ' + '{0: >2}'.format(str(v_twins)) + '/' + '{0: >3}'.format(str(v_tlosses)) + '/' + '{0: >3}'.format(str(v_totl)) + '/' + '{0: >3}'.format(str(v_points)) +  '       W/L/OTL/Pnts                ' + '{0: >3}'.format(str(h_twins)) + '/' + '{0: >3}'.format(str(h_tlosses)) + '/' + '{0: >3}'.format(str(h_totl)) + '/' + '{0: >3}'.format(str(h_points)) + '                ' + str(points_ldr))

    if v_percent > h_percent:
        percent_ldr = away_name
    if v_percent < h_percent:
        percent_ldr = home_name
    if v_percent == h_percent:
        percent_ldr = '   ** TIE **'
    print('                           Visitor W/L/OTL     ' + '{0: >3}'.format(str(v_wins)) + '/' + '{0: >3}'.format(str(v_losses)) + '/' + '{0: >3}'.format(str(v_otl)) + '  ' + '{:8.4f}'.format(v_percent) + ' %' + '       Home W/L/OTL        ' + '{0: >3}'.format(str(h_wins)) + '/' + '{0: >3}'.format(str(h_losses)) + '/' + '{0: >3}'.format(str(h_otl)) + '  ' + '{:8.4f}'.format(h_percent) + ' %'  + '                ' + str(percent_ldr))

    if v_goalsforpergame > h_goalsforpergame:
        goalsfor_ldr = away_name
    if v_goalsforpergame < h_goalsforpergame:
        goalsfor_ldr = home_name
    if v_goalsforpergame == h_goalsforpergame:
        goalsfor_ldr = '   ** TIE **'
    print('                           Visit Goals For/Game        ' + '{:6.2f}'.format(v_goalsforpergame) +  '                Home Goals For/Game          ' + '{:6.2f}'.format(h_goalsforpergame)  + '                        ' + str(goalsfor_ldr))

    if v_goalsagnstpergame < h_goalsagnstpergame:
        goalsagnst_ldr = away_name
    if v_goalsagnstpergame > h_goalsagnstpergame:
        goalsagnst_ldr = home_name
    if v_goalsagnstpergame == h_goalsagnstpergame:
        goalsagnst_ldr = '   ** TIE **'
    print('                           Visit Goals Against/Game    ' + '{:6.2f}'.format(v_goalsagnstpergame) + '                Home Goals Against/Game      ' + '{:6.2f}'.format(h_goalsagnstpergame)  + '                        ' + str(goalsagnst_ldr))
    print('                           Visit Goals TOTAL GOALS     ' + '{:6.2f}'.format(v_GTOTAL) + '                Home TOTAL GOALS             ' + '{:6.2f}'.format(h_GTOTAL) + '                  TOTAL GOALS  ' + '{:6.2f}'.format(TOTGOALS))

    if v_sogforpergame > h_sogforpergame:
        sogfor_ldr = away_name
    if v_sogforpergame < h_sogforpergame:
        sogfor_ldr = home_name
    if v_sogforpergame == h_sogforpergame:
        sogfor_ldr = '   ** TIE **'
    print('                           Visit SOGs For/Game         ' + '{:6.2f}'.format(v_sogforpergame) +  '                Home SOGs For/Game           ' + '{:6.2f}'.format(h_sogforpergame)  + '                        ' + str(sogfor_ldr))

    if v_sogagnstpergame < h_sogagnstpergame:
        sogagnst_ldr = away_name
    if v_sogagnstpergame > h_sogagnstpergame:
        sogagnst_ldr = home_name
    if v_sogagnstpergame == h_sogagnstpergame:
        sogagnst_ldr = '   ** TIE **'
    print('                           Visit SOGs Against/Game     ' + '{:6.2f}'.format(v_sogagnstpergame) + '                Home SOGs Against/Game       ' + '{:6.2f}'.format(h_sogagnstpergame)  + '                        ' + str(sogagnst_ldr))
    print('                           Visit TOTAL SOGs            ' + '{:6.2f}'.format(v_SOGTOTAL) + '                Home TOTAL SOGs              ' + '{:6.2f}'.format(h_SOGTOTAL) + '                  TOTAL SOGs   ' + '{:6.2f}'.format(TOTSOGS))
    print(' ')
