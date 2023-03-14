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


async def check_user_id():
    users = cursor.execute("""SELECT user_id FROM users;""").fetchall()
    user = [row[0] for row in users]
    return user


async def save_user(user_id, name, phone_number, date_saved):
    cursor.execute("""INSERT INTO users(user_id, name, phone_number, date_saved)
                      VALUES ({}, '{}', '{}', '{}');""".format(user_id, name, phone_number, date_saved))
    user = cursor.lastrowid
    conn.commit()


# ADMIN SQL REQUEST
async def delete_user(id):
    cursor.execute("""DELETE FROM users WHERE id = {}""".format(id))
    conn.commit()


async def check_id():
    users = cursor.execute("""SELECT id FROM users;""").fetchall()
    user = [row[0] for row in users]
    return user


async def get_user(id):
    user = cursor.execute("""SELECT * FROM users WHERE id = {}""".format(id)).fetchone()
    return (f'🆔: {id}\n'
            f'<b>Имя</b>: {user[2]}\n'
            f'📞: {user[3]}\n'
            f'🕘: {user[4]}\n')


async def get_users():
    users = cursor.execute("""SELECT * FROM users""").fetchall()
    return '\n'.join([f'🆔: {id}\n'
                      f'<b>Имя</b>: {name}\n'
                      f'📞: {phone_number}\n'
                      f'🕘: {date}\n'
                      f'<b><u>LINK</u></b>: <a href="tg://user?id={user_id}">Ссылка {name}</a>' for id, user_id, name, phone_number, date in users])


