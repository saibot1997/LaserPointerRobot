from ctypes import pointer
import tkinter as tk
from tkinter import ttk
from xmlrpc.client import boolean
import serial
import socket
import struct
import time


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
  except:
    print("Error!")

#################   MAIN   ###########################
# platform angles
a1=0
a2=0
LPointer = False


if SERIAL_PORT:
  try:
    ser = serial.Serial(COM_PORT, COM_BAUD, timeout=1)

  except:
    print("Could not connect to serial port...",COM_PORT)

else:
  # WIFI conection
  try:
    print("Opening socket...")
    LaserPointerSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    LaserPointerSock.sendto(b'JJAH0000000000000000',(IP,PORT))
    print("Connected to Laser Pointer via Wifi... ")

  except:
    print("! Could not connect to laser pointer!. Check you are connected to the robot Wifi network (JJROBOTS_xx)")

sendCommand(b'JJAS',50,0,70,0) # 50% speed, 70% accel

running = True  

while running:
    sendLPointer()
    sendAngles(a1,a2)
    time.sleep(1)
    sendAngles(a1+10, a2+10)
    time.sleep(1)
    sendLPointer()
    running = False
