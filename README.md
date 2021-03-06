# Backstop

Backstop is an emergency contact notification built in Python Using [Flask](https://flask.palletsprojects.com/en/1.1.x/). Users can Authenticate with their Google account then create emergency alerts which are sent to a specified contact if a certain time stamp is passed. These emails are sent using [FlaskMail](https://pythonhosted.org/Flask-Mail/) and [AdvancedPythonScheduler](https://apscheduler.readthedocs.io/en/stable/)

Currently works locally BUT is not deployable on heroku due to being built with a SQLite database(I did deploy on AWS and incurred monthly data charges, I think due to maintaining the in memory db). I'm working on changing to an ORM and Migration manager in the branch setup-postgres

## Why Backstop

I do a lot of hiking and I like to go light. I generally don't take a gps or phone and pack light on food too. One thing I do take however, is a jar of peanut butter as a caloric 'backstop'. If I run out of food, I won't go hungry. I created this application as a simple way for people to create emergency alerts to send to an emergency contact if they didn't return from a trip. I had never used Python or Flask before and started by following the Flask Tutorial to build a blog application. I then modeled my routes and tests off of this pattern before removing the original blog functionality and adding the mailer and scheduler functionality.

## Lessons Learned

- SQLite is inappropriate for a production database as it uses in memory storage. For this reason it will NOT work on heroku, it will work on AWS BUT will incur monthly charges
- Some sort of DB migration system is necessary to maintain a database across multiple platforms i.e. dev and production. Without this one will have to maintain databses by hand with raw SQL queries which is tedious and error prone.
- ORM's have major upsides I am used to enjoying having worked primarily in rails
- Convention over configuration standardizes documentation in a really nice way. Because an opionion free framework like flask lets you do anything Python can do tutorials are not standardized and it can be hard to combine different tutorials/functionalities.
