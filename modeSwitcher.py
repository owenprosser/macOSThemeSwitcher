from subprocess import Popen, PIPE
import datetime, time ,ephem, json
import requests

darkMode = None
dayTime = None
pause = 0.05 #Number of minutes between updates
useGeoIP = False
lat = None
long = None

def sunUp():
   o = ephem.Observer()
   o.long = -0.540579
   o.lat = 53.230686
   if useGeoIP != False:
       o.long = long
       o.lat = lat
       print("Location from IP Address: ")
       print(lat, long)
   o.date = datetime.datetime.now()#'2018/10/15 22:30:00'
   print(o.date)
   s = ephem.Sun()
   s.compute(o)
   print(s.alt)

   return  s.alt < 0

def getCurrentMode():
    scpt = '''
        tell application "System Events"
      tell appearance preferences
        get dark mode
      end tell
    end tell
        '''
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = (p.communicate(scpt.encode()))
    stdout = stdout.decode()
    print(stdout)
    if stdout == 'true\n':
        print ("Dark mode on")
        return True
    elif stdout == 'false\n':
        print ("LightMode mode on")
        return False

def changeMode():
    scpt = '''
        tell application "System Events"
      tell appearance preferences
        set dark mode to not dark mode
      end tell
    end tell
        '''

    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(scpt.encode())

def GeoIP():
    send_url = 'http://api.ipstack.com/check?access_key=ebb35d3b8119a4d82aa93285578c2196'
    r = requests.get(send_url)
    j = json.loads(r.text)
    latitude = j['latitude']
    longitude = j['longitude']
    lat = int(latitude)
    long = int(longitude)
    print("Location from IP Address %s %s" % (lat, long))
    return(latitude,longitude)

if useGeoIP == True:
    (lat, long) = GeoIP()

while True:
    dayTime = sunUp()
    darkMode = getCurrentMode()

    if dayTime == True and darkMode == True:
        print ("DayTime but in Dark Mode")
        changeMode()
    elif dayTime == False and darkMode == False:
        print("NightTime but in LightMode")
        changeMode()
    elif dayTime == True and darkMode == False:
        print("In correct Mode. Daytime with LightMode")
    elif dayTime == False and darkMode == True:
        print("In correct Mode. NightTime with DarkMode")
    else:
        print("error")
    time.sleep(60*pause)