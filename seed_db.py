#!/usr/bin/env python3
# Seed the database with sample data.
# Run this script once with: python seed_db.py

# Once you have seeded your data, you can run sqlite3 users.db in the terminal
# This opens a sqlite3 shell and you can run commands like:
# - .tables to see all tables
# - SELECT * FROM users; to see all users
# - .exit to exit the shell
# *Note: If you try to seed data and get an error about "UNIQUE constraint failed: users.username", it means you have already seeded the database.
# If you need to seed the database again, simply delete the users.db file and run the seed script again.

from database import get_db, init_db, get_animals_db
import bcrypt

def seed_database():
    """Add sample users to the database"""
    init_db()  # Ensure tables are created
    
    conn = get_db()
    a_conn = get_animals_db()
    
    # Sample users with passwords
    sample_users = [
        ("alice", "Password123!"),
        ("bob", "SecurePass456@"),
        ("charlie", "MyPassword789#"),
    ]

    sample_animals = [
        ("hyena", "sub-saharan", "meat", "img"),
        ("cheetah", "africa", "meat", "img"),
        ("tiger", "asia", "meat", "img"),
        ("horse", "grasslands and prairies", "grass", "img"),
        ("dog", "households", "high protein", "img"),
        ("cat", "households, wild", "high nutrition", "img"),
    ]
    
    try:
        for username, password in sample_users:
            hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_pw)
            )
        for animal_name, habitat, food, image in sample_animals:
            a_conn.execute(
                "INSERT INTO animals (animal_name, habitat, food, image) VALUES (?, ?, ?, ?)",
                (animal_name, habitat, food, image),
            )
            print(f"Added animal: {animal_name}")
            

        a_conn.commit()
        conn.commit()
        print("\nDatabase seeding complete!")
    
    except Exception as e:
        conn.rollback()
        a_conn.rollback()
        print(f"Error: {e}")
    
    finally:
        conn.close()
        a_conn.close()

if __name__ == "__main__":
    seed_database()