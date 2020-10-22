from getpass import getpass

import psycopg2

def ConnectDatabase(user: str, db_name: str='scraper_db', host: str='localhost'):
    password = getpass(prompt='Password of user: ')
    connect_string = 'dbname={} user={} host={} password={}'.format(
      db_name, user, host, password)

    return psycopg2.connect(connect_string)

def InitializePostgreSQLDatabase(connection):
    cursor = connection.cursor()

    command = \
      """
      create table if not exists shopee_items (
        item_id SERIAL PRIMARY KEY,
        name varchar(255) not null,
        price integer not null,
        search_phrase varchar(255) not null,
        update_date date not null default current_date,
        url text not null
      );
      """

    cursor.execute(command)
    connection.commit()

    cursor.close()
    connection.close()
