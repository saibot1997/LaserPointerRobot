
# Example code to test 2 axis Robot
# JJRobots

# Example of stelarium web coordinates: 307°55'51.1"   +38°26'32.9"

from ctypes import pointer
import tkinter as tk
from tkinter import ttk
from xmlrpc.client import boolean
import serial.tools
import socket
import struct
import time

try:
  import pygame
  from pygame.locals import *
except:
  print("Warning: You need to install pygame (pip install pygame) if you want to use a GamePad...")

# Variables for Wifi connection:
IP = "192.168.4.1" # Default ROBOT IP (with BROBOT JJROBOTS_XX wifi)
PORT = 2222        # Default ROBOT port
IN_PORT = 2223     # Default ROBOT input port
LaserPointerSock = None

SERIAL_PORT = False  # True if you want to use serial port, False (default) to use Wifi conection
# If you use wifi connection (SERIAL_PORT=False) be sure to connect first your PC to your robor netork (JJROBOTS_xx)
COM_PORT = 'COM12'   # You could check the Serial port number on Arduino
COM_BAUD = 115200
ser = None

def sendCommand(Header,p1,p2,p3=0,p4=0,p5=0,p6=0,p7=0,p8=0):
    base = bytearray(Header)  # message
    param1 = bytearray(struct.pack(">h",p1))
    param2 = bytearray(struct.pack(">h",p2))
    param3 = bytearray(struct.pack(">h",p3))
    param4 = bytearray(struct.pack(">h",p4))
    param5 = bytearray(struct.pack(">h",p5))
    param6 = bytearray(struct.pack(">h",p6))
    param7 = bytearray(struct.pack(">h",p7))
    param8 = bytearray(struct.pack(">h",p8))
    message = base+param1+param2+param3+param4+param5+param6+param7+param8
    #print(message)
    if SERIAL_PORT:
      try:
        ser.write(message)
      except:
        print("Could not send message (serial port)!")
    else:
      try:
        LaserPointerSock.sendto(message,(IP,PORT))
      except:
        print("Could not send message (Wifi)!")

def send_position():
    global az, alt, az_deg,alt_deg
    c = coords.get()
    print("Coords: %s" % (c))
    try:
      az = c.split("  ")[0].strip()
      alt = c.split("  ")[1].strip()
      print("Azimuth: %s" % (az))
      print("Altitud: %s" % (alt))
      deg, minutes, seconds,other =  re.split('[°\'"]', az)
      az_deg = (float(deg) + float(minutes)/60 + float(seconds)/(60*60))
      if (az_deg>180):
        az_deg =az_deg-360
      print(deg,minutes,seconds,"=>deg:",az_deg)
      deg, minutes, seconds,other =  re.split('[°\'"]', alt)
      alt_deg = (float(deg) + float(minutes)/60 + float(seconds)/(60*60))
      if (alt_deg>180):
        alt_deg = alt_deg-360
      print(deg,minutes,seconds,"=>deg:",alt_deg)
      sendCommand(b'JJAM',int(az_deg*100),int(alt_deg*100),0,0,0,LPointer)
    except:
      print("Error on input!")

def sendLPointer():
  global LPointer
  try:
    LPointer = not LPointer
    if (LPointer):
      print("Laser on")
    else:
      print("Laser off")
    sendCommand(b'JJAM',int(a1*100),int(a2*100),0,0,0,LPointer)
    time.sleep(0.5)
  except:
    print("Error!")

def sendAngles(new_a1,new_a2):
  global a1,a2
  try:
    #print("a1:",a1,"a2:",a2)
    a1 = new_a1
    a2 = new_a2
    sendCommand(b'JJAM',int(a1*100),int(a2*100),0,0,0,LPointer)
    Rtext_a1.set('{:.2f}'.format(a1))
    Rtext_a2.set('{:.2f}'.format(a2))
  except:
    print("Error!")

def sendAngles2(new_a1,new_a2,s=0.5):
  global a1,a2
  try:
    #print("a1:",a1,"a2:",a2)
    a1 = new_a1
    a2 = new_a2
    sendCommand(b'JJAM',int(a1*100),int(a2*100),0,0,0,LPointer)
    time.sleep(s)
    text_a1.set('{:.2f}'.format(a1))
    text_a2.set('{:.2f}'.format(a2))
  except:
    print("Error!")

def sendAnglesKey(event=None):
  try:
    sendAngles(float(angle1.get()),float(angle2.get()))
    print("a1:",a1,"a2:",a2)
  except:
    print("Error!")

def leftKey(event=None):
    sendAngles(a1-1,a2)

def rightKey(event=None):
    sendAngles(a1+1,a2)

def upKey(event=None):
    sendAngles(a1,a2+1)

def downKey(event=None):
    sendAngles(a1,a2-1)

def CleftKey(event=None):
    sendAngles(a1-0.02,a2)

def CrightKey(event=None):
    sendAngles(a1+0.02,a2)

def CupKey(event=None):
    sendAngles(a1,a2+0.02)

def CdownKey(event=None):
    sendAngles(a1,a2-0.02)

def SleftKey(event=None):
    sendAngles(a1-4,a2)

def SrightKey(event=None):
    sendAngles(a1+4,a2)

def SupKey(event=None):
    sendAngles(a1,a2+4)

def SdownKey(event=None):
    sendAngles(a1,a2-4)

def space(event=None):
    sendLPointer()


#################   MAIN   ###########################
# platform angles
a1=0
a2=0
LPointer = False
# Try to detect a GAMEPAD
try:
  pygame.quit()
  pygame.init()
  pad_count = pygame.joystick.get_count()
  if pad_count > 0:
    myPAD = pygame.joystick.Joystick(0)
    myPAD.init()
    gamepad_ready = True
    if "XBOX" in myPAD.get_name():
        XBOX_Pad = True
    else:
        XBOX_Pad = False
            
    print("GAMEPAD detected ", myPAD.get_name())
  else:
    gamepad_ready = False
    print("GAMEPAD NOT detected")
except:
  gamepad_ready = False

master = tk.Tk()
master.title("JJROBOTS 2Axis Laser pointer control app")
master.bind('<Return>', sendAnglesKey)
master.bind('<Left>', leftKey)
master.bind('<Right>', rightKey)
master.bind('<Up>', upKey)
master.bind('<Down>', downKey)
master.bind('<Control-Left>', CleftKey)
master.bind('<Control-Right>', CrightKey)
master.bind('<Control-Up>', CupKey)
master.bind('<Control-Down>', CdownKey)
master.bind('<Shift-Left>', SleftKey)
master.bind('<Shift-Right>', SrightKey)
master.bind('<Shift-Up>', SupKey)
master.bind('<Shift-Down>', SdownKey)
master.bind('<space>', space)

if SERIAL_PORT:
  try:
    ser = serial.Serial(COM_PORT, COM_BAUD, timeout=1)
    tk.Label(master,text="Connected to COM port...").grid(row=0)
  except:
    print("Could not connect to serial port...",COM_PORT)
    tk.Label(master,text="Could not connect to serial port...").grid(row=0)
else:
  # WIFI conection
  try:
    print("Opening socket...")
    LaserPointerSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    LaserPointerSock.sendto(b'JJAH0000000000000000',(IP,PORT))
    print("Connected to Laser Pointer via Wifi... ")
    tk.Label(master,text="Connected to Robot via Wifi...").grid(row=0)
  except:
    print("! Could not connect to laser pointer!. Check you are connected to the robot Wifi network (JJROBOTS_xx)")
    tk.Label(master,text="Could not connect to robot wifi").grid(row=0)

tk.Label(master,text="Coordenadas Stellarium:").grid(row=1)
tk.Label(master,text="Az/Alt:").grid(row=2)

coords = tk.Entry(master)
coords.config(width=30)
coords.grid(row=2, column=1,padx=10)
tk.Button(master,text='  Go!  ', 
          command=send_position).grid(row=3,column=0, 
                                    sticky=tk.W,padx=20,pady=12)

tk.Label(master,text="Angle1:").grid(row=4)
tk.Label(master,text="Angle2:").grid(row=5)
text_a1 = tk.StringVar()
text_a1.set("0")
angle1 = tk.Entry(master,textvariable=text_a1)
angle1.grid(row=4, column=1,padx=10)
text_a2 = tk.StringVar()
angle2 = tk.Entry(master,textvariable=text_a2)
text_a2.set("0")
angle2.grid(row=5, column=1,padx=10)
tk.Button(master,text='  Go!  ',
          command=sendAnglesKey).grid(
            row=6,column=0,sticky=tk.W,padx=20,pady=12)

separator = ttk.Separator(master, orient='horizontal')
separator.grid(row=7,column=0,columnspan=4, ipadx=200)


tk.Button(master,text='  Laser  ',
          command=sendLPointer).grid(
            row=8,column=0,sticky=tk.W,padx=20,pady=12)

separator = ttk.Separator(master, orient='horizontal')
separator.grid(row=9,column=0,columnspan=4, ipadx=200)

tk.Label(master,text="Robot angle1:").grid(row=10)
tk.Label(master,text="Robot angle2:").grid(row=11)
Rtext_a1 = tk.StringVar()
Rtext_a1.set("0")
Rangle1 = tk.Label(master,textvariable=Rtext_a1)
Rangle1.grid(row=10, column=1,padx=0)
Rtext_a2 = tk.StringVar()
Rangle2 = tk.Label(master,textvariable=Rtext_a2)
Rtext_a2.set("0")
Rangle2.grid(row=11, column=1,padx=0,pady=10)

# Reduce accelerations and speed
##sendCommand(b'JJAS',10,0,25,0) # 10% speed, 25% accel
##sendAngles(3,0)
##time.sleep(1.0)
##sendAngles(3,3)
##time.sleep(1.0)
##sendAngles(0,3)
##time.sleep(1.0)
##sendAngles(0,0)
##time.sleep(1.0)

sendCommand(b'JJAS',50,0,70,0) # 50% speed, 70% accel

#########################################       
### CUSTOM MAIN LOOP
#########################################   
running = True  
X_gp_step = 0
Y_gp_step = 0  
old_time = time.time()
while running:
  if gamepad_ready:
    for event in pygame.event.get():
      if event.type == JOYAXISMOTION:
        #axes = myPAD.get_numaxes()
        X_gp_step = round(myPAD.get_axis(2),2)
        Y_gp_step = round(myPAD.get_axis(3),2)

        if abs(X_gp_step)<0.2:
          X_gp_step=0
        if abs(Y_gp_step)<0.2:
          Y_gp_step=0

        #sendAngles(a1+X_gp_step,a2+Y_gp_step)

        #print("JOY",X_gp_step,Y_gp_step)
      if event.type == JOYBUTTONDOWN:
        print("Joystick button!",myPAD.get_button(0),myPAD.get_button(1),myPAD.get_button(2),myPAD.get_button(3))


    # Send gamepad command at 10Hz
    if (time.time()-old_time)>0.02:
      old_time = time.time()
      if (X_gp_step!=0 or Y_gp_step!=0):
        #print("joy command")
        # Non linear joystick adjust
        if X_gp_step<0:
          a1_step = -X_gp_step*X_gp_step*3
        else:
          a1_step = X_gp_step*X_gp_step*3
        if Y_gp_step<0:
          a2_step = -Y_gp_step*Y_gp_step*3
        else:
          a2_step = Y_gp_step*Y_gp_step*3
        sendAngles(a1+a1_step,a2+a2_step)

  master.update_idletasks()
  master.update()

try:
  ser.close()
except:
  print("Could not close serial port...")
  
print("End...")
