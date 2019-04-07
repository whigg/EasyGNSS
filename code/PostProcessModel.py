#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:12:09 2019

@author: pc-apple
"""

import ftplib as f #library used to interact with a ftp server
import os #library used to interact with the operating system

class PostProcessModel:
    
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
        os.system("./CRX2RNX " + dFile) #command-line to process the uncompression with CRX2RNX
        
        
if __name__ == "__main__":
    postPross = PostProcessModel()
    path = "pub/data/2019/093/data_1"
    toDownload = "agds093p.19d.Z"
    downloadPath = ""
    #postPross.downloadFTPIGN(path, toDownload, downloadPath)
    
    #postPross.uncompress(toDownload)
    postPross.uncompressHatanaka("agds093p.19d")
    