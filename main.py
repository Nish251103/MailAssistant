# import google.generativeai as genai
# genai.configure(api_key='')
# model = genai.GenerativeModel('gemini-pro')
# responses = model.generate_content("what is bardai")
# all_responses = []
# for response in responses:
#     for part in response.parts:
#         if part.text:
#             all_responses.append(part.text)
# print(all_responses)

import os
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.send', 
          'https://www.googleapis.com/auth/calendar']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def get_email_messages(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    email_contents = []
    for message in messages[:5]:  # Limiting to 5 messages for example
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                email_contents.append(base64.urlsafe_b64decode(part['body']['data']).decode('utf-8'))
    return email_contents

import requests
import google.generativeai as genai
def google_genai_api_call_summarize(content):
        
    genai.configure(api_key='')
    model = genai.GenerativeModel('gemini-pro')
    responses = model.generate_content(content+"\n"+"Sumarize the above content")
    all_responses = []
    for response in responses:
        for part in response.parts:
            if part.text:
                all_responses.append(part.text)
    return " ".join(all_responses)



def google_genai_api_call_generate_response(summary):
    genai.configure(api_ke')
    model = genai.GenerativeModel('gemini-pro')
    responses = model.generate_content(summary+"\n"+"Create a email response for the above email message")
    all_responses = []
    for response in responses:
        for part in response.parts:
            if part.text:
                all_responses.append(part.text)
    return " ".join(all_responses)
    


def summarize_email(content):
    return google_genai_api_call_summarize(content)

def generate_response(summary):
    return google_genai_api_call_generate_response(summary)


def send_email(service, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
    raw = raw.decode('utf-8')
    body = {'raw': raw}
    try:
        message = service.users().messages().send(userId='me', body=body).execute()
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def create_event(service, summary, start_time, end_time):
    event = {
      'summary': summary,
      'start': {
        'dateTime': start_time,
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': end_time,
        'timeZone': 'America/Los_Angeles',
      },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def summarize_email(content):
    return google_genai_api_call_summarize(content)

def generate_response(summary):
    return google_genai_api_call_generate_response(summary)
# def main():
#     

#     gmail_service = get_gmail_service()
#     calendar_service = get_calendar_service()

#     # Read and process emails
#     messages = get_email_messages(gmail_service)
#     for message in messages:
#         summary = summarize_email(message)
#         response = generate_response(summary)

#         # Send email response
#         send_email(gmail_service, 'recipient@example.com', 'Re: ' + 'Subject', response)

#         # Schedule a meeting if necessary
#         if 'schedule a meeting' in summary.lower():
#             create_event(calendar_service, 'Meeting', '2023-07-01T09:00:00-07:00', '2023-07-01T10:00:00-07:00')

# if __name__ == '__main__':
#     main()

def main():
    print("Starting script...")
    gmail_service = get_gmail_service()
    calendar_service = get_calendar_service()

    # Read and process emails
    print("Fetching emails...")
    messages = get_email_messages(gmail_service)
    print(f"Fetched {len(messages)} messages.")

    for message in messages:
        summary = summarize_email(message)
        print(f"Summarized email: {summary}")

        response = generate_response(summary)
        print(f"Generated response: {response}")

        # Send email response
        to = "aaron.a.noronha@gmail.com"
        send_email(gmail_service, to, 'Re: ' + 'Subject', response)
        print("Email sent.")

        # Schedule a meeting if necessary
        if 'schedule a meeting' in summary.lower():
            create_event(calendar_service, 'Meeting', '2023-07-01T09:00:00-07:00', '2023-07-01T10:00:00-07:00')
            print("Meeting scheduled.")

if __name__ == '__main__':
    main()







# import os
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# # If modifying these SCOPES, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
#           'https://www.googleapis.com/auth/gmail.send', 
#           'https://www.googleapis.com/auth/calendar']

# def get_gmail_service():
#     creds = None
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#     return build('gmail', 'v1', credentials=creds)

# def get_calendar_service():
#     creds = None
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#     return build('calendar', 'v3', credentials=creds)

# if __name__ == '__main__':
#     # This will initiate the authentication flow and create the token.json file
#     gmail_service = get_gmail_service()
#     calendar_service = get_calendar_service()
