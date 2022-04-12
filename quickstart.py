# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# good stuff 
# https://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html
# https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html#envs
# https://loft.sh/blog/python-django-development-on-kubernetes-with-devspace/

# [START gmail_quickstart]
from __future__ import print_function

import os
import re
import sys
# for encoding/decoding messages in base64
import time
from base64 import urlsafe_b64decode
# from common import gmail_authenticate, search_messages

import base64
import os.path
import markdownify
from datetime import datetime

import jsons
import pytz as pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

from commit import commit

est = pytz.timezone('America/Denver')

WRITE_SECONDARY_FILES=False
# If modifying these scopes, delete the file credentials.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
bodies = []

SIGNATURE = '''<p style="color:rgb(0,0,0);font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:14px;margin-bottom:15px"><a href="mailto:chase@gfic.io" style="color:rgb(251,229,162);font-weight:bold;display:inline" target="_blank">Chase Gibbons</a>&nbsp;/&nbsp;<span style="color:rgb(68,68,68)">Manager</span>&nbsp;<span style="color:rgb(68,68,68)"></span><br><a href="tel:435-248-0677" style="color:rgb(68,68,68);font-weight:bold;display:inline" target="_blank">435-248-0677</a></p>\n<p style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:14px;color:rgb(33,33,33);margin-bottom:10px"><a href="https://www.gfic.io" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://www.gfic.io&amp;source=gmail&amp;ust=1649794186074000&amp;usg=AOvVaw0d-aPEkq-0BEYTYyO4wPat"><img src="https://ci5.googleusercontent.com/proxy/8VkmwA4e5rRc2WaUiul-fToaEmPH7DY7CEoVztjamiwbSLpaVsytJe-KY9xckml8xyojyxMSzxM9yttuUWQ2JEl43Q=s0-d-e1-ft#http://zoogle.imgix.net/gfic_logo.png?h=50&amp;w=150" alt="">&nbsp;</a><br><span style="color:rgb(68,68,68)">PO Box 747</span><span style="display:block"></span><span style="color:rgb(68,68,68)">Logan, UT 84321</span>&nbsp;<br><a href="https://www.gfic.io" style="color:rgb(251,229,162);display:inline" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://www.gfic.io&amp;source=gmail&amp;ust=1649794186074000&amp;usg=AOvVaw0d-aPEkq-0BEYTYyO4wPat">gfic.io</a></p>\n<p style="color:rgb(0,0,0);font-size:0px;line-height:0;font-family:Helvetica,Arial,sans-serif"><a href="https://twitter.com/gfic" style="display:inline" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://twitter.com/gfic&amp;source=gmail&amp;ust=1649794186074000&amp;usg=AOvVaw1hDPf0xi3Jgu4N_YShteue"><img src="https://ci3.googleusercontent.com/proxy/ni9IQ93mdSv5aafQ3fQiOcAUEktglKXQl548b5BqBO4SjQ_icjQ8MjYlqEp8cMGk2A4mm-nXu6Qpc21vbZCQtQ=s0-d-e1-ft#http://zoogle.imgix.net/twitter.png?h=16&amp;w=16" alt="Twitter" style="margin-bottom:2px;border:none;display:inline">&nbsp;</a><span style="white-space:nowrap"><img src="https://ci3.googleusercontent.com/proxy/87dbxbAKZxqMJ5B-UgIc9GGo9H9cEACGc7vS-o87dWcQh9WWUyuMEca8FywQVCxePFn89vSw1pSOBZMoQQ=s0-d-e1-ft#http://zoogle.imgix.net/spacer.gif?h=1&amp;w=2" width="2">&nbsp;</span><a href="https://www.facebook.com/gfic/" style="display:inline" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://www.facebook.com/gfic/&amp;source=gmail&amp;ust=1649794186074000&amp;usg=AOvVaw2t77O0R0xS6sULgDctuSdq"><img src="https://ci4.googleusercontent.com/proxy/etHZaDtSDw6euctZCofAOF5BvhADNRc3KZO7bFs02sfxFSrCqGvRTlVqu8a-Ws2-7ByRI5pt8q58bYqa4tFmCWI=s0-d-e1-ft#http://zoogle.imgix.net/facebook.png?h=16&amp;w=16" alt="Facebook" style="margin-bottom:2px;border:none;display:inline">&nbsp;</a><span style="white-space:nowrap"><img src="https://ci6.googleusercontent.com/proxy/__bX3lyRh1gRMlQZRbUKVW_Uyu1Uuxrdz2-6QOP76ljRZn6Hf6NRnhFH3ExTUe4ekP6SodYtQZ37cSnW6w=s0-d-e1-ft#http://zoogle.imgix.net/spacer.gif?w=2&amp;h=1" width="2">&nbsp;</span><a href="https://www.linkedin.com/company/gfic" style="display:inline" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://www.linkedin.com/company/gfic&amp;source=gmail&amp;ust=1649794186074000&amp;usg=AOvVaw1jxETS4aOg2Ud1mzi4Ei1G"><img src="https://ci6.googleusercontent.com/proxy/TJ0o8fvaZcKc13sty_1vlGeFOWHS0iErJb-_FkaoljhgfefmsmqO1ulEPZlQRBkVp1TKDm3lJc-KZCdBoEHXmxc=s0-d-e1-ft#http://zoogle.imgix.net/linkedin.png?h=16&amp;w=16" alt="LinkedIn" style="margin-bottom:2px;border:none;display:inline">&nbsp;</a><span style="white-space:nowrap"><img src="https://ci3.googleusercontent.com/proxy/87dbxbAKZxqMJ5B-UgIc9GGo9H9cEACGc7vS-o87dWcQh9WWUyuMEca8FywQVCxePFn89vSw1pSOBZMoQQ=s0-d-e1-ft#http://zoogle.imgix.net/spacer.gif?h=1&amp;w=2" width="2"></span></p>'''

def mySortFunc(e):
  return datetime.fromtimestamp(int(e['internalDate']) / 1000).astimezone(est).strftime("%Y/%m/%d %H:%M:%S")

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file credentials.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        # # Save the credentials for the next run
        # with open('token.json', 'w') as token:
        #     token.write(creds.to_json())

    try:
        # Call the Gmail API
        results = []
        service = build('gmail', 'v1', credentials=creds)
        labels_raw = service.users().labels().list(userId='me').execute()
        labels = labels_raw.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')

        label_timeline = [x for x in labels if x['name'] == 'DustyTimelineReadme'][0]

        messages_raw = service.users().messages().list(userId='me', labelIds=label_timeline['id'], maxResults=500).execute()

        if messages_raw.get('nextPageToken', None):
            messages_raw = messages_raw + service.users().messages().list(userId='me', labelIds=label_timeline['id'], pageToken=messages_raw['nextPageToken']).execute()

        messages = [service.users().messages().get(id=message['id'], userId='me').execute() for message in messages_raw.get('messages', {})]
        messages.sort(key=mySortFunc)

        print(len(messages))

        for message_full in messages:
            # message_full = service.users().messages().get(id=message['id'], userId='me').execute()
            # message_full = message_full.get('parts', {}).get('body', {}).get('data', '')
            all_message_bodies = read_message(service, message_full)
            message_full['all_message_bodies'] = [body for body in all_message_bodies]
            print(str(message_full))
            results.append(message_full)

        print(str(bodies))

        for i, body in enumerate(bodies):
            # with open(os.path.join('README.md'), "wb") as f:

            # data = data.replace("-", "+").replace("_", "/").encode('utf-8')
            # decoded_data = base64.b64decode(data)
            # # decoded_data = urlsafe_b64decode(data)
            # # f.write(decoded_data)
            # # Now, the data obtained is in lxml. So, we will parse
            # # it with BeautifulSoup library
            # # soup = BeautifulSoup(decoded_data, "lxml")
            # # body = soup.body()
            # # decoded_data = urlsafe_b64decode(data)
            markdown = markdownify.markdownify(body['body'], heading_style="ATX")
            # f.write(body['data'])
            sanitized_markdown = markdown.replace(SIGNATURE, '')
            x = re.search("If this ever goes to court then", sanitized_markdown)

            if x is None:

                with open(os.path.join('README.md'), "w", encoding='utf-8') as f:
                    f.write(sanitized_markdown)

                commit(commit_msg=body['tag_name'] + " " + body['subject'],
                       tag_name=body['tag_name'])
                time.sleep(2)
                print('push {}'.format(i))
            else:
                with open(os.path.join('README.simple.md'), "w", encoding='utf-8') as f:
                    f.write(sanitized_markdown)
                commit(commit_msg="{} {} (Simple)".format(body['tag_name'], body['subject']),
                       tag_name=body['tag_name'])
                time.sleep(2)
                print('push {}'.format(i))


        import json
        with open('results.json', 'w') as fp:
            try:
                json.dump(results, fp)
            except Exception as e:
                pass
            finally:
                print('finished')


            # if message['labelId'] == label_timeline['id']
        # messages_ = [message for message in messages.get('messages', {})]

        # for msg in messages_w_timeline_label:
        #     print(str(msg))
        #     # print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def parse_parts(service, subject, parts, folder_name, filename, message, tag_name):
    all_parts_bodies = []
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            fname = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                sub_parts_bodies = parse_parts(service, subject, part.get("parts"), folder_name, filename, message, tag_name)
                all_parts_bodies = all_parts_bodies + sub_parts_bodies
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    # text = urlsafe_b64decode(data).decode()
                    # print(text)
                    filepath = os.path.join(folder_name, filename + '__' + subject + '.txt')
                    print("Saving plaintext to", filepath)
                    with open(filepath, "w", encoding='utf-8') as f:
                        data = data.replace("-", "+").replace("_", "/").encode('utf-8')
                        decoded_data = base64.b64decode(data)
                        # decoded_data = urlsafe_b64decode(data)
                        # f.write(decoded_data)
                        # Now, the data obtained is in lxml. So, we will parse
                        # it with BeautifulSoup library
                        # soup = BeautifulSoup(decoded_data, "lxml")
                        # body = soup.body()
                        # decoded_data = urlsafe_b64decode(data)
                        if WRITE_SECONDARY_FILES:
                            f.write(decoded_data.decode('utf-8'))

                        all_parts_bodies.append({ 'body': decoded_data, 'subject': subject, 'tag_name': tag_name })
                        bodies.append({ 'body': decoded_data, 'subject': subject, 'tag_name': tag_name })
            elif mimeType == "text/html":
                if data:
                    # # if the email part is an HTML content
                    # # save the HTML file and optionally open it in the browser
                    # if not filename:
                    #     filename = "index.html"
                    filepath = os.path.join(folder_name, filename + '__' + subject + '.html')
                    print("Saving HTML to", filepath)

                    # http://blog.conceptnet.io/posts/2012/fixing-common-unicode-mistakes-with-python-after-theyve-been-made/
                    # https://www.justinweiss.com/articles/how-to-get-from-theyre-to-theyre/
                    with open(filepath, "wb") as f:
                        # data = data.encode("Windows-1252")
                        decoded_data = urlsafe_b64decode(data)

                        # Now, the data obtained is in lxml. So, we will parse
                        # it with BeautifulSoup library
                        # soup = BeautifulSoup(decoded_data, "lxml")
                        # body = soup.body()
                        # decoded_data = urlsafe_b64decode(data)
                        if WRITE_SECONDARY_FILES:
                            f.write(b'<meta charset="utf-8">\n' + decoded_data)

                        all_parts_bodies.append({ 'body': decoded_data, 'subject': subject, 'tag_name': tag_name })
                        # bodies.append({ 'body': decoded_data, 'subject': subject, 'tag_name': tag_name })
                        # data = data.replace("-", "+").replace("_", "/")
                        # decoded_data = base64.b64decode(data.encode('utf8'))
                        # decoded_data = urlsafe_b64decode(data.encode('utf8')

                        # # Now, the data obtained is in lxml. So, we will parse
                        # # it with BeautifulSoup library
                        # soup = BeautifulSoup(decoded_data, "lxml")
                        # body = soup.body()
                        # f.write(body)
            else:
                # attachment other than a plain text or HTML
                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")
                    if part_header_name == "Content-Disposition":
                        if "attachment" in part_header_value:
                            # we get the attachment ID
                            # and make another request to get the attachment itself
                            try:
                                print("Saving the file:", part.get("filename"), "size:", get_size_format(file_size))
                                attachment_id = body.get("attachmentId")
                                attachment = service.users().messages() \
                                            .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                                data = attachment.get("data")
                                filepath = os.path.join(folder_name, filename + '__Attachment__' + part.get("filename"))
                                if data and WRITE_SECONDARY_FILES:
                                    with open(filepath, "wb") as f:
                                        f.write(base64.urlsafe_b64decode(data))
                            except Exception as e:
                                pass

    return all_parts_bodies

# https://www.geeksforgeeks.org/how-to-read-emails-from-gmail-using-gmail-api-in-python/
def read_message(service, message):
    all_msg_bodies = []
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    sent_date = None
    date_local = datetime.fromtimestamp(int(msg['internalDate']) / 1000).astimezone(est)
    # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(msg['internalDate'])))
    # date = datetime.fromtimestamp(int(msg['internalDate'])).strftime('%Y-%m-%d %H:%M:%S')
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                # make a directory with the name of the subject
                # folder_name = clean(date)

                folder_name = datetime.fromtimestamp(int(msg['internalDate']) / 1000).astimezone(est).strftime("%Y/%m/%d")
                filename = datetime.fromtimestamp(int(msg['internalDate']) / 1000).astimezone(est).strftime(
                    "%H-%M-%S")


                # we will also handle emails with the same subject name
                folder_counter = 0
                # while os.path.isdir(folder_name):
                #     folder_counter += 1
                #     # we have the same folder name, add a number next to it
                #     if folder_name[-1].isdigit() and folder_name[-2] == "_":
                #         folder_name = f"{folder_name[:-2]}_{folder_counter}"
                #     elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                #         folder_name = f"{folder_name[:-3]}_{folder_counter}"
                #     else:
                #         folder_name = f"{folder_name}_{folder_counter}"
                if not os.path.isdir(folder_name):
                    os.makedirs(folder_name, exist_ok=True)

                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
                print('areDatesEqual', msg['internalDate'] == value)
                sent_date = value
                # folder_name = datetime.fromtimestamp(int(value) / 1000).astimezone(est).strftime("%Y/%m/%d")
                # filename = datetime.fromtimestamp(int(value) / 1000).astimezone(est).strftime(
                #     "%H-%M-%S")
    if not has_subject:
        # if the email does not have a subject, then make a folder with "email" name
        # since folders are created based on subjects
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name, exist_ok=True)

    subject = [header['value'] for header in headers if header['name'] == 'Subject'][0]
    tag_name = datetime.fromtimestamp(int(msg['internalDate']) / 1000).astimezone(est).strftime("%Y.%m.%d_%H.%M.%S")
    all_msg_bodies = parse_parts(service, subject, parts, folder_name, filename, message, tag_name)
    print("="*50)
    # commit(commit_msg=subject, tag_name=datetime.fromtimestamp(int(msg['internalDate']) / 1000).astimezone(est).strftime("%Y.%m.%d_%H.%M.%S"))
    return all_msg_bodies


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(str(e))
# [END gmail_quickstart]
