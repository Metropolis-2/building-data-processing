import geopandas as gpd

# convex hulls
convex_hull = gpd.read_file("data/rounded_bldgs.gpkg")

# bldgs to replace in convex hulls
extracted = gpd.read_file("data/cleaned_hard_bldgs.gpkg")

# bldgs that replace those in convex hulls
orig_bldg = gpd.read_file("data/cleaned_hard_bldgs.gpkg")

# make new dataframe from orig_bldg with ids frome extracted
relevant_fid2 = extracted.iloc[:,3].values
orig_bldg_geom = orig_bldg.iloc[:, 4]


mydict = {}

for idx, gdfrow in orig_bldg.iterrows():
    orig_bldg_fid = gdfrow['fid_2']
    
    if orig_bldg_fid in relevant_fid2:
        poly_needed = gdfrow['geometry']

        mydict[orig_bldg_fid] = poly_needed

# replace geometry
my_gdf = []
for idx, gdfrow in convex_hull.iterrows():

    o_KOTE_MAX = gdfrow['O_KOTE_max']
    t_KOTE_MAX = gdfrow['T_KOTE_max']
    bldg_h_max = gdfrow['bldg_h_max']
    fid_2 = gdfrow['fid_2']
    geom = gdfrow['geometry']

    if fid_2 in relevant_fid2:
        geom = mydict[fid_2]

    my_gdf.append([o_KOTE_MAX, t_KOTE_MAX, bldg_h_max, geom, fid_2])

relevant_gdf = gpd.GeoDataFrame(my_gdf, columns=['O_KOTE_max', 'T_KOTE_max','bldg_h_max', 'geometry', 'fid_2'], crs=orig_bldg.crs)

relevant_gdf.to_file("data/cleaned_bldgs.gpkg", driver="GPKG")