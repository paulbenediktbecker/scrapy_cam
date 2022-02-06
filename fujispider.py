import scrapy
import scrapydo
from scrapy import Spider, signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy import signals
import ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json
import time 

import spider_database

'''
There has to be a file called secret.json :

{
    "1":{
        "passwort_g":"", //password of sender mail
        "recipent": "['test@gmail.com']",
        "sender_email": "testdev@gmail.com",
    }
}   


'''




def spider_results(all_spiders):
    results = []
    for spider in all_spiders:
        results.append(scrapydo.run_spider(spider))
    return results
def parse_json():
        with open("secret.json") as f:
            data = json.load(f)

        return data[str(1)]
    
def send_mail(personal_data, new_result, old_result, url, ):
    passwort_g = personal_data["passwort_g"]
    recipent = personal_data["recipent"]
    sender_email = personal_data["sender_email"]
    

    message_content = f"""Change detected !
    From: {old_result}
    to: {new_result}
    url: {url}"""

    port = 465  # For SSL
    context = ssl.create_default_context()
    msg = MIMEMultipart()
    msg.attach(MIMEText(
        message_content))
    msg['Subject'] = 'Fuji'
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipent)  # Therefore you can achieve mutliple recipents

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, passwort_g)
        print("Login for E-Mail")
        server.sendmail(sender_email, recipent, msg.as_bytes())
        print("Email send")


def send_error_mail(personal_data):
    passwort_g = personal_data["passwort_g"]
    recipent = personal_data["recipent"]
    sender_email = personal_data["sender_email"]
    

    message_content = "Error in Fuji script ! "

    port = 465  # For SSL
    context = ssl.create_default_context()
    msg = MIMEMultipart()
    msg.attach(MIMEText(
        message_content))
    msg['Subject'] = 'Fuji'
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipent)  # Therefore you can achieve mutliple recipents

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, passwort_g)
        print("Login for E-Mail")
        server.sendmail(sender_email, recipent, msg.as_bytes())
        print("Email send")
   
if __name__ == '__main__':
    personal_data = parse_json()
    try:
        scrapydo.setup()
        
        all_spiders = spider_database.get_all_spiders()
        
        
        scrape_base = spider_results(all_spiders)
        minutes_to_wait = 5
        seconds_to_wait = 60 * minutes_to_wait
        
        counter = 1
        while True:
            print(f"SCRAPING NEW ENTRY: {counter}")
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print(current_time)
            print("#########################################################################################################")

            scrape_new = spider_results(all_spiders)
            found_change = False
            for result_old, result_new in zip(scrape_base, scrape_new):

                status_old = result_old[0]["status"]
                status_new = result_new[0]["status"]
                print(status_new)
                if( status_old != status_new): # if they are not the same
                    print("#########################################################################################################")
                    print(f"FOUND CHANGE. WILL SEND MAIL. WILL WAIT FOR {minutes_to_wait} MINUTES.")
                    send_mail(personal_data,status_new, status_old, result_old[0]["url"])
                    found_change = True
                    break
            if not found_change:
                print("#########################################################################################################")
                print(f"NO NEW CHANGES FOUND. WILL WAIT FOR {minutes_to_wait} MINUTES.")
            scrape_base = scrape_new
            time.sleep(seconds_to_wait)
            counter +=1
    except:
        send_error_mail(personal_data)
        