import time

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Configure Yandex Maps specific class names
route_button = "route-control__inner"
transport_mode = "_mode_masstransit"
result = "masstransit-route-snippet-view__route-duration"
no_route_error = "route-error-view__text"


def look_up_transit_time(from_: str, to: str, driver) -> str:
    """Lookup transit time between to points on Yandex Maps.

    Args:
        from_ (str): The start point.
        to (str): The end point.
        driver: Selenium webdriver instance.

    Returns:
        A string with the best time suggested by Yandex Maps.

    Notes:
        The function expects that `driver` exists in the global scope.
        It is meant to be run from within the Selenium webdriver context.

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

    # Activate the public transport route
    time.sleep(1)
    driver.find_element(by=By.CLASS_NAME, value=transport_mode).click()

    # Extract the time suggested in the first result
    time.sleep(2)
    try:
        best_time = driver.find_element(by=By.CLASS_NAME, value=result).text
    except selenium.common.exceptions.NoSuchElementException:
        return "no route"

    return best_time
