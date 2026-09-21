"""MySQL backend that still accepts 5.7.

Django 4.2 official support starts at MySQL 8. Prod datadir is mysql:5.7 and
must not be swapped in this deploy. Remove this engine after the 8 / MariaDB
cutover.
"""

from django.db.backends.mysql.base import DatabaseWrapper as MysqlDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures as MysqlFeatures


class DatabaseFeatures(MysqlFeatures):
    minimum_database_version = (5, 7)


class DatabaseWrapper(MysqlDatabaseWrapper):
    features_class = DatabaseFeatures
