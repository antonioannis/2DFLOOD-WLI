#-----------------------------------------------------
# 2DFLOOD-WLI.py
# Water Levels Interpolator from FLO-2D Water surface elevation
# It interpolates the Water Surface Elevation (WSE) results from FLO-2D
# using an higher resolution DTM compared to the  resolution of the hydraulic model
# --
# 1st release: 23/09/2014
# Author: Antonio Annis
#-----------------------------------------------------

#Import system modules
from __future__ import division
import sys, string, os, arcpy, math, traceback, glob
from arcpy.sa import *

# Allow output to overwrite...
arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")


try:
    
    #INPUTS----------------------------------------------------------------------------------

    NAME= arcpy.GetParameterAsText(0)          #Short name of the basin/channel whathever you want (3-4 letters maximum)
    WS = arcpy.GetParameterAsText(1)           #Shape of Water Sutrface from FLO-2D
    CELL = arcpy.GetParameterAsText(2)         #Buffer for the Water level interpolation in meters
    DEM = arcpy.GetParameterAsText(3)          #DEM at higher resolution
    PATH= arcpy.GetParameterAsText(4)          #Output path

    #OUTPUTS----------------------------------------------------------------------------------

    BUFF = PATH + "\\ws_buffer.shp"            #buffer of the Water surface shape
    WSPOINTS = PATH + "\\WS_Points.shp"        #Centroids of the water surface elevation cells
    KRIG =    PATH + "\\krig"                  #water surface raster resulted from kriging
    DIFF    = PATH + "\\diff"                  #raster fo the WSE minus DEM
    FLDEP   = PATH + "\\"+ NAME + "_fldp"      #raster of flow depths
    FLDEPSHP = PATH + "\\"+ NAME + "_fldp.shp" #Shapefile of flow dept
    EXT=  PATH + "\\ext"                       #Extension of the calculation
    AUX= PATH + "\\aux1"                       #auxiliar matrix
 

    #PRELIMIARY OPERATIONS---------------------------------------------------------------------
    
    #get the cellsize of DEM grid
    pixelsize = float(arcpy.GetRasterProperties_management (DEM, "CELLSIZEX").getOutput(0) )
    #Calculating the area of the cell
    cell_area = pixelsize * pixelsize
    #Setting the size of the enviroment 
    arcpy.env.cellSize = pixelsize

    CELL_FLO = float(CELL)

    
    #FLOW DEPTH CALCULATION--------------------------------------------------------------------
    
    #Determining the extension of the calculation
    arcpy.Buffer_analysis(WS,BUFF,  CELL_FLO, "FULL")            #Buffer of the WSE
    arcpy.FeatureToRaster_conversion(BUFF, "Var", EXT, CELL_FLO) #Rasterization of the buffer as coputational domain
    arcpy.env.extent= EXT
    arcpy.env.mask =EXT

    
    arcpy.FeatureToPoint_management(WS, WSPOINTS, "CENTROID")    #Extraction of the centroids
                            
    #Kriging application for WLI
    outKriging = Kriging(WSPOINTS, "Var", "SPHERICAL", pixelsize)
    outKriging.save(AUX)
    outExtractByMask = ExtractByMask(AUX, EXT)
    outExtractByMask.save(KRIG)


    #subtracion WS-DEM
    outM= Raster(KRIG) - Raster(DEM)
    outM.save(DIFF)
    outSN = SetNull (DIFF, DIFF,  "VALUE < 0")
    outSN.save(FLDEP)
    
    #Deleting auxiliary files
    arcpy.Delete_management(AUX)
    arcpy.Delete_management(DIFF)
    arcpy.Delete_management(BUFF)
    arcpy.Delete_management(KRIG)
    arcpy.Delete_management(EXT)
    arcpy.env.extent= FLDEP
    arcpy.env.mask =FLDEP


    #Convertion raster flow depth to polygon
    outP= Int(Raster(FLDEP)*100)
    outP.save(EXT)
    arcpy.RasterToPolygon_conversion(EXT, FLDEPSHP, "NO_SIMPLIFY")
  
    
    arcpy.AddField_management (FLDEPSHP, "Depth", "FLOAT")
    arcpy.CalculateField_management(FLDEPSHP, "Depth", "float(!GRIDCODE!)/100.00", "PYTHON")
    arcpy.Delete_management(AUX)
    arcpy.Delete_management(EXT)
    arcpy.Delete_management(WSPOINTS)
    

    
    
except: 
    arcpy.AddError(arcpy.GetMessages())
    arcpy.AddMessage(traceback.format_exc()) 
    #print arcpy.GetMessages()
