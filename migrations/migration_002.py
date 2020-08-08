from playhouse.migrate import *
from peewee import *
from playhouse.db_url import connect
import os

db = connect(os.getenv('DATABASE_URL'))
migrator = SqliteMigrator(db)

# migrate(
#     migrator.add_column('daily_regional_report', 'total_cases', IntegerField(null=True)),
#     migrator.drop_column('daily_regional_report', 'new_cases')
# )