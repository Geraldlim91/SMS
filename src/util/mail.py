import smtplib
import threading
import traceback

from django.core.mail import send_mail

from src.config import ServerMail


def SendMail(a_recipient, a_subject, a_message, request = None):
    recipient = uniq(a_recipient)
    sender = "Singapore Government Hospital <%s>" % ServerMail

    msg = "Dear Ms/Mr, \n\n " + a_message + "\n\nRegards, \nSingapore Government Hospital \n\n--------------------------------------------------------------------------- \nThis is a computer generated email. No reply is required."

    if request is None:
        if '' not in recipient:
            t = threading.Thread(target=send_mail, args=[a_subject, msg, sender, recipient], kwargs={'fail_silently': False})
            t.setDaemon(True)
            t.start()
    else:
        for eachEmail in recipient:
            message = """\
From:  %s
To: %s
Subject: %s

%s
""" % (sender, eachEmail, a_subject, msg)

            s = smtplib.SMTP('localhost')
            s.sendmail(ServerMail, eachEmail, message)
            s.close()

def uniq(alist):    # Fastest order preserving
    set = {}
    return [set.setdefault(e,e) for e in alist if e not in set]