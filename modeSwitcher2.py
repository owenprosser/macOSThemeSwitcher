from subprocess import Popen, PIPE
import datetime, ephem

darkMode = None

def sunup():
   o = ephem.Observer()
   o.long = -0.540579
   o.lat = 53.230686
   o.date = datetime.datetime.now()#'2018/10/15 22:30:00'
   s = ephem.Sun()
   s.compute(o)
   print(s.alt)
   return s.alt > 0

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
    darkMode = True
else:
    print ("Dark mode off")
    darkMode = False


print(sunup())

print(datetime.datetime.now())
