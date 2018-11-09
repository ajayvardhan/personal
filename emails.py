import email
from os import walk
from collections import OrderedDict
from dateutil.parser import parse
import unittest

# email object to store each email along with it's parent
class Email:

    def __init__(self, message_id, reply_to, date, from_address, to_addresses, subject):
        self.message_id = message_id
        self.reply_to = reply_to
        self.date = date
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.subject = subject
        self.parent = None

# get the parent of "in reply to"
def reply_to_parent(mail, mails):
    for m in mails:
        if mail.reply_to == m.message_id:
            return m
    return None

# get parent for the same subject and the from and to addresses match
def subject_parent(mail, mails):
    for m in mails:
        if mail.subject == m.subject and mail.from_address in m.to_addresses and m.from_address in mail.to_addresses:
            return m
    return None

# parse the subject out of the email
def get_subject(sub):
    subject = sub.lower()
    if "fw" in subject.split(":"):
        return subject
    return subject.split(":")[-1].strip()

# parse the emails and create email objects for each email
def parse_emails(directory):
    for (dirpath, dirnames, filenames) in walk(directory):
        emails = filenames
    mails = OrderedDict()
    unsorted_mails = {}
    conversations = OrderedDict()
    visited = {}
    email_list = []

    for mail in emails:
        message = open(directory + "/" + mail, "r").read()
        msg = email.message_from_string(message)

        msg_subject = get_subject(msg['subject'])

        to = msg["To"].split(', ')
        if "Cc" in msg:
            to.extend(msg["Cc"].split(', '))

        email_item = Email(msg["Message-ID"],
                           msg['In-Reply-To'],
                           parse(msg['Date']),
                           msg["From"],
                           to,
                           msg_subject)
        first_parent = reply_to_parent(email_item, email_list)
        second_parent = subject_parent(email_item, email_list)
        if first_parent:
            email_item.parent = first_parent
        elif second_parent:
            email_item.parent = second_parent

        email_list.append(email_item)


    email_list.sort(key=lambda x: x.date, reverse=True)
    return email_list

# create thread for each email. DFS traversal the email until we each the topmost parent
def get_thread(mail, thread):
    thread.append(mail)
    if not mail.parent:
        return thread
    else:
        return get_thread(mail.parent, thread)

# get the thread for each email
def get_conversations(email_list):
    conversations = []
    visited = []
    for mail in email_list:
        thread = get_thread(mail, [])
        if mail not in visited:
            conversations.append(thread)
        visited.extend(thread)
    return conversations

# main program
def main():
    emails = parse_emails("raw_emails")
    conversations = get_conversations(emails)
    conversations.reverse()
    for conv in conversations:
        conv.sort(key=lambda x: x.date, reverse=False)
        final = []
        for c in conv:
            final.append(c.message_id)
        print final

if __name__ == '__main__':
    main()

# Output:
# ['<1@example>', '<3@example>']
# ['<4@example>']
# ['<1@example>', '<2@example>', '<6@example>', '<7@example>', '<8@example>']
# ['<5@example>']
# ['<9@example>', '<10@example>']
# ['<11@example>']
# ['<12@example>', '<13@example>', '<14@example>']
# ['<15@example>']
# ['<16@example>']
# ['<17@example>']