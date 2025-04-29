# generate_replies.py

from db import create_connection, close_connection
import random
from faker import Faker

fake = Faker()

def get_all_threads():
    connection = create_connection()
    if not connection:
        print("[-] Could not retrieve threads.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = "SELECT id FROM discussion_threads"
        cursor.execute(sql)
        threads = cursor.fetchall()
        return [thread['id'] for thread in threads]

    except Exception as e:
        print(f"[-] Error retrieving threads: {e}")
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

def create_reply(thread_id, parent_reply_id, content, user_id):
    connection = create_connection()
    if not connection:
        print("[-] Failed to create reply: No DB connection.")
        return False

    cursor = connection.cursor()

    try:
        sql = "INSERT INTO replies (thread_id, parent_reply_id, content, user_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (thread_id, parent_reply_id, content, user_id))
        connection.commit()
        return cursor.lastrowid  # Return the newly created reply id (for nested replies)

    except Exception as e:
        print(f"[-] Error during reply creation: {e}")
        return None

    finally:
        cursor.close()
        close_connection(connection)

def generate_replies(min_replies=5, max_replies=15):
    threads = get_all_threads()
    users = get_all_users()

    if not threads or not users:
        print("[-] No threads or users found.")
        return

    total_created = 0

    for thread_id in threads:
        num_replies = random.randint(min_replies, max_replies)
        parent_id = None  # Start at thread level

        for _ in range(num_replies):
            content = fake.paragraph(nb_sentences=2)
            user_id = random.choice(users)

            new_reply_id = create_reply(thread_id, parent_id, content, user_id)

            # Randomly sometimes reply to a previous reply (nesting)
            if random.random() < 0.3 and new_reply_id:
                parent_id = new_reply_id
            else:
                parent_id = None

            total_created += 1

        if thread_id % 20 == 0:
            print(f"[+] Created replies for {thread_id} threads...")

    print(f"[+] Completed creating {total_created} replies.")

if __name__ == "__main__":
    generate_replies()
