# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 18:46:37 2022

@author: catpo
"""

import arcpy


sample_data = r"C:\PSU\test\sample_data\jsonresponse.txt"


# Set local variables for blank shapefile
out_path = r"C:\PSU\test"
out_name = "Output.shp"
geom_type = "POLYLINE" 
sr = arcpy.SpatialReference(4326) 


# Define a function that creates a shapefile and populates geometry to be called later in the script
def CreateFeatureClass(coordlist):
    arcpy.CreateFeatureclass_management(out_path, out_name, geom_type, "", "", "", sr.factoryCode)
    with arcpy.da.InsertCursor(out_name, ('SHAPE@')) as cursor:
        cursor.insertRow((coordlist,))

if sample_data.endswith('.csv'):
    
    try:
    
        # import modules necessary to parse csv files
        import csv
        
        # Parse the text file

        with open(sample_data, "r") as gpsTrack:
       
        #Set up CSV reader and process the header
            csvReader = csv.reader(gpsTrack)
            header = next(csvReader)
            latIndex = header.index("latitude")
            lonIndex = header.index("longitude")
        
        # Make an empty list
            vertices = []

        # Loop through the lines in the file to write each coordinate pair to the dictionary
            for row in csvReader:
                lat = row[latIndex]
                lon = row[lonIndex]
                vertex = (lon,lat)
                vertices.append(vertex)
        
        # Call createfeatureclass function        
            CreateFeatureClass(vertices)
    except:
        # Print error messages
        print("Script failed.") 
        print(arcpy.GetMessages(2))
            
            
elif sample_data.endswith('.kml'):
    
    try:
        
        # Import modules necessary to parse kml files
        from pykml import parser
        from os import path
        import csv 
        
        # Parse kml file and create list of coordinates
        kml_file = path.join(sample_data)
        coords = []
        with open(kml_file) as f:
            doc = parser.parse(f).getroot()
            for e in doc.Document.Folder.Placemark:
                coor = e.Point.coordinates.text.split(',')
                coor.pop(2)
                lon = float(coor[0])
                lat = float(coor[1])
                vertex = (lon, lat)
                coords.append(vertex)
                
        # Call createfeatureclass function        
        CreateFeatureClass(coords)         

    except:
        # Print error messages
        print("Script failed.") 
        print(arcpy.GetMessages(2))
            
        
elif sample_data.endswith('.txt'):
    
    try:
        # Import modules necessary to parse json web service response .txt files 
        import json
        
        # Parse txt file and create list of coordinates
        with open(sample_data) as f:
            json_data = json.load(f)
            json_range = len(json_data['features'])
            vertices = [] 
            for x in range(json_range):   
                coord = json_data["features"][x]['geometry']['coordinates']
                vertices.append(coord)
                
        # Call createfeatureclass function        
        CreateFeatureClass(vertices)        
       
    except:
        # Print error messages
        print("Script failed.") 
        print(arcpy.GetMessages(2))
        
else:
    # Prompt user to rerun script with different file type
    print("You have provided an unsupported file type.")         