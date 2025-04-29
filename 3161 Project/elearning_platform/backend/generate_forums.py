from db import create_connection, close_connection

def get_all_courses():
    connection = create_connection()
    if not connection:
        print("[-] Could not retrieve courses.")
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        sql = "SELECT id FROM courses"
        cursor.execute(sql)
        courses = cursor.fetchall()
        return [course['id'] for course in courses]

    except Exception as e:
        print(f"[-] Error retrieving courses: {e}")
        return []

    finally:
        cursor.close()
        close_connection(connection)

def create_forum(course_id, title):
    connection = create_connection()
    if not connection:
        print("[-] Failed to create forum: No DB connection.")
        return False

    cursor = connection.cursor()

    try:
        sql = "INSERT INTO forums (course_id, title) VALUES (%s, %s)"
        cursor.execute(sql, (course_id, title))
        connection.commit()
        return True

    except Exception as e:
        print(f"[-] Error during forum creation: {e}")
        return False

    finally:
        cursor.close()
        close_connection(connection)

def generate_forums():
    courses = get_all_courses()
    if not courses:
        print("[-] No courses found.")
        return

    total_created = 0

    for course_id in courses:
        title = f"Forum for Course {course_id}"
        create_forum(course_id, title)
        total_created += 1

        if total_created % 20 == 0:
            print(f"[+] Created forums for {total_created} courses...")

    print(f"[+] Completed creating {total_created} forums.")

if __name__ == "__main__":
    generate_forums()
