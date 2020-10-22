from getpass import getpass

import psycopg2

def InitializePostgreSQLDatabase(
  user: str, db_name: str='scraper_db', host: str='localhost') -> None :
    password = getpass(prompt='Password of user: ')

    connect_string = 'dbname={} user={} host={} password={}'.format(
      db_name, user, host, password)

    connection = psycopg2.connect(connect_string)
    cursor = connection.cursor()

    command = \
      """
      create table if not exists shopee_items (
        item_id SERIAL PRIMARY KEY,
        title varchar(255) not null,
        price integer not null,
        search_phrase varchar(255) not null,
        update_date date not null default current_date
      );
      """

    cursor.execute(command)
    connection.commit()

    cursor.close()
    connection.close()
