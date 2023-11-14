import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class DBConnector:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.conn.cursor()
        self.initializeDatabase()

    def initializeDatabase(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dev_status (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type INT,
                protocolo INT,
                utc DATETIME,
                status INT,
                device_id VARCHAR(255)
            )
        ''')
        self.conn.commit()

    def storeDataInDatabase(self, parsedData):
        try:
            self.cursor.execute('''
                INSERT INTO dev_status (type, protocolo, utc, status, device_id)
                VALUES (%s, %s, %s, %s, %s)
            ''', (parsedData["type"], parsedData["protocolo"], parsedData["utc"], parsedData["status"], parsedData["id"]))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao armazenar dados no banco de dados: {e}")

    def closeConnections(self):
        self.conn.close()