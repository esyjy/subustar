from tkinter import Tk, Canvas
from bussqlhandle import start_server, init_table, insert
import time
import datetime

def setspeed(number) :
    global speed
    speed = number
    canvas.itemconfig(speedtext, text = 'speed : ' + str(speed))

def run() :
    global raillist, canvas, speed
    for rail in raillist :
        canvas.move(rail, speed, 0)
        pos = canvas.coords(rail)
        if pos[0] > 800 :
            canvas.move(rail, -880, 0)

    canvas.after(100, run)

def speed_up(event) :
    global speed
    setspeed(round(speed+0.1,1))
    canvas.itemconfig(bus_body, fill="green")

def speed_down(event) :
    global speed
    if speed > 0:
        setspeed(round(speed-0.1,1))
        canvas.itemconfig(bus_body, fill="green")

def people(event):
    global peoplenum
    if speed == 0:
        peoplenum += 1
        canvas.itemconfig(peopletext, text = 'people : ' + str(peoplenum))
        canvas.itemconfig(bus_body, fill="red")

def people2(event):
    global peoplenum
    if speed == 0 and peoplenum > 0:
        peoplenum -= 1
        canvas.itemconfig(peopletext, text = 'people : ' + str(peoplenum))
        canvas.itemconfig(bus_body, fill = "blue")

def break_(event):
    global speed
    setspeed(round(0))

def gettime():
    return str(datetime.datetime.now())[:-3]

def changetime():
    global timetext
    canvas.itemconfig(timetext, text = gettime())
    screen.after(50, changetime)

def savevalue(event):
    global speed, peoplenum, conn
    insert(conn, "speed_table", [str(speed), "'"+gettime()+"'", str(peoplenum)])

screen = Tk()
screen.title('bus simulator')
screen.wm_attributes('-topmost', 1)
screen.resizable(0, 0)

canvas = Canvas(screen, width = 800, height = 600)
canvas.pack()
screen.update()

speed = 0
peoplenum = 0
raillist = list()
for x in range(0, 801, 80) :
    rail = canvas.create_rectangle(x, 450, x+50, 470, fill = 'yellow')
    raillist.append(rail)

bus_body = canvas.create_rectangle(200, 250, 600, 400, fill = 'green')
bus_tire = canvas.create_oval(220, 350, 320, 450, fill = 'black')
bus_tire = canvas.create_oval(480, 350, 580, 450, fill = 'black')
speedtext = canvas.create_text(400, 100,
                               text = 'speed : ' + str(speed), font = ('consolas', 30))
peopletext = canvas.create_text(400, 150,
                                text = 'people : ' + str(peoplenum), font =('consolas', 30))
t = time.localtime()
timetext = canvas.create_text(400, 50,
                              text = gettime() , font =('consolas', 30))

canvas.bind_all('<KeyPress-Up>', speed_up)
canvas.bind_all('<KeyPress-Down>', speed_down)
canvas.bind_all('<KeyPress-space>', break_)
canvas.bind_all('<KeyPress-p>', people)
canvas.bind_all('<KeyPress-m>', people2)
canvas.bind_all('<KeyPress-s>', savevalue)

if __name__ == "__main__" :
    run()
    conn = start_server()
    init_table(conn,"speed_table")
    changetime()
    screen.mainloop()