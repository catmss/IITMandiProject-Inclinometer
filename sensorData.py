#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 23:36:07 2018

@author: Mrinalini Singh
"""


import csv
import serial
import datetime
import numpy 
import matplotlib.pyplot as plt
from drawnow import *   


temp1= []
temp2=[]
volt=[]
current=[]
#power=[]
#energy=[]
angle=[]
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0



def makeFig(): #Create a function that makes our desired plot

    plt.subplot(111)
    plt.ylim(-30, 30)                                 #Set angle of inclination min and max values
    plt.title('Angle of inclination')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Angle')                            #Set ylabels
    plt.plot(angle, 'm-', label='Degrees')       #plot the angle
    plt.legend(loc='upper left')                   #plot the legend
    
    plt.subplot(222)
    plt.ylim(-20, 150)                                 #Fix range for Tempertature 1
    plt.title('Temperature')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Temperature 1')                            #Set ylabels
    plt.plot(temp1, 'b-', label='°C')       #plot the temperature1
    plt.legend(loc='upper left')                   #plot the legend
    plt2=plt.twinx()                                #Create a second y axis
    plt.ylim(-20, 150)                           #Fix range for Tempertature 2
    plt2.plot(temp2, 'r-', label='°C') #plot the temperature2
    plt2.set_ylabel('Temperature 2')                    #label second y axis
    plt2.ticklabel_format(useOffset=False)           #Force matplotlib to NOT autoscale y axis
    plt.legend(loc='upper right')                  #plot the legend

    plt.subplot(223)
    plt.ylim(-10, 75)                                 #Set angle of inclination min and max values
    plt.title('Voltage')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Voltage')                            #Set ylabels
    plt.plot(volt, 'g-', label='V')       #plot the voltage
    plt.legend(loc='upper left')                   #plot the legend

    plt.subplot(224)
    plt.ylim(-10, 60)                                 #Set angle of inclination min and max values
    plt.title('Current')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Current')                            #Set ylabels
    plt.plot(current, 'c-', label='A')       #plot the current
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
            
            #print(string_data)
            updated_float_data = [float(i) for i in string_data]
            
                #power.append(updated_float_data[5]);
                #energy.append(updated_float_data[6]);
            if len(updated_float_data) == 9:
                angle.append(updated_float_data[8])
                temp1.append(updated_float_data[1])
                temp2.append(updated_float_data[2])
                volt.append(updated_float_data[3]);
                current.append(updated_float_data[4]);
                
            drawnow(makeFig)
           
            plt.pause(.05)                     #Pause Briefly. Important to keep drawnow from crashing
            cnt=cnt+1
            if(cnt>100):                            #If you have 50 or more points, delete the first one from the array
                angle.pop(0)
                temp1.pop(0)
                temp2.pop(0)
                current.pop(0)
                volt.pop(0)
                
                     
            file_writer.writerow([str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))]+updated_float_data)
            
            print(updated_float_data)
            
        else:
            print(serial_data)

    

    


