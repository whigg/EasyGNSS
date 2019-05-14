#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 09:42:07 2019

@author: edgar
"""

import telnetlib
import time
from subprocess import Popen
import os
from shutil import copyfile

class RoverModel():
    '''
    RoverModel is the class that contains the model for the rover acquisition
    It communicates with rtkrcv through command line and telnet protocol
    
    Attributes :    
        private int tnport : telnet port of rtkrcv
        private Telnet tn : Telnet accessor for rtkrcv
        private path dirtrs : directory of the script
        private path dirrtk : directory to rtkrcv
        private path optfile : directory to the .conf file that will be sent to rtkrcv
        private list options : options of the acquisition
        private Popen p : command line that will be launched for the acquisition
    '''
    
    def __init__(self):
        # telnet port for rtkrcv
        self.__tnport = 1234
        self.__tn = None        
        # directory of rtkrcv
        self.__dirrtk = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/RTKLIB/2.4.3/RTKLIB/app/rtkrcv/gcc/rtkrcv'
        #directory of the script
        self.__dirtrs = os.path.dirname(os.path.abspath(__file__))   
        #directory of the configuration file
        self.__optfile = self.__dirtrs +'/conf/' + 'file.conf' 
        #RTKLIB command 
        self.__p = None
        
        
        # sets default options
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
        options.append([False, True, '', os.path.abspath(os.path.join(self.__dirtrs, os.pardir)) +'/saved_conf/'+ time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()) + '.conf']) #configuration file
        options.append(['dgps','1','0','brdc','saas','brdc','15.0']) #calculus
        options.append(['ttyACM0','115200','8','n','1','off']) #input
        options.append([False]) #correction
        options.append([True,'xyz','all', os.path.abspath(os.path.join(self.__dirtrs, os.pardir)) +'Results/Solutions/'+ time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()) + '.pos']) #solution
        options.append([True, os.path.abspath(os.path.join(self.__dirtrs, os.pardir)) +'Results/Logs/'+ time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()) + '.ubx']) #log
        options.append(['llh','48.8','2.35','35','0']) #base position
        
        return options
      
        
    ######  FUNCTIONS  #######
        
    def startRover(self):
        '''
        Starts and sets the acquisition
        '''
        print("start")
        
        #check wether we are using a brand new conf file or uploading an existing one
        if self.__options[0][0] == True :
            self.__optfile = self.__options[0][2] # change the file to the desired one
        
            
            
        #launching rtkrcv in command line
        self.__p = Popen(self.__dirrtk +' -o '+ self.__optfile +' -p '+ str(self.__tnport), shell=True)
        #pauses the process so that options are uploaded
        time.sleep(2)   
        
         #connecting to rtkrcv through telnet protocol
        self.__tn = telnetlib.Telnet('localhost',self.__tnport) 
        self.__tn.read_until(b'password: ')
        self.rtkrcvCommand('admin')
        

        
        # if we are not using an existing conf
        if self.__options[0][0] == False : 
            # if the user decided to save his conf file
            if self.__options[0][1] == True:
                self.createConf() #create the conf file
                
            # setting the options   
            self.makeCommandRover()
            
            # Receiver command
            ubxcmd = self.__dirtrs + '/conf/ubx_m8t_bds_raw_1hz.cmd'
            self.rtkrcvOption('file-cmdfile1',ubxcmd)
        
            #delteing the temporary file
            os.remove(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/saved_conf/file.conf')
            

        else:
            # Receiver command
            ubxcmd = self.__dirtrs + '/conf/ubx_m8t_bds_raw_1hz.cmd'
            self.rtkrcvOption('file-cmdfile1',ubxcmd)
        
        
        #starting the acquisition
        self.rtkrcvCommand('start')  
        
        
        
    def stopRover(self):
        '''
        Stops the acquisition
        '''
               
        self.__p.terminate()
        time.sleep(0.2)

        # shutdown
        self.__tn.write('shutdown\r\n'.encode())
        
        
        
    def getRaw(self):
        '''
        Returns the raw solutions of the GNSS
        '''
        
        rawsol = self.rtkrcvCommand2('solution')
        rawstream = self.rtkrcvCommand2('stream')
        
        return rawsol, rawstream
    
    def getSatellites(self):
        '''
        returns the avalaible satellites of the GNSS
        '''
        
        if self.__tn != None :
            satellites = self.rtkrcvCommand2('satellite')
        else:
            satellites = ''
        
        return satellites
        
    
    
    
    def createConf(self):
        '''
        copy the basic conf file to the saved_conf repository
        '''
        
        src = self.__dirtrs +'/conf/file.conf' 
        temp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/saved_conf/file.conf'
        
        copyfile(src, temp_file)
        
    
    def editConf(self, opt, val):
        '''
        edit the saved conf file with the new value
        '''

        old_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/saved_conf/file.conf'
        new_file = open(self.__options[0][3], 'w')
        old_file = open(old_file_path, 'r')
            
        # look for the option line in the file
        for line in old_file:
            if opt in line: 
                #write the line with the new value and by respecting the space
                line = opt
                for i in range(19 - len(opt)): #in case the program is sensible to length modifications
                    line += ' ' 
                line += '=' + val +'\n'
            
            new_file.write(line)
            
        new_file.close()
        old_file.close()
        
        copyfile(self.__options[0][3], old_file_path) #changing the old file so that the new feature is saved
        


    ######  RTKRCV COMMAND FUNCTIONS  ######      
    
    

    def makeCommandRover(self):
        '''
        Main command that is launched when the rover starts
        Sets options of the acquisition
        '''
        
        calculus_options = self.__options[1]    
        input_options = self.__options[2]          
        correction_options = self.__options[3] 
        sol_options = self.__options[4] 
        log_options = self.__options[5] 
        base_pose_options = self.__options[6]
        
        
        # Calculus options
        self.setCalculusOptions(calculus_options)

        # Input options
        itype=['serial']
        iformat=['ubx']
        ipath=[]
        ipath.append(self.setInputOptions(input_options))
        
        # Correction options
        ipath, itype, iformat = self.setCorrectionOptions(correction_options, ipath, itype, iformat)
              
        # Solution options
        otype, oformat, opath = self.setSolOptions(sol_options)

        # Log options
        ltype, lformat, lpath = self.setLogOptions(log_options)
        
        # Base position options
        self.setBasePosOptions(base_pose_options)
        
        # Setting Stream
        self.rtkrcvOption('pos1-posmode',calculus_options[0])
        for i,path in enumerate(ipath):
            self.rtkrcvSetStream('inpstr'+str(i+1),itype[i],iformat[i],path)
        for i,path in enumerate(opath):
            self.rtkrcvSetStream('outstr'+str(i+1),otype[i],oformat[i],path)
        for i,path in enumerate(lpath):
            self.rtkrcvSetStream('logstr'+str(i+1),ltype[i],lformat[i],path)

        
    def rtkrcvCommand(self,cmd):
        '''
        Encode and send the command to rtkrcv
        '''
        sendcmd=cmd+'\r\n'
        self.__tn.write(sendcmd.encode())


    def rtkrcvCommand2(self,cmd):
        '''
        Encode and send the command to rtkrcv to get the rawdata
        '''
        sendcmd=cmd+'\r\n'
        self.__tn.write(sendcmd.encode())
        ret=self.__tn.read_until(b'rtkrcv> ')
        return ret.decode()
    
    
    def rtkrcvOption(self,opt,val):
        '''
        Write the command to be sent to rtkrcv
        '''
        #send the option to rtkrcv 
        cmd='set '+opt+' '+val
        self.rtkrcvCommand(cmd)
        
        if self.__options[0][1] == True:
            self.editConf(opt, val)
        
        #saves the option into the conf file
        

    def rtkrcvSetStream(self,name,stype,sformat,spath):
        '''
        Prepare the command to set the streamflow of rtkrcv
        '''
        self.rtkrcvOption(name+'-type',stype)
        self.rtkrcvOption(name+'-format',sformat)
        self.rtkrcvOption(name+'-path',spath)
        
        
        
        
    ######  OPTIONS FUNCTIONS  ######
    
    def setCalculusOptions(self,options):
        '''
        Sets informations for calculus options
        '''

        self.rtkrcvOption('pos1-posmode',options[0]) # calculus mode (default : dgps)
        self.rtkrcvOption('pos1-navsys',options[1]) # satellite systems to be used
        self.rtkrcvOption('ant1-antdelu ',options[2]) # antenna height
        self.rtkrcvOption('pos1-ionoopt',options[3]) #ionospheric correction
        self.rtkrcvOption('pos1-tropopt',options[4]) #tropospheric correction
        self.rtkrcvOption('pos1-sateph',options[5]) #satellites ephemerids
        self.rtkrcvOption('pos1-elmask',options[6]) #elevation mask (deg)
        
        
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

        return cmd
        
    def setSolOptions(self,options):
        '''
        Sets informations for solution options
        '''
        
        sol_flag = options[0]
        otype=[]
        oformat=[]
        opath=[]
        
        if sol_flag == True:
            otype.append('file')
            oformat.append(options[1])  #LLH, Cartesian or plane
            self.rtkrcvOption( 'out-solstatic', options[2]) #all or single
            opath.append(options[3]) #path to file
            
        return otype, oformat, opath
    
    def setLogOptions(self, options):
        '''
        Sets informations for logs options
        '''
        
        log_flag = options[0]
        
        ltype=[]
        lformat=[]
        lpath=[]
        
        if log_flag == True:
            ltype.append('file')
            lformat.append('')
            lpath.append(options[1]) #path to file

        return ltype, lformat, lpath
    
    def setCorrectionOptions(self, options, ipath, itype, iformat):
        '''
        Sets informations for correction options
        '''
        
        corr_flag = options[0]
        cmd = ''
        
        if corr_flag == True:
            corr_type = options[1] 
            corr_format = options[2]
            itype.append(corr_type)
            iformat.append(corr_format)
        
            if corr_type == 'tcpcli':
                addr = options[7] #addresse
                port = options[5] #port
                cmd = addr+':'+port
                ipath.append(cmd)
    
            elif corr_type == 'ntripcli':
                user= options[3] #user
                pw  = options[4] #password
                port= options[5] #port
                mp  = options[6] #mountpoint
                addr= options[7] #addresse
                cmd = user+':'+pw+'@'+addr+':'+port+'/'+mp
                ipath.append(cmd)
            
        return ipath, itype, iformat
    
    
    def setBasePosOptions(self, options):
        '''
        Sets informations for base position options
        '''

        self.rtkrcvOption('ant2-postype',options[0]) # manual(llh) or radio transmitted
        
        if options[0] == 'rtcm':           
            self.rtkrcvOption('ant2-pos1', '') #latitude
            self.rtkrcvOption('ant2-pos2', '') #longitude
            self.rtkrcvOption('ant2-pos3', '') #height
            self.rtkrcvOption('ant2-antdelu', '') #antenna height
            
        else:           
            self.rtkrcvOption('ant2-pos1',options[1]) #latitude
            self.rtkrcvOption('ant2-pos2',options[2]) #longitude
            self.rtkrcvOption('ant2-pos3',options[3]) #height
            self.rtkrcvOption('ant2-antdelu',options[4]) #antenna height
            

        
