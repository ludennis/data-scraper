from getpass import getpass

import psycopg2

def InitializePostgreSQLDatabase(
  user: str, db_name: str='scrapper_db', host: str='localhost') -> None :
    password = getpass(prompt='Password of user: ')

    connect_string = 'dbname={} user={} host={} password={}'.format(
      db_name, user, host, password)

    connection = psycopg2.connect(connect_string)
    cursor = connection.cursor()

    cursor.close()
    connection.close()
