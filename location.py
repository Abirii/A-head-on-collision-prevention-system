"""
Get current location:
https://pythonspot.com/category/selenium/

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from geopy.distance import geodesic


TIMEOUT = 0.0001

# Make the browser grant permission to access the current location by default
def get_current_location():

    try:
        # To start a browser.
        options = Options()
        # Permission for location, microphone,etc.
        options.add_argument("--use-fake-ui-for-media-stream")
        # Edit path of chromedriver accordingly

        driver = webdriver.Chrome(options=options)

        # GET call the webpage and wait for the page to load.
        driver.get("https://mycurrentlocation.net/")
        wait = WebDriverWait(driver,TIMEOUT)

        longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')

        longitude = [x.text for x in longitude]
        longitude = str(longitude[0])
        latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
        latitude = [y.text for y in latitude]
        latitude = str(latitude[0])
        driver.quit()

    except:
        print('Failed to get location')

    return (latitude,longitude)



# Get two locations and return distance in miles
def measuring_distance(current_location,other_location):
    current_x, current_y = current_location
    other_x, other_y = other_location

    current_x = float(current_x)
    current_y = float(current_y)
    other_x = float(other_x)
    other_y = float(other_y)


    distance = geodesic((current_x,current_y),(other_x,other_y)).miles

    return distance