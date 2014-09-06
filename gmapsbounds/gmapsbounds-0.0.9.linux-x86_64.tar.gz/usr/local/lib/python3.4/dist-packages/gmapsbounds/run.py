import os
import re
import sys
import time
import subprocess
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import obj
import reader
import utils

def main():
    # cities = utils.get_city_list('files/cities.txt')[:3]
    cities = ['Instanbul, Turkey']
    if cities:
        driver = utils.launch_driver()
        try:
            for city_name in cities:
                city = obj.City(driver, city_name)
                city.download_center_map()
                city.center, city.zoom = utils.parse_url(city.driver.current_url)
                city.set_corner_information()
                city.calculate_coordinates()
        finally:
            driver.close()

if __name__ == '__main__':
    main()
