from tkinter import Tk, Canvas

screen = Tk()
screen.title('bus simulator')
screen.wm_attributes('-topmost', 1)
screen.resizable(0, 0)

canvas = Canvas(screen, width = 800, height = 600)
canvas.pack()
screen.update()

bus_body = canvas.create_rectangle(200, 250, 600, 400, fill = 'green')
bus_tire = canvas.create_oval(220, 350, 320, 450, fill = 'black')
bus_tire = canvas.create_oval(480, 350, 580, 450, fill = 'black')

raillist = list()
for x in range(0, 801, 80) :
           rail = canvas.create_rectangle(x, 450, x+50, 470, fill = 'yellow')
           raillist.append(rail)

speed = 1
peoplenum = 0

speedtext = canvas.create_text(400, 100, text = 'speed : ' + str(speed), font = ('consolas', 30))
peopletext = canvas.create_text(400, 150, text = 'people :' + str(peoplenum), font =('consolas', 30))

def setspeed(number) :
           global speed
           speed = number
           canvas.itemconfig(speedtext, text = 'speed : ' + str(speed))
           
def run() :
           for rail in raillist :
                      canvas.move(rail, speed, 0)
                      pos = canvas.coords(rail)
                      if pos[0] > 800 :
                                 canvas.move(rail, -880, 0)
           canvas.after(100, run)
run()

def speed_up(event) :
           setspeed(speed+1)
           

def speed_down(event) :
        if speed > 0:
                setspeed(speed-1)

def people():
        global peoplenum
        peoplenum += 1
        canvas.itemconfig(peopletext, text = 'people : ' + str(peoplenum))
           
canvas.bind_all('<KeyPress-Up>', speed_up)
canvas.bind_all('<KeyPress-Down>', speed_down)
canvas.bind_all('<KeyPress-P>', people)

screen.mainloop()
