import requests #Used to make HTTP requests to the API.
from xlwt import Workbook #Typically used to write data to Excel files
import smtplib  #Used for sending email.
from os.path import basename #Used to get the base name of a path

#Used to create email messages with attachments.
from email.mime.application import MIMEApplication  
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

# Used for formatting email addresses and dates.
from email.utils import COMMASPACE,formatdate

BASE_URL = 'https://remoteok.com/api/'  #The URL of the RemoteOK API.

#A string representing the user agent, which identifies the browser or client making the request. To check in--(https://www.whatismybrowser.com/)
USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' 
REQUEST_HEADER={
    'User-Agent':USER_AGENT,
    'Accept-Language':'en-US,en;q=0.5'
    } #A dictionary containing request headers, including the user agent and accept language.


def get_job_posting():
    res = requests.get(url=BASE_URL, headers=REQUEST_HEADER)
    return res.json()


def output_jobs_to_xls(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs')
    headers = list(data[0].keys())
    for i in range(0, len(headers)):
        job_sheet.write(0, i, headers[i])
    for i in range(0, len(data)):
        job = data[i]
        values = list(job.values())
        for x in range(0, len(values)):
            job_sheet.write(i + 1, x, values[x])
    wb.save('remote_jobs.xls')


def send_email(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
        msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login(send_from, 'ENTER-YOUR-GOOGLE-APP-PASSWORD')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == "__main__":
    data = get_job_posting()[1:]
    output_jobs_to_xls(data)
    send_email('from@gmail.com', ['to@gmail.com'],
               'jobs posting', 'Please, Find attached a list of jobs posting to this email', files=['remote_jobs.xls'])
