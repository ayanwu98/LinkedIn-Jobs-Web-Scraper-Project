# -*- coding: utf-8 -*-

''' In this project, we are creating a web scraping tool to collect information about Data Science job postings on Linkedin.
    We aim to extract information about company names, job titles, location, seniority levels. and skills required.
    We will be collecting this information from 1000 jobs.
'''

# We first import the required libraries.

from bs4 import BeautifulSoup
import requests
import time
import csv

# Now we create the main function which extracts the necessary information about each job posting

def webscrapping_one_page(url, headers):
  try:
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all("li")

    links = []
    for job in jobs:
      link = job.find("a", {"class":"base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]", "href":True})["href"]
      links.append(link)
    
    for link in links:
      time.sleep(1)
      headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"}
      html_text = requests.get(link, headers=headers).text
      soup = BeautifulSoup(html_text, 'lxml')
      company_name = soup.find("a", class_="topcard__org-name-link topcard__flavor--black-link").text.strip()
      job_title = soup.find("h1", class_="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title").text
      location = soup.find("span", class_="topcard__flavor topcard__flavor--bullet").text.strip()
      seniority_level = soup.find("span", class_="description__job-criteria-text description__job-criteria-text--criteria").text.strip()
      description = soup.find("div", class_="show-more-less-html__markup")
      description = str(description).casefold()
      if "python".casefold() in description:
        python = True
      else:
        python = False
      if "sql".casefold() in description:
        sql = True
      else:
        sql = False
      if " R ".casefold() in description:
        R = True
      else:
        R = False
      if "excel".casefold() in description:
        excel = True
      else:
        excel = False
      if "tableau".casefold() in description:
        tableau = True
      else:
        tableau = False
      if "power bi".casefold() in description:
        power_bi = True
      else:
        power_bi = False
      if "machine learning".casefold() in description:
        ml = True
      else:
        ml = False
      data = [company_name,job_title,location,seniority_level,python,sql,R,excel,tableau,power_bi,ml]
      print(data)
      with open('linkedinwebscraper.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)  
  except:
    print('error')

table = ['Company','Job_Title', 'Location', 'Seniority_level', 'Python',
         'SQL', 'R', 'Excel', 'Tableau', 'Power_BI', 'Machine_Learning']
with open('linkedinwebscraper.csv', 'w', newline='', encoding='UTF8') as f:
  writer = csv.writer(f)
  writer.writerow(table)  

url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Scientist&location=canada&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"}

# Now since there are 25 jobs per page, in order for us to extract the desired amount of jobs (in this case 1000),
# we need to loop through 1000/25 = 40 pages.

for page in range(40):

  webscrapping_one_page(url+str(page*25), headers)

