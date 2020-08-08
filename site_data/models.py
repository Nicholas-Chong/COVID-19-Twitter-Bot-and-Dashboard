'''----------------------------------------------------------------------------
Name:        Models (models.py)
Purpose:     To create the Daily_Report data model and setup the database. 

Author:      Nicholas Chong
Created:     2020-06-23 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

from peewee import *
from playhouse.db_url import connect
import os

# db = PostgresqlDatabase(os.getenv('DATABASE_URL'))

# Open a connection to the database
db = connect(os.getenv('DATABASE_URL'))

# Create a data model for a Daily_Report
class Daily_Report(Model):
    date = DateField(null=True)
    net_new_cases = IntegerField(null=True)
    net_new_tests = IntegerField(null=True)
    net_new_deaths = IntegerField(null=True)
    total_cases = IntegerField(null=True)
    total_deaths  = IntegerField(null=True)
    total_resolved = IntegerField(null=True)

    class Meta:
        # This data model "belongs" to the database db
        database = db


class Daily_Regional_Report(Model):
    date = DateField(null=True)
    reporting_phu = CharField(max_length=100, null=True)
    total_cases = IntegerField(null=True)

    class Meta:
        # This data model "belongs" to the database db
        database = db


if __name__ == '__main__':
    db.create_tables([Daily_Regional_Report])