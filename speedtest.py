import RPi.GPIO as GPIO

import Tkinter

GPIO.setmode(GPIO.BCM)

IR = 16

GPIO.setup(IR, GPIO.OUT, initial=GPIO.LOW)

def func():

    GPIO.output(IR, not GPIO.input(IR))

root = Tkinter.Tk()

label = Tkinter.Label(root, text='press button')

label.pack()

button = Tkinter.Button(root, text='IR', command=func)

button.pack()

root.mainloop()

GPIO.cleanup()
