#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:12:09 2019

@author: nassim
"""

import ftplib as f #library used to interact with a ftp server
import os #library used to interact with the operating system
import requests as r #library used to do Internet requests
#import vincenty as v #library used to compute distance with geographic coordinates
import numpy as np
import glob
import datetime
import vincenty as v

deg2rad = np.pi / 180
rad2deg = 1 / deg2rad

class PostProcessModel:
    '''
    '''
    
    def __init__(self):
        
        self.__confpath = None
        self.__ubxpath = None
        self.__pospath = None
        self.__mode = 'static'
        self.__output_format = 'xyz'
        self.__nb_station = '3'
        self.__dist_max = '100'
        
    
    def setOptions(self, confpath, ubxpath, pospath, mode, output_format, nb_station, dist_max):
        '''
        Sets the options after parameters have been saved in config window
        '''
        
        self.__confpath = confpath
        self.__ubxpath = ubxpath
        self.__pospath = pospath
        self.__mode = mode
        self.__output_format = output_format
        self.__nb_station = nb_station
        self.__dist_max = dist_max
        
        
    def start(self):
        '''
        '''
        self.editConf()
        self.launchPostProcessing(self.__confpath, self.__nb_station, self.__dist_max)
        os.remove(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/saved_conf/file.conf')
    
    def editConf(self):
        '''
        create and edit the a new temporary conf file from the selected conf file 
        this new conf file will be used for the postprocessing
        '''

        temp_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/saved_conf/file.conf'
        temp_file = open(temp_file_path, 'w')
        file = open(self.__confpath, 'r')

            
        # look for the options line in the file
        for line in file:
            opt1 = 'pos1-posmode'
            opt2 = 'out-solformat'
            if opt1 in line: 
                #write the line with the new value and by respecting the space
                line = opt1
                for i in range(19 - len(opt1)): #in case the program is sensible to length modifications
                    line += ' ' 
                line += '=' + self.__mode +'\n'
                
            if opt2 in line:
                #write the line with the new value and by respecting the space
                line = opt2
                for i in range(19 - len(opt2)): #in case the program is sensible to length modifications
                    line += ' ' 
                line += '=' + self.__output_format +'\n'
                
         
            temp_file.write(line)
            
        temp_file.close()
        file.close()
        self.__confpath = temp_file_path #this conf file will be used from now  

          
    
    
    def launchCONVBINCommand(self, ubxFile, posFile):
        """
        Is used to launch a CONVBIN command-line to convert from a .ubx file to rinex files.
        
        The rinex files are created in the directory called rinex. They have the same name as the 
        .ubx file but with a different extensions (.obs, .nav, ...). See RTKlib documentation for
        further information.
        
        Parameters:
            Mandatory:
                ubxFile (str): path of the .ubx file
                posFile (str): path of the positionning file processed with RTKRCV
                
        Return:
            lat (float): latitude of the receiver
            lng (float): longitude of the receiver
            h (float): height above the WGS84 ellipsoid of the receiver  
        """
        file = open(posFile, "r") #opening the position file
        lines = file.readlines() #retrieving all the lines
        file.close()
        cpt = 0 #number of commentary lines
        for line in lines:
            if line[0] == "%": #commentary line
                cpt += 1
        
        file = open(self.__confpath, "r") #opening the conf file
        for line in file:
            if "ant1-antdelu" in line:
                line = line.split()
                line = line[1].replace('=','')
                hAnt = float(line) #height of the antenna in relation to the ground 
        file.close()
                
        data = np.genfromtxt(posFile, skip_header=cpt) #creating a numpy array
        
        line = lines[cpt - 1] #retrieving the last commentary line
        if data.size == data.shape[0]: #one position line
            if "x-ecef(m)" in line: #cartesian coordinates
                x = data[2]
                y = data[3]
                z = data[4]
                lng, lat, h = self.cartesian2geographic(x, y, z)
            else: #geographic coordinates
                lat = data[2]
                lng = data[3]
                h = data[4]
                x, y, z = self.geographic2cartesian(lat, lng, h)
        else: #many position lines
            if "x-ecef(m)" in line: #cartesian coordinates
                x = data[0, 2]
                y = data[0, 3]
                z = data[0, 4]
                lng, lat, h = self.cartesian2geographic(x, y, z)
            else: #geographic coordinates
                lat = data[0, 2]
                lng = data[0, 3]
                h = data[0, 4]
                x, y, z = self.geographic2cartesian(lat, lng, h)
                

        #launch command-line
        os.system("../RTKLIB/2.4.3/RTKLIB/app/convbin/gcc/convbin -hp " + str(x) + "/" + str(y) + "/" + str(z) + " -hd " + str(hAnt) + "/0/0 -d ../rinex " + ubxFile)
        
        return lat, lng, h
        

    def launchRNX2RTKPCommand(self, confFile, outFile, roverObsFile, baseObsFile, lst_navFile, orbitesFile):
        """
        Is used to launch a RNX2RTKP command-line to do post-processing.
        
        Parameters:
            Mandatory:
                confFile (str): path of a RTKlib configuration file
                outFile (str): path of the out file where the solution will be saved
                roverObsFile (str): path of the rover observation file
                baseObsFile (str): path of the base observation file
                lst_navFile (list): list of paths of navigation files
                orbitesFile (str): path of an orbites file 
        """
        cmd = "../RTKLIB/2.4.2/RTKLIB/app/rnx2rtkp/gcc/rnx2rtkp -k " + confFile + " -o " + outFile + " " + roverObsFile + " " + baseObsFile + " "

        for navFile in lst_navFile:
            cmd += navFile + " "
        cmd += orbitesFile
        
        os.system(cmd) #command-line to do post-processing
    
    
    def downloadFTP(self, server, path, toDownload, downloadPath, username="anonymous", password=""):
        """
        Is used to download a file from a ftp server. Assumes that the receiver is connected to the Internet.
        
        Parameters:
            Mandatory:
                server (str): name of the ftp server
                path (str): path of the directory where the file is
                toDownload (str): name of the file to download
                downloadPath (str) : path of the directory where the file will be downloaded 
            Optional:
                username (str): name of the user (by default 'anonymous')
                password (str): password of the user (by default '')
                
        Return:
            status (int): -1 if the downloading has failed, 0 if not
        """
        ftp = f.FTP(server) #connection to the ftp server
        log = ftp.login(username, password) #login to the ftp server
        
        if log == "230 Login successful.": # access accepted
            ftp.cwd(path) #navigate to the file's directory
            localFile = open(downloadPath + toDownload, "wb") #open the file where the result will be written in binary mode
            files = ftp.nlst() #retrieve files in the download directory
            if toDownload in files: #if the file to download exists
                ftp.retrbinary("RETR " + toDownload, localFile.write) #download the file 
                print("File downloaded")
                status = 0
            else:
                print("This file does not exist")
                status = -1
            
        else: #access denied
            print("Access denied")
            status = -1
            
        return status
    
    
    def downloadFTPIGN(self, path, toDownload, downloadPath):
        """
        Is used to download a file from the IGN ftp server. Assumes that the receiver is connected to the Internet.
        
        Parameters:
            Mandatory:
                path (str): path of the directory where the file is
                toDownload (str): name of the file to download
                downloadPath (str) : path of the directory where the file will be downloaded
                
        Return:
            status (int): -1 if the downloading has failed, 0 if not
        """
        return self.downloadFTP("rgpdata.ign.fr", path, toDownload, downloadPath)
    


    def downloadFTPIGS(self, path, toDownload, downloadPath):
        """
        Is used to download a file from the IGS ftp server. Assumes that the receiver is connected to the Internet.
        
        Parameters:
            Mandatory:
                path (str): path of the directory where the file is
                toDownload (str): name of the file to download
                downloadPath (str) : path of the directory where the file will be downloaded
                
        Return:
            status (int): -1 if the downloading has failed, 0 if not
        """
        return self.downloadFTP("igs.ensg.ign.fr", path, toDownload, downloadPath)  
    
    
    def downloadCoord(self, url, toDownload, downloadPath):
        """
        Is used to download a coordinates' file of permanent GNSS stations. Assumes that the receiver is connected to the Internet.
        
        Parameters:
            Mandatory:
                url (str): downloading link
                toDownload (str): name of the file to download
                downloadPath (str) : path of the directory where the file will be downloaded
                
        Return:
            status (int): -1 if the downloading has failed, 0 if not
        """
        request = r.get(url) #request to do the downloading
        file = open(downloadPath + toDownload, "w") #file where the file will be downloaded
        file.write(request.text)
        file.close()
    
    
    def uncompress(self, Zfile):
        """
        Is used to uncompress a .Z file.
        
        Parameters:
            Mandatory:
                Zfile (str): name of the .Z file to uncompress
        """
        os.system("uncompress " + Zfile) #command-line to process the uncompression
        
      
    def uncompressHatanaka(self, dFile):
        """
        Is used to uncompress a .d file with the Hatanaka method.
        
        Parameters:
            Mandatory:
                dfile (str): name of the .d file to uncompress
        """
        os.system("../lib/CRX2RNX " + dFile) #command-line to process the uncompression with CRX2RNX
        
        
    def delete(self, file):
        """
        Is used to delete a file.
        
        Parameters:
            Mandatory:
                file (str): name of the file to delete
        """
        os.system("rm " + file) #command-line to delete the file
        
        
    
    def distance(self, receiverLng, receiverLat, stationLng, stationLat):
        """
        Is used to compute distance with geographic coordinates with Vincenty method.
        
        Parameters:
            Mandatory:
                receiverLng (float): longitude of the receiver (at decimal degree format)
                receiverLat (float): latitude of the receiver (at decimal degree format)
                stationLng (float): longitude of the station (at decimal degree format)
                stationLat (float): latitude of the station (at decimal degree format)
                
        Return:
            dist (float): distance between the receiver and the station
        """
        dist = v.vincenty((receiverLat, receiverLng), (stationLat, stationLng)) 
        return dist
    
    
    def nearestStationsDMS(self, receiverLng, receiverLat, coord, idLat, idLng, header, footer):
        """
        Is used to find the nearest permanent GNSS stations with coordinates at dd.mmsssssss format.
        
        Parameters:
            Mandatory:
                receiverLng (float): longitude of the receiver (at dd format)
                receiverLat (float): latitude of the receiver (at dd format)
                coord (str): path of the file with the coordinates of the permanent GNSS stations
                idLat (int): number of column where latitude is in the coordinates file
                idLng (int): number of column where longitude is in the coordinates file
                header (int): number of lines to skip in the header
                footer (int): number of lines to skip in the footer
            
        Return:
            noun (list): noun of the nearest stations
            dist (list): distance between the receiver and the nearest stations (in kilometers)
        """
        listStations = np.genfromtxt(coord, dtype=np.str, skip_header=header, skip_footer=footer)
        lat = listStations[:, idLat]
        lng = listStations[:, idLng]
        nbStations = listStations.shape[0]
        lst_dist = []
        noun = []
        dist = []
        
        for i in range(nbStations):
            lst_dist.append(self.distance(receiverLng, receiverLat, self.dms2dd(float(lng[i])), self.dms2dd(float(lat[i]))))
        
        index = np.argsort(lst_dist)
        
        for i in range(nbStations):
            noun.append(listStations[index[i], 0])
            dist.append(lst_dist[index[i]])
            
        return noun, dist
    
    
    def dms2dd(self, dms):
        """
        Is used to convert from dd.mmssssss format to dd format.
        
        Parameters:
            Mandatory:
                dms (float): angle at dd.mmssssss format
            
        Return:
            ret (float): angle at dd format
        """
        symbol = 1.0
        if dms < 0:
            symbol = -1.0
            
        dms = abs(dms)
        
        dd = np.floor(dms)
        mm = np.floor(100 * (dms - dd))
        ss = 10000 * (dms - dd - 0.01 * mm)
        ret = symbol * (dd + mm/60 + ss/3600)
        
        return ret
    
    
    def geographic2cartesian(self, lat, lng, h):
        """
        Is used to go from geographic coordinates in WGS84 to cartesian coordinates in WGS84.
        Parameters:
            Mandatory:
                lat (float): latitude 
                lng (float): longitude
                h (float): height above the WGS84 ellipsoid
                
        Return:
            X (float): X coordinate
            Y (float): Y coordinate
            Z (float): Z coordinate
        """
        a = 6378137 #semi-major axis of the WGS84 ellipsoid
        f = 1 / 298.257223563 #flattening 
        b = a - a*f #minor semi-axis
        e2 = (a*a - b*b) / (a*a) # exentricity
        
        lat *= deg2rad #from degree to radian
        lng *= deg2rad
        
        w = np.sqrt( 1 - e2 * np.sin(lat) ** 2 ) #temporary values
        N = a / w 
        
        X = (N + h) * np.cos(lng) * np.cos(lat)
        Y = (N + h) * np.sin(lng) * np.cos(lat)
        Z = (N * (1-e2) + h) * np.sin(lat)
        
        return X, Y, Z
    
    
    def cartesian2geographic(self, X, Y, Z):
        """
        Is used to go from cartesian coordinates in WGS84 to geographic coordinates in WGS84.
        Parameters:
            Mandatory:
                X (float): X coordinate
                Y (float): Y coordinate
                Z (float): Z coordinate        
                
        Return:
            lat (float): latitude 
            lng (float): longitude
            h (float): height above the WGS84 ellipsoid        
        """
        a = 6378137 #semi-major axis of the WGS84 ellipsoid
        f = 1 / 298.257223563 #flattening 
        b = a - a*f #minor semi-axis
        e2 = (a*a - b*b) / (a*a) #exentricity
        
        r = np.sqrt(X**2 + Y**2 + Z**2) #temporary values
        mu = np.arctan(Z * (1-f + a*e2/r) / np.sqrt(X**2 + Y**2))

        lng = np.arctan(Y/X)
        lat = np.arctan((Z*(1-f) + e2*a*np.sin(mu)**3) / ((1-f)*(np.sqrt(X**2 + Y**2) - e2*a*np.cos(mu)**3)))
        h = np.sqrt(X**2 + Y**2) * np.cos(lat) + Z*np.sin(lat) - a*np.sqrt(1 - e2*np.sin(lat)**2)
    
        return lng*rad2deg, lat*rad2deg, h
    
    
    def launchPostProcessing(self, confFile, stat_max, dist_max):
        """
        Is used to launch the post-processing.
        
        Parameters:
            Mandatory:
                confFile (str): path of the configuration file used for the post-processing
                stat_max (int): maximum number of stations used for the post-processing 
                dist_max (int): maximum distance between the receiver and the stations used for the post-processing
        """
        #retrieving .ubx file
        last_ubxFile = self.__ubxpath

        #retrieving .pos file
        last_posFile = self.__pospath  
        
        #converting from .ubx file to rinex files
        lat, lng, h = self.launchCONVBINCommand(last_ubxFile, last_posFile)

        
        #downloading coordinates of the RGP stations
        self.downloadCoord("http://rgp.ign.fr/STATIONS/coordRGP.php", "coordRGP.txt", "../download/")
        
        #retrieving the nearest stations
        stat_noun, stat_dist = self.nearestStationsDMS(lng, lat, "../download/coordRGP.txt", 4, 5, 31, 3)

        #keeping the maximum number of stations
        stat_noun = stat_noun[:stat_max]
        stat_dist = stat_dist[:stat_max]
        
        #keeping the stations at a distance lower than the maximum distance
        new_stat_noun = []
        new_stat_dist = []
        for i in range(len(stat_noun)):
            if stat_dist[i] <= dist_max:
                new_stat_noun.append(stat_noun[i])
                new_stat_dist.append(stat_dist[i])
        stat_noun = new_stat_noun
        stat_dist = new_stat_dist

        #retrieving the date of the last acquisition
        dateTime = last_ubxFile[-23:-4]
        lst_dateTime = dateTime.split("_")
        
        date = lst_dateTime[0]
        lst_date = date.split("-")
        year = int(lst_date[0]) 
        mounth = int(lst_date[1])
        day = int(lst_date[2])

        DATE = datetime.datetime(year, mounth, day)
        dateTuple = DATE.timetuple()
        yDay = dateTuple.tm_yday #number of day in the year
        
        
#        #retrieving rover obs file       
        name = os.path.basename(self.__ubxpath)
        name = os.path.splitext(name)

        rover_file = "../rinex/" + name[0] + ".obs"

#       retrieving rover navigation files 
        lst_navFile = []
        list_files = glob.glob("../rinex/*" )
        for i in range(len(list_files)):
            if os.path.splitext(list_files[i])[-1] != ".obs" :
                lst_navFile.append(list_files[i])
        print(lst_navFile)

        
        
        #reading rover obs file
        file = open(rover_file, "r")
        lines = file.readlines()
        file.close()
        for line in lines:
            if  "TIME OF LAST OBS" in line:
                hour_end = int(line[22:24])
            elif  "TIME OF FIRST OBS" in line:
                hour_start = int(line[22:24])
       
        if len(str(yDay)) == 1:
            yDay = "00" + str(yDay)
        elif len(str(yDay)) == 2:
            yDay = "0" + str(yDay)
        else:
            yDay = str(yDay)
        path = "pub/data/" + str(year) + "/" + yDay + "/data_1" #downloading path

        
        
        
        #downloading observation files of the choosen RGP stations
        for station in stat_noun:    
            lstRinex = []
            for hour in range(hour_start, hour_end + 1): #each hour of the acquisition
              toDownload = station.lower() + str(yDay) + chr(hour + 97) + "." + str(year)[2:4] + "d.Z" #file to download
              print(toDownload)
              status = self.downloadFTPIGN(path, toDownload, "../download/") #status of the downloading
              if status == 0: #succesful downloading
                  self.uncompress("../download/" + toDownload)
                  self.uncompressHatanaka("../download/" + toDownload[:-2])
                  
                  lstRinex.append("../download/" + toDownload[:-3] + "o")
                  self.delete("../download/" + toDownload[:-2])
              else: #unsuccesful downloading
                  self.delete("../download/" + toDownload)
                
            if len(lstRinex) != 0: #rinex files downloaded
                newRinex = self.concatenateRinex(lstRinex, dateTime)
                self.launchRNX2RTKPCommand(confFile, "../post_processing/" + dateTime + "_postProcessing_" + station.lower() + ".pos", rover_file, newRinex, lst_navFile, "")

    def concatenateRinex(self, lstRinex, dateTime):
        """
        Is used to concatenate hourly rinex files of the same station. The header of the first rinex file will be kept.
        
        Parameters:
            Mandatory:
                lstRinex (list): list of paths of rinex files to concatenate
                dateTime (str): date and time of the acquisition at the format yyyy-mm-dd_hh-mm-ss 
        """
        firstRinex = lstRinex[0] 
        lstRinex.pop(0)
        firstFile = open(firstRinex, "r")
        firstLines = firstFile.readlines()
        firstFile.close()
        self.delete(firstRinex)
        
        newRinex = firstRinex[:-5] + "_" + dateTime + "." + dateTime[2:4] + "o"
        newFile = open(newRinex, "w")
        newFile.writelines(firstLines)
        
        lstLines = []
        
        for rinex in lstRinex:
            file = open(rinex, "r")
            lines = file.readlines()
            file.close()
            self.delete(rinex)
            #deleting header lines
            while "END OF HEADER" not in lines[0]:
                lines.pop(0)
            lines.pop(0)
            lstLines.append(lines)
        
        for lines in lstLines:
                newFile.writelines(lines)
                
        newFile.close()
            
        return newRinex
        
        

