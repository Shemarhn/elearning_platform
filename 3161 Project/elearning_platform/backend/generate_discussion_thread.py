# generate_discussion_threads.py

from db import create_connection, close_connection
import random
from faker import Faker

fake = Faker()

def get_all_forums():
    connection = create_connection()
    if not connection:
        print("[-] Could not retrieve forums.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = "SELECT id FROM forums"
        cursor.execute(sql)
        forums = cursor.fetchall()
        return [forum['id'] for forum in forums]

    except Exception as e:
        print(f"[-] Error retrieving forums: {e}")
        return []

    finally:
        cursor.close()
        close_connection(connection)

def get_all_users():
    connection = create_connection()
    if not connection:
        print("[-] Could not retrieve users.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = "SELECT id FROM users"
        cursor.execute(sql)
        users = cursor.fetchall()
        return [user['id'] for user in users]

    except Exception as e:
        print(f"[-] Error retrieving users: {e}")
        return []

    finally:
        cursor.close()
        close_connection(connection)

def create_discussion_thread(forum_id, title, content, user_id):
    connection = create_connection()
    if not connection:
        print("[-] Failed to create discussion thread: No DB connection.")
        return False

    cursor = connection.cursor()

    try:
        sql = "INSERT INTO discussion_threads (forum_id, title, content, user_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (forum_id, title, content, user_id))
        connection.commit()
        return True

    except Exception as e:
        print(f"[-] Error during discussion thread creation: {e}")
        return False

    finally:
        cursor.close()
        close_connection(connection)

def generate_discussion_threads(min_threads=5, max_threads=10):
    forums = get_all_forums()
    users = get_all_users()

    if not forums or not users:
        print("[-] No forums or users found.")
        return

    total_created = 0

    for forum_id in forums:
        num_threads = random.randint(min_threads, max_threads)

        for _ in range(num_threads):
            title = fake.sentence(nb_words=6)
            content = fake.paragraph(nb_sentences=3)
            user_id = random.choice(users)

            create_discussion_thread(forum_id, title, content, user_id)
            total_created += 1

        if forum_id % 20 == 0:
            print(f"[+] Created threads for {forum_id} forums...")

    print(f"[+] Completed creating {total_created} discussion threads.")

if __name__ == "__main__":
    generate_discussion_threads()
