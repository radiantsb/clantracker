import requests
import json
import datetime
from tkinter import *
import time
clan_name = "" #your clan clan name
userid = #your roblox userid (user must be in the above clan)
collect_data = True #saves data about clan points over time to text files on your pc, this is not sent anywhere outside of your pc and does not contian sensitive data
personalpointlist = []
clanpointlist = []
lb_position = 0
url = "https://ps99.biggamesapi.io/api/activeClanBattle"
if collect_data:
    personal_points = open("personalpointdata.txt","a")
    clan_points = open("clanpointdata.txt","a")
payload={}
headers = {}
starttime = datetime.datetime.now().replace(microsecond=0)-datetime.timedelta(seconds=1)
class Win(Tk):

    def __init__(self,master=None):
        Tk.__init__(self,master)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y

def close():
    root.destroy()
def shrink():
    if root.geometry().startswith("180x160"):
        root.geometry("180x20")
    else:
        root.geometry("180x160")
root = Win()
json_response = requests.request("GET", url, headers=headers, data=payload).text
data = json.loads(json_response)
battle_name = data['data']['configName']
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
        personal_points.write(str(datetime.datetime.now().replace(microsecond=0).timestamp()))
        personal_points.write("\n")
        personal_points.write(str(mypoints))
        personal_points.write("\n")
        clan_points.write(str(datetime.datetime.now().replace(microsecond=0).timestamp()))
        clan_points.write("\n")
        clan_points.write(str(c_points))
        clan_points.write("\n")
get_point_data()
root.overrideredirect(True)
root.geometry("180x160")
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
Label(textvariable=line1,bg="black",fg="white").place(x = 0, y = 0)
Label(textvariable=line2,bg="black",fg="white").place(x = 0, y = 20)
Label(textvariable=line3,bg="black",fg="white").place(x = 0, y = 40)
Label(textvariable=line4,bg="black",fg="white").place(x = 0, y = 60)
Label(textvariable=line5,bg="black",fg="white").place(x = 0, y = 80)
Label(textvariable=line6,bg="black",fg="white").place(x = 0, y = 100)
Label(textvariable=line7,bg="black",fg="white").place(x = 0, y = 120)
Label(textvariable=line8,bg="black",fg="white").place(x = 0, y = 140)
closebutton = Button(root,command=close,bg="black",height=1,width=2,text="X",fg="white",border=0).place(x=160,y=0)
shrinkbutton = Button(root,command=shrink,bg="black",height=1,width=2,text="^",fg="white",border=0).place(x=140,y=0)
def update_time():
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
    root.after(60000,update_stats)
update_time()
root.after(60000,update_stats)
root.mainloop()
