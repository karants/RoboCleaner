"""
Project: The Bot Project
Module: RoboCleaner Class
Course: 3PR3
Author: Karan Shah
Created: 29/3/2021
"""

#Class definition

class RoboCleaner:
    
    def __init__(self,RoboNumber,RoboName,Speed,SerialNumber,RoboColour,initialX,initialY,finalX,finalY):
        self.__RoboNumber = RoboNumber   
        self.__RoboName = RoboName
        self.__Speed = Speed
        self.__SerialNumber = SerialNumber
        self.__Colour = RoboColour
        self.__ix = initialX
        self.__iy = initialY
        self.__fx = finalX
        self.__fy = finalY
        
    def GetInitialCoordinates(self):
        return self.__ix, self.__iy
    
    def GetFinalCoordinates(self):
        return self.__fx, self.__fy
    
    def SetCoordinates(self,cx,cy):
        
        self.__cx = cx
        self.__cy = cy
        
    def GetCoordinates(self):    
        return self.__cx, self.__cy
    
    def GetSerialNumber(self):
        return self.__SerialNumber
    
    def GetSpeed(self):
        
        return self.__Speed
        
    def GetTilesOnTime(self,time):
        
        totaltiles = (self.__fy - self.__iy + 1) * self.__fx
        tilesontime = int(self.__Speed) * time
        
        if(tilesontime > totaltiles):
            tilesontime = totaltiles
        
        return tilesontime
    
    def GetTotalTiles(self):
        
        totaltiles = (self.__fy - self.__iy + 1) * self.__fx
        return totaltiles
    
    def GetTotalTime(self):
        
        totaltime = ((self.__fy - self.__iy + 1) * self.__fx) / int(self.__Speed)
        return totaltime
    
    def GetColour(self):
        return self.__Colour