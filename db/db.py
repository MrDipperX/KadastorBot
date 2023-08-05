import psycopg2
from datetime import datetime
from config.config import HOST, DBNAME, USER, PORT, PASSWORD


class PgConn:
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(database=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            print(error)

    def create_tables(self):
        with self.conn:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    id_tg BIGINT ,
                                    username CHARACTER VARYING(100),
                                    name CHARACTER VARYING(100),
                                    surname CHARACTER VARYING(100),
                                    patronymic CHARACTER VARYING(100),
                                    date_reg TIMESTAMP WITHOUT TIME ZONE,
                                    phone_numb BIGINT,
                                    lang CHARACTER VARYING(50),
                                    temp CHARACTER VARYING(50) DEFAULT 'no')""")
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS admins(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    id_tg BIGINT,
                                    username CHARACTER VARYING(100))
                                    """)
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS photos(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    id_user INTEGER REFERENCES users(id) ON DELETE SET NULL,
                                    date_create TIMESTAMP WITHOUT TIME ZONE,
                                    eval_type CHARACTER VARYING(30),
                                    url CHARACTER VARYING(150))
                                """)
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS ads(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    text TEXT,
                                    url CHARACTER VARYING(100))
                                """)
            self.conn.commit()

    def set_user_temp(self, temp, user_id):
        with self.conn:
            self.cur.execute("UPDATE users SET temp = %s WHERE id_tg = %s;", (temp, user_id))
            self.conn.commit()

    def get_user_temp(self, user_id):
        with self.conn:
            self.cur.execute("SELECT temp FROM users WHERE id_tg = %s;", (user_id,))
            user_temp = self.cur.fetchone()
            return user_temp[0]

    def set_user_lang(self, lang, user_id):
        with self.conn:
            self.cur.execute("UPDATE users SET lang = %s WHERE id_tg = %s;", (lang, user_id))
            self.conn.commit()

    def get_user_lang(self, user_id):
        with self.conn:
            self.cur.execute("SELECT lang FROM users WHERE id_tg = %s;", (user_id,))
            user_lang = self.cur.fetchone()
            return user_lang[0]

    def get_user_info(self):
        with self.conn:
            self.cur.execute("SELECT  id, id_tg, username, date_reg, phone_numb  FROM users ")
            return self.cur.fetchall()

    def add_user(self, user_id, user_name, message_date):
        with self.conn:
            self.cur.execute(f"SELECT id FROM users WHERE id_tg={user_id}")
            id_data = self.cur.fetchone()
            if id_data is None:
                date_login = datetime.fromtimestamp(message_date).strftime('%m-%d-%y %H:%M:%S')
                self.cur.execute("INSERT INTO users(id_tg, username, date_reg) VALUES(%s,%s,%s);",
                                 (user_id, user_name, date_login))
                self.conn.commit()
            else:
                pass

    def del_user(self, user_id):
        with self.conn:
            self.cur.execute("DELETE FROM users WHERE id_tg = %s;", (user_id,))
            self.conn.commit()

    def set_user_fullname(self, user_id, surname, name, patronymic):
        with self.conn:
            self.cur.execute("UPDATE users SET name = %s, surname = %s, patronymic = %s WHERE id_tg = %s;",
                             (name, surname, patronymic, user_id))
            self.conn.commit()

    def get_user_fullname(self, user_id):
        with self.conn:
            self.cur.execute("SELECT surname, name, patronymic FROM users WHERE id_tg = %s", (user_id,))
            return self.cur.fetchone()

    def add_user_contact(self, user_id, user_phone):
        with self.conn:
            self.cur.execute("UPDATE users SET phone_numb = %s WHERE id_tg =%s;", (user_phone, user_id,))
            self.conn.commit()

    def is_old_user(self, user_id):
        with self.conn:
            self.cur.execute("SELECT phone_numb FROM users WHERE id_tg = %s", (user_id,))
            is_true = self.cur.fetchone()
            return is_true

    def add_photo(self, user_id, photo_url, photo_date, eval_type):
        with self.conn:
            self.cur.execute("INSERT INTO photos(id_user, url, date_create, eval_type) VALUES "
                             "((SELECT id FROM users WHERE id_tg = %s), %s, %s, %s)",
                             (user_id, photo_url, photo_date, eval_type))
            self.conn.commit()

    def get_album(self, user_id, eval_type):
        with self.conn:
            self.cur.execute("SELECT NOW() AT TIME ZONE 'Asia/Tashkent'")
            tash_time = self.cur.fetchone()[0]
            self.cur.execute("SELECT * FROM photos WHERE id_user = (SELECT id FROM users WHERE id_tg = %s) AND "
                             "eval_type = %s AND date_create BETWEEN %s - INTERVAL '15 minutes' "
                             "AND %s", (user_id, eval_type, tash_time, tash_time))

            album = self.cur.fetchall()
            return album

    def add_main_admin(self):
        with self.conn:
            self.cur.execute("SELECT username FROM admins")
            admin_name = self.cur.fetchone()
            if admin_name is None:
                self.cur.execute("INSERT INTO admins(id_tg,username) VALUES(%s,%s);", ("111312651", "MrDipper"))
                self.conn.commit()
            else:
                pass

    def add_admin(self, user_id, username):
        with self.conn:
            self.cur.execute("INSERT INTO admins(id_tg,username) VALUES(%s,%s);", (user_id, username))
            self.conn.commit()

    def edit_admin(self, user_id, username):
        with self.conn:
            self.cur.execute("UPDATE admins SET username = %s WHERE id_tg = %s;", (username, user_id))
            self.conn.commit()

    def delete_admin(self, username):
        with self.conn:
            self.cur.execute("DELETE FROM users WHERE username = %s;", (username,))
            self.conn.commit()

    def get_admin_info(self, user_id):
        with self.conn:
            self.cur.execute("SELECT id_tg, username FROM admins WHERE id_tg = %s;", (user_id,))
            admin_id = self.cur.fetchone()
            return admin_id

    def add_ad_text(self, text):
        with self.conn:
            self.cur.execute(f"INSERT INTO ads(text) VALUES(%s)", (text,))
            self.conn.commit()

    def send_add(self):
        with self.conn:
            self.cur.execute(f"SELECT text, url FROM ads WHERE id = (SELECT MAX(id) FROM ads)")
            return self.cur.fetchone()

    def add_ad_media(self, src):
        with self.conn:
            self.cur.execute(f"UPDATE ads SET url= %s WHERE id = (SELECT MAX(id) From ads);", (src,))
            self.conn.commit()
