from datetime import timedelta, date
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from datetime import datetime
import time as t
import pandas as pd

date_start = date(2015,1,1)
date_end = date(2019,11,26)

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)
 
dates = []
for dt in daterange(date_start, date_end):
    dates.append(dt.strftime("%d%m%Y"))

# Retrieve programme for each date

t1 = t.time()
with FuturesSession() as session:
    programmes = []
    urls = ["https://online.turfinfo.api.pmu.fr/rest/client/1/programme/%s?meteo=true&specialisation=INTERNET" % date for date in dates[:3]]
    future_to_url = {session.get(url): url for url in urls}
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        programmes.append([url, future.result()])
        
print("Time spent: %s s" % (t.time() - t1))

def add_row(tab, columns, json):
    row = [0]*len(columns)
    for key in json:
        if key in columns:
            row[columns.index(key)] = json[key]
        else:
            columns.append(key)
            row.append(json[key])
            tab = list(map(lambda r: r + [None], tab))
    tab.append(row)
            
    return tab, columns

reunions = []
reunions_columns = ['date']
courses = []
courses_columns = []

reunion_id = 0
course_id = 0

for programme in programmes:
    programme_json = programme.json()['programme']
    date = datetime.fromtimestamp(programme_json['date']//1000).strftime("%d%m%Y")
    print(date)
    
    for reunion in programme_json['reunions']:
        reunion_courses = reunion.pop('courses', None)
        reunion['reunion_id'] = reunion_id
        reunion['date'] = date
        reunions, reunions_columns = add_row(reunions, reunions_columns, reunion)
        reunion_id += 1
        for course in reunion_courses:
            course['reunion_id'] = reunion_id
            course['course_id'] = course_id
            courses, courses_columns = add_row(courses, courses_columns, course)
            course_id += 1

df_reunions = pd.DataFrame(reunions, columns = reunions_columns)
df_courses = pd.DataFrame(courses, columns = courses_columns)

df_reunions.to_csv("reunions_%s_%s.csv" % (date_start, date_end))
df_courses.to_csv("courses%s_%s.csv" % (date_start, date_end))

# Retrieve participans for each date

urls = []

url_to_course_id = {}
for course in courses:
    course_number = "R%s/C%s" % (course['numReunion'], course['numOrdre'])
    date = df_reunions.query('reunion_id == %s' % reunion_id).iloc[0]['date']
    urls.append("https://online.turfinfo.api.pmu.fr/rest/client/1/programme/%s/%s/participants?specialisation=INTERNET" % (date, course_number))
    url_to_course_id[url] = course_id

t1 = t.time()
with FuturesSession() as session:
    courses_participants = []
    future_to_url = {session.get(url): url for url in urls}
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        courses_participants.append([url, future.result()])
        
print("Time spent: %s s" % (t.time() - t1))

participant_id = 0
participants_columns = []

for url, course_participants in courses_participants:
    participants = course_participants.json()['participants']
    for participant in participants:
        participant['course_id'] = url_to_course_id[url]
        participant['participant_id'] = participant_id
        participants, participants_columns = add_row(participants, participants_columns, participant)
        participant_id += 1
