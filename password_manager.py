import os
from cryptography.fernet import Fernet
import json

# Generate a key for encryption
def generate_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    return open('key.key', 'rb').read()

# Encrypt a password
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Decrypt a password
def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Save the password to a JSON file
def save_password(service, password):
    encrypted_password = encrypt_password(password)
    if os.path.exists('passwords.json'):
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    else:
        data = {}

    data[service] = encrypted_password.decode()

    with open('passwords.json', 'w') as file:
        json.dump(data, file)

# Retrieve a password
def get_password(service):
    if os.path.exists('passwords.json'):
        with open('passwords.json', 'r') as file:
            data = json.load(file)

        if service in data:
            encrypted_password = data[service].encode()
            return decrypt_password(encrypted_password)
    return None

# Delete a password
def delete_password(service):
    if os.path.exists('passwords.json'):
        with open('passwords.json', 'r') as file:
            data = json.load(file)

        if service in data:
            del data[service]
            with open('passwords.json', 'w') as file:
                json.dump(data, file)
            print(f"Password for {service} deleted.")
        else:
            print(f"No password found for {service}.")
    else:
        print("No passwords stored yet.")

# Show menu options
def show_menu():
    print("\nPassword Manager Menu:")
    print("1. Add Password")
    print("2. Retrieve Password")
    print("3. Delete Password")
    print("4. Exit")

# Main function
def main():
    if not os.path.exists('key.key'):
        generate_key()  # Generate a key only once

    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            service = input("Enter the service name: ")
            password = input("Enter the password: ")
            save_password(service, password)
            print(f"Password for {service} saved.")

        elif choice == '2':
            service = input("Enter the service name to retrieve: ")
            retrieved_password = get_password(service)
            if retrieved_password:
                print(f"Password for {service}: {retrieved_password}")
            else:
                print(f"No password found for {service}.")

        elif choice == '3':
            service = input("Enter the service name to delete: ")
            delete_password(service)

        elif choice == '4':
            print("Exiting the Password Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please choose again.")

if __name__ == '__main__':
    main()
