import requests
import json
import datetime
from tkinter import *
import time
clan_name = "" #your clan clan name
userid = 1234567890#your roblox userid (user must be in the above clan)
collect_data = False #saves data about clan points over time to text files on your pc, this is not sent anywhere outside of your pc and does not contian sensitive data
personalpointlist = []
clanpointlist = []
lb_position = 0
targetPoints = None
if collect_data:
    personal_points = open("personalpointdata.txt","a")
    clan_points = open("clanpointdata.txt","a")
url = "https://ps99.biggamesapi.io/api/activeClanBattle"

payload={}
headers = {}
json_response = requests.request("GET", url, headers=headers, data=payload).text
data = json.loads(json_response)
battle_name = data['data']['configName']
def predictTime():
    global targetPoints
    global personalpointlist
    global minutes 
    if targetPoints is not None:
        try:
            perMin = round((personalpointlist[-1]-personalpointlist[0])/minutes,2)
            curPoints = personalpointlist[-1]
            mins = (targetPoints-curPoints)/perMin
            return datetime.timedelta(seconds=round(mins*60))
        except ZeroDivisionError:
            return "00:00:00"
    else:
        return "00:00:00"
def updatePrediction():
    global line9
    line9.set(f"in {predictTime()}")

starttime = datetime.datetime.now().replace(microsecond=0)-datetime.timedelta(seconds=1)
class Win(Tk):

    def __init__(self,master=None):
        Tk.__init__(self,master)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)
        self._listening = False
        self._input_buffer = ""
        self.bind("<Key>", self._on_key)
    def start_listening(self):
        self._listening = True
        self._input_buffer = ""
        self.focus_force()

    def _on_key(self, event):
        if not self._listening:
            return

        if event.keysym == "Return":
            self._listening = False
            self.on_input_complete(self._input_buffer)
            self._input_buffer = ""
        elif event.keysym == "BackSpace":
            self._input_buffer = self._input_buffer[:-1]
        elif len(event.char) == 1:
            self._input_buffer += event.char

    def on_input_complete(self, text):
        global targetPoints
        mult = 1
        final = 0
        if text[-1]=="k":
            mult = 1000
            final = int(text[:-1])*mult
        elif text[-1] =="m":
            mult = 1000000
            final = int(text[:-1])*mult
        else:
            final = int(text)
        targetPoints = final
        updatePrediction()

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y
root = Win()    

def close():
    root.destroy()
def shrink():
    if root.geometry().startswith("180x180"):
        root.geometry("180x20")
    else:
        root.geometry("180x180")
def get_point_data():
    url = f"https://ps99.biggamesapi.io/api/clan/{clan_name}"
    payload={}
    headers = {}
    mypoints = 0
    json_response = requests.request("GET", url, headers=headers, data=payload).text
    data = json.loads(json_response)
    c_points = int(data['data']['Battles'][battle_name]['Points'])
    current_battle_points = data['data']['Battles'][battle_name]['PointContributions']
    global lb_position 
    lb_position = data['data']['Battles'][battle_name]['Place']
    for contribution in current_battle_points:
        if contribution['UserID'] == userid:
            mypoints = contribution['Points']
            break
    personalpointlist.append(mypoints)
    clanpointlist.append(c_points)
    if collect_data:
        csvfile = open("data.txt","w+",1)
        personal_points.write(str(datetime.datetime.now().replace(microsecond=0).timestamp()))
        personal_points.write("\n")
        personal_points.write(str(mypoints))
        personal_points.write("\n")
        clan_points.write(str(datetime.datetime.now().replace(microsecond=0).timestamp()))
        clan_points.write("\n")
        clan_points.write(str(c_points))
        clan_points.write("\n")
        csvfile.write(f"clan,{c_points},{lb_position}\n")
        for contribution in current_battle_points:
            csvfile.write(f"{contribution['UserID']},{contribution['Points']}\n")
        csvfile.close()
        
get_point_data()
root.overrideredirect(True)
root.geometry("180x180")
root.title("[KORG]")
root.attributes("-topmost", True)
root.config(bg="black")
root.attributes("-alpha", 0.5)
sessiontime = datetime.datetime.now().replace(microsecond=0)-starttime
minutes = 1
line1 = StringVar(root, f"Points: {format(personalpointlist[-1],',')} ({round(100*(personalpointlist[-1]/clanpointlist[-1]),2)}%)")
line2 = StringVar(root, f"This session: {format(personalpointlist[-1]-personalpointlist[0],',')}")
line3 = StringVar(root, f"Avg /min: {format(round((personalpointlist[-1]-personalpointlist[0])/minutes,2),',')}")
line4 = StringVar(root, f"Clan points: {format(clanpointlist[-1],',')}")
line5 = StringVar(root, f"This session: {format(clanpointlist[-1]-clanpointlist[0],',')}")
line6 = StringVar(root, f"Avg /min: {format(round((clanpointlist[-1]-clanpointlist[0])/minutes,2),',')}")
line7 = StringVar(root, f"Clan position: #{lb_position}")
line8 = StringVar(root, f"Session duration: {sessiontime}")
line9 = StringVar(root, f"in 00:00:00")
Label(textvariable=line1,bg="black",fg="white").place(x = 0, y = 0)
Label(textvariable=line2,bg="black",fg="white").place(x = 0, y = 20)
Label(textvariable=line3,bg="black",fg="white").place(x = 0, y = 40)
Label(textvariable=line4,bg="black",fg="white").place(x = 0, y = 60)
Label(textvariable=line5,bg="black",fg="white").place(x = 0, y = 80)
Label(textvariable=line6,bg="black",fg="white").place(x = 0, y = 100)
Label(textvariable=line7,bg="black",fg="white").place(x = 0, y = 120)
Label(textvariable=line8,bg="black",fg="white").place(x = 0, y = 140)
Label(textvariable=line9,bg="black",fg="white").place(x = 0, y = 160)
closebutton = Button(root,command=close,bg="black",height=1,width=2,text="X",fg="white",border=0).place(x=160,y=0)
shrinkbutton = Button(root,command=shrink,bg="black",height=1,width=2,text="^",fg="white",border=0).place(x=140,y=0)
predictbutton = Button(root,command = root.start_listening,bg="black",fg="white",height=1,width=2,text="+",border=0).place(x=160,y=160)
def update_time():
    global minutes
    sessiontime = datetime.datetime.now().replace(microsecond=0)-starttime
    minutes = sessiontime.seconds/60
    line8.set(f"Session duration: {sessiontime}")
    root.after(1000,update_time)
def update_stats():
    sessiontime = datetime.datetime.now().replace(microsecond=0)-starttime
    minutes = round(sessiontime.seconds/60)
    get_point_data()
    line1.set(f"Points: {format(personalpointlist[-1],',')} ({round(100*(personalpointlist[-1]/clanpointlist[-1]),2)}%)")
    line2.set(f"This session: {format(personalpointlist[-1]-personalpointlist[0],',')}")
    line3.set(f"Avg /min: {format(round((personalpointlist[-1]-personalpointlist[0])/minutes,2),',')}")
    line4.set(f"Clan points: {format(clanpointlist[-1],',')}")
    line5.set(f"This session: {format(clanpointlist[-1]-clanpointlist[0],',')}")
    line6.set(f"Avg /min: {format(round((clanpointlist[-1]-clanpointlist[0])/minutes,2),',')}")
    line7.set(f"Clan position: #{lb_position}")
    updatePrediction()
    root.after(60000,update_stats)
update_time()
root.after(60000,update_stats)
root.mainloop()