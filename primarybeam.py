# -*- coding: utf-8 -*-
"""

Primary beam evaluator - 

Mimic what happens in ASKAPSoft - Stephen Ord 2018

The parameters are:
    
    ApertureSize(parset.getDouble("aperture",12));      
    setExpScaling(parset.getDouble("expscaling", 4.*log(2.)));
    Xwidth(parset.getDouble("xwidth",0.0));
    Ywidth(parset.getDouble("ywidth",0.0));
    Alpha(parset.getDouble("alpha",0.0));
    Xoff(parset.getDouble("xoff",0.0));
    Yoff(parset.getDouble("yoff",0.0));


"""
import math


class GaussianPB:
    
    def __init__(self,aperture=12,expscaling=4.*math.log(2.),frequency=1.1e9):
        
        self.aperture = aperture
        self.expScaling = expscaling
        self.frequency=frequency
        self.setXwidth(self.getFWHM())
        self.setYwidth(self.getFWHM())
        self.setAlpha(0.0)
        self.setXoff(0.0)
        self.setYoff(0.0)
        
    
    def getFWHM(self):
        sol = 299792458.0;
        fwhm = sol/self.frequency/self.aperture
        return fwhm
    
    def evaluate(self,offset=0,freq=0):
        if (freq > 0):
            self.frequency=freq
            
        pb = math.exp(-offset*offset*self.expScaling/(self.getFWHM()*self.getFWHM()));
        return pb
    
    def setXwidth(self,xwidth):
        self.xwidth = xwidth
        
    def setYwidth(self,ywidth):
        self.ywidth = ywidth
        
    def setAlpha(self,Angle):
        self.Alpha = Angle
        
    def setXoff(self,xoff):
        self.xoff = xoff
        
    def setYoff(self,yoff):
        self.yoff = yoff
        
    def evaluateAtOffset(self,offsetPAngle=0, offsetDist=0, freq=0):
            
        # x-direction is assumed along the meridian in the direction of north celestial pole
        # the offsetPA angle is relative to the meridian
        # the Alpha angle is the rotation of the beam pattern relative to the meridian
        # Therefore the offset relative to the
                
        if (freq > 0):
            self.frequency=freq
            
        x_angle = offsetDist * math.cos(offsetPAngle-self.Alpha)
        y_angle = offsetDist * math.sin(offsetPAngle-self.Alpha)
                    
        x_pb = math.exp(-1*self.expScaling*math.pow((x_angle-self.xoff)/self.xwidth,2.))
        y_pb = math.exp(-1*self.expScaling*math.pow((y_angle-self.yoff)/self.ywidth,2.))

        return x_pb*y_pb

                



