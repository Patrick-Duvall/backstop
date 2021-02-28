# Backstop

Backstop is an emergency contact notification built in Python Using [Flask](https://flask.palletsprojects.com/en/1.1.x/). Users can Authenticate with their Google account then create emergency alerts which are sent to a specified contact if a certain time stamp is passed. These emails are sent using (FlaskMail)[https://pythonhosted.org/Flask-Mail/] and (AdvancedPythonScheduler)[https://apscheduler.readthedocs.io/en/stable/]

## Why Backstop

I do a lot of hiking and I like to go light. I generally don't take a gps or phone and pack light on food too. One thing I do take however, is a jar of peanut butter as a caloric 'backstop'. If I run out of food, I won't go hungry. I created this application as a simple way for people to create emergency alerts to send to an emrgency contact if they didn't return form a trip. I had never used Python or Flask before and started by using the Flask Tutorial to build a blog application. I then modeled my routes and tests off of this pattern before removing that functionality and adding the mailer and scheduler functionality.

