def migrate(migrator, database, fake=False, **kwargs):

    migrator.sql("""CREATE TABLE measures(
        id INTEGER PRIMARY KEY, 
        created timestamp not null default CURRENT_TIMESTAMP,
        modified timestamp not null default CURRENT_TIMESTAMP,

        name text,
        gender text,
        age int,
        height real,
        weight real,

        file_path text,
        request_id text,
        result text
    )""")

def rollback(migrator, database, fake=False, **kwargs):

    migrator.sql("""DROP TABLE measures""")
