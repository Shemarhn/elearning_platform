from user_ops import register_user
import random


LECTURER_NAMES = [
    "Sophia_Johnson", "Liam_Williams", "Olivia_Brown", "Noah_Jones",
    "Emma_Garcia", "Lucas_Martinez", "Ava_Davis", "Mason_Rodriguez",
    "Isabella_Hernandez", "Ethan_Lopez", "Mia_Gonzalez", "Logan_Wilson",
    "Amelia_Anderson", "James_Thomas", "Charlotte_Taylor", "Benjamin_Moore",
    "Harper_Jackson", "Elijah_White", "Evelyn_Lewis", "Sebastian_Hall",
    "Abigail_Young", "Alexander_Allen", "Emily_Scott", "Henry_King",
    "Elizabeth_Wright", "Daniel_Green", "Sofia_Baker", "Matthew_Adams",
    "Scarlett_Nelson", "Jack_Carter", "Victoria_Mitchell", "Owen_Perez",
    "Aria_Roberts", "Wyatt_Turner", "Ella_Phillips", "Dylan_Campbell",
    "Grace_Parker", "Gabriel_Evans", "Chloe_Edwards", "Jayden_Collins",
    "Layla_Stewart", "Julian_Sanchez", "Penelope_Morris", "Levi_Rogers",
    "Lily_Reed", "Isaac_Cook", "Hannah_Morgan", "Samuel_Bell",
    "Nora_Murphy", "David_Bailey"
]

def create_fake_lecturers():
    """
    Creates fake lecturers with realistic names.
    """
    for name in LECTURER_NAMES:
        userid = name.lower()  
        password = "DefaultPass123!"  # same password for all (can randomize later)
        role = "lecturer"

        success = register_user(userid, password, role)
        if success:
            print(f"[+] Created lecturer: {userid}")
        else:
            print(f"[-] Failed to create lecturer: {userid}")

if __name__ == "__main__":
    create_fake_lecturers()
