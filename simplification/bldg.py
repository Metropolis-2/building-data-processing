import geopandas as gpd
import osmnx as ox

airspace_gdf = gpd.read_file("constrained_airspace.gpkg", layer='constrained_airspace')

fun_polygon = airspace_gdf.loc[0].geometry

# create MultiDigraph from polygon
G = ox.graph_from_polygon(fun_polygon, network_type='drive', simplify=True)


# Save geopackage for import to QGIS and momepy
ox.save_graph_geopackage(G, 'constrained_road.gpkg')
