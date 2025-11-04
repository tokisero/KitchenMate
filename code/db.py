import sqlite3
import json


class Database:
    def __init__(self, db_name='kitchen_mate.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Pantry
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pantry
                               (
                                   id
                                   INTEGER
                                   PRIMARY
                                   KEY
                                   AUTOINCREMENT,
                                   name
                                   TEXT,
                                   amount
                                   TEXT
                               )''')

        # Shopping
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS shopping
                               (
                                   id
                                   INTEGER
                                   PRIMARY
                                   KEY
                                   AUTOINCREMENT,
                                   name
                                   TEXT,
                                   amount
                                   TEXT,
                                   checked
                                   BOOLEAN
                               )''')

        # Favorites
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS favorites
                               (
                                   id
                                   INTEGER
                                   PRIMARY
                                   KEY
                                   AUTOINCREMENT,
                                   name
                                   TEXT,
                                   ingredients
                                   TEXT,
                                   instructions
                                   TEXT,
                                   time
                                   TEXT
                               )''')

        self.conn.commit()

    def load_pantry(self):
        self.cursor.execute('SELECT name, amount FROM pantry')
        return [{'name': row[0], 'amount': row[1]} for row in self.cursor.fetchall()]

    def save_pantry(self, items):
        self.cursor.execute('DELETE FROM pantry')
        for item in items:
            self.cursor.execute('INSERT INTO pantry (name, amount) VALUES (?, ?)', (item['name'], item['amount']))
        self.conn.commit()

    def load_shopping(self):
        self.cursor.execute('SELECT name, amount, checked FROM shopping')
        return [{'name': row[0], 'amount': row[1], 'checked': bool(row[2])} for row in self.cursor.fetchall()]

    def save_shopping(self, items):
        self.cursor.execute('DELETE FROM shopping')
        for item in items:
            self.cursor.execute('INSERT INTO shopping (name, amount, checked) VALUES (?, ?, ?)',
                                (item['name'], item['amount'], item['checked']))
        self.conn.commit()

    def load_favorites(self):
        self.cursor.execute('SELECT name, ingredients, instructions, time FROM favorites')
        return [{'name': row[0], 'ingredients': row[1], 'instructions': row[2], 'time': row[3]} for row in
                self.cursor.fetchall()]

    def save_favorites(self, items):
        self.cursor.execute('DELETE FROM favorites')
        for item in items:
            self.cursor.execute('INSERT INTO favorites (name, ingredients, instructions, time) VALUES (?, ?, ?, ?)',
                                (item['name'], item['ingredients'], item['instructions'], item['time']))
        self.conn.commit()

    def close(self):
        self.conn.close()