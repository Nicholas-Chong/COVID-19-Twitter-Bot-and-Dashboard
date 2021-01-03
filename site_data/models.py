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
    Date = DateField(null=True)
    Algoma_Public_Health_Unit = IntegerField(default=0)
    Brant_County_Health_Unit = IntegerField(default=0)
    Chatham_Kent_Health_Unit = IntegerField(default=0)
    Durham_Region_Health_Department = IntegerField(default=0)
    Eastern_Ontario_Health_Unit = IntegerField(default=0)
    Grey_Bruce_Health_Unit = IntegerField(default=0)
    Haldimand_Norfolk_Health_Unit = IntegerField(default=0)
    Haliburton_Kawartha_Pine_Ridge_District_Health_Unit = IntegerField(default=0)
    Halton_Region_Health_Department = IntegerField(default=0)
    Hamilton_Public_Health_Services = IntegerField(default=0)
    Hastings_and_Prince_Edward_Counties_Health_Unit = IntegerField(default=0)
    Huron_Perth_District_Health_Unit = IntegerField(default=0)
    Kingston_Frontenac_and_Lennox_and_Addington_Public_Health = IntegerField(default=0)
    Lambton_Public_Health = IntegerField(default=0)
    Leeds_Grenville_and_Lanark_District_Health_Unit = IntegerField(default=0)
    Middlesex_London_Health_Unit = IntegerField(default=0)
    Niagara_Region_Public_Health_Department = IntegerField(default=0)
    North_Bay_Parry_Sound_District_Health_Unit = IntegerField(default=0)
    Northwestern_Health_Unit = IntegerField(default=0)
    Ottawa_Public_Health = IntegerField(default=0)
    Peel_Public_Health = IntegerField(default=0)
    Peterborough_Public_Health = IntegerField(default=0)
    Porcupine_Health_Unit = IntegerField(default=0)
    Region_of_WaterlooPublic_Health = IntegerField(default=0)
    Renfrew_County_and_District_Health_Unit = IntegerField(default=0)
    Simcoe_Muskoka_District_Health_Unit = IntegerField(default=0)
    Southwestern_Public_Health = IntegerField(default=0)
    Sudbury_and_District_Health_Unit = IntegerField(default=0)
    Thunder_Bay_District_Health_Unit = IntegerField(default=0)
    Timiskaming_Health_Unit = IntegerField(default=0)
    Toronto_Public_Health = IntegerField(default=0)
    Wellington_Dufferin_Guelph_Public_Health = IntegerField(default=0)
    Windsor_Essex_County_Health_Unit = IntegerField(default=0)
    York_Region_Public_Health_Services = IntegerField(default=0)

    class Meta:
        # This data model "belongs" to the database db
        database = db


class Daily_Vacination(Model):
    date = DateField()
    new_doses = IntegerField(default=0)
    total_doses = IntegerField(default=0)
    
    class Meta:
        database = db


if __name__ == '__main__':
    db.create_tables([Daily_Vacination])