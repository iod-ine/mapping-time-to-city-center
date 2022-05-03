import sys
import time
import argparse
import datetime

import geopandas as gpd

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Import the configuration dictionary with defined cities
from yandex_cities_config import city_grids_and_center_coords

# Configure Yandex Maps specific class names
route_button = "route-control__inner"

modes = {
    # mode: (button_class, result_class)
    "car": ("_mode_auto", "auto-route-snippet-view__route-title-primary"),
    "public": ("_mode_masstransit", "masstransit-route-snippet-view__route-duration"),
    "walk": ("_mode_pedestrian", "pedestrian-route-snippet-view__route-title-primary"),
    "cycle": ("_mode_bicycle", "bicycle-route-snippet-view__route-title-primary"),
}


def look_up_transit_time(from_: str, to: str, driver) -> str:
    """Lookup transit time between to points on Yandex Maps.

    Args:
        from_ (str): The start point.
        to (str): The end point.
        driver: Selenium webdriver instance.

    Returns:
        A string with the best time suggested by Yandex Maps.

    Notes:
        The strings will be typed into the search fields, they can be
        coordinates or names of places. When using coordinates, note that
        Yandex Maps expects them latitude-first.

    """

    driver.get("https://yandex.ru/maps")

    # Let the page load: wait till DOM is fully constructed
    time.sleep(2)

    # Enter the route construction mode
    driver.find_element(by=By.CLASS_NAME, value=route_button).click()

    # Construct the keystroke sequence
    actions = ActionChains(driver)
    actions.send_keys(from_)
    actions.send_keys(Keys.ENTER)
    actions.send_keys(Keys.TAB)
    actions.send_keys(to)
    actions.send_keys(Keys.ENTER)

    # Type everything in
    time.sleep(1)
    actions.perform()

    # Go through all route modes
    time.sleep(1)
    times = dict()
    for mode, (btn, res) in modes.items():
        # Activate the corresponding mode by clicking the button
        driver.find_element(by=By.CLASS_NAME, value=btn).click()
        time.sleep(1.5)

        try:
            travel_time = driver.find_element(by=By.CLASS_NAME, value=res).text
        except selenium.common.exceptions.NoSuchElementException:
            travel_time = "no route"

        times[mode] = travel_time

    return times


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Yandex.Maps for travel times.")

    parser.add_argument(
        "--city",
        required=True,
        help='the city to query for [i.e. "moscow"]',
    )

    args = parser.parse_args()

    try:
        city = city_grids_and_center_coords[args.city]
    except KeyError:
        print("No such city defined in yandex_cities_config.")
        sys.exit()

    grid = gpd.read_file(f"data/shp/{city.shp_stem}.shp")

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
                times = look_up_transit_time(point, args.center_coords, driver)

                for mode, time_ in times.items():
                    grid.loc[i, mode] = time_.replace("ч", "h").replace("мин", "m")

                grid.loc[i, "date"] = now.isoformat()

                # Be nice to the Yandex Maps server and separate the requests
                time.sleep(3)

    finally:
        grid.to_file(f"data/shp/{city.shp_stem}.shp", index=False)
