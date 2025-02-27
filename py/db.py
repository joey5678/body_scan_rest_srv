#!/usr/bin/python
# -*- coding: utf-8 -*-

"""db.py: Models and functions for accessing the database
   - using peewee orm
   - preferably have all SQL in this file



http://docs.peewee-orm.com/en/latest/peewee/querying.html
http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#postgres-ext
"""

from peewee import *
from playhouse.shortcuts import model_to_dict

from flask import abort
import config

import logging
log = logging.getLogger("db")

if config.IS_SQLITE:
    # config.DATABASE_HOST is full path to sqlite file
    database = SqliteDatabase(config.DATABASE_HOST, pragmas={})
else:
    from playhouse.postgres_ext import PostgresqlExtDatabase, ArrayField, BinaryJSONField, BooleanField, JSONField
    # support for arrays of uuid
    import psycopg2.extras
    psycopg2.extras.register_uuid()

    database = PostgresqlExtDatabase(config.DATABASE_NAME,
        user=config.DATABASE_USER, password=config.DATABASE_PASSWORD,
        host=config.DATABASE_HOST, port=config.DATABASE_PORT)


# --------------------------------------------------------------------------
# Base model and common methods

class BaseModel(Model):
    """Base class for all database models."""

    # exclude these fields from the serialized dict
    EXCLUDE_FIELDS = []

    def serialize(self):
        """Serialize the model into a dict."""
        d = model_to_dict(self, recurse=False, exclude=self.EXCLUDE_FIELDS)
        d["id"] = str(d["id"]) # unification: id is always a string
        return d

    class Meta:
        database = database


def get_object_or_404(model, **kwargs):
    """Retrieve a single object or abort with 404."""

    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        log.warning("NO OBJECT {} {}".format(model, kwargs))
        abort(404)

def get_object_or_none(model, **kwargs):
    """Retrieve a single object or return None."""

    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        return None


# --------------------------------------------------------------------------
# USER

class User(BaseModel):

    # Should user.id be an integer or uuid? Both have pros and cons.
    # Since user.id is sensitive data, I selected uuid here.
    if not config.IS_SQLITE:
        id = UUIDField(primary_key=True)
        id.auto_increment = True # is auto generated by server

    email = TextField()
    password = TextField()
    first_name = TextField()
    last_name = TextField()
    role = TextField()
    if not config.IS_SQLITE:
        tags = ArrayField(TextField)
    else:
        tags = TextField()

    created = DateTimeField()
    modified = DateTimeField()

    EXCLUDE_FIELDS = [password] # never expose password


    def is_superuser(self):
        return self.role == "superuser"

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name or '')

    def serialize(self):
        """Serialize this object to dict/json."""

        d = super(User, self).serialize()

        # add extra data
        d["fullname"] = self.full_name()
        d["tags"] = self.tags or [] # never None
        return d

    def __str__(self):
        return "<User {}, {}, role={}>".format(self.id,
                self.email, self.role)

    class Meta:
        db_table = 'users'


def get_user(uid):
    """Return user object or throw."""
    return get_object_or_404(User, id=uid)


def get_user_by_email(email):
    """Return user object or None"""

    if not email:
        return None

    try:
#         return User.select().where(User.email == email).get()
        # case insensitive query
        if config.IS_SQLITE:
            sql = "SELECT * FROM users where email = ? LIMIT 1"
            args = email.lower()
        else:
            sql = "SELECT * FROM users where LOWER(email) = LOWER(%s) LIMIT 1"
            args = (email,)
        return list(User.raw(sql, args))[0]

    except IndexError:
        return None


def query_users(page=0, limit=1000, search=None):
    """Return list of users. Desc order"""

    page = int(page or 0)
    limit = int(limit or 1000)

    q = User.select()
    if search:
        search = "%"+search+"%"
        q = q.where(User.first_name ** search | User.last_name ** search |
                User.email ** search)
    q = q.paginate(page, limit).order_by(User.id.desc())
    return q


# 3D Measure

class Measure(BaseModel):

    name = TextField()
    age = IntegerField()
    gender = TextField()
    height = FloatField()
    weight = FloatField()
    birth = TextField()

    file_path = TextField()
    request_id = TextField()
    result = TextField()

    created = DateTimeField()
    modified = DateTimeField()

    class Meta:
        db_table = 'measures'

def get_measure(id):
    """Return Movie or throw."""
    return get_object_or_404(Measure, id=id)

def query_measure_by_file_name(fname):

    if not fname:
        return None

    search = "%" + fname + "%"
    q = Measure.select()
    q = q.where(Measure.file_path ** search)
    if not q:
        return None
    for m in q:
        return m

# --------------------------------------------------------------------------
# MOVIE - just an example for CRUD API...

class Movie(BaseModel):

    #id - automatic

    title = TextField()
    director = TextField()

    created = DateTimeField()
    modified = DateTimeField()

    creator = ForeignKeyField(db_column='creator', null=True,
                    model=User, to_field='id')

    class Meta:
        db_table = 'movies'


def get_movie(id):
    """Return Movie or throw."""
    return get_object_or_404(Movie, id=id)


def query_movies(page=None, limit=None, search='', creator=None):
    """Return list of movies which match given filters."""

    page  = page or 0
    limit = limit or 1000

    q = Movie.select()

    if search:
        search = "%"+search+"%"
        q = q.where(Movie.title ** search | Movie.director ** search)

    if creator:
        q = q.where(Movie.creator == creator)

    q = q.paginate(page, limit).order_by(Movie.id)
    return q


def query_unique_directors():
    """Return list of unique directors. An example of a raw SQL query."""

    sql = "SELECT DISTINCT(director) FROM movies"
    rq = database.execute_sql(sql)
    return [x[0] for x in rq]


# --------------------------------------------------------------------------

if __name__ == '__main__':

    # quick adhoc tests
    logging.basicConfig(level=logging.DEBUG)

    #u = User(first_name="tomi")
    #u.email = "myemailx@example.org"
    #u.save(force_insert=True)
    #print(u)

    #print(list(query_users(0, "10", "example")))

    #print(list(query_movies()))
    #print(query_unique_directors())

    m = Measure(name='jd', age=20, gender='male', height=1.99, file_path='/jj/bb/ccc')
    m.save()

    print(query_measure_by_file_name('jj'))

