# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function for existing user check
def check_existing_user(username):
    with open("user.txt", "r") as file:
        for line in file:
            existing_username, _ = line.strip().split(";")
            if existing_username == username:
                return True
    return False

# Function for a new user
def reg_user():
    '''Add a new user to the user.txt file'''
        # - Request input of a new username
    new_username = input("New Username: ")
    
    # Existing user check
    if check_existing_user(new_username):
        print("User already exists.")

        # - Request input of a new password
    else:
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")
# Creating tasks
def add_task():
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    else:
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        
        task_id = len(task_list) + 1 # Adding variable to add an number to the start of each task

        new_task = {
            "task_id": task_id, # Adding to the task
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    str(t['task_id']), # Writing to the file
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task ID: \t {t['task_id']}\n" # Displaying the task ID
        disp_str += f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    '''
    while True:
        print("These are your assigned tasks:\n")
    
        for t in task_list:
            if t['username'] == curr_user:
                disp_str = f"Task ID: \t {t['task_id']}\n" # Displaying the task ID
                disp_str += f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)

        task_edit = input("Enter a task ID to update or enter '-1' to exit to main menu: ")
        if task_edit == '-1':
            break

        task_edit = int(task_edit)
        task_sign_off(task_edit, curr_user)
        update_task(task_edit, curr_user)

# Function for signing off tasks
def task_sign_off(task_id, username):
    found_task = False
    for t in task_list:
        if str(t['task_id']) == str(task_id) and t['username'] == username:
            found_task = True
# Completion check
            if t['completed']:
                print("Task has already been marked as completed. Cannot update.")
                break
# Task sign off
            while True:
                sign_off = input("Would you like to mark this task as complete? (yes/no): ")
                if sign_off.lower() == 'yes':
                    t['completed'] = True
                    update_tasks_file()
                    break
                elif sign_off.lower() == 'no':
                    t['completed'] = False
                    update_tasks_file()
                    break
                else:
                    print("Invalid entry. Please type 'yes' or 'no'.")
    if not found_task:
        print("Task ID not found or you don't have permission to update this task.")

# Function for updating the task
def update_task(task_id, username):
    found_task = False

    for t in task_list:
        if str(t['task_id']) == str(task_id) and t['username'] == username:
            found_task = True
# Completion check            
            if t['completed']:
                break
# Update task
            while True:
                updated_username = input("\nEnter new assigned user or press Enter to keep current: ")
                if updated_username:
                    if updated_username not in username_password.keys():
                        print("User does not exist. Please enter a valid username.")
                    else:
                        t['username'] = updated_username
                        update_tasks_file()
                        print("username updated successfully!")
                        break
                else:
                    print("Task username unchanged.")

                updated_due_date = input("\nEnter new due date (YYYY-MM-DD) or press Enter to keep current: ")
                if updated_due_date:
                    t['due_date'].strftime(DATETIME_STRING_FORMAT)
                    update_tasks_file()
                    print("Due date updated successfully!")
                    break
                else:
                    print("Task due date unchanged.\n")
                    break
            break

    if not found_task:
        print("Task ID not found, you don't have permission to update this task n\or the task has been completed")

# Function for updating the task file when changes are made
def update_tasks_file():
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                str(t['task_id']),  # Writing to the file
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Function for generating the task report
def task_report():
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n") # to 2 decimal places
        task_overview_file.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

# Function for generating the user report
def user_report():
    total_users = len(username_password)
    total_tasks = len(task_list)

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total users: {total_users}\n")
        user_overview_file.write(f"Total tasks: {total_tasks}\n")
# Stats for each user      
        for username in username_password:
            user_tasks = [task for task in task_list if task['username'] == username]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(task['completed'] for task in user_tasks)
            uncompleted_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'].date() < date.today())

            user_tasks_percentage = (total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            completed_percentage = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            uncompleted_percentage = (uncompleted_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            overdue_user_percentage = (overdue_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0

            user_overview_file.write(f"\nUser: {username}\n")
            user_overview_file.write(f"Total tasks assigned: {total_user_tasks}\n")
            user_overview_file.write(f"Percentage of total tasks: {user_tasks_percentage:.2f}%\n")
            user_overview_file.write(f"Percentage of completed tasks: {completed_percentage:.2f}%\n")
            user_overview_file.write(f"Percentage of uncompleted tasks: {uncompleted_percentage:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {overdue_user_percentage:.2f}%\n")

# Open the files and display file not found error used for error checking
def display_stats():
    report_gen()

    try:
        with open("task_overview.txt", "r") as task_overview_file:
            task_stats = task_overview_file.read()
            print("\nTask Statistics:")
            print(task_stats)
    except FileNotFoundError:
        print("Task statistics not found.")

    try:
        with open("user_overview.txt", "r") as user_overview_file:
            user_stats = user_overview_file.read()
            print("User Statistics:")
            print(user_stats)
    except FileNotFoundError:
        print("User statistics not found.")

# Create reports if it doesn't exist
def report_gen():
    if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
        print("Reports not found. Generating reports.")
        task_report()
        user_report()

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]



task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component, moved each component forward 1 to add ID
    task_components = t_str.split(";")
    curr_t['task_id'] = task_components[0]
    curr_t['username'] = task_components[1]
    curr_t['title'] = task_components[2]
    curr_t['description'] = task_components[3]
    curr_t['due_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[5], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[6] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Created a dedicated admin menu
while True:
    print()
    if curr_user == 'admin':
        menu_admin = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

        if menu_admin == 'r':
            reg_user()

        elif menu_admin == 'a':
            add_task()

        elif menu_admin == 'va':
            view_all()
     
        elif menu_admin == 'vm':
            view_mine()

        elif menu_admin == 'gr':
            task_report()
            user_report()
            print("Reports generated")
            
        elif menu_admin == 'ds': 
            display_stats()    

        elif menu_admin == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")

# Removed the admin functions from general users
    else:
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
: ''').lower()

        if menu == 'r':
            reg_user()

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()
     
        elif menu == 'vm':
            view_mine()
                
        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")
