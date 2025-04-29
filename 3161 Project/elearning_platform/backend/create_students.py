
from user_ops import register_user
from faker import Faker

fake = Faker()

def create_fake_students(num_students=100000):
    """
    Creates a specified number of fake students using realistic names.
    """
    for i in range(1, num_students + 1):
        full_name = fake.name()  # example: "John Doe"
        userid = full_name.lower().replace(" ", "_") + f"_{i}"  # ensure unique
        password = "DefaultPass123!"  # default password (can randomize if you want)
        role = "student"

        success = register_user(userid, password, role)
        if success and i % 1000 == 0:  # Only print every 1000 students to avoid console overload
            print(f"[+] Created {i} students so far...")

if __name__ == "__main__":
    create_fake_students(100000)  # Creates 100,000 students
