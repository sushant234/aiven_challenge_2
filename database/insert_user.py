import psycopg2
from confluent_kafka import Producer # type: ignore
import json, os
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# Function to connect to PostgreSQL
def connect_to_postgresql():
    return psycopg2.connect(
    dbname=os.getenv("PG_DB"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    sslmode='require',
    sslrootcert=os.getenv("PG_CA_CERT")
)


# Function to insert data into PostgreSQL
def insert_data(cursor, name, email, data_classification):
    cursor.execute("""
        INSERT INTO public.users (name, email, data_classification)
        VALUES (%s, %s, %s)
    """, (name, email, data_classification))
    print(f"Inserted user: {name}, {email}, {data_classification}")

# Function to update data in PostgreSQL
def update_data(cursor, user_id, name, email, data_classification):
    cursor.execute("""
        UPDATE public.users
        SET name = %s, email = %s, data_classification = %s
        WHERE id = %s
    """, (name, email, data_classification, user_id))
    print(f"Updated user: {user_id}, {name}, {email}, {data_classification}")

# Function to delete data from PostgreSQL
def delete_data(cursor, user_id):
    cursor.execute("""
        DELETE FROM public.users WHERE id = %s
    """, (user_id,))
    print(f"Deleted user with user_id: {user_id}")


# Main function to handle user input and operations
def main():
    while True:
        print("\nSelect operation:")
        print("1. Insert new record")
        print("2. Update existing record")
        print("3. Delete record")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3/4): ").strip()
        
        conn = connect_to_postgresql()
        cursor = conn.cursor()

        if choice == '1':  # Insert new record
            name = input("Enter name: ")
            email = input("Enter email: ")
            data_classification = input("Enter data classification (public/private): ").lower()
            
            if data_classification not in ['public', 'private']:
                print("Invalid data classification. Please choose 'public' or 'private'.")
                continue
            
            insert_data(cursor, name, email, data_classification)
            
            # Commit the changes
            conn.commit()

        elif choice == '2':  # Update existing record
            user_id = input("Enter user_id to update: ")
            name = input("Enter new name: ")
            email = input("Enter new email: ")
            data_classification = input("Enter new data classification (public/private): ").lower()
            
            if data_classification not in ['public', 'private']:
                print("Invalid data classification. Please choose 'public' or 'private'.")
                continue

            update_data(cursor, user_id, name, email, data_classification)
            
            # Commit the changes
            conn.commit()

        elif choice == '3':  # Delete record
            user_id = input("Enter user_id to delete: ")
            delete_data(cursor, user_id)
            
            # Commit the changes
            conn.commit()

        elif choice == '4':  # Exit
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose a valid operation.")
        
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

