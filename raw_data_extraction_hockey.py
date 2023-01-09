# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 17:01:50 2022

@author: catpo
"""

import arcpy

# Set paths and variables
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\PSU\Geog485\Lesson3"
roster_shp = r"C:\PSU\Geog485\Lesson3\nhlrosters.shp"
countries_shp = r"C:\PSU\Geog485\Lesson3\Countries_WGS84.shp"  
country = "Sweden"
position_list = ["RW", "LW", "C"]
countryNameField = "CNTRY_NAME"
positionNameField = "position"
players = r"C:\PSU\Geog485\Lesson3\players"
position_layer = r"C:\PSU\Geog485\Lesson3\position_layer"

try:

    # Create a feature layer of boundary for desired country
    countryWhereClause = countryNameField + " =  '" + country + "'"
    selectionCountryLayer = arcpy.SelectLayerByAttribute_management(countries_shp, 'NEW_SELECTION', countryWhereClause)


    # Select all players with position RW, LW, and C in Sweden, respectively
    for x in position_list:
        positionWhereClause = positionNameField + " = '" + x + "'"
        selectionPositionLayer = arcpy.SelectLayerByAttribute_management(roster_shp, 'SUBSET_SELECTION', positionWhereClause)
        arcpy.management.CopyFeatures(selectionPositionLayer, position_layer + "{0}".format(x))
        roster_sweden = arcpy.SelectLayerByLocation_management(position_layer + "{0}".format(x), "WITHIN", selectionCountryLayer)
        arcpy.management.CopyFeatures(roster_sweden, players + "{0}".format(x))
        arcpy.Delete_management(position_layer + "{0}".format(x)) 

    # Reformat height field
    for x in position_list:    
        with arcpy.da.UpdateCursor(players + "{0}".format(x), ("height")) as cursor:
            for row in cursor:
                row[0] = row[0].replace('"',"")
                row[0] = row[0].replace("'","")
                cursor.updateRow(row)       
                
                
    # Calculate height and weight fields in metric units      
    for x in position_list:            
        arcpy.management.CalculateField(players + "{0}".format(x), "inch", '!height!.split(" ")[-1]', "PYTHON3")
        arcpy.management.CalculateField(players + "{0}".format(x), "foot", '!height!.split(" ")[0]', "PYTHON3")
        arcpy.management.CalculateField(players + "{0}".format(x), "height_cm", '(int(!foot!) * 12 + int(!inch!)) * 2.54')
        arcpy.management.CalculateField(players + "{0}".format(x), "weight_kg", 'float(!weight!) * 0.453592')
        arcpy.management.DeleteField(players + "{0}".format(x), ["inch", "foot"])
            
    print("Success!")       
    
except: 
    print("There was a problem selecting Swedish players by position and updating height and weight fields.")
    print(arcpy.GetMessages())
    
finally:
    del cursor
  