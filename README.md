## 2DFLOOD-WLI
Water Levels Interpolator from FLO-2D Water surface elevation
It interpolates the Water Surface Elevation (WSE) results from FLO-2D
using an higher resolution DTM compared to the  resolution of the hydraulic model

## Prerequisites
The 2DFLOOD-WLI v2.0 is a phyton script prepared to run within a GIS ESRI environment. A ESRI toolbox is also provided for having a easy-to-use interface guiding 

## Instructions
The tool requires 5 main inputs:
 - A short name (3-4 characters) of the river/basin
 - The shapefile of the Water Surface Elevation (WSE) provided by the FLO-2D Mapper (or a similar shapefile in which the value of the water surface elevation is specified in the "Var" field of the attribute table
 - The value of the buffer (in meters) for the water levels interpolation, starting from the boundaries of the WSE shapefile
 - A DTM with a resolution higher than the one related to the FLO-2D hydraulic model (ESRI Grid format)
 - The Output path
 
## Outputs
The tool provides two outputs: the raster and the shapefile of the water depths at the smae resolution of the input DTM
