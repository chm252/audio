import sqlite3

conn = sqlite3.connect("transcriptions.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS transcriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    filename TEXT, 
                    text TEXT, 
                    timestamp TIMESTAMP)""")

conn.commit()
conn.close()

print("Database initialized successfully.")

