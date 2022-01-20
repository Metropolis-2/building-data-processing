# script to further simplify buildings
# note that difference takes quite a long time
from qgis import processing 

# get buffer layer to perform the difference
buffer_dist = 5 #meters
buffer_path = f"/Users/andresmorfin/Desktop/M2/building_buffer/buffers/{buffer_dist}m"
buffer_layer = QgsVectorLayer(f"{buffer_path}/union_{buffer_dist}.gpkg")

# remove buidings less than this area
area_filter = 50

# process the buildings
building_path = "/Users/andresmorfin/Desktop/M2/building_buffer/buildings/"
  
# import street graphs
bldgs = QgsVectorLayer(f"{building_path}preclean/bldgs.gpkg")

# first get the minimum bounding geometry
temp_bounding = processing.run("qgis:minimumboundinggeometry",
                { 'FIELD' : 'fid', 
                'INPUT' : bldgs, 
                'OUTPUT' : 'TEMPORARY_OUTPUT', 
                'TYPE' : 3 }
               )

# now do a dissolve on this
temp_dissolve = processing.run("native:dissolve",
                                { 'FIELD' : [], 
                                'INPUT' : temp_bounding['OUTPUT'],
                                'OUTPUT' : 'TEMPORARY_OUTPUT' })
                                
                                

# now do multiparts to single parts
single_part_path = f'{building_path}/tmp/single.gpkg'
multi_single = processing.run("native:multiparttosingleparts",
                                { 'INPUT' : temp_dissolve['OUTPUT'],
                                'OUTPUT' : f'{single_part_path}' })
                                
                                
layer_single = QgsVectorLayer(single_part_path)

# add a spatial index to layer _single
processing.run("native:createspatialindex",
                                { 'INPUT' : layer_single})
                                
                                
layer_single = QgsVectorLayer(single_part_path)


# perform a difference between layer_single and street buffer layer
tmp_difference = processing.run("qgis:difference",
                                { 'INPUT' : layer_single,
                                'OVERLAY' : buffer_layer,
                                'OUTPUT' : 'TEMPORARY_OUTPUT'})
                                
# now do multiparts to single parts
single_part_path = f'{building_path}/tmp/single_clean.gpkg'
multi_single = processing.run("native:multiparttosingleparts",
                                { 'INPUT' : tmp_difference['OUTPUT'],
                                'OUTPUT' : f'{single_part_path}' })
                                
                                
layer_single = QgsVectorLayer(single_part_path)

# now drop some fields
drop_fields = processing.run("qgis:deletecolumn",
                            {'COLUMN' : ['id','area','perimeter'], 
                             'INPUT' : layer_single,
                             'OUTPUT' : 'TEMPORARY_OUTPUT' })
                                
# now add back the geometry columns
add_geom_columns =  processing.run("qgis:exportaddgeometrycolumns",
                            {'CALC_METHOD' : 0,
                             'INPUT' : drop_fields['OUTPUT'],
                             'OUTPUT' : 'TEMPORARY_OUTPUT' })
                             
# now filter the geometry based on area
area_filter = processing.run("qgis:extractbyexpression",
                                            { 'EXPRESSION' : f' \"area\" > {area_filter}', 
                                            'INPUT' : add_geom_columns['OUTPUT'], 
                                            'OUTPUT' : 'TEMPORARY_OUTPUT'})
                                            

# drop fields
drop_fields = processing.run("qgis:deletecolumn",
                            {'COLUMN' : ['fid', 'id'], 
                             'INPUT' : area_filter['OUTPUT'],
                             'OUTPUT' : 'TEMPORARY_OUTPUT' })
                             

# join attribute by location to get building height
processing.runAndLoadResults("qgis:joinbylocationsummary",
                {'DISCARD_NONMATCHING' : True,
                'INPUT' : drop_fields['OUTPUT'],
                'JOIN': bldgs,
                'JOIN_FIELDS' : ['bldg_h_max'], 
                'OUTPUT' : f'{building_path}cleaned.gpkg', 
                'PREDICATE' : [0], 
                'SUMMARIES' : [3]
                })
                
                
                
