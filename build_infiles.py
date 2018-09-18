#!/usr/bin/env python3

import math
import subprocess
import primarybeam as pb

import numpy as np
from astropy import units as u
from astropy.coordinates import Angle


def get_flux_density(ref_freq,ref_flux,freq,index):
    k=ref_flux/math.pow(ref_freq,index)

    return k*math.pow(freq,index)



# 300 MHz

src1_rf = 1.0
src2_rf = 1.0
src3_rf = 1.0

src1_index = 0
src2_index = 0
src3_index = 0


reference = float(-46.0)
sources_on_a_side = 9;
# changing units to be cell size to ensure the centre of a pixel
npix = 1024
cell_size = 4 
# field size is:
full_field = npix * cell_size
#in cells
num_sources = sources_on_a_side * sources_on_a_side;


step_size_in_cells = 100

print(step_size_in_cells)

# how many cells from the centre do we start.

start = -1.0*int(sources_on_a_side/2.) * step_size_in_cells
print(start)

for pointing in range(0,2,1):

    step=1
    for x in range(1100,1420,40):
   
        
        #offset the two beams by
        
        if (pointing == 0):
            filename = "chan_%d.in" % step
            ms_name = "chan_%d.ms" % step
            field_offset = float(0)
        elif (pointing == 1):
            filename = "chan_%d" % step
            filename = filename + "a.in"
            ms_name = "chan_%d" % step
            ms_name = ms_name + "a.ms"
            field_offset = float(0.5)

        # need to generate all the sources - lets start w. 1

        g = pb.GaussianPB(12)
        fp=open(filename,"w")
    
        fp.write( "Csimulator.dataset                              = %s \n" % ms_name)
        fp.write( "Csimulator.sources.names                        =       [field1]\n")
        field_offset_in_min = field_offset * 60;




# below only works because the offset is less than 1. Careful not a general solution
        fp.write( "Csimulator.sources.field1.direction              =       [12h30m00.000, %2d.%02d.000, J2000]\n" % (int(reference+field_offset),int(field_offset_in_min)))
#        fp.write( "Csimulator.sources.field1.components             =       [src1,src2,src3]\n")

        # ten by ten source grid?
        label = "Csimulator.sources.field1.components             =       ["
        for i in range(1,num_sources+1,1):
            source_label = "src%d" % int(i)
            label = label + source_label
            if (i < num_sources):
                label = label + ","
            else:
                label = label + "]\n"
                
        fp.write(label)
        
        src_count = 1
 
        for src_x in range(0,sources_on_a_side,1):
            for src_y in range(0,sources_on_a_side,1):
                
                source_label = "src%d" % int(src_count)
                # now these are measured in cells
                ra_source_offset = (start + src_x * step_size_in_cells)*cell_size
                dec_source_offset = (start + src_y * step_size_in_cells)*cell_size - (field_offset_in_min * 60.0)
                
                
                # now lets bring in the angle class
                # print(src_x,":",src_y," ",ra_source_offset)
                
                ra_angle_offset = Angle(ra_source_offset,unit=u.arcsec)
                dec_angle_offset = Angle(dec_source_offset,unit=u.arcsec)

                
                
                fr = x*1e6
                f1 = get_flux_density(1400e6,src1_rf,fr,src1_index)
            
                # this is for the source flux so does not need the field offset

                offsetangle = math.atan2(ra_angle_offset.rad,dec_angle_offset.rad)
                # pythagoras on the sphere
                # cos dist = cos(ra)*cos(dec)
                offsetdist =  math.cos(ra_angle_offset.rad)*math.cos(dec_angle_offset.rad)
                offsetdist = math.acos(offsetdist)
                
                        
                f1 = f1*g.evaluateAtOffset(offsetangle,offsetdist,fr);
    
                fp.write( "Csimulator.sources.%s.flux.i                  = %f \n" %  (source_label,f1) )
                fp.write( "Csimulator.sources.%s.direction.ra           = %lf \n" % (source_label,ra_angle_offset.rad) )
                fp.write( "Csimulator.sources.%s.direction.dec          = %lf \n" % (source_label,dec_angle_offset.rad) )
                src_count = src_count + 1
#            
        fp.write( "# \n")
        fp.write( "# Define the antenna locations, feed locations, and spectral window definitions\n")
        fp.write( "# \n")
        fp.write( "Csimulator.antennas.definition                  =       definitions/A27CR3P6B.in\n")
        fp.write( "Csimulator.feeds.names                          = [feed0] \n")
        fp.write( "Csimulator.feeds.feed0                          = [0.0, 0.0]\n" )
        fp.write( " \n")
        fp.write( "Csimulator.spws.names                      =       [Wide0]\n")
        fp.write( "Csimulator.spws.Wide0  =[ 1, %.3fMHz, 10kHz, \"XX XY YX YY\"]\n" % x)
        fp.write( "# \n")
        fp.write( "# Standard settings for the simulaton step\n")
        fp.write( "# \n")
        fp.write( "Csimulator.simulation.blockage                  =       0.01 \n")
        fp.write( "Csimulator.simulation.elevationlimit            =       8deg\n")
        fp.write( "Csimulator.simulation.autocorrwt                =       0.0\n")
        fp.write( "Csimulator.simulation.usehourangles             =       True\n")
        fp.write( "Csimulator.simulation.referencetime             =       [2007Mar07, UTC]\n")
        fp.write( "##\n")
        fp.write( "Csimulator.simulation.integrationtime           =       10s\n")
        fp.write( "#\n")
        fp.write( "# Observe field1 for 5 minutes with a single channel spectral window\n")
        fp.write( "#\n")

        fp.write( "Csimulator.observe.number                       =       5\n")

        fp.write( "Csimulator.observe.scan0                        =       [field1, Wide0, -4.0416667h, -3.9583333h]\n")              
        fp.write( "Csimulator.observe.scan1                        =       [field1, Wide0, -3.0416667h, -2.9583333h]\n")
        
        fp.write( "Csimulator.observe.scan2                        =       [field1, Wide0, -2.0416667h, -1.9583333h]\n")
        fp.write( "Csimulator.observe.scan3                        =       [field1, Wide0, -1.0416667h, -0.9583333h]\n")
        fp.write( "Csimulator.observe.scan4                        =       [field1, Wide0, -0.0416667h, 0.0416667h]\n")
        
        fp.write( "#\n")
        fp.write( "#\n")
        fp.write( "##\n")
        fp.write( "Csimulator.gridder                                 = WProject\n")
        fp.write( "Csimulator.gridder.WProject.wmax                   = 25000\n")
        fp.write( "Csimulator.gridder.WProject.nwplanes               = 129\n")
        fp.write( "Csimulator.gridder.WProject.oversample             = 16\n")
        fp.write( "Csimulator.gridder.WProject.maxsupport             = 1024\n")

        fp.write( "# optional corruption due to calibration effect\n")
        fp.write( "Csimulator.corrupt                              = false\n")

        fp.write( "# optional noise addition\n")
        fp.write( "Csimulator.noise                                = false\n")
        if (pointing == 0): 
            fp.write("Csimulator.noise.variance = 10\n")
            fp.write("Csimulator.noise.seed1 = %d\n" % int(10+step))
            fp.write("Csimulator.noise.seed2 = %d\n" % int(100+step))
        if (pointing == 1): 
            fp.write("Csimulator.noise.variance = 10\n")
            fp.write("Csimulator.noise.seed1 = %d\n" % int(15+step))
            fp.write("Csimulator.noise.seed2 = %d\n" % int(150+step))
       


        fp.close


        step = step+1

