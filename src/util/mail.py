from smtplib import *
import threading
import traceback
import subprocess

from django.core.mail import send_mail

from src.config import ServerMail, ServerMailPassword


def SendMail(a_recipient, a_subject, a_message):
    recipient = uniq(a_recipient)
    sender = "Singapore Government Hospital <%s>" % ServerMail

    msg = "Dear Ms/Mr, \n\n" + a_message + "\n\nRegards, \nSingapore Government Hospital \n\n--------------------------------------------------------------------------- \nThis is a computer generated email. No reply is required."
    for eachEmail in recipient:

        message = """\
From:  %s
To: %s
Subject: %s

%s
""" % (sender, eachEmail, a_subject, msg)

        try:
            s = SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(ServerMail, ServerMailPassword)
            s.sendmail(ServerMail, eachEmail, message)
            s.quit()
        except SMTPException:
            print "Error: unable to send email"

def uniq(alist):    # Fastest order preserving
    set = {}
    return [set.setdefault(e,e) for e in alist if e not in set]
