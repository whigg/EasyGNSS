#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:12:09 2019

@author: pc-apple
"""

import ftplib as f #library used to interact with a ftp server
import os #library used to interact with the operating system
import requests as r #library used to do Internet requests
#import vincenty as v #library used to compute distance with geographic coordinates
import numpy as np

deg2rad = np.pi / 180
rad2deg = 1 / deg2rad

class PostProcessModel:
    
    """
    Is used to launch a CONVBIN command-line to convert from a .ubx file to rinex files.
    
    The rinex files are created in the directory called rinex. They have the same name as the 
    .ubx file but with a different extensions (.obs, .nav, ...). See RTKlib documentation for
    further information.
    
    Parameters:
        Mandatory:
            ubxFile (str): path of the .ubx file
            posFile (str): path of the last positionning file processed with RTKRCV
            hAnt (float): height of the antenna in relation to the ground
            toDownload (str): name of the file to download
    """
    def launchCONVBINCommand(self, ubxFile, posFile, hAnt):
        file = open(posFile, "r") #opening the position file
        lines = file.readlines() #retrieving all the lines
        file.close()
        cpt = 0 #number of commentary lines
        for line in lines:
            if line[0] == "%": #commentary line
                cpt += 1
        data = np.genfromtxt(posFile, skip_header=cpt) #creating a numpy array
        
        line = lines[cpt - 1] #retrieving the last commentary line
        if data.size == data.shape[0]: #one position line
            if "x-ecef(m)" in line: #cartesian coordinates
                x = data[2]
                y = data[3]
                z = data[4]
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
            else: #geographic coordinates
                lat = data[0, 2]
                lng = data[0, 3]
                h = data[0, 4]
                x, y, z = self.geographic2cartesian(lat, lng, h)
        
        #launch command-line
        os.system("convbin -hp " + str(x) + "/" + str(y) + "/" + str(z) + " -hd " + str(hAnt) + "/0/0 -d ../rinex ../ubx/" + ubxFile)
        

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
    def launchRNX2RTKPCommand(self, confFile, outFile, roverObsFile, baseObsFile, lst_navFile, orbitesFile):
        cmd = "rnx2rtkp -k " + confFile + " -o " + outFile + " " + roverObsFile + " " + baseObsFile + " "
        for navFile in lst_navFile:
            cmd += navFile + " "
        cmd += orbitesFile
        
        os.system(cmd) #command-line to do post-processing
    
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
    def downloadFTP(self, server, path, toDownload, downloadPath, username="anonymous", password=""):
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
    def downloadFTPIGN(self, path, toDownload, downloadPath):
        return self.downloadFTP("rgpdata.ign.fr", path, toDownload, downloadPath)
    

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
    def downloadFTPIGS(self, path, toDownload, downloadPath):
        return self.downloadFTP("igs.ensg.ign.fr", path, toDownload, downloadPath)  
    
    
    
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
    def downloadCoord(self, url, toDownload, downloadPath):
        request = r.get(url) #request to do the downloading
        file = open(downloadPath + toDownload, "w") #file where the file will be downloaded
        file.write(request.text)
        file.close()
    
    
    """
    Is used to uncompress a .Z file.
    
    Parameters:
        Mandatory:
            Zfile (str): name of the .Z file to uncompress
    """
    def uncompress(self, Zfile):
        os.system("uncompress " + Zfile) #command-line to process the uncompression
        
      
    """
    Is used to uncompress a .d file with the Hatanaka method.
    
    Parameters:
        Mandatory:
            dfile (str): name of the .d file to uncompress
    """
    def uncompressHatanaka(self, dFile):
        os.system("../lib/CRX2RNX " + dFile) #command-line to process the uncompression with CRX2RNX
        
        
    """
    Is used to compute distance with geographic coordinates with Vincenty method.
    
    Parameters:
        Mandatory:
            receiverLng (float): longitude of the receiver (at dd format)
            receiverLat (float): latitude of the receiver (at dd format)
            stationLng (float): longitude of the station (at dd format)
            stationLat (float): latitude of the station (at dd format)
            
    Return:
        dist (float): distance between the receiver and the station
    """
    def distance(self, receiverLng, receiverLat, stationLng, stationLat):
        dist = v.vincenty((receiverLat, receiverLng), (stationLat, stationLng))
        return dist
    
    
    """
    Is used to find the nearest permanent GNSS stations with coordinates at dd.mmsssssss format.
    
    Parameters:
        Mandatory:
            receiverLng (float): longitude of the receiver (at dd format)
            receiverLat (float): latitude of the receiver (at dd format)
            nbLim (int): number of stations that want
            coord (str): path of the file with the coordinates of the permanent GNSS stations
            idLat (int): number of column where latitude is in the coordinates file
            idLng (int): number of column where longitude is in the coordinates file
            header (int): number of lines to skip in the header
            footer (int): number of lines to skip in the footer
        
    Return:
        noun (list): noun of the nearest stations
        dist (list): distance between the receiver and the nearest stations (in meters)
    """
    def nearestStationsDMS(self, receiverLng, receiverLat, nbLim, coord, idLat, idLng, header, footer):
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
        
        for i in range(nbLim):
            noun.append(listStations[index[i], 0])
            dist.append(lst_dist[index[i]] * 1000)
            
        return noun, dist
    
    
    """
    Is used to convert from dd.mmssssss format to dd format.
    
    Parameters:
        Mandatory:
            dms (float): angle at dd.mmssssss format
        
    Return:
        ret (float): angle at dd format
    """
    def dms2dd(self, dms):
        symbol = 1.0
        if dms < 0:
            symbol = -1.0
            
        dms = abs(dms)
        
        dd = np.floor(dms)
        mm = np.floor(100 * (dms - dd))
        ss = 10000 * (dms - dd - 0.01 * mm)
        ret = symbol * (dd + mm/60 + ss/3600)
        
        return ret
    
    
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
    def geographic2cartesian(self, lat, lng, h):
        a = 6378137 #semi-major axis of the WGS84 ellipsoid
        f = 1 / 298.257223563 #flattening 
        b = a - a*f #minor semi-axis
        e2 = (a*a - b*b) / (a*a) # exentricity
        
        lat *= deg2rad #from degree to radian
        lng *= deg2rad
        
        w = np.sqrt( 1 - e2 * np.sin(lat) ** 2 ) 
        N = a / w 
        
        X = (N + h) * np.cos(lng) * np.cos(lat)
        Y = (N + h) * np.sin(lng) * np.cos(lat)
        Z = (N * (1-e2) + h) * np.sin(lat)
        
        return X, Y, Z
        
if __name__ == "__main__":
    postPross = PostProcessModel()
    path = "pub/data/2019/093/data_1"
    toDownload = "agds093p.19d.Z"
    downloadPath = "../download/"
    
#    postPross.downloadFTPIGN(path, toDownload, downloadPath)
#    postPross.uncompress(downloadPath + toDownload)
#    postPross.uncompressHatanaka(downloadPath + "agds093p.19d")
    #postPross.downloadCoord("http://rgp.ign.fr/STATIONS/coordRGP.php", "coordRGP.txt", "../download/")
    #print(postPross.distance(0, 0, 90,0))
    #print(postPross.nearestStationsDMS(2.5872222222222225, 48.840833333333336, 10, "../download/coordRGP.txt", 4, 5, 31, 3))
    #postPross.launchCONVBINCommand("2019-0217-230342.ubx", "../pos/P1_RGP1.pos", 1)
    #postPross.launchCONVBINCommand("2019-0217-230342.ubx", "../pos/mobile.pos", 1)
    
    #postPross.downloadFTPIGS("pub/igs/products/2049/", "igv20491_00.sp3.Z", "../download/")
    
    #postPross.launchRNX2RTKPCommand("../conf/test.conf", "../post_processing/test.pos", "../rinex/mobile.o", "../rinex/ct10069z.17o", ["../rinex/ct10069z.17n"], "../download/igs19395.sp3")