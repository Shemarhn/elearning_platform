# create_fake_courses.py

from course_ops import create_course
import random

# Course prefixes
PREFIXES = [
    "Introduction to", "Fundamentals of", "Principles of",
    "Essentials of", "Applications of", "Advanced",
    "Theory of", "Techniques in", "Basics of", "Concepts of"
]

# Course topics
TOPICS = [
    "Computer Science", "Data Science", "Artificial Intelligence",
    "Machine Learning", "Cybersecurity", "Business Management",
    "Marketing", "Accounting", "Finance", "Entrepreneurship",
    "Psychology", "Sociology", "Political Science", "Public Relations",
    "Physics", "Chemistry", "Biology", "Anatomy", "Astronomy",
    "Environmental Science", "Software Engineering", "Web Development",
    "Graphic Design", "Digital Media", "Cloud Computing", "Robotics",
    "Statistics", "Mathematics", "Health and Wellness", "Music Theory",
    "Law", "Economics", "Ethics in Technology", "Creative Writing",
    "Education Technology", "Mobile Application Development", "Networking",
    "Operating Systems", "Database Systems", "Game Development"
]

def create_fake_courses(num_courses=200):
    """
    Creates a specified number of fake courses with dynamically generated names.
    """
    used_titles = set()

    for i in range(1, num_courses + 1):
        prefix = random.choice(PREFIXES)
        topic = random.choice(TOPICS)
        title = f"{prefix} {topic}"

        # Make sure no duplicate titles
        while title in used_titles:
            prefix = random.choice(PREFIXES)
            topic = random.choice(TOPICS)
            title = f"{prefix} {topic}"

        used_titles.add(title)

        description = f"This course provides an in-depth study of {topic.lower()}."

        success = create_course(title, description)
        if success and i % 20 == 0:
            print(f"[+] Created {i} courses so far...")

if __name__ == "__main__":
    create_fake_courses(200)
