buffer buildings from concept airspace for safety


simplification code is run from qgis python console:

1) buffer_script.py
	- this turns all the concept graphs into polygons where the streets are 10 meters wide (5 meter buffer)
	- It then makes a union of all the graphs so that we encapsulate all possible differences.

2) bldg_script.py
	- script first further simplifies bldgs.gpkg by making a convex hull
	- second it dissolves the convex hull and explodes to single parts.
	- Then we make a difference with the result of buffer_script.py to get buildings that are at least 5 meters from the center line of all concepts.
	- We then do a single parts just in case the street polygons split one polygon into two.
	- After that we filter out all areas that are less than 50 meters squared
	- Then we use the original buildings and do a join attribute by location (summary) to get the original heights.
