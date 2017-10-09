from bs4 import BeautifulSoup
import requests
import smtplib
import sys

# assumes command form is python script.py user pass another_email
EMAIL_USER = sys.argv[1]
EMAIL_PASSWORD = sys.argv[2]
ADDITIONAL_TO_EMAIL = sys.argv[3]
STATUS_FILE = 'temp-status.txt'

def row_matches(row, title):
    try:
        return row.td.div.string == title
    except Exception as e:
        return False

def row_float_value(row):
    return float(row.find_all('td')[1].input['value'])

def send_email(subject, text):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(
        EMAIL_USER,
        [EMAIL_USER, ADDITIONAL_TO_EMAIL],
        'Subject: {}\n\n{}'.format(subject, text)
    )
    server.close()

def write_temp_status():
    global last_status
    last_status = 'indoor' if indoorTemp > outdoorTemp else 'outdoor'
    with open(STATUS_FILE, 'w') as f:
        f.write(last_status)

# get data from ambient weather observerIP 3.0 website
r = requests.get('http://192.168.0.99/livedata.htm', timeout=10)
soup = BeautifulSoup(r.text, 'html.parser')

# parse data
form = soup.find('form')

# go through rows and extract indoor and outdoor temps
for row in form.find_all('tr'):
    if row_matches(row, 'Indoor Temperature'):
        indoorTemp = row_float_value(row)
    elif row_matches(row, 'Outdoor Temperature'):
        outdoorTemp = row_float_value(row)

# get last know status
try:
    with open(STATUS_FILE) as f:
        last_status = f.read()
except Exception as e:
    # file probably doesn't exist, create a new one with current status
    write_temp_status()

# compare to last know status
if last_status == 'indoor':
    if outdoorTemp > indoorTemp:
        send_email(
            "It's warmer outdoors now",
            'Outdoor temperature ({}) is now warmer than indoor temperature ({})'.format(outdoorTemp, indoorTemp)
        )
        write_temp_status()
else:
    if indoorTemp > outdoorTemp:
        send_email(
            "It's warmer indoors now",
            'Indoor temperature ({}) is now warmer than outdoor temperature ({})'.format(indoorTemp, outdoorTemp)
        )
        write_temp_status()
