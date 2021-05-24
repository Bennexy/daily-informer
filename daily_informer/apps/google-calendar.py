from __future__ import print_function
import datetime
import pickle
import sys
import os.path
import regex as re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
sys.path.append('.')

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def google_calendar():
    ret = []
    aller = []
    """
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(os.getcwd(), 'daily_informer', 'src', 'google', 'token.pickle')):
        with open(os.path.join(os.getcwd(), 'daily_informer', 'src', 'google', 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(os.getcwd(), 'daily_informer', 'src', 'google', 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.join(os.getcwd(), 'daily_informer', 'src', 'google', 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=20, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print(None)
        return None
    for event in events:
        #print(event['start'], datum_iso())
        #print(event['summary'])

        if 'date' in event['start']:
            if datum_iso() in event['start']['date']:
                ret.append([datum_iso(), event['summary']])
            
        else:
            if reg_start_date(event['start'].get("dateTime")) == datum_iso():
                times = reg_time(event['start'].get("dateTime"))
                ret.append([datum_iso(), event['summary'], times[0][0], times[1][0]])

        start = event['start'].get('dateTime', event['start'].get('date'))
        aller.append(start + event['summary'])

    
    return ret

def reg_start_date(event_date):

    regex_pattern = r"\d{4}-\d{2}-\d{2}"

    return re.findall(regex_pattern, event_date)[0]

def reg_time(event_data):
    reg_start = r"(?<=T)\d{2}:\d{2}"
    reg_end = r"(?<=\+)\d{2}:\d{2}"

    return [re.findall(reg_start, event_data), re.findall(reg_end, event_data)]

def datum_iso():

    d = datetime.datetime.now()

    return d.strftime("%Y") + "-" + d.strftime("%m") + "-" + d.strftime("%d")

def calendar_data_read():
    sorted_data = {}
    sorted_data['events-today'] = google_calendar()
    return sorted_data

if __name__ == '__main__':

    print(calendar_data_read())

