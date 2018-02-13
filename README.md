# twistedhelscan scraper

## Install Dependencies
To start scraping twistedhelscans, you first must install all of the files in `requirements.txt`. It's recommended that you do this using`virtualenv`. 

`$ pip install virtualenv`
`$ virtualenv -p python3 scraper_env`

Activate the virtualenv

`$ source scraper_env/bin/activate`

Install dependencies

`$ pip install -r requirements.txt`

Now you need to download a webdriver that will allow python to control your browser. I tested this using chrome, so I used the chrome driver. https://sites.google.com/a/chromium.org/chromedriver/downloads

Download the latest webdriver and extract it to `~/chromedriver`

## Specify the Chapters to Download
You're almost ready to run things. Create `chapters.yaml` of the chapters you want to download, along with the volumes that they belong to. The key is the volume, and the list of integers are the chapters you want to download from that volume. 
```
1:
  - 1
  - 2
  - 3
2:
  - 10
```
This yaml file will download chapters 1, 2, 3 and 10. You should check wikipedia or the wikia to see which chapters belong to each volume.

## Run It
`$ python download.py chapters.yaml` 

Manga pages will be downloaded and saved to directories based on chapter. 

## Todo:
- Refactor code
- Make it generic. Right now it only works on Tokyo Ghoul: Re unless you edit the source
- I never tested partial chapters like 31.5. These chapters have different URLs, that I can't test because TwistedHelScans doesn't have chapters 30 or higher. 
