#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import smtplib to provide email functions
Send an HTML email with an embedded image and a plain text message
for email clients that don't want to display the HTML.
"""
import json
import time
from datetime import datetime
from smtplib import SMTP_SSL
import platform
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


import config as config


class SendEmail:
    openFileHTML = json.load(open(config.path + 'openFileHTML.json'))

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = config.subject
    msgRoot['From'] = config.strFrom

    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in
    # an 'alternative' part, so message agents can decide which they
    # want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    reportTime = str(open(config.path + "reportTime", "r").read())
    NetworkError = str(open(config.path + "erroSys.html", "r").read())
    reportHtml = str(open(config.path + openFileHTML['body'],
                          "r").read()).replace('%REPORTTIME%',
                                               reportTime).replace(
        '%NetworkError%', NetworkError)

    msgText = MIMEText(reportHtml, 'html')
    msgAlternative.attach(msgText)

    # Send the email (this example assumes SMTP
    # authentication is required)
    toEmails = config.emails
    msgRoot['To'] = ', '.join(toEmails)

    def send_email_to(self, to_email, num_error):
        try:
            print('Send ' + str(datetime.now()) + " " + to_email)
            smtp = SMTP_SSL(config.smtp_server, 465)
            smtp.login(config.smtp_user, config.smtp_pass)
            smtp.sendmail(config.strFrom, to_email,
                          self.msgRoot.as_string())
            smtp.quit()
        except Exception as e:
            if num_error < config.numberAttempts:
                print("""There was an error sending the email. Check the 
                    smtp settings.\n""" + str(e))
                time.sleep(config.waitingTime)
                self.send_email_to(to_email, num_error + 1)

    def set_image(self, img, cid):
        fp = open(config.path + img, 'rb')
        msg_image = MIMEImage(fp.read())
        fp.close()
        msg_image.add_header('Content-ID', '<{}>'.format(cid))
        self.msgRoot.attach(msg_image)
        pass

    def main(self):
        print('Main send Email')
        if not self.openFileHTML['error']:
            for img in config.imgs:
                self.set_image(img['img'], img['cid'])
            pass
        for to_email in self.toEmails:
            self.send_email_to(to_email, 0)
            pass
        pass
