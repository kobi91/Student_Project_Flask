import sqlite3

DB_FILE_NAME = "data.db"

class HomePage():
    
    def __init__(self):
        self.messages = self.create_messages_list()
        
    def create_messages_list(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            self.messages = [s for s in mycursor.execute("SELECT * FROM messages")]
        return self.messages
    
    def add_message(self, message):
        if message:
            with sqlite3.connect(DB_FILE_NAME) as conn:
                mycursor = conn.cursor()
                mycursor.execute("CREATE TABLE IF NOT EXISTS messages(ID INTEGER PRIMARY KEY, Message TEXT NOT NULL)")
                mycursor.execute(f"INSERT OR IGNORE INTO messages (Message) VALUES ('{message}')")
                conn.commit()
        else:
            None
            
    def delete(self, message_id):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()
            mycursor.execute(f"DELETE FROM messages WHERE ID = '{message_id}'")
            conn.commit()

    def delete_all(self):
        with sqlite3.connect(DB_FILE_NAME) as conn:
            mycursor = conn.cursor()  
            mycursor.execute("DELETE FROM messages")
            conn.commit()
            