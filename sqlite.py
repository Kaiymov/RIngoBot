import sqlite3

conn = sqlite3.connect('ringo.db')
cursor = conn.cursor()


async def start_db():
    global conn, cursor

    conn = sqlite3.connect('ringo.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY,
                       user_id INTEGER UNIQUE,
                       name VARCHAR(40) NOT NULL,
                       phone_number VARCHAR(13) NOT NULL,
                       date_saved VARCHAR(20));""")
    conn.commit()


def check_user():
    users = cursor.execute("""SELECT user_id FROM users WHERE user_id;""").fetchall()
    user = [row[0] for row in users]
    return user


async def save_user(user_id, name, phone_number, date_saved):
    cursor.execute("""INSERT INTO users(user_id, name, phone_number, date_saved)
                      VALUES ({}, '{}', '{}', '{}');""".format(user_id, name, phone_number, date_saved))
    user = cursor.lastrowid
    conn.commit()


def get_users():
    users = cursor.execute("""SELECT * FROM users""").fetchall()
    return '\n'.join([f'Имя: {name}\n'
                      f'📞: {number}\n'
                      f'🕘: {date}\n'
                      f'🆔: {id}, user_ID: {user_id}\n' for id, user_id, name, number, date in users])
