import unittest
from emails import Email, reply_to_parent, subject_parent, get_subject

email1 = Email("1",
               None,
               "2017-11-02 00:00:00+00:00",
               "a@test.com",
               ["b@test.com"],
               "test")

email2 = Email("2",
               None,
               "2017-11-02 01:00:00+00:00",
               "b@test.com",
               ["c@test.com"],
               "test")

email3 = Email("3",
               "1",
               "2017-11-02 02:00:00+00:00",
               "b@test.com",
               ["a@test.com", "c@test.com"],
               "test")

email4 = Email("4",
               "",
               "2017-11-02 03:00:00+00:00",
               "c@test.com",
               ["b@test.com"],
               "test")

email5 = Email("5",
               "",
               "2017-11-02 04:00:00+00:00",
               "g@test.com",
               ["h@test.com"],
               "re: test")

email6 = Email("6",
               "",
               "2017-11-02 05:00:00+00:00",
               "i@test.com",
               ["j@test.com"],
               "fw: test")

mails = [email1,email2,email3,email4,email5,email6]


class MyTest(unittest.TestCase):

	def test_no_parent(self):
		self.assertEqual(reply_to_parent(email1, mails), None)

	def test_reply_to(self):
		self.assertEqual(reply_to_parent(email3, mails).message_id, "1")

	def test_subject_parent(self):
		self.assertEqual(subject_parent(email4, mails).message_id, "2")

	def test_no_subject_parent(self):
		self.assertEqual(subject_parent(email5, mails), None)

	def test_subject(self):
		self.assertEqual(get_subject(email5.subject), "test")

	def test_subject_forward(self):
		self.assertEqual(get_subject(email6.subject), "fw: test")

if __name__ == '__main__':
    unittest.main()