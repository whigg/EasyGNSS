#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 16:39:57 2019

@author: edgar
"""

from roverModel import RoverModel
from baseModel import BaseModel
from PostProcessModel import PostProcessModel

class ConnectionToModel():
    '''
    This class is the singleton that ensures the connection of the UI part to the Model
    Attributes :
        private RoverModel roverModel 
        private BaseModel baseModel
    '''
    
    def __init__(self):
        
        self.__roverModel = None
        self.__baseModel = None
        self.__postProcessModel = None
        
    def getInstanceRover(self):
        '''
        Returns the model of the rover
        '''   
        if self.__roverModel == None: 
            self.__roverModel = RoverModel()    
        return self.__roverModel
            
    def getInstanceBase(self):
        '''
        Returns the model of the base
        '''
        
        if self.__baseModel == None:
            
            self.__baseModel = BaseModel()
        
        return self.__baseModel
    
    def getInstancePostProcess(self):
        '''
        Returns the model of the post processing
        '''
        
        if self.__postProcessModel == None:
            
            self.__postProcessModel = PostProcessModel()
        
        return self.__postProcessModel  