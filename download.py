import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sys
import time 
import yaml


def get_args():
	"""
	Get volume and chapter from command line
	"""
	if len(sys.argv) < 2:
		print('usage: python download.py <volume list>')
		sys.exit(1)
	return sys.argv[1]

def get_link(soup):
	"""
	Get direct link to the image scan
	"""
	for link in soup.find_all('img'):
		image = link.get('src')
		if '/comics/' in image:
			return image 
	return None


def create_and_init_driver(url):
	"""
	Starts a web driver and clicks the "i'm an adult" button
	"""
	# start web driver
	driver = webdriver.Chrome(os.path.join(os.path.expanduser("~"), 'chromedriver'))
	driver.get(url)

	# click through the restriction button
	xpath = "//input[@type='submit']"
	submit = driver.find_element_by_xpath(xpath)
	submit.click()

	return driver

def download_page(driver, url, output_dir):
	"""
	Download image from the web viewer
	"""
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	image = get_link(soup)

	if image:
		name = os.path.join(output_dir, os.path.split(image)[1])

		if os.path.isfile(name):
			print('{} already exists.'.format(name))
			return False

		result = requests.get(image)

		# create directory 
		if not os.path.isdir(output_dir):
			os.makedirs(output_dir)

		# write file 
		with open(name, 'wb') as file:
			file.write(result.content)
			print('Downloading {}'.format(name))

		return True

	print('No image link found on {}'.format(url))
	return False

def download_chapter(driver, base_url, vol, chapter, output_dir):
	"""
	Download an entire chapter
	"""
	print('Starting download of chapter {}'.format(chapter))
	page = 1
	current_url = os.path.join(base_url, str(vol), str(chapter), 'page', str(page))
	driver.get(current_url)
	success = download_page(driver, current_url, output_dir)

	while(success):
		page = page + 1
		if type(chapter) is int:
			current_url = os.path.join(base_url, str(vol), str(chapter), 'page', str(page))
		elif type(chapter) is float:
			chapter = int(chapter)
			current_url = os.path.join(base_url, str(vol), str(chapter), '1', 'page', str(page))
		driver.get(current_url)
		success = download_page(driver, current_url, output_dir)

	print('Finished downloading chapter {}'.format(chapter))

if __name__ == '__main__':
	base_url = 'http://www.twistedhelscans.com/read/tokyo_ghoul_re/en/'
	volume_chapter_map = get_args()

	driver = create_and_init_driver(os.path.join(base_url))

	volumes = yaml.load(open(volume_chapter_map, 'r'))

	for key in volumes.keys():
		for ch in volumes[key]:
			download_chapter(driver, base_url, key, ch, 'Chapter {}'.format(ch))

	driver.quit()
