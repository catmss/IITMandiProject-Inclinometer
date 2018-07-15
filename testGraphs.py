#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 23:36:07 2018

@author: Mrinalini Singh
"""


import csv
import serial
import datetime
import matplotlib.pyplot as plt
from drawnow import *   


pitchg = []
pitcha = []
pitch_Mahony = []
pitch_Kalman = []
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0



def makeFig(): #Create a function that makes our desired plot

    plt.subplot(221)
    plt.ylim(-30, 30)                                 #Set angle of inclination min and max values
    plt.title('Using only gyroscope')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Angle')                            #Set ylabels
    plt.plot(pitchg, 'r-', label='Degrees')       #plot the temperature
    plt.legend(loc='upper left')                   #plot the legend
    
    plt.subplot(222)
    plt.ylim(-30, 30)                                 #Set angle of inclination min and max values
    plt.title('Using only accelerometer')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Angle')                            #Set ylabels
    plt.plot(pitcha, 'b-', label='Degrees')       #plot the temperature
    plt.legend(loc='upper left')                   #plot the legend
    
    plt.subplot(223)
    plt.ylim(-30, 30)                                 #Set angle of inclination min and max values
    plt.title('Using Mahony filter')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Angle')                            #Set ylabels
    plt.plot(pitch_Mahony, 'c-', label='Degrees')       #plot the temperature
    plt.legend(loc='upper left')                   #plot the legend
    
    plt.subplot(224)
    plt.ylim(-30, 30)                                 #Set angle of inclination min and max values
    plt.title('Using Kalman filter')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Angle')                            #Set ylabels
    plt.plot(pitch_Kalman, 'm-', label='Degrees')       #plot the temperature
    plt.legend(loc='upper left')                   #plot the legend
   
    # run "ls /dev/tty*" on terminal without arduino connected,
    # then connect the Arduino and run the command again.
    #Check ttyACM*, where * maybe 0 or 1, edit this code accordingly.
baud_rate = 115200 #set baudrate
ser = serial.Serial('/dev/ttyACM0', baud_rate)
    #ser = serial.Serial('/dev/ttyACM1', baud_rate)
if (not ser.readline()):
    print("Connection to Arduino failed")
    exit()
else:
    print("Connection to Arduino succeeded")
 
    
new_file_name = "Log-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".csv"

with open(new_file_name, 'w') as data_csv:
    file_writer = csv.writer(data_csv) #this will also save the time attribute
    while True:
        serial_data = str(ser.readline())
        serial_data = serial_data.rstrip()
        #print(serial_data)
        cmp = 'DATA_LINE'
        if serial_data.find(cmp) != -1 : 
            deletestr = "bn'rt ," 
            raw_data = serial_data.translate(str.maketrans('', '', deletestr))
            delimiter = '\\'
            string_data = raw_data.split(delimiter)
            string_data.pop()
            string_data.pop()
            string_data.pop()
            
            print(string_data)
            updated_float_data = [float(i) for i in string_data]

                #power.append(updated_float_data[5]);
                #energy.append(updated_float_data[6]);
            if len(updated_float_data) == 5:
                pitchg.append(updated_float_data[1])
                pitcha.append(updated_float_data[2])
                pitch_Mahony.append(updated_float_data[3])
                pitch_Kalman.append(updated_float_data[4]);
                
            drawnow(makeFig)
           
            plt.pause(.05)                     #Pause Briefly. Important to keep drawnow from crashing
            cnt=cnt+1
            if(cnt>100):                            #If you have 100 or more points, delete the first one from the array
                pitchg.pop(0)
                pitcha.pop(0)
                pitch_Mahony.pop(0)
                pitch_Kalman.pop(0)
                
                     
            file_writer.writerow([str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))]+updated_float_data)
            
            print(updated_float_data)
            
        else:
            print(serial_data)

    

    


