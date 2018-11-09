For my solution, I assumed that two emails could be related by the following ways:

1. Linked by "In-Reply-To"
2. Mail 1 and 2 have similar Subject. From address of Mail 2 belongs to the To address of Mail 1. From address of Mail 1 is the To address of Mail 2. To address include the cc addresses as well.

This way, I calculated the parent of each email. Then created a thread using these parents by traversing from the leaf node email until I reach the root email for that thread.

I had to assume that all Forwarded mails don't belong to any conversation. Given more time, I would have tried to find the forward messages in a better way instead of hard coding way of finding "FW" in the subject. I also would have tried to group similar threads together. For Eg, (1,2) and (1,3) are 2 different threads but originate from the same root. So this could be group together. I would also have tried to include more test cases that cover all the functions and write integration tests as well.

Time Taken to solve the problem:

Understanding, making sense of the email files, parsing and creating email objects - 30 mins.

Finding the grouping conditions and implementing it - 2.5 hours.

Cleaning and documenting the code - 30 mins.

Test - 20 mins

Instructions to execute:

1. To execute the main program, you can run the "emails.py" file from either the command line or any IDE
2. TO run the test cases, you can run the "test.py"