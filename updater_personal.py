import urllib.request
from bs4 import BeautifulSoup
import smtplib
import datetime
from email.mime.text import MIMEText
com_url = 'http://xkcd.com/'
ap_url = 'http://shortorderfiction.com/'
latest = ''


def scrape_com():
    with urllib.request.urlopen(com_url) as response:
        com_doc = response.read()
    soup = BeautifulSoup(com_doc, 'html.parser')
    try:
        comic_url = 'http:' + soup.find(id='comic').img.get('src')
    except:
        comic_url = com_url
    return comic_url


def ap_latest():
    global latest
    with urllib.request.urlopen(ap_url) as response:
        ap_doc = response.read()
    soup = BeautifulSoup(ap_doc, 'html.parser')
    latest = soup.findAll('a')[3].get('href')


def scrape_ap():
    global latest
    with urllib.request.urlopen(latest) as response1:
        latest_doc = response1.read()
    soup1 = BeautifulSoup(latest_doc, 'html.parser')
    texts = soup1.find('div', class_='entry-content').findAll('p')
    final_text = ''
    for x in texts:
        final_text += x.get_text() + '\n\n'
    return final_text


def check_comic(comic_url):
    with open('xkcd_ver.txt') as f:
        if comic_url != f.read():
            with open('xkcd_ver.txt', 'w') as fo:
                fo.write(str(comic_url))
            return True
        else:
            return False


def check_ap(url):
    with open('ap_ver.txt', 'r') as f:
        if url != f.read():
            with open('ap_ver.txt', 'w') as fo:
                fo.write(str(url))
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
    server.login("spartyupdate@gmail.com", "C[u[M9/u?{5w:V87") #Don't be taking this
    server.sendmail("spartyupdate@gmail.com", "sparty48@gmail.com", str(fin_msg))
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
    ap_latest()
    if comic_url == com_url:
        prep_msg += "Something went wrong, the image can't be found.\n\n"
    elif check_comic(comic_url):
        prep_msg += "Your new xkcd can be found at {0}".format(comic_url)
    if check_ap(latest):
        send = True
        prep_msg += "Here is the latest A.P. Boland Story: \n\n {0}".format(scrape_ap())
    prep_msg += "Your bad pun today: {0}".format(pun())
    if send:
        build_mail(prep_msg)

main()
