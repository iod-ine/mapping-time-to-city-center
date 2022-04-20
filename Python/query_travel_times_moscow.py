import time
import datetime

import geopandas as gpd

from selenium import webdriver

from yandex_maps_lookup import look_up_transit_time


# Use Zaryadye Park as a symbolic center of Moscow
zaryadye_park = "55.749435, 37.629416"

# Load the point grid
grid = gpd.read_file("data/shp/moscow_grid.shp")

try:
    with webdriver.Firefox() as driver:
        # iterate over the grid to find best time for each point
        for i, row in grid.iterrows():

            now = datetime.datetime.now()
            if now.hour < 8 or now.hour > 19:
                raise ValueError(
                    "It's either too early or too late! Results might be skewed."
                )

            # skip already fetched times
            if row["date"] is not None:
                continue

            geometry = row["geometry"]
            point = f"{geometry.y:.6f}, {geometry.x:.6f}"
            times = look_up_transit_time(point, zaryadye_park, driver)

            for mode, time_ in times.items():
                grid.loc[i, mode] = time_.replace("ч", "h").replace("мин", "m")

            grid.loc[i, "date"] = now.isoformat()

            # Be nice to the Yandex Maps server and separate the requests
            time.sleep(3)

finally:
    grid.to_file("data/shp/moscow_grid.shp", index=False)
