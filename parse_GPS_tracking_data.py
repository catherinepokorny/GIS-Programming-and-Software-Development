# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 23:17:27 2022

@author: catpo
"""

import arcpy
import csv

arcpy.env.workspace = r"C:/PSU/test"


# Set local variables for blank shapefile
out_path = r"C:\PSU\test"
out_name = "Coordinates.shp"
geom_type = "POLYLINE" 
sr = arcpy.SpatialReference(4326) 


try:
    # Parse the text file

    with open(r"C:\Users\catpo\OneDrive\Desktop\WakefieldParkRaceway_20160421.csv", "r") as gpsTrack:
       
        #Set up CSV reader and process the header
        csvReader = csv.reader(gpsTrack)
        header = next(csvReader)
        latIndex = header.index("Latitude")
        lonIndex = header.index("Longitude")
        lapIndex = header.index("Lap")
        
        # Make an empty dictionary
        lap_dict = {}

  
        # Loop through the lines in the file to write each coordinate pair to the dictionary
        for row in csvReader:
            try:
                lat = float(row[latIndex])
                lon = float(row[lonIndex])
                lap = row[lapIndex]
                vertex = (lon,lat)
                if lap not in lap_dict:
                    lap_dict[lap] = [vertex]
                else:
                    vertices = lap_dict[lap]
                    vertices.append(vertex)
            except:
                if not (row):
                    continue
            
        # Create a list of keys in dictionary            
        keys = lap_dict.keys()
              
    
    # Create shapefile and write the coordinate list to the shapefile as polyline features separated by lap number
    arcpy.CreateFeatureclass_management(out_path, out_name, geom_type, "", "", "", sr.factoryCode)
    arcpy.management.AddField(out_name, "Lap", "FLOAT") 
    for key in keys:
        with arcpy.da.InsertCursor(out_name, ('Lap', 'SHAPE@')) as cursor:
            cursor.insertRow((key, lap_dict[key]))

except:
    # Print error messages
    print("Script failed")
    print(arcpy.GetMessages(2))
    


    