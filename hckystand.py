import csv
import sqlite3
import datetime as dt
import config

fieldnames = ("D_YR", "D_DVNUM", "D_DVNAME", "D_DVCONF", "D_TMID", "D_TMNAME")

TodayDt = dt.date.today().strftime("%Y%m%d")

con=sqlite3.connect(config.dbpath)
con.isolation_level = None
cur=con.cursor()

cur.execute('''DROP TABLE HCKYSTAND''')
cur.execute('''CREATE TABLE HCKYSTAND
               (STD_YR INTEGER(4), STD_ID INTEGER(3), STD_GMS INTEGER(4), STD_WINS INTEGER(4), STD_LOSS INTEGER(4), STD_OTL INTEGER(4), STD_TOTPOINTS INTEGER(4), STD_GOALFOR INTEGER(4), STD_GOALAGNST INTEGER(4), STD_HGMS INTEGER(4), STD_HWINS INTEGER(4), STD_HLOSS INTEGER(4), STD_HOTL INTEGER(4), STD_HGOALFOR INTEGER(4), STD_HGOALAGNST INTEGER(4), STD_VGMS INTEGER(4), STD_VWINS INTEGER(4), STD_VLOSS INTEGER(4), STD_VOTL INTEGER(4), STD_VGOALFOR INTEGER(4), STD_VGOALAGNST INTEGER(4), STD_SOGFOR INTEGER(4), STD_SOGAGNST INTEGER(4), STD_HSOGFOR INTEGER(4), STD_HSOGAGNST INTEGER(4), STD_VSOGFOR INTEGER(4), STD_VSOGAGNST INTEGER(4))''')

cur.execute('''DROP TABLE HCKYDVSN''')
cur.execute('''CREATE TABLE HCKYDVSN
               (DVSN_YR INTEGER(4), DVSN_NUM INTEGER(2), DVSN_CONFERENCE TEXT(30), DVSN_NAME TEXT(30), DVSN_TMID INTEGER(2), DVSN_TEAMNN TEXT(30))''')

reader = csv.DictReader(open("c:/users/skyle/documents/NHLconf.txt"), delimiter=";", fieldnames=fieldnames)

RowCnt = 0
sched_year = "2019-"
sched_mm = "  "
sched_hyphen="-"
sched_dd = "  "
sched_Date = "   "
gmtime = "  "
sched_DOW = "  "
visit_city = "   "
visit_nname = "   "
visit_score = 0
home_city = "   "
home_nname = "   "
home_score = 0
OTSOIND = "  "
DONEIND = " "
var_year = 2019

calyear = {"October" : "2019", "November" : "2019", "December" : "2019", "January" : "2019", "February" : "2019", "March" : "2019", "April" : "2019"}
months = {"October" : "10", "November" : "11", "December" : "12", "January" : "01", "February" : "02", "March" : "03", "April" : "04"}
days = {"Wed" : "04", "Thu" : "05", "Fri" : "06", "Sat" : "07", "Sun" : "01", "Mon" : "02", "Tue" : "03"}

part_cities=['St.', 'San', 'Los', 'Tampa', 'Las', 'New']
cities= ['Toronto', 'Winnipeg', 'Pittsburgh', 'St. Louis', 'Calgary', 'Edmonton', 'Philadelphia', 'San Jose', 'Nashville', 'Boston', 'Montreal', 'Buffalo', 'Colorado', 'New York', 'New York2', 'Washington', 'Ottawa', 'Minnesota', 'Chicago', 'Detroit', 'Arizona', 'Anaheim', 'Los Angeles', 'Tampa Bay', 'Vancouver', 'Florida', 'Dallas', 'Carolina', 'Las Vegas', 'New Jersey', 'Columbus']
nicknames=['Maple Leafs', 'Jets', 'Penguins', 'Blues', 'Flames', 'Oilers', 'Flyers', 'Sharks', 'Predators', 'Bruins', 'Canadiens', 'Sabres', 'Avalanche', 'Rangers', 'Islanders', 'Capitals', 'Senators', 'Wild', 'Blackhawks', 'Red Wings', 'Coyotes', 'Ducks', 'Kings', 'Lightning', 'Canucks', 'Panthers', 'Stars', 'Hurricanes', 'Golden Knights', 'Devils', 'Blue Jackets']

for row in reader:
    params = (row['D_YR'], row['D_DVNUM'], row['D_DVNAME'], row['D_DVCONF'], row['D_TMID'], row['D_TMNAME'])
    cur.execute("INSERT INTO HCKYDVSN VALUES(?, ?, ?, ?, ?, ?)", params)

cur.execute("SELECT vtmid from HCKYSCHED where hckysched.schedyr = 2019 group by vtmid")
result=cur.fetchall()

cnt=0

for row in result:
    params = (2019, row[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    cur.execute("INSERT INTO HCKYSTAND VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

cur.execute("UPDATE HCKYSTAND SET STD_GMS=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND (B.VTMID = STD_ID or B.HTMID = STD_ID) and GMDONEIND = 'Y')")
cur.execute("UPDATE HCKYSTAND SET STD_WINS=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND ((B.VTMSCORE > B.HTMSCORE and B.VTMID = STD_ID) OR (B.HTMSCORE > B.VTMSCORE and B.HTMID = STD_ID)))")
cur.execute("UPDATE HCKYSTAND SET STD_LOSS=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND ((B.VTMSCORE < B.HTMSCORE and B.VTMID = STD_ID) OR (B.HTMSCORE < B.VTMSCORE and B.HTMID = STD_ID)) and (TRIM(GMOTSOIND != 'OT') AND TRIM(GMOTSOIND != 'SO')))")
cur.execute("UPDATE HCKYSTAND SET STD_OTL=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND ((B.VTMSCORE < B.HTMSCORE and B.VTMID = STD_ID OR (B.HTMSCORE < B.VTMSCORE and B.HTMID = STD_ID)) and (TRIM(GMOTSOIND = 'OT') OR TRIM(GMOTSOIND = 'SO'))))")
cur.execute("UPDATE HCKYSTAND SET STD_TOTPOINTS=((STD_WINS * 2) + STD_OTL)")
cur.execute("UPDATE HCKYSTAND SET STD_VWINS=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND (B.VTMSCORE > B.HTMSCORE and B.VTMID = STD_ID))")
cur.execute("UPDATE HCKYSTAND SET STD_VGMS=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND (VTMID = STD_ID) and gmdoneind = 'Y')")
cur.execute("UPDATE HCKYSTAND SET STD_VLOSS=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND ((B.VTMSCORE < B.HTMSCORE and B.VTMID = STD_ID) and (TRIM(GMOTSOIND != 'OT') AND TRIM(GMOTSOIND != 'SO'))))")
cur.execute("UPDATE HCKYSTAND SET STD_VOTL=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND ((B.VTMSCORE < B.HTMSCORE and B.VTMID = STD_ID)) and (TRIM(GMOTSOIND = 'OT') OR TRIM(GMOTSOIND = 'SO')))")
cur.execute("UPDATE HCKYSTAND SET STD_HGMS=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND (HTMID = STD_ID) and gmdoneind = 'Y')")
cur.execute("UPDATE HCKYSTAND SET STD_HWINS=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND (B.HTMSCORE > B.VTMSCORE and B.HTMID = STD_ID))")
cur.execute("UPDATE HCKYSTAND SET STD_HLOSS=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND ((B.HTMSCORE < B.VTMSCORE and B.HTMID = STD_ID) and (TRIM(GMOTSOIND != 'OT') AND TRIM(GMOTSOIND != 'SO'))))")
cur.execute("UPDATE HCKYSTAND SET STD_HOTL=(SELECT count(*) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND ((B.HTMSCORE < B.VTMSCORE and B.HTMID = STD_ID)) and (TRIM(GMOTSOIND = 'OT') OR TRIM(GMOTSOIND = 'SO')))")
cur.execute("UPDATE HCKYSTAND SET STD_VGOALFOR=(SELECT sum(B.VTMSCORE) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.VTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_HGOALFOR=(SELECT sum(B.HTMSCORE) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.HTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_HGOALAGNST=(SELECT sum(B.VTMSCORE) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.HTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_VGOALAGNST=(SELECT sum(B.HTMSCORE) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.VTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_GOALAGNST= STD_GOALAGNST + (SELECT sum(B.HTMSCORE) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.VTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_GOALAGNST= STD_GOALAGNST + (SELECT sum(B.VTMSCORE) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.HTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_GOALFOR= STD_GOALFOR + (SELECT sum(B.HTMSCORE) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.HTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_GOALFOR= STD_GOALFOR + (SELECT sum(B.VTMSCORE) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.VTMID = STD_ID)")
###
cur.execute("UPDATE HCKYSTAND SET STD_VSOGFOR=(SELECT sum(B.VTMSOG) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.VTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_HSOGFOR=(SELECT sum(B.HTMSOG) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.HTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_HSOGAGNST=(SELECT sum(B.VTMSOG) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.HTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_VSOGAGNST=(SELECT sum(B.HTMSOG) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.VTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_SOGAGNST= STD_SOGAGNST + (SELECT sum(B.HTMSOG) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.VTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_SOGAGNST= STD_SOGAGNST + (SELECT sum(B.VTMSOG) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.HTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_SOGFOR= STD_SOGFOR + (SELECT sum(B.HTMSOG) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.HTMID = STD_ID)")
cur.execute("UPDATE HCKYSTAND SET STD_SOGFOR= STD_SOGFOR + (SELECT sum(B.VTMSOG) from HCKYSCHED B WHERE B.SCHEDYR = 2019 AND B.VTMID = STD_ID)")

cur.execute("SELECT * FROM HCKYdvsn")

tmdata = cur.fetchall()

print (tmdata)

cur.execute("SELECT dvsn_num, dvsn_name, dvsn_conference, DVSN_TEAMNN, std_gms, std_wins, std_loss, std_otl, std_totpoints, STD_GOALFOR, STD_GOALAGNST, std_vwins, std_vloss, std_votl, STD_VGOALFOR, STD_VGOALAGNST, std_hwins, std_hloss, std_hotl, STD_HGOALFOR, STD_HGOALAGNST from hckydvsn, hckystand where std_yr = 2019 and dvsn_yr = std_yr and dvsn_TMID = STD_ID order by dvsn_num, std_totpoints desc, std_gms, std_wins desc")
resultstd=cur.fetchall()

prev_dv_name = ' '
prev_conf_name = ' '

for index, dat in enumerate(resultstd):

    ##for cntdat in range(21):
    ##    print ("DAT " + str(cntdat) + "  type " + str(type(dat[cntdat])) + str(dat[cntdat]))
    ## dat 14 is visitor goals for

    if dat[1] != prev_conf_name:
        print (' ')
        print ("  " + dat[1])
        prev_conf_name = dat[1]

    if dat[2] != prev_dv_name:
        print (' ')
        print ("      " + dat[2])
        prev_dv_name = dat[2]
        print (' ')
        print ("                                                                                                           ------------ Visitor -----------------   --------------- Home -----------------")
        print ("                                                                                        Goals     Goals                             Goals   Goals                            Goals  Goals  ")
        print ("             Team                                  Gms     Win   Loss  OTL   Points       For   Against     Wins    Loss      OTL     For  Against   Wins     Loss    OTL     For  Against")

    print ("             " + "     " + '{0:<30}'.format(dat[3]) + "    " + '{0:>2}'.format(str(dat[4])) + "      " + '{0:>2}'.format(str(dat[5])) + "     " + '{0:>2}'.format(str(dat[6])) + "   " + '{0:>2}'.format(str(dat[7]))  + "     " + '{0:>3}'.format(str(dat[8]))  + "        " + '{0:>3}'.format(str(dat[9]))  + "      " + '{0:>3}'.format(str(dat[10]))  + "       " + '{0:>2}'.format(str(dat[11]))  + "      " + '{0:>2}'.format(str(dat[12]))  + "       " + '{0:>2}'.format(str(dat[13]))  + "      " + '{0:>3}'.format(str(dat[14])) + "     "  + '{0:>3}'.format(str(dat[15]))  + "     " + '{0:>2}'.format(str(dat[16])) + "       " + '{0:>2}'.format(str(dat[17]))  + "      " + '{0:>2}'.format(str(dat[18])) + "     "  + '{0:>3}'.format(str(dat[19]))  + "     " + '{0:>3}'.format(str(dat[20])))
    ###
