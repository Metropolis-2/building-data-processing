Vienna building data for metropolis2
---------------downloaded data metadata-------
LOD0.4

Accessed May 20, 2021


https://www.data.gv.at/katalog/dataset/76c2e577-268f-4a93-bccd-7d5b43b14efd

title: Baukörpermodell (LOD0.4) Grunddaten aus der Flächen-MZK Vektordaten Wien

original metadata for this:

F_KLASSE: Land use class LINK: https://www.wien.gv.at/stadtentwicklung/stadtvermessage/pdf/fmzk-attribute-wertbereiche.pdf LAYER: Textual description for attribute F_KLASSE REFERENCE: Address code for building H_KLASSE: Height classes for building height plan KLASSE_SUB: Definition the land use of the lower surface when surfaces are on top of each other; Value range as for the attribute F_KLASSE O_KOTE: absolute building height of the eaves U_KOTE: absolute building height below HOEHE_DGM: absolute terrain height T_KOTE: lowest point of the terrain on the edges of the partial building area FMZK_ID: unique area reference for the FMZK BW_GEB_ID: unique area reference for the FMZK BW_GEB_ID: address code for building areas together

----------------------data processing steps----------
processing data steps to clean with QGIS
1) import all vienna datasets to QGIS
2) press magic merge button
3) press magic fix geometry button
4) press dissolve button to combine all buildings that touch
5) click delete holes to make footprints have less detail
6) Use multipart to single part so that all buildings are individual geometries
7) fix geometries again.
8) create a spatial index to make things go faster
9) join attributes by location with original data. This will allow you to take heights from original data and match it with the processed city blocks.
10) filter any polygons with less than 40 m^2 and height less than 10 meters
11) export to correct CRS for bluesky
12) get actual building height from ground by subtracting O_KOTE-T_KOTE

future
-maybe get rid of holes somehow and simplify polygons

--------------folder structure------------------
data/vienna_LOD_0.4/: contains original downloaded data of Vienna
data/*: contains shapefiles for  processed layers

3d_viennna.qgz: QGIS file that processed the 3D data
ViennaDownloader.py: Python script to download 3D data
building_heights.zip: a zipped verion of processed_vienna

processed_vienna/data/*: contains final geopackage layer with processed buildings
processed_vienna/3d_vienna_fixed.qgz: QGIS file that shows final version of vienna for bluesky

