from subprocess import Popen, PIPE
import datetime, ephem

darkMode = None
dayTime = None

def sunUp():
   o = ephem.Observer()
   o.long = -0.540579
   o.lat = 53.230686
   o.date = datetime.datetime.now()#'2018/10/15 22:30:00'
   s = ephem.Sun()
   s.compute(o)
   return s.alt > 0

def getCurrentMode():
    scpt = '''
        tell application "System Events"

    	tell appearance preferences

    		get dark mode

    	end tell

    end tell
        '''

    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(scpt)

    print (stdout[0])

    if stdout[0] == 't':
        print ("Dark mode on")
        return True
    else:
        print ("Dark mode off")
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
    stdout, stderr = p.communicate(scpt)

dayTime = sunUp()

darkMode = getCurrentMode()
print(dayTime)

if dayTime == True and darkMode == True:
    print ("DayTime but in Dark Mode")
    changeMode()
elif dayTime == False and darkMode == False:
    print("NightTime but in LightMode")
    changeMode()
elif dayTime == True and darkMode == True:
    print("In correct Mode. Daytime with LightMode")
elif dayTime == False and darkMode == True:
    print("In correct Mode. NightTimetime with DarkMode")
