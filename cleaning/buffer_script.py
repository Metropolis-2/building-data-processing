# script to buffer the streets a certain distance and then unify
from qgis import processing

buffer_dist = 5 # meters

street_path = "/Users/andresmorfin/Desktop/M2/building_buffer/graphs/"

# import street graphs
centralised_streets = QgsVectorLayer(f"{street_path}centralised.gpkg")
decentralised_streets = QgsVectorLayer(f"{street_path}decentralised.gpkg")
hybrid_streets = QgsVectorLayer(f"{street_path}hybrid_constrained.gpkg")

graph_list = [centralised_streets, decentralised_streets, hybrid_streets]

# buffer the streets
path_to_save = f"/Users/andresmorfin/Desktop/M2/building_buffer/buffers/{buffer_dist}m"

# layers to create
buffer_layers = ['centralised', 'decentralised', 'hybrid']

# perform the buffer for each layer
for idx, buffer_layer in enumerate(buffer_layers): 

    processing.run("native:buffer", {'INPUT': graph_list[idx],
                   'DISTANCE': buffer_dist,
                   'SEGMENTS': 5,
                   'DISSOLVE': True,
                   'END_CAP_STYLE': 0,
                   'JOIN_STYLE': 0,
                   'MITER_LIMIT': 10,
                   'OUTPUT': f'{path_to_save}/{buffer_layer}_buffer_{buffer_dist}'
                   })
                   
                   

concept_layers = ['centralised', 'decentralised', 'hybrid']

buffer_path = f"/Users/andresmorfin/Desktop/M2/building_buffer/buffers/{buffer_dist}m/"

# import street graphs
layer_list = []
for concept_layer in concept_layers:
    layer_add = QgsVectorLayer(f"{buffer_path}{concept_layer}_buffer_{buffer_dist}.gpkg")
    
    layer_list.append(layer_add)
    

# first perform a union between centralised and decentralised
temp_union = processing.run("native:union", 
                                            { 'INPUT' : layer_list[0], 
                                            'OUTPUT' : 'TEMPORARY_OUTPUT', 
                                            'OVERLAY' : layer_list[1], 
                                            'OVERLAY_FIELDS_PREFIX' : '' })
                                            
                                            
# now do a dissolve on this union
temp_dissolve = processing.run("native:dissolve",
                                { 'FIELD' : [], 
                                'INPUT' : temp_union['OUTPUT'],
                                'OUTPUT' : 'TEMPORARY_OUTPUT' })

# now do a union again with temp_dissolve and hybrid
temp_union = processing.run("native:union", 
                                            { 'INPUT' : temp_dissolve['OUTPUT'], 
                                            'OUTPUT' : 'TEMPORARY_OUTPUT', 
                                            'OVERLAY' : layer_list[2], 
                                            'OVERLAY_FIELDS_PREFIX' : '' })
                                            

# dissolve again and save
temp_dissolve = processing.runAndLoadResults("native:dissolve",
                                            { 'FIELD' : [], 
                                            'INPUT' : temp_union['OUTPUT'],
                                            'OUTPUT' : f'{buffer_path}/union_{buffer_dist}' })

layer_dissolve = QgsVectorLayer(f'{buffer_path}/union_{buffer_dist}')

# add a spatial index to this layer
processing.run("native:createspatialindex",
                                { 'INPUT' : layer_single})