from cryptography.fernet import Fernet
import csv
import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

# Generate or load encryption key
def load_key():
    if os.path.exists("key.key"):
        return open("key.key", "rb").read()
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

# Initialize Fernet with the loaded key
key = load_key()
fer = Fernet(key)

# Function to verify master key
def verify_master_key(master_key):
    stored_master_key = b"masterkey"
    return master_key == stored_master_key

# Function to view decrypted password
def view(master_key):
    if verify_master_key(master_key):
        try:
            # Read passwords.csv into a pandas DataFrame
            df = pd.read_csv("passwords.csv", sep="|", header=None, names=["Website/APP", "Username", "Password"])

            # Decrypt passwords
            df["Password"] = df["Password"].apply(lambda x: fer.decrypt(x.encode()).decode())

            # Set "Website/APP" column as index
            df.set_index("Website/APP", inplace=True)

            # Create a new window for displaying passwords
            view_window = tk.Toplevel(root)
            view_window.title("Password List")

            # Create a Text widget to display passwords
            text_widget = tk.Text(view_window, wrap=tk.WORD, font=font, width=60, height=20)
            text_widget.pack()

            # Insert data into Text widget
            for index, row in df.iterrows():
                text_widget.insert(tk.END, f"Website/APP: {index}\n")
                text_widget.insert(tk.END, f"Username: {row['Username']}\n")
                text_widget.insert(tk.END, f"Decrypted Password: {row['Password']}\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt passwords: {str(e)}")
    else:
        messagebox.showerror("Error", "Incorrect master key!")

# Function to add a new password with website, username, and password inputs
def add():
    website_app = website_entry.get()
    name = username_entry.get()
    pwd = password_entry.get()
    encrypted_pwd = fer.encrypt(pwd.encode()).decode()

    try:
        with open("passwords.csv", mode="a", newline="") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow([website_app, name, encrypted_pwd])
        messagebox.showinfo("Success", "Password added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add password: {str(e)}")

# GUI setup
root = tk.Tk()
root.title("Password Manager")

#background
root.configure(bg="light gray")

#Defining a font
font = tkFont.Font(family="Helvetica", size=12)

#tk.Frame for better layout management and organization
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.grid(row=0, column=0)

# Labels and Entries for adding passwords
website_label = tk.Label(main_frame, text="Website/APP Name:", font=font)
website_label.grid(row=0, column=0, padx=10, pady=5)
website_entry = tk.Entry(main_frame, font=font, width=30)
website_entry.grid(row=0, column=1, padx=10, pady=5)

username_label = tk.Label(main_frame, text="Username:", font=font)
username_label.grid(row=1, column=0, padx=10, pady=5)
username_entry = tk.Entry(main_frame, font=font, width=30)
username_entry.grid(row=1, column=1, padx=10, pady=5)

password_label = tk.Label(main_frame, text="Password:", font=font)
password_label.grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(main_frame, show="*", font=font, width=30)
password_entry.grid(row=2, column=1, padx=10, pady=5)

add_button = tk.Button(main_frame, text="Add Password", command=add, font=font, padx=10, pady=5)
add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

view_button = tk.Button(main_frame, text="View Passwords", command=lambda: view(master_key_entry.get().encode()), font=font, padx=10, pady=5)
view_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

master_key_label = tk.Label(main_frame, text="Enter Master Key:", font=font)
master_key_label.grid(row=5, column=0, padx=10, pady=5)
master_key_entry = tk.Entry(main_frame, show="*", font=font, width=30)
master_key_entry.grid(row=5, column=1, padx=10, pady=5)

root.mainloop()
