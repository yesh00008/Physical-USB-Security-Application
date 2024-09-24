import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import webbrowser
import json
import os.path

# Path to devcon.exe
DEVCON_PATH =  r"C:\Program Files (x86)\Windows Kits\10\Tools\10.0.26100.0\x64\devcon.exe"  # Update this path
USER_DATA_FILE = 'user_data.json'  # File to store user data

# Function to save user data to a JSON file
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f)

# Function to load user data from the JSON file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Function to enable USB ports
def enable_usb():
    check_user_password("enable")

# Function to disable USB ports
def disable_usb():
    check_user_password("disable")

# Function to check user password before enabling or disabling USB
def check_user_password(action):
    password = simpledialog.askstring("Password Required", "Enter your password:", show='*')
    if password:
        user_data = load_user_data()
        current_user = email_entry.get()  # Get the current user's email

        if current_user in user_data and user_data[current_user]['password'] == password:
            if action == "enable":
                try:
                    result = os.system(f'"{DEVCON_PATH}" enable *USB*')
                    if result == 0:
                        messagebox.showinfo("USB Status", "USB ports enabled successfully.")
                    else:
                        messagebox.showerror("Error", "Failed to enable USB ports.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")
            elif action == "disable":
                try:
                    result = os.system(f'"{DEVCON_PATH}" disable *USB*')
                    if result == 0:
                        messagebox.showinfo("USB Status", "USB ports disabled successfully.")
                    else:
                        messagebox.showerror("Error", "Failed to disable USB ports.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "Incorrect password.")

# Function to open the About Project webpage
def open_about_project():
    html_file_path = r"C:\Users\thota\Desktop\Usb\About.html"  # Save the HTML code in this file
    webbrowser.open(f'file:///{html_file_path}')

# Function to validate login
def validate_login():
    email = email_entry.get()
    password = password_entry.get()
    user_data = load_user_data()

    if email in user_data and user_data[email]['password'] == password:
        messagebox.showinfo("Login Status", "Login successful!")
        enable_disable_frame.pack()  # Show enable/disable frame after login
        login_frame.pack_forget()  # Hide the login frame
    else:
        messagebox.showerror("Login Status", "Invalid email or password.")

# Function to handle registration
def register_user():
    name = name_entry.get()
    email = email_reg_entry.get()
    password = password_reg_entry.get()
    
    if not name or not email or not password:
        messagebox.showerror("Registration Error", "All fields are required!")
        return

    user_data = load_user_data()
    if email in user_data:
        messagebox.showerror("Registration Error", "Email already registered!")
        return

    user_data[email] = {'name': name, 'password': password}
    save_user_data(user_data)
    messagebox.showinfo("Registration Status", "Registration successful! You can now log in.")

# Function to switch to the registration frame
def show_registration():
    login_frame.pack_forget()
    registration_frame.pack()

# Function to switch to the login frame
def show_login():
    registration_frame.pack_forget()
    login_frame.pack()

# Create the main application window
root = tk.Tk()
root.title("USB Port Control")
root.geometry("600x600")  # Increased window size
root.configure(bg='black')  # Set background color to black

# Create frames for login and registration
login_frame = tk.Frame(root, bg='black')
registration_frame = tk.Frame(root, bg='black')
enable_disable_frame = tk.Frame(root, bg='black')  # Frame for enable/disable buttons

# Login Frame UI
tk.Label(login_frame, text="Login", bg='black', fg='white', font=("Arial", 30)).pack(pady=20)
tk.Label(login_frame, text="Email:", bg='black', fg='white', font=("Arial", 20)).pack()
email_entry = tk.Entry(login_frame, font=("Arial", 20))
email_entry.pack(pady=5)

tk.Label(login_frame, text="Password:", bg='black', fg='white', font=("Arial", 20)).pack()
password_entry = tk.Entry(login_frame, show='*', font=("Arial", 20))
password_entry.pack(pady=5)

tk.Button(login_frame, text="Login", command=validate_login, bg='green', fg='white', font=("Arial", 20)).pack(pady=20)
tk.Button(login_frame, text="Register", command=show_registration, bg='white', fg='black', font=("Arial", 20)).pack()

# Registration Frame UI
tk.Label(registration_frame, text="Register", bg='black', fg='white', font=("Arial", 30)).pack(pady=20)
tk.Label(registration_frame, text="Name:", bg='black', fg='white', font=("Arial", 20)).pack()
name_entry = tk.Entry(registration_frame, font=("Arial", 20))
name_entry.pack(pady=5)

tk.Label(registration_frame, text="Email:", bg='black', fg='white', font=("Arial", 20)).pack()
email_reg_entry = tk.Entry(registration_frame, font=("Arial", 20))
email_reg_entry.pack(pady=5)

tk.Label(registration_frame, text="Password:", bg='black', fg='white', font=("Arial", 20)).pack()
password_reg_entry = tk.Entry(registration_frame, show='*', font=("Arial", 20))
password_reg_entry.pack(pady=5)

tk.Button(registration_frame, text="Register", command=register_user, bg='green', fg='white', font=("Arial", 20)).pack(pady=20)
tk.Button(registration_frame, text="Back to Login", command=show_login, bg='red', fg='white', font=("Arial", 20)).pack()

# Enable/Disable Frame UI
tk.Label(enable_disable_frame, text="USB Port Control", bg='black', fg='white', font=("Arial", 30)).pack(pady=20)
enable_button = tk.Button(enable_disable_frame, text="Enable USB Ports", command=enable_usb, bg='green', fg='white', font=("Arial", 20))
enable_button.pack(pady=20)

disable_button = tk.Button(enable_disable_frame, text="Disable USB Ports", command=disable_usb, bg='red', fg='white', font=("Arial", 20))
disable_button.pack(pady=20)

# Create the About Project button
about_button = tk.Button(root, text="About Project", command=open_about_project, bg='white', fg='black', font=("Arial", 20))
about_button.pack(pady=20)

# Start with the login frame
show_login()

# Start the Tkinter event loop
root.mainloop()
