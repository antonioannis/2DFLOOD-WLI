## FLO-2D-Post-Processing-Tools

## Prerequisites
FLO-2D-Post-Processing-Tools v1.0 is a phyton toolbox prepared to run within a GIS ESRI environment.

## DESCRIPTION
List of the tools
 -  01- 2DFLOOD-WLI
Water Levels Interpolator from FLO-2D Water surface elevation
It interpolates the Water Surface Elevation (WSE) results from FLO-2D
using an higher resolution DTM compared to the  resolution of the hydraulic model
The tool requires 5 main inputs:
1. A short name (3-4 characters) of the river/basin
2. The shapefile of the Water Surface Elevation (WSE) provided by the FLO-2D Mapper (or a similar shapefile in which the value of the water surface elevation is specified in the "Var" field of the attribute table
3. The value of the buffer (in meters) for the water levels interpolation, starting from the boundaries of the WSE shapefile
4. A DTM with a resolution higher than the one related to the FLO-2D hydraulic model (ESRI Grid format)
5. The Output path
The tool provides two outputs: the raster and the shapefile of the water depths at the smae resolution of the input DTM

## Authors
* **Antonio Annis**  - [antonioannis](https://github.com/antonioannis)
