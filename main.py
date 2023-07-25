import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import colorama
import pymongo
#user object id
import bson
#regex
import re
#python gui (window)
import tkinter as tk
from tkinter import messagebox, ttk

# Initialize colorama
colorama.init()

# Color codes for menu
MENU_COLOR = '\033[38;2;255;165;0m'
OPTION_COLOR = '\033[38;2;0;191;255m'
OUTPUT_COLOR = '\033[38;2;50;205;50m'
PROMPT_COLOR = '\033[38;2;255;255;0m'
RESET_COLOR = '\033[0m'

def connect_to_mongodb():
    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.r6eddxt.mongodb.net/?retryWrites=true&w=majority")
    db = client["Python"]
    collection = db["users"]
    return collection


def display_table(dataframe):
    table = tabulate(dataframe, headers=dataframe.columns, tablefmt='fancy_grid')
    print(f"{OUTPUT_COLOR}{table}")

def display_graph(dataframe, x, y, graph_type='bar'):
    dataframe.plot(x=x, y=y, kind=graph_type)
    plt.show()

def average_age(collection):
    current_year = pd.to_datetime('today').year
    data = collection.find({})
    df = pd.DataFrame(data)
    df['birth_date'] = pd.to_datetime(df['birth_date'])
    df['age'] = current_year - df['birth_date'].dt.year
    avg_age = df['age'].mean()
    print(f"{OUTPUT_COLOR}The average age of individuals is: {avg_age:.2f} years")

def most_common_first_names(collection):
    data = collection.find({})
    df = pd.DataFrame(data)
    common_names = df['first_name'].value_counts().reset_index()
    common_names.columns = ['First Name', 'Count']
    print(f"{OUTPUT_COLOR}Most common first names:")
    display_table(common_names)

    # Pie chart of top 5 most common first names
    common_names[:5].plot(kind='pie', y='Count', labels=common_names['First Name'][:5], autopct='%1.1f%%')
    plt.title("Top 5 Most Common First Names")
    plt.ylabel('')
    plt.show()

def percentage_by_city(collection):
    data = collection.find({})
    df = pd.DataFrame(data)
    city_percentage = (df['city'].value_counts() / len(df)) * 100
    print(f"{OUTPUT_COLOR}Percentage of individuals from each city:")
    print(city_percentage)

    # Bar chart of percentage by city
    city_percentage.plot(kind='bar')
    plt.title("Percentage of Individuals from Each City")
    plt.ylabel('Percentage')
    plt.show()

def earliest_birth_date(collection):
    data = collection.find({})
    df = pd.DataFrame(data)
    earliest_date = df['birth_date'].min()
    person = df[df['birth_date'] == earliest_date]
    print(f"{OUTPUT_COLOR}Person with the earliest birth date:")
    display_table(person)

def count_gmail_users(collection):
    data = collection.find({})
    df = pd.DataFrame(data)
    gmail_users = df[df['email'].str.contains('gmail.com')]
    count = len(gmail_users)
    print(f"{OUTPUT_COLOR}Number of individuals with Gmail email address: {count}")

def sort_by_last_name(collection):
    data = collection.find({})
    df = pd.DataFrame(data)
    sorted_data = df.sort_values('last_name')
    print(f"{OUTPUT_COLOR}Sorted data by last name in alphabetical order:")
    display_table(sorted_data)

def count_last_name_occurrences(collection):
    data = collection.find({})
    df = pd.DataFrame(data)
    last_name_counts = df['last_name'].value_counts().reset_index()
    last_name_counts.columns = ['Last Name', 'Occurrences']
    print(f"{OUTPUT_COLOR}Occurrences of individuals with the same last name:")
    display_table(last_name_counts)

    # Bar chart of last name occurrences
    last_name_counts.plot(kind='bar', x='Last Name', y='Occurrences')
    plt.title("Occurrences of Individuals with the Same Last Name")
    plt.xlabel('Last Name')
    plt.ylabel('Occurrences')
    plt.show()

def average_email_length(collection):
    data = collection.find({})
    df = pd.DataFrame(data)
    df['email_length'] = df['email'].apply(len)
    avg_length = df['email_length'].mean()
    print(f"{OUTPUT_COLOR}The average length of email addresses is: {avg_length:.2f} characters")

def individuals_by_decade(collection):
    data = collection.find({})
    df = pd.DataFrame(data)
    df['birth_date'] = pd.to_datetime(df['birth_date'])
    df['decade'] = (df['birth_date'].dt.year // 10) * 10
    individuals_per_decade = df['decade'].value_counts().sort_index().reset_index()
    individuals_per_decade.columns = ['Decade', 'Count']
    print(f"{OUTPUT_COLOR}Number of individuals born in each decade:")
    display_table(individuals_per_decade)

    # Line graph of individuals by decade
    individuals_per_decade.plot(kind='line', x='Decade', y='Count', marker='o')
    plt.title("Number of Individuals Born in Each Decade")
    plt.xlabel('Decade')
    plt.ylabel('Count')
    plt.show()

def filter_older_than_50(collection):
    current_year = pd.to_datetime('today').year
    data = collection.find({})
    df = pd.DataFrame(data)
    df['birth_date'] = pd.to_datetime(df['birth_date'])
    df['age'] = current_year - df['birth_date'].dt.year

    filtered_data = df[df['age'] > 50]
    print(f"{OUTPUT_COLOR}Filtered data including only individuals older than 50 years:")
    display_table(filtered_data)

def youngest_oldest_individuals_by_city(collection):
    data = collection.find({})
    df = pd.DataFrame(data)
    df['birth_date'] = pd.to_datetime(df['birth_date'])
    df['age'] = pd.to_datetime('today').year - df['birth_date'].dt.year
    grouped_data = df.groupby('city')

    youngest = df.loc[grouped_data['age'].idxmin()]
    oldest = df.loc[grouped_data['age'].idxmax()]

    print(f"{OUTPUT_COLOR}Youngest individuals by city:")
    display_table(youngest)
    print(f"{OUTPUT_COLOR}Oldest individuals by city:")
    display_table(oldest)

    # Bar chart of youngest and oldest individuals by city
    youngest_oldest_data = pd.concat([youngest, oldest])
    display_graph(youngest_oldest_data, 'city', 'age', 'bar')

def add_new_user_gui(collection):
    def is_valid_first_name(first_name):
        return bool(re.match("^[a-zA-Z]+$", first_name))

    def is_valid_last_name(last_name):
        return bool(re.match("^[a-zA-Z]+$", last_name))
    def is_valid_username(username):
        return bool(re.match("^[a-zA-Z0-9]{1,15}$", username))

    def is_valid_email(email):
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

    def is_valid_phone(phone):
        return bool(re.match(r"^\+972\d{9}$", phone))

    def is_valid_birth_date(birth_date):
        return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", birth_date))

    def is_valid_city(city):
        return bool(re.match(r"^[a-zA-Z\s]+$", city))

    def add_user_to_db():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        username = entry_username.get()
        email = entry_email.get()
        phone = entry_phone.get()
        birth_date = entry_birth_date.get()
        city = entry_city.get()

        if not first_name or not last_name or not username or not email or not phone or not birth_date or not city:
            messagebox.showerror("Error", "All fields are required.")
            return
        if not is_valid_first_name(first_name):
            messagebox.showerror("Error", "Invalid first name. It should contain only letters.")
            return

        if not is_valid_last_name(last_name):
            messagebox.showerror("Error", "Invalid last name. It should contain only letters.")
            return

        if not is_valid_username(username):
            messagebox.showerror("Error", "Invalid username. It can contain only characters and numbers, maximum 15 characters.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        if not is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone number. It should start with +972 and have 9 digits.")
            return

        if not is_valid_birth_date(birth_date):
            messagebox.showerror("Error", "Invalid birth date format. Use yyyy-mm-dd.")
            return

        if not is_valid_city(city):
            messagebox.showerror("Error", "Invalid city name. It should contain only letters and spaces.")
            return

        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "phone": phone,
            "birth_date": birth_date,
            "city": city
        }

        collection.insert_one(user_data)
        messagebox.showinfo("Success", "User added successfully.")
        root.destroy()  # Close the GUI window after adding the user

    root = tk.Tk()
    root.title("Add New User")
    root.geometry("450x450")

    # Styling the GUI with ttk theme
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 16))
    style.configure('TEntry', font=('Arial', 16))
    style.configure('TButton', font=('Arial', 16))


    # GUI elements for user input
    label_first_name = tk.Label(root, text="First Name:")
    label_first_name.pack()
    entry_first_name = tk.Entry(root)
    entry_first_name.pack()

    label_last_name = tk.Label(root, text="Last Name:")
    label_last_name.pack()
    entry_last_name = tk.Entry(root)
    entry_last_name.pack()

    label_username = tk.Label(root, text="Username:")
    label_username.pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    label_email = tk.Label(root, text="Email:")
    label_email.pack()
    entry_email = tk.Entry(root)
    entry_email.pack()

    label_phone = tk.Label(root, text="Phone Number:")
    label_phone.pack()
    entry_phone = tk.Entry(root)
    entry_phone.pack()

    label_birth_date = tk.Label(root, text="Birth Date (yyyy-mm-dd):")
    label_birth_date.pack()
    entry_birth_date = tk.Entry(root)
    entry_birth_date.pack()

    label_city = tk.Label(root, text="City:")
    label_city.pack()
    entry_city = tk.Entry(root)
    entry_city.pack()

    button_add = ttk.Button(root, text="Add User", command=add_user_to_db, style='Custom.TButton')
    button_add.pack(pady=10)

    style = ttk.Style()
    style.configure('Custom.TButton', background='blue', foreground='black', font=('Arial', 16))

    root.mainloop()

# New function to delete a user by ID
def delete_user_by_id(collection):
    user_id_str = input(f"{PROMPT_COLOR}Enter user ID: {RESET_COLOR}")

    try:
        user_id = bson.ObjectId(user_id_str)
    except bson.errors.InvalidId:
        print(f"{OUTPUT_COLOR}Invalid user ID format. Please enter a valid hexadecimal ID.")
        return

    # Find the user in the collection by ID
    user = collection.find_one({"_id": user_id})

    if user:
        # Extract the first name and last name of the user
        first_name = user.get('first_name', 'Unknown')
        last_name = user.get('last_name', 'Unknown')

        # Delete the user with the given ID
        collection.delete_one({"_id": user_id})
        print(f"{OUTPUT_COLOR}{first_name} {last_name} with ID {user_id} has been deleted.")
    else:
        print(f"{OUTPUT_COLOR}User with ID {user_id} not found.")

# New function to get a user by ID
def get_user_by_id(collection):
    user_id_str = input(f"{PROMPT_COLOR}Enter user ID: {RESET_COLOR}")

    try:
        user_id = bson.ObjectId(user_id_str)
    except bson.errors.InvalidId:
        print(f"{OUTPUT_COLOR}Invalid user ID format. Please enter a valid hexadecimal ID.")
        return

    # Find the user in the collection by ID
    user = collection.find_one({"_id": user_id})

    if user:
        # Convert the user data to a pandas DataFrame
        user_df = pd.DataFrame([user])

        # Print the user information using tabulate
        print(f"{OUTPUT_COLOR}User information for ID {user_id}:")
        display_table(user_df)
    else:
        print(f"{OUTPUT_COLOR}User with ID {user_id} not found.")

def update_user_by_id(collection, user_id):
    def is_valid_first_name(first_name):
        return bool(re.match("^[a-zA-Z]+$", first_name))

    def is_valid_last_name(last_name):
        return bool(re.match("^[a-zA-Z]+$", last_name))

    def is_valid_username(username):
        return bool(re.match("^[a-zA-Z0-9]{1,15}$", username))

    def is_valid_email(email):
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

    def is_valid_phone(phone):
        return bool(re.match(r"^\+972\d{9}$", phone))

    def is_valid_birth_date(birth_date):
        return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", birth_date))

    def is_valid_city(city):
        return bool(re.match(r"^[a-zA-Z\s]+$", city))

    def update_user_in_db():
        updated_data = {
            "first_name": entry_first_name.get(),
            "last_name": entry_last_name.get(),
            "username": entry_username.get(),
            "email": entry_email.get(),
            "phone": entry_phone.get(),
            "birth_date": entry_birth_date.get(),
            "city": entry_city.get()
        }

        # Perform validation checks on the updated data
        if not entry_first_name.get() or not entry_last_name.get() or not entry_username.get() or not entry_email.get() or not entry_phone.get() or not entry_birth_date.get() or not entry_city.get():
            messagebox.showerror("Error", "All fields are required.")
            return
        if not is_valid_first_name(entry_first_name.get()):
            messagebox.showerror("Error", "Invalid first name. It should contain only letters.")
            return

        if not is_valid_last_name(entry_last_name.get()):
            messagebox.showerror("Error", "Invalid last name. It should contain only letters.")
            return

        if not is_valid_username(entry_username.get()):
            messagebox.showerror("Error",
                                 "Invalid username. It can contain only characters and numbers, maximum 15 characters.")
            return

        if not is_valid_email(entry_email.get()):
            messagebox.showerror("Error", "Invalid email format.")
            return

        if not is_valid_phone(entry_phone.get()):
            messagebox.showerror("Error", "Invalid phone number. It should start with +972 and have 9 digits.")
            return

        if not is_valid_birth_date(entry_birth_date.get()):
            messagebox.showerror("Error", "Invalid birth date format. Use yyyy-mm-dd.")
            return

        if not is_valid_city(entry_city.get()):
            messagebox.showerror("Error", "Invalid city name. It should contain only letters and spaces.")
            return

        # Update the user in the database
        collection.update_one({"_id": user_id}, {"$set": updated_data})
        messagebox.showinfo("Success", "User updated successfully.")
        root.destroy()  # Close the GUI window after updating the use

    # Fetch the user data by ID
    user = collection.find_one({"_id": user_id})

    if not user:
        print(f"{OUTPUT_COLOR}User with ID {user_id} not found.")
        return

    root = tk.Tk()
    root.title("Update User")
    root.geometry("450x450")

    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 16))
    style.configure('TEntry', font=('Arial', 16))
    style.configure('TButton', font=('Arial', 16))


    # GUI elements for user input
    label_first_name = tk.Label(root, text="First Name:")
    label_first_name.pack()
    entry_first_name = tk.Entry(root)
    entry_first_name.insert(0, user.get('first_name', ''))  # Populate the field with the existing value
    entry_first_name.pack()

    label_last_name = tk.Label(root, text="Last Name:")
    label_last_name.pack()
    entry_last_name = tk.Entry(root)
    entry_last_name.insert(0, user.get('last_name', ''))
    entry_last_name.pack()

    label_username = tk.Label(root, text="Username:")
    label_username.pack()
    entry_username = tk.Entry(root)
    entry_username.insert(0, user.get('username', ''))
    entry_username.pack()

    label_email = tk.Label(root, text="Email:")
    label_email.pack()
    entry_email = tk.Entry(root)
    entry_email.insert(0, user.get('email', ''))
    entry_email.pack()

    label_phone = tk.Label(root, text="Phone Number:")
    label_phone.pack()
    entry_phone = tk.Entry(root)
    entry_phone.insert(0, user.get('phone', ''))
    entry_phone.pack()

    label_birth_date = tk.Label(root, text="Birth Date (yyyy-mm-dd):")
    label_birth_date.pack()
    entry_birth_date = tk.Entry(root)
    entry_birth_date.insert(0, user.get('birth_date', ''))
    entry_birth_date.pack()

    label_city = tk.Label(root, text="City:")
    label_city.pack()
    entry_city = tk.Entry(root)
    entry_city.insert(0, user.get('city', ''))
    entry_city.pack()

    button_update = ttk.Button(root, text="Update User", command=update_user_in_db, style='Custom.TButton')
    button_update.pack(pady=10)

    style = ttk.Style()
    style.configure('Custom.TButton', background='green', foreground='black', font=('Arial', 16))
    root.mainloop()

def update_user_gui(collection):
    user_id_str = input(f"{PROMPT_COLOR}Enter user ID to update: {RESET_COLOR}")

    try:
        user_id = bson.ObjectId(user_id_str)
    except bson.errors.InvalidId:
        print(f"{OUTPUT_COLOR}Invalid user ID format. Please enter a valid hexadecimal ID.")
        return

    # Call the update_user_by_id function to handle the GUI part
    update_user_by_id(collection, user_id)

# Menu options
menu_options = {
    '1': (average_age, "Calculate the average age of individuals"),
    '2': (most_common_first_names, "Identify the most common first names in the dataset"),
    '3': (percentage_by_city, "Determine the percentage of individuals from each city"),
    '4': (earliest_birth_date, "Find the person with the earliest birth date"),
    '5': (count_gmail_users, "Count the number of individuals with a Gmail email address"),
    '6': (sort_by_last_name, "Sort the data by last name in alphabetical order"),
    '7': (count_last_name_occurrences, "Identify individuals with the same last name and count their occurrences"),
    '8': (average_email_length, "Calculate the average length of email addresses"),
    '9': (individuals_by_decade, "Calculate the number of individuals born in each decade"),
    '10': (filter_older_than_50, "Filter the data to include only individuals older than 50 years"),
    '11': (youngest_oldest_individuals_by_city, "Determine the youngest and oldest individuals from each city"),
    '12': (add_new_user_gui, "Add a new user"),
    '13': (delete_user_by_id, "Delete a user by ID"),
    '14': (get_user_by_id, "Get user by ID"),
    '15': (update_user_gui, "Update user by ID"),
}

# Display menu
def display_menu():
    print(MENU_COLOR + "Statistical Reports Menu:")
    for option, description in menu_options.items():
        print(OPTION_COLOR + f"{option}. {description[1]}")

# User input for menu selection
def get_user_choice():
    selected_option = input(PROMPT_COLOR + "Select an option (1-11): ")
    print(RESET_COLOR)  # Reset colorama style
    return selected_option

# Validate and execute selected option
def execute_option(option):
    if option in menu_options:
        selected_function, _ = menu_options[option]
        selected_function(collection)
    else:
        print(OPTION_COLOR + "Invalid option selected.")

# Main program
if __name__ == "__main__":
    collection = connect_to_mongodb()

    while True:
        display_menu()
        choice = get_user_choice()
        execute_option(choice)
        print()
        continue_choice = input(PROMPT_COLOR + "Do you want to choose another option? (y/n): ")
        print()
        if continue_choice.lower() != 'y':
            break

    # Reset colorama style
    colorama.deinit()

