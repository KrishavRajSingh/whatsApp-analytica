import psycopg2

class WhatsAppDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="krishav",
            password="secret",
            host="localhost",
            port="5432"
        )
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            # Create messages table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS whatsapp_messages (
                    id SERIAL PRIMARY KEY,
                    chat_name VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sender VARCHAR(255) NOT NULL,
                    time_stamp TIMESTAMP NOT NULL,
                    message TEXT
                )
            """)

            # Create images table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS whatsapp_images (
                    id SERIAL PRIMARY KEY,
                    message_id INTEGER REFERENCES whatsapp_messages(id) ON DELETE CASCADE,
                    image_path VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.conn.commit()

    def save_message(self, chat_name, sender, time_stamp, message):
        with self.conn.cursor() as cur:
            # Check if the message already exists
            cur.execute("""
                SELECT id 
                FROM whatsapp_messages
                WHERE chat_name = %s AND sender = %s AND time_stamp = %s AND message = %s
            """, (chat_name, sender, time_stamp, message))
            existing_message = cur.fetchone()

            if existing_message:
                # if message exists, return the existingID
                return existing_message[0]
            else:
                # if message does not exist, insert the message and return the new ID
                cur.execute("""
                    INSERT INTO whatsapp_messages (chat_name, sender, time_stamp, message)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (chat_name, sender, time_stamp, message))
                new_message_id = cur.fetchone()[0]
                self.conn.commit()
                return new_message_id

    def save_image(self, message_id, image_path):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO whatsapp_images (message_id, image_path)
                VALUES (%s, %s)
            """, (message_id, image_path))
            self.conn.commit()

    def close(self):
        self.conn.close()