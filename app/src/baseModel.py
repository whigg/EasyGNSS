#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 11:59:27 2019

@author: edgar
"""

import shlex
import time
from subprocess import Popen, PIPE
import os

class BaseModel():
    '''
    BaseModel is the class that contains the model for the base acquisition
    It communicates with rtkrcv through command line and telnet protocol
    
    Attributes :    
        private int tnport 
        private Telnet tn
        private path dirtrs
        private list options
    '''
    
    def __init__(self):
        

        # directory of rtk str2str
        self.__dirrtk = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/RTKLIB/2.4.3/RTKLIB/app/str2str/gcc/str2str'       
        #directory of the script
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))         
        #RTKLIB command 
        self.__p = None
        # Setting default values
        self.__options = self.setDefaultOptions() 
        
        

        
    def setOptions(self, options):
        '''
        Setter of options attribute
        '''
        self.__options = options

        
    def setDefaultOptions(self):
        '''
        Sets the options attribute to its default value
        '''
        options = []
        options.append(['48','2.35','35','0']) #basepos
        options.append([True, os.path.abspath(os.path.join(self.__dirtrs, os.pardir)) + '/Results/Logs/'+ time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()) + '.ubx']) #log
        options.append(['ttyACM0','115200','8','n','1','off']) #input
        options.append([False]) #output1
        options.append([False,'ubx','ttyUSB0','115200','8','n','1','off'])  #output2      
        
        return options
    
    
    ###### FUNCTIONS #######
    
    
    def startBase(self):
        '''
        Starts and sets the acquisition
        '''
        #directory to the ubx (radio) file
        ubxcmd = self.__dirtrs+'/conf/ubx_m8t_bds_raw_1hz.cmd'
        rcvcmd =' -c '+ ubxcmd
        # base position transmission
        llhcmd =' -p '+ self.__options[0][0] +' '+ self.__options[0][1] +' '+ self.__options[0][2]
        rtcmcmd=' -msg 1006(10),1004,1019'

        # options of the acquisition
        opt = self.makeCommandBase()
        print(opt)
        cmd = shlex.split(self.__dirrtk + opt + rcvcmd + llhcmd + rtcmcmd)
        print('go')
        self.__p = Popen(cmd, stdin=PIPE, stderr=PIPE, bufsize=0)
        print('ok')
    
    def stopBase(self):
        '''
        Stops the acquisition
        '''
        
        self.__p.stderr.close()       
        self.__p.terminate()
    
    
    def makeCommandBase(self):
        '''
        Main command that is launched when the base starts
        Sets options of the acquisition
        '''
        cmd = self.setInputOptions(self.__options[2])       
        cmd += self.setLogOptions(self.__options[1])
        cmd += self.setOutputOptions(self.__options[3])
        cmd += self.setOutput2Options(self.__options[4])               
        return cmd
    
    
    def getRaw(self):
        '''
        Returns the raw solutions of the GNSS
        '''
        rawstream = self.__p.stderr.readline().decode('utf-8')
        return rawstream
    
    
    ######  OPTIONS FUNCTIONS  ######
    
    def setInputOptions(self,options):
        '''
        Write command for input options
        '''
               
        port    = options[0]
        bitrate = options[1]
        byte = options[2]
        parity = options[3]
        stopb = options[4]
        flwctr = options[5]
        cmd = port+':'+bitrate+':'+byte+':'+parity+':'+stopb+':'+flwctr
        
        cmd=' -in serial://'+cmd+'#ubx' #specification for str2str
        
        return cmd
    
    
    def setLogOptions(self, options):
        '''
        Sets informations for logs options
        '''
        
        log_flag = options[0]
        
        
        if log_flag == True:
            file = options[1]
            cmd=' -out file://'+ file
          
        else:
            cmd =''
            
        return cmd
    
    def setOutputOptions(self, options):
        '''
        Sets informations for output options
        '''

        output_flag = options[0]     

        if output_flag == True:
            
            output_type = options[1]
            output_format = options[2]
            user = options[3]
            addr = options[4]
            port = options[5]
            pw = options[6]
            mp = options[7]
            
            #type conversion
            if output_type == 'tcpcli':
                cmd = ' -out tcpsvr://:'+addr+':'+port   
                
            elif output_type == 'ntripcli':
                cmd = ' -out ntrips://:'+user+':'+pw+'@'+addr+':'+port+'/'+mp  
            
            if output_format == 'rtcm3':
                cmd=cmd+'#'+output_format
            
        else:
            cmd = ''
        
        return cmd
    
    def setOutput2Options(self, options):
        '''
        Sets informations for output2 options
        '''
        
        output2_flag = options[0]
        
        
        if output2_flag == True:
            
            output2_format = options[1]
            port    = options[2]
            bitrate = options[3]
            byte = options[4]
            parity = options[5]
            stopb = options[6]
            flwctr = options[7]
                
            cmd = ' -out serial://'+port+':'+bitrate+':'+byte+':'+parity+':'+stopb+':'+flwctr
            
            if output2_format == 'rtcm3':
                cmd=cmd+'#'+output2_format
            
        else:
            cmd = ''
        
        return cmd