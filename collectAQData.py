import sqlite3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import glob
import os


def createWebDriver(download_dir):

	fp = webdriver.FirefoxProfile()
	fp.set_preference('browser.download.manager.showWhenStarting', False)
	fp.set_preference('browser.download.folderList', 2) 
	fp.set_preference('browser.download.dir', download_dir)
	fp.set_preference("browser.download.manager.showWhenStarting", False)
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");

	driver = webdriver.Firefox(executable_path='C:/Users/ehopl/Desktop/geckodriver', firefox_profile = fp)

	return driver

def getAQData(driver):

	location_list = []

	driver.get("https://sim.csb.gov.tr/STN/STN_Report/StationDataDownloadNew")
	sleep(3)

	driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/fieldset[1]/div[1]/div[1]/div[1]/div[5]/div/div/span[1]').click()

	city_sub_elm = driver.find_element_by_xpath('/html/body/div[12]/div/span/input')

	city_sub_elm.send_keys(u'\ue015')

	sleep(2)

	html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

	soup = BeautifulSoup(html, 'html.parser')

	location = soup.find('span', attrs={'class': 'k-input'}).text

	location = location.replace(" - ", "_")

	while location not in location_list:

		location_list.append(location)
		### PRESS SORGULA
		driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/fieldset[1]/div[1]/div[2]/div[1]/div/div/div/button').click()

		sleep(2)

		try:
			### PRESS EXCEL'E AKTAR
			driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/fieldset[3]/div/div[1]/a').click()

			list_of_files = glob.glob('C:\\Users\\ehopl\\Desktop\\veriler\\*')
			latest_file = max(list_of_files, key=os.path.getctime)
			print("Latest File: " + latest_file)
			print("Latest File Renamed: " + latest_file.replace(".xlsx", "") + "_" + location + "_hourly.xlsx")
			os.rename(latest_file, latest_file.replace(".xlsx", "") + "_" + location + "_hourly.xlsx")


			### PRESS GUNLUK
			driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/fieldset[1]/div[1]/div[1]/div[2]/div[1]/div/div/label[2]').click()

			### PRESS SORGULA
			driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/fieldset[1]/div[1]/div[2]/div[1]/div/div/div/button').click()

			sleep(2)

			### PRESS EXCEL'E AKTAR
			driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/fieldset[3]/div/div[1]/a').click()

			list_of_files = glob.glob('C:\\Users\\ehopl\\Desktop\\veriler\\*')
			latest_file = max(list_of_files, key=os.path.getctime)
			print("Latest File: " + latest_file)
			print("Latest File Renamed: " + latest_file.replace(".xlsx", "") + "_" + location + "_daily.xlsx")
			os.rename(latest_file, latest_file.replace(".xlsx", "") + "_" + location + "_daily.xlsx")

			sleep(3)

		except:
			print('No data found for this location!')	

		driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/fieldset[1]/div[1]/div[1]/div[1]/div[5]/div/div/span[1]').click()

		city_sub_elm = driver.find_element_by_xpath('/html/body/div[12]/div/span/input')

		city_sub_elm.send_keys(u'\ue015')

		sleep(2)

		html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

		soup = BeautifulSoup(html, 'html.parser')

		location = soup.find('span', attrs={'class': 'k-input'}).text

		location = location.replace(" - ", "_")


def main():
	driver = createWebDriver("C:\\Users\\ehopl\\Desktop\\AirQualityAPI\\veriler")
	getAQData(driver)

if __name__ == '__main__':
	main()