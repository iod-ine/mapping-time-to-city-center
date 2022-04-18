import time

import fiona
import geopandas as gpd

from selenium import webdriver

from yandex_maps_lookup import look_up_transit_time


# Use Zaryadye Park as a symbolic center of Moscow
zaryadye_park = "55.749435, 37.629416"

# Load the point grid: reload an interrupted attempt if possible
try:
    grid = gpd.read_file("data/shp/moscow_times.shp")
except fiona.errors.DriverError:
    grid = gpd.read_file("data/shp/moscow_grid.shp")

    # Add a column to store the extracted times
    grid["best_time"] = str()

try:
    with webdriver.Firefox() as driver:
        # iterate over the grid to find best time for each point
        for i, row in grid.iterrows():

            # skip already fetched times
            if row["best_time"] is not None:
                continue

            geometry = row["geometry"]
            point = f"{geometry.y:.6f}, {geometry.x:.6f}"
            best_time = look_up_transit_time(point, zaryadye_park, driver)

            best_time = best_time.replace("ч", "h")
            best_time = best_time.replace("мин", "m")
            grid.loc[i, "best_time"] = best_time

            # Be nice to the Yandex Maps server and separate the requests
            time.sleep(3)

finally:
    grid.to_file("data/shp/moscow_times.shp", index=False)
