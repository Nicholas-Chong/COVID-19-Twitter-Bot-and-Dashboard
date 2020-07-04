'''----------------------------------------------------------------------------
Name:        Models (models.py)
Purpose:     To create the Daily_Report data model and setup the database. 

Author:      Nicholas Chong
Created:     2020-06-23 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

from peewee import *

# Create the sqlite database file (called database.db)
# If the file already exists, no new file will be created and the variable "db"
#   will be a database object
db = SqliteDatabase('database.db')

# Create a data model for a Daily_Report
class Daily_Report(Model):
    date = DateField(null=True)
    net_new_cases = IntegerField(null=True)
    net_new_tests = IntegerField(null=True)
    net_new_deaths = IntegerField(null=True)
    total_cases = IntegerField(null=True)
    total_deaths  = IntegerField(null=True)

    class Meta:
        # This data model "belongs" to the database db
        database = db

# Open a connection to the database
db.connect()

if __name__ == '__main__':
    # Create the tables
    db.create_tables([Daily_Report])