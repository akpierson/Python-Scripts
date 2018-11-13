import requests
from bs4 import BeautifulSoup
import string
import os
import subprocess
import datetime
import time

hashtags = "#remotejobsdaily #remotework #remotejobs #remotejob #remoteworker #remoteworklife #jobsearch #jobs #jobseekers #computers #tech #instajob #myjob #dayjob #instalife #company #work #working #jobsearching #jobhunting #jobalert #newjob #jobopportunity #goodjob #workfromhome"

# COUNTDOWN TIMER #
def countdown(p,q):
	i=p
	j=q
	k=0
	while True:
		if(j==-1):
			j=59
			i -=1
		if(j > 9):  
			print(str(k)+str(i)+":"+str(j), end="\r")
		else:
			print(str(k)+str(i)+":"+str(k)+str(j), end="\r")
		time.sleep(1)
		j -= 1
		if(i==0 and j==-1):
			break
	if(i==0 and j==-1):
		print("Ending Countdown", end="\r")
		time.sleep(1)

# SITES TO SCRAPE #

def scrape_remoteok():
	remoteok_page = requests.get("https://remoteok.io/")
	remoteok_page_content = BeautifulSoup(remoteok_page.text, 'html.parser')
	remoteok_first_listing = remoteok_page_content.find("tr", {"class": "job"})

	remoteok_job_url_text = 'https://remoteok.io' + remoteok_first_listing.find("a")['href']

	remoteok_job_title = remoteok_first_listing.find("h2")
	remoteok_job_title_text = BeautifulSoup(remoteok_job_title.text, 'html.parser')

	remoteok_company_title = remoteok_first_listing.find("h3")
	remoteok_company_title_text = BeautifulSoup(remoteok_company_title.text, 'html.parser')

	remoteok_remoteok = [remoteok_job_url_text, remoteok_job_title_text, remoteok_company_title_text]

	return remoteok_remoteok

def scrape_we_work_remotely():
	weworkremotely_page = requests.get("https://weworkremotely.com/")
	weworkremotely_page_content = BeautifulSoup(weworkremotely_page.text, 'html.parser')

	weworkremotely_listing_wrapper = weworkremotely_page_content.find("section", {"class": "jobs"})
	weworkremotely_listing_wrapper2 = weworkremotely_listing_wrapper.find("ul")

	weworkremotely_first_listing = weworkremotely_listing_wrapper2.find("li")

	# Account for sporratic <a> tag being or not being there...
	try:
		weworkremotely_job_url_text = 'https://weworkremotely.com' + weworkremotely_first_listing.find_all("a")[1]['href']
	except:
		weworkremotely_job_url_text = 'https://weworkremotely.com' + weworkremotely_first_listing.find("a")['href']

	weworkremotely_job_title = weworkremotely_first_listing.find("span", {"class": "title"})
	weworkremotely_job_title_text = BeautifulSoup(weworkremotely_job_title.text, 'html.parser')

	weworkremotely_company_title = weworkremotely_first_listing.find("span", {"class": "company"})
	weworkremotely_company_title_text = BeautifulSoup(weworkremotely_company_title.text, 'html.parser')

	weworkremotely_we_work_remotely = [weworkremotely_job_url_text, weworkremotely_job_title_text, weworkremotely_company_title_text]

	return weworkremotely_we_work_remotely

def scrape_careerbuilder():
	careerbuilder_page = requests.get("https://www.careerbuilder.com/jobs-remote?keywords=remote&posted=1")
	careerbuilder_page_content = BeautifulSoup(careerbuilder_page.text, 'html.parser')
	careerbuilder_first_listing = careerbuilder_page_content.find("div", {"class": "job-row"})

	careerbuilder_job_title = careerbuilder_first_listing.find("h2", {"class": "job-title"})
	careerbuilder_job_title_text = str(BeautifulSoup(careerbuilder_job_title.text, 'html.parser')).lstrip()

	if "\n" in careerbuilder_job_title_text:
		careerbuilder_job_title_text = careerbuilder_job_title_text[:-1]
	else:
		pass

	careerbuilder_job_url_text = 'https://www.careerbuilder.com' + careerbuilder_job_title.find("a")['href']

	careerbuilder_company_title = careerbuilder_first_listing.find("div", {"class": "columns large-2 medium-3 small-12"})
	careerbuilder_company_title2 = careerbuilder_company_title.find("a")
	careerbuilder_company_title_text = str(BeautifulSoup(careerbuilder_company_title2.text, 'html.parser')).lstrip()

	careerbuilder_careerbuilder = [careerbuilder_job_url_text, careerbuilder_job_title_text, careerbuilder_company_title_text]

	return careerbuilder_careerbuilder

def scrape_atlasandboots():
	atlasandboots_page = requests.get("https://www.atlasandboots.com/remote-jobs/")
	atlasandboots_page_content = BeautifulSoup(atlasandboots_page.text, 'html.parser')
	atlasandboots_first_listing = atlasandboots_page_content.find("div", {"class": "col-md-12 col-sm-12 col-xs-12 pt-cv-content-item pt-cv-1-col"})
	
	atlasandboots_url_text = atlasandboots_first_listing.find("a")['href']

	atlasandboots_job_title = atlasandboots_first_listing.find("a")
	atlasandboots_job_title_text = BeautifulSoup(atlasandboots_job_title.text, 'html.parser')

	atlasandboots_company_title = atlasandboots_first_listing.find("div", {"class": "col-md-12 pt-cv-ctf-column"})
	atlasandboots_company_title_text = BeautifulSoup(atlasandboots_company_title.text, 'html.parser')

	atlasandboots_atlasandboots = [atlasandboots_url_text, atlasandboots_job_title_text, atlasandboots_company_title_text]

	return atlasandboots_atlasandboots

# CHECK JOB. IF JOB HASN'T BEEN ADDED TO INSTAGRAM, ADD IT #

def check_create_upload(url, title, company):
	master_text_list = open("master_list.txt", 'r').read()

	concact_title_company = str(title) + str(company)

	if url in master_text_list or concact_title_company in master_text_list:
		print("Job already added.")
	else:
		open("master_list.txt", 'a').write("\n" + url)
		open("master_list.txt", 'a').write("\n" + concact_title_company)
		print("Job uploading!")

		# DRAW SVG AND EXPORT #

		drawingsvg = open("drawing.svg", 'r').read()

		change_job_text = drawingsvg.replace('jobtitle', str(title))
		change_company_text = change_job_text.replace('companytitle', str(company))
		change_company_url = change_company_text.replace('urltitle', str(url))

		today = datetime.date.today().strftime("%B %d, %Y")
		change_todays_date = change_company_url.replace('datetitle', str(today))

		outfile = open('uploadsvg.svg','w')

		outfile.write(change_todays_date)

		os.chdir('C:\\Program Files\\Inkscape')

		subprocess.Popen('inkscape.exe -f C:\\Users\\Austin\\Desktop\\remote.jobs.daily\\uploadsvg.svg -e C:\\Users\\Austin\\Desktop\\remote.jobs.daily\\uploadimage.png', shell = True)

		os.chdir('C:\\Users\\Austin\\Desktop\\remote.jobs.daily')

		# Change png to jpg #
		time.sleep(5)
		subprocess.Popen('magick convert uploadimage.png uploadimage.jpg', shell = True)
		time.sleep(10)

		os.chdir('C:\\Users\\Austin\\Desktop\\remote.jobs.daily\\akpierson.github.io')
		subprocess.Popen('git add index.html', shell = True)
		time.sleep(3)
		subprocess.Popen("git commit -m \"Job Added\"", shell = True)
		time.sleep(3)
		subprocess.Popen("git push", shell = True)
		os.chdir('C:\\Users\\Austin\\Desktop\\remote.jobs.daily')
		print("Job added via git")

		# UPLOAD TO INSTAGRAM! #

		from InstagramAPI import InstagramAPI

		InstagramAPI = InstagramAPI("remote.jobs.daily", "NOTHINGHERE")
		InstagramAPI.login()

		photo_path = 'uploadimage.jpg'
		caption = "New remote job opening found. \"{}\" is looking for a \"{}\". You can find a link to this job on our website, which is in our bio section. {}".format(str(company), str(title), hashtags)
		print(caption)
		
		InstagramAPI.uploadPhoto(photo_path, caption=caption)

		print("Instagram upload Success!")

		time.sleep(15)

		os.remove("uploadimage.png")
		os.remove("uploadimage.jpg")

# MAIN FUNCTION #

def main():
	
	try:
		remoteok_values = scrape_remoteok()
		check_create_upload(remoteok_values[0], remoteok_values[1], remoteok_values[2])
	except:
		print("Couldn't scrape remoteok. skipping for now")

	countdown(2,0)

	try:
		we_work_remotely_values = scrape_we_work_remotely()
		check_create_upload(we_work_remotely_values[0], we_work_remotely_values[1], we_work_remotely_values[2])
	except:
		print("Couldn't scrape weworkremotely. skipping for now")

	countdown(2,0)

	try:
		careerbuilder_values = scrape_careerbuilder()
		check_create_upload(careerbuilder_values[0], careerbuilder_values[1], careerbuilder_values[2])
	except:
		print("Couldn't scrape careerbuilder. skipping for now")

	countdown(2,0)

	try:
		atlasandboots_values = scrape_atlasandboots()
		check_create_upload(atlasandboots_values[0], atlasandboots_values[1], atlasandboots_values[2])
	except:
		print("Couldn't scrape atlasandboots. skipping for now")


# RUN IT ALL #

while True:
	print("Beginning new search!")
	main()
	print("Ending new search. Sleeping for 20 minutes...")
	countdown(180,0) # 20 minutes

