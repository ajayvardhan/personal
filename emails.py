import email
from os import walk
from collections import OrderedDict
from sets import Set
from dateutil.parser import parse
import pprint

class Email:

    def __init__(self, message_id, reply_to, date, from_address, to_addresses, subject):
        self.message_id = message_id
        self.reply_to = reply_to
        self.date = date
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.subject = subject
        self.parent = None


def get_parent_reply_to(mail, mails):
    for m in mails:
        if mail.reply_to == m.message_id:
            return m

def get_parent_subject(mail, mails):
    for m in mails:
        if mail.subject == m.subject and mail.from_address in m.to_addresses and m.from_address in mail.to_addresses:
            return m

def get_subject(mail):
    subject = mail['subject'].lower()
    if "fw" in subject.split(":"):
        return subject
    return subject.split(":")[-1].strip()


for (dirpath, dirnames, filenames) in walk("raw_emails"):
    emails = filenames
mails = OrderedDict()
unsorted_mails = {}
conversations = OrderedDict()
visited = {}
email_list = []

for mail in emails:
    message = open("raw_emails/" + mail, "r").read()
    msg = email.message_from_string(message)

    msg_subject = get_subject(msg)

    email_item = Email(msg["Message-ID"],
                       msg['In-Reply-To'],
                       parse(msg['Date']),
                       msg["From"],
                       msg["To"].split(', '),
                       msg_subject)
    first_parent = get_parent_reply_to(email_item, email_list)
    second_parent = get_parent_subject(email_item, email_list)
    if first_parent:
        email_item.parent = first_parent
    elif second_parent:
        email_item.parent = second_parent

    email_list.append(email_item)


email_list.sort(key=lambda x: x.date, reverse=True)

def print_thread(mail, thread):
    thread.append(mail.message_id)
    if not mail.parent:
        return thread
    else:
        return print_thread(mail.parent, thread)

visited = []
for mail in email_list:
    thread = print_thread(mail, [])
    if mail.message_id not in visited:
        print print_thread(mail, [])
    visited.extend(thread)

# Output:
# ['<17@example>']
# ['<16@example>']
# ['<15@example>']
# ['<14@example>', '<13@example>', '<12@example>']
# ['<11@example>']
# ['<10@example>', '<9@example>']
# ['<5@example>']
# ['<8@example>', '<7@example>', '<6@example>', '<2@example>', '<1@example>']
# ['<4@example>']
# ['<3@example>', '<1@example>']