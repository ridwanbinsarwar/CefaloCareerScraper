import requests
from bs4 import BeautifulSoup
import json
from src.Job import Job
import smtplib


def parse_career():
    URL = 'https://www.cefalo.com/en/career'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    # job_elems = soup.find_all('div', class_='custom-open-job-position clearfix')
    jobs = soup.find_all('div', class_='custom-column-wrap-inner')
    return jobs


def get_current_job():
    job_list = []
    jobs = parse_career()
    for job in jobs:
        h = job.find('h3')
        h.find("span").decompose()
        position = h.text.strip()
        p = job.find('p')
        description = p.text.strip()
        link = job.find('a')['href']
        new_job = Job(position, description, link)
        job_list.append(new_job)
    return job_list


def get_previous_jobs():
    with open('data.json') as json_file:
        data = json.load(json_file)
        previous_jobs_json = json.loads(data)
        previous_jobs = [Job(**i) for i in previous_jobs_json]
        return previous_jobs


def update_job_list(job_list):
    json_string = json.dumps([ob.__dict__ for ob in job_list])
    # print(json_string, end='\n' * 2)
    with open("data.json", "w") as fileRead:
        json.dump(json_string, fileRead, sort_keys=True)


current_jobs = get_current_job()
previous_jobs = get_previous_jobs()
newJobs = []
newOpenings = False
if len(current_jobs) != len(previous_jobs):
    print("There is a update on Cefalo career")
    update_job_list(current_jobs)

    for current_job in current_jobs:
        newOpening = True
        for previous_job in previous_jobs:
            if current_job.position == previous_job.position:
                newOpening = False
        if newOpening:
            newOpenings = True
            newJobs.append(current_job)


if newOpenings:
    gmail_user = 'r@x.com'  # update email
    gmail_password = 'pass'  # update pass
    to = ['k@y.com']  # add email to sent notification

    subject = 'There is a update on Cefalo career'
    body = ''
    for newJob in newJobs:
        body = body + newJob.__str__() + '\n'

    email_text = """\
    From: %s
    To: %s
    Subject: %s
    
    %s
    """ % (gmail_user, ", ".join(to), subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, email_text)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')
