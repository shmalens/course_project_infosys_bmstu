import logging
import os
from string import Template

import mysql.connector
from mysql.connector import errorcode


class ConnectorDatabase:
    def __init__(self, config):
        self.config = config

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise RuntimeError("CONNECTING TO DATABASE ACCESS DENIED")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                raise RuntimeError("DATABASE DOES NOT EXISTS")
            else:
                print(error)
        self.cursor = self.connection.cursor()

        if self.cursor is None:
            raise RuntimeError("CURSOR IS EMPTY")

        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


def querying_data(sql_request, config):
    with ConnectorDatabase(config) as cursor:
        cursor.execute(sql_request)
        return cursor.fetchall()


def inserting_data(sql_request, config):
    with ConnectorDatabase(config) as cursor:
        cursor.execute(sql_request)


class ProviderSQL:
    def __init__(self, sql_requests_files_path):
        self.scripts = dict()
        for file in os.listdir(sql_requests_files_path):
            if file.endswith('.sql'):
                self.scripts[file] = Template(open(f'{sql_requests_files_path}/{file}', 'r').read())

    def get_request(self, filename, **kwargs):
        if filename in self.scripts:
            return self.scripts[filename].substitute(**kwargs)
        else:
            raise RuntimeError('SCRIPT DOES NOT EXITS')


if __name__ == '__main__':
    test_config = {
        'user': 'shmalens',
        'password': 'shmalens',
        'host': 'localhost',
        'database': 'disease_history'
    }
    # _SQL = """
    # insert into Note (date, note, doctor, history)
    # values ('2021-02-12', 'Некоторая запись 1 в истории 5', 6, 5);
    # """
    # inserting_data(_SQL, test_config)
    # print(querying_data('SELECT * FROM Note;', test_config))
