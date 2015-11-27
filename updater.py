import urllib.request
from bs4 import BeautifulSoup
import smtplib
import datetime
from email.mime.text import MIMEText
com_url = 'http://xkcd.com/'
latest = ''
username = 'EMAIL' #Replace with your email
password = 'PASSWORD' #replace with your password
destination = 'DESTINATION' #The destination for the email

def scrape_com():
    with urllib.request.urlopen(com_url) as response:
        com_doc = response.read()
    soup = BeautifulSoup(com_doc, 'html.parser')
    try:
        comic_url = 'http:' + soup.find(id='comic').img.get('src')
    except:
        comic_url = com_url
    return comic_url


def check_comic(comic_url):
    with open('xkcd_ver.txt') as f:
        if comic_url != f.read():
            with open('xkcd_ver.txt', 'w') as fo:
                fo.write(str(comic_url))
            return True
        else:
            return False


def pun(): 
    with urllib.request.urlopen('http://badpuns.com/jokes.php?section=oneline&pos=random') as response:
        rand_pun = response.read()
    soup = BeautifulSoup(rand_pun, 'html.parser')
    bad_pun = soup.find('div', class_='joke_body_text').get_text()
    return bad_pun


def mail(fin_msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, destination, str(fin_msg))
    server.quit()


def build_mail(sen_msg):
    msg = MIMEText(sen_msg.encode('utf-8'), _charset='utf-8')
    msg["From"] = "spartyupdate@example.com"
    msg["To"] = "sparty48@example.com"
    msg["Subject"] = str(datetime.date.today()) + "'s update"
    mail(msg)


def main():
    send = False
    prep_msg = ''
    comic_url = scrape_com()
    if check_comic(comic_url):
        send = True
    if comic_url != com_url:
        prep_msg += "Your new xkcd can be found at {0}\n\n".format(comic_url)
    else:
        prep_msg += "Something went wrong, the image can't be found"
    #prep_msg += "Your bad pun today: {0}".format(pun())
    if send:
        build_mail(prep_msg)

main()
