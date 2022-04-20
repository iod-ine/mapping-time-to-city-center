import time

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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
