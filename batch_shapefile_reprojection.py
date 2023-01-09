# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 15:15:34 2022

@author: catpo
"""
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\PSU\Geog485\Lesson2" #arcpy.GetParameterAsText(0) 

try:
    # Set local variables
    target_shp = r"C:\PSU\Geog485\Lesson2\StateRoutes.shp" #arcpy.GetParameterAsText(1)
    targetSR = arcpy.Describe(target_shp).spatialReference

    # Create list of shapefiles that are not already in the target projection
    project_datasets = arcpy.ListFeatureClasses()

    for fc in project_datasets:
        fcSR = arcpy.Describe(fc).spatialReference
        if fcSR.Name == targetSR.name:
            project_datasets.remove(fc)  
                                                                                    

    if target_shp in project_datasets:
        project_fcs.remove(target_shp)        


    # Project dataset list into target projection
    for fc in project_datasets:
        rootName = fc
        if rootName.endswith(".shp"):
            rootName = rootName.replace(".shp","")
        if not arcpy.env.workspace.endswith(".gdb"):
            rootNameProjected = rootName + "_projected.shp"
        else:
            rootNameProjected = rootName + "_projected"
        arcpy.management.Project(rootName, rootNameProjected, targetSR.PCSCode)

    
    
    # # Create custom geoprocessing message
    separator = ", "
    arcpy.AddMessage("Projected" + " " + separator.join(project_datasets)) 
    
    # Report a geoprocessing message
    print(arcpy.GetMessages())
    
except:
    print("Script failed :(") 
    print(arcpy.GetMessages(2))