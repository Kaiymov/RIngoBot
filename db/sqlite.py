from data import DB_PORT, DB_USER, DB_NAME, DB_HOST, DB_PASSWORD
import psycopg2
import sqlite3


conn = sqlite3.connect('/home/manas/Desktop/RingoBot/ringo.db')
cursor = conn.cursor()


# DB POSTGRESQL
class DB:
    connect = psycopg2.connect(host=DB_HOST,
                               dbname=DB_NAME,
                               user=DB_USER,
                               password=DB_PASSWORD,
                               port=DB_PORT)
    cursor = connect.cursor()

    def close_db(self):
        self.cursor.close()
        self.connect.close()

    def save_user_id(self, user_id):
        self.cursor.execute("""INSERT INTO users (user_id, check_req, is_req_discount) VALUES ({}, 'n', FALSE)""".format(user_id))
        self.connect.commit()

    def update_save_user(self, user_id, name, phone_number, date_saved):
        sql = "UPDATE users SET name='{}', phone_number='{}', date_saved='{}', check_req='y'" \
              "WHERE user_id = {}"
        self.cursor.execute(sql.format(name, phone_number, date_saved, user_id))
        self.connect.commit()

    def get_user(self, user_id):
        sql = "SELECT * FROM users WHERE user_id = {};"
        self.cursor.execute(sql.format(user_id))
        user = self.cursor.fetchone()
        if user is not None:
            return (f'🆔: {user[0]}\n'
                    f'<b>Имя</b>: {user[2]}\n'
                    f'📞: {user[3]}\n'
                    f'🕘: {user[4]}\n'
                    f'<b><u>LINK</u></b>: <a href="tg://user?id={user_id}">Ссылка {user[2]}</a>\n')

    def check_request_user(self, user_id):
        sql = "SELECT user_id, check_req FROM users WHERE user_id = {} AND check_req = 'y';"
        self.cursor.execute(sql.format(user_id))
        result = self.cursor.fetchone()

        return result

    def get_users_id(self):
        self.cursor.execute("""SELECT user_id FROM users;""")
        users = self.cursor.fetchall()

        return [user[0] for user in users]

    def get_users_paginate(self, page_number):
        sql = 'SELECT id, user_id, name, phone_number, date_saved FROM users LIMIT {} OFFSET {}*{};'
        self.cursor.execute(sql.format(10, page_number - 1, 10))

        users = self.cursor.fetchall()

        return '\n'.join([f'🆔: {id}\n'
                          f'<b>Имя</b>: {name}\n'
                          f'📞: {phone_number}\n'
                          f'🕘: {date}\n'
                          f'<b><u>LINK</u></b>: <a href="tg://user?id={user_id}">Ссылка {name}</a>\n'
                          for id, user_id, name, phone_number, date in users])

    def get_count_users(self):
        self.cursor.execute("""SELECT COUNT(*) FROM users""")
        users = self.cursor.fetchone()
        return users[0]

    def get_user_id(self, id):
        self.cursor.execute("""SELECT * FROM users WHERE id = {};""".format(id))
        user = self.cursor.fetchone()
        if user is not None:
            return (f'🆔: {user[0]}\n'
                    f'<b>Имя</b>: {user[2]}\n'
                    f'📞: {user[3]}\n'
                    f'🕘: {user[4]}\n')

    def delete_user(self, id):
        self.cursor.execute("""DELETE FROM users WHERE id = {};""".format(id))
        self.connect.commit()

    def update_res_discount(self):
        self.cursor.execute('UPDATE users SET is_req_discount = FALSE;')
        self.connect.commit()

    def update_req_discount(self, user_id):
        self.cursor.execute('UPDATE users SET is_req_discount = TRUE WHERE user_id = {}'.format(user_id))
        self.connect.commit()

    def is_req_discount(self, user_id):
        self.cursor.execute('SELECT is_req_discount FROM users WHERE user_id = {}'.format(user_id))
        response = self.cursor.fetchone()
        return response[0]


class DataBaseConnect:
    connect = psycopg2.connect(host=DB_HOST,
                               dbname=DB_NAME,
                               user=DB_USER,
                               password=DB_PASSWORD,
                               port=DB_PORT)
    cursor = connect.cursor()

    def create_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                               id SERIAL PRIMARY KEY,
                               user_id BIGINT UNIQUE,
                               name VARCHAR(40) NULL,
                               phone_number VARCHAR(13) NULL,
                               check_req VARCHAR(1) NULL,
                               is_req_discount BOOLEAN NULL,
                               date_saved VARCHAR(20) NULL);""")
        print('create/connect datebase')
        self.connect.commit()
        self.cursor.close()
        self.connect.close()


# RESAVE SQLITE TO PSQL
def resave_sqlite_to_psql():
    psql_conn = psycopg2.connect(host=DB_HOST,
                                 dbname=DB_NAME,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 port=DB_PORT)
    psql_cursor = psql_conn.cursor()

    users = cursor.execute('SELECT user_id, name, phone_number, date_saved FROM users;')
    count = 0
    for user in users.fetchall():
        psql_cursor.execute("""INSERT INTO users (user_id, name, phone_number, date_saved, check_req)
                            VALUES (%s, %s, %s, %s, 'y')""", user)
        count += 1
        print(count)
    print('All users saved')
    psql_conn.commit()

    psql_cursor.close()
    psql_conn.close()

    cursor.close()
    conn.close()

# TODO вызвать resave_sqlite_to_psql() чтобы перенести данные из sqlite в postgresql
# TODO перезаписапть is_req_dicount на FALSE