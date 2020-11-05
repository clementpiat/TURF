from datetime import timedelta, date
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from datetime import datetime
import time as t
import pandas as pd
import os
from tqdm import tqdm
import json

# Every race within this period of time will be retrieved
date_start = date(2017,1,2)
date_end = date(2019,1,1)
data_folder = f"data/{date_start}_{date_end}"
os.mkdir(data_folder)


# A simple generator of date being given lower and upper bounds
def daterange():
    for n in range(int ((date_end - date_start).days)+1):
        yield (date_start + timedelta(n)).strftime("%d%m%Y")

# Method that maps a list of urls to their respective api responses
def scrap_urls(urls, message):
    print(f"\n> SCRAPING {message}...")
    data = []
    t1 = t.time()
    with FuturesSession() as session:
        future_to_url = {session.get(url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            data.append([url, future.result()])
            
    print("\nTime spent: %s s" % (t.time() - t1))
    return data

# Method that dynamically add a new row in the format of an hash to a table
# If there is a key in the hash which is not present in the table columns, we add a new column
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

# Retrieve programme for each date and store the responses in the array programmes
# A programme contains a list of reunions, which contains a list of courses 
urls = ["https://online.turfinfo.api.pmu.fr/rest/client/1/programme/%s?meteo=true&specialisation=INTERNET" % date for date in daterange()]
programmes = scrap_urls(urls, "PROGRAMMES")


print("\n> FILLING COURSES AND REUNIONS TABLES...")
# Create the tables for storing reunions data and courses data
reunions = []
reunions_columns = ['date']
courses = []
courses_columns = []
bad_response_programmes = []
bad_response_columns = ['url', 'status_code']

reunion_id = 0
course_id = 0

for url, programme in tqdm(programmes):
    # Just in case so that .json() doesn't crash
    if(programme.status_code == 200):
        programme_json = programme.json()['programme']
        date = datetime.fromtimestamp(programme_json['date']//1000).strftime("%d%m%Y")

        for reunion in programme_json['reunions']:
            reunion_courses = reunion.pop('courses', None)
            reunion['reunion_id'] = reunion_id
            reunion['date'] = date
            reunions, reunions_columns = add_row(reunions, reunions_columns, reunion)
            for course in reunion_courses:
                course['reunion_id'] = reunion_id
                course['course_id'] = course_id
                courses, courses_columns = add_row(courses, courses_columns, course)
                course_id += 1
            reunion_id += 1
    else:
        bad_response_programmes.append([url, programme.status_code])

print("\n> SAVING TABLES...")
df_reunions = pd.DataFrame(reunions, columns = reunions_columns)
df_courses = pd.DataFrame(courses, columns = courses_columns)
df_bad_response_programmes = pd.DataFrame(bad_response_programmes, columns = bad_response_columns)

df_reunions.to_csv(os.path.join(data_folder, "reunions.csv"))
df_courses.to_csv(os.path.join(data_folder, "courses.csv"))
df_bad_response_programmes.to_csv(os.path.join(data_folder, "bad_response_programmes%s_%s.csv" % (date_start, date_end)))



# Retrieve participants for each race
# We start by storing the urls corresponding to the api calls needed to get the data
urls = []
rapports_urls = []

url_to_course_id = {}
numReunion_index, numOrdre_index = courses_columns.index('numReunion'), courses_columns.index('numOrdre')
reunion_id_index, course_id_index = courses_columns.index('reunion_id'), courses_columns.index('course_id')
for course in courses:
    course_number = "R%s/C%s" % (course[numReunion_index], course[numOrdre_index])
    reunion_id, course_id = course[reunion_id_index], course[course_id_index]
    date = df_reunions.query('reunion_id == %s' % reunion_id).iloc[0]['date']
    url = "https://online.turfinfo.api.pmu.fr/rest/client/1/programme/%s/%s/participants?specialisation=INTERNET" % (date, course_number)
    urls.append(url)
    url_to_course_id[url] = course_id

    rapports_url = "https://online.turfinfo.api.pmu.fr/rest/client/1/programme/%s/%s/rapports-definitifs" % (date, course_number)
    rapports_urls.append(rapports_url)
    url_to_course_id[rapports_url] = course_id

# Here we actually do api calls
courses_participants = scrap_urls(urls, "PARTICIPANTS")
rapports = scrap_urls(rapports_urls, "RAPPORTS")

print("\n> FILLING  PARTICIPANTS AND RAPPORTS TABLES...")
# And again we store everything in the table participants
participants = []
participants_columns = []
bad_response_participants = []

participant_id = 0

for url, course_participants in tqdm(courses_participants):
    if(course_participants.status_code == 200):
        participants_json = course_participants.json()['participants']
        for participant in participants_json:
            participant['course_id'] = url_to_course_id[url]
            participant['participant_id'] = participant_id
            participants, participants_columns = add_row(participants, participants_columns, participant)
            participant_id += 1
    else:
        bad_response_participants.append([url, course_participants.status_code])

rapports_definitifs = {}
for url, rapport in tqdm(rapports):

    if(rapport.status_code == 200):
        rapports_definitifs[url_to_course_id[url]] = rapport.json()
    else:
        rapports_definitifs[url_to_course_id[url]] = "Scraping failed"

print("\n> SAVING TABLES...")
df_participants = pd.DataFrame(participants, columns = participants_columns)
df_bad_response_participants = pd.DataFrame(bad_response_participants, columns = bad_response_columns)

df_participants.to_csv(os.path.join(data_folder, "participants.csv"))
df_bad_response_participants.to_csv(os.path.join(data_folder, "bad_response_participants.csv"))

with open(os.path.join(data_folder, "rapports_definitifs.json"), "w") as f:
    json.dump(rapports_definitifs, f, indent=4, sort_keys=True)