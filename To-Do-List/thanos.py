# IMPORTS

# json: Let's us save and load data to/from JSON files
# datetime: Lets us work with dates and times 
import json 
from datetime import datetime 



#Constants 

# Constants are values that never change during the program
# By convention, we use ALL_CAPS for constant names 

# This is the file where all tasks will be saved
TASKS_FILE = "infinity_stones.json" 

# This dictionary maps prirority keys to their display names with emjois 
# Keys (left side): what we store in the data 
# Values (right side): what we show to the user 

PRIORITY_STONES = {
    "power": "POWER (Urgent & Critical)", 
    "reality": "REALITY (Important Deadline)", 
    "soul": "SOUL (Flexible Timeline)", 
    "time": "TIME (Scheduled Future)", 
    "mind": "MIND (Ideas/Brainstorming)"
}


# File Handling Functions

# These two functions handle saving and loading data from the JSON file
# They are the foundation of data persistence in the app 

def load_tasks(): 
    """
    Load tasks from the JSON file. 

    How it works: 
    1. Try to open the file and read the JSON data 
    2. If the file doesn't exist yet, return to an empty list 

    Returns: 
    list: A list of task dictionaries, or empty list if no file exists
    """

    try: 
        # "r" means read mode 
        # "with" automatically closes the file when done 
        with open(TASKS_FILE, "r") as file: 
            # json.load() converts JSON text into Python objects 
            return json.load(file) 
    except FileNotFoundError:
        # File doesn't exist yet (first time running) 
        # Return empty list so the program can still work 
        return []
    

def save_tasks(tasks): 
    """
    Save task to the JSON file. 

    How it works: 
    1. Open the file is write mode (creates it if it doesn't exist) 
    2. Convert the Python list to JSON and write it

    Args: 
        taks (list): The list of task dictionaries to save
    """
    # "w" means write mode (overwrites existing content) 
    with open(TASKS_FILE, "w") as file: 
        # json.dump() converts Python objects to JSON text
        # indent=2 makes the file human-readable with nice formatting 
        json.dump(tasks, file, indent=2)




# Helper Functions 


# These are utility finctions that help other function do their job 
# Breaking code into small helper functions makes it easier to read and maintain 

def get_days_remaining(due_date): 
    """
    Calculate how many days until a task is due. 

    How it works: 
    1. Convert the due date string to a datetime object 
    2. Get today's date
    3. Subtract to find the difference in days


    Args: 
        due_date (str): Data string in "YYYY-MM-DD" format 

    Returns: 
        int: Number of dats until due (negative if overdue) 
    """

    # strptime = "string parse time" - converts string to datetime
    # The format string tells it how to interpret the date
    # %Y = 4 - digit year, %m = 2-digit month, "%d = 2-digit day 
    due = datetime.strptime(due_date, "&Y-%m-%d")
    
    
    # Get current date and time" 
    today = datetime.now()
    
    
    # Subtracitng datetimes gives a timedelta object 
    # .days extracts just the number of days
    delta = (due - today).days
    
    return delta

def select_priority(): 
    """
    Display priority menu and get user's choice. 

    How it works: 
    1. Show all available Infinity Stone options
    2. Keep asking until user gives valid input
    3. Convert their number choice to a priority key 

    Returns: 
        str: The priority key (e.g., "power", "reality", etc.) 
    """

    print("\n--- SELECT YOUR INFINITY STONE ---")
    print("[1] Power = Urget & Critical") 
    print("[2] Reality - Important Deadline") 
    print("[3] Space - Flexible Timeline") 
    print("[4] Soul - Personal/Optional") 
    print("[5] Time - Scheduled Future") 
    print("[6] Mind - Ideas/Brainstorming") 

    # This dictionary maps user input in priority keys 
    # Makes it easy to convert "1" to "power", "2" to "reality", etc.
    stone_map = {
        "1": "power", 
        "2": "reality", 
        "3": "space", 
        "4": "soul", 
        "5": "time", 
        "6": "mind"
    }

    # Keep looping until we get valid input 
    while True: 
        choice = input("\nChoose stone (1-6): ").strip()

        # Check if the choice exists in our map 
        if choice in stone_map: 
            return stone_map[choice]
        
        # Invalid input - show error and loop again 
        print("Invalid choice. The stones reject your selection.") 

def get_time_status(days): 
    """
    Convert days remaining into a human-readble status message. 
     Args: 
      days (int): Number of days until due date
       
    Returns: 
     str: A formatted status message
     """
    if days < 0: 
        # Task is overdue 
        # abs() converts negative to positive for display 
        return f"OVERDUE by {abs(days)} days!"
    elif days == 0: 
        return "DUE TODAY!"
    elif days == 1: 
        return "Due Tomorrow" 
    else: 
        return f"{days} days remaining" 
    

# DISPLAY FUNCTIONS

# This function shows taks to the user with nice formatting 

def display__tasks(tasks, filter_type=None): 
    """
    Display tasks with formatting and optional filtering.

    How it works:
    1. Check if there are any tasks to display 
    2. Apply any filters (active, complete, or by priority) 
    3. Loop through and display each task with details
    4. Show progress statistics at the end 

    Args: 
        tasks (list): The full list of task dictionaries 
        filter_type(str, optional): Filter toapply = "active", "complete",
        or a priority key. Defaults to None (show all) 
    """
    # Handle empty task list 
    if not tasks: 
        print("\n The Gauntlet is empty. No tasks found in this reality.")
        return 
    
    #Start with all tasks 
    filtered = tasks 

    # Apply filters based on filter_type parameter 
    # List comprehesnions create a new list based on a condition 
    if filter_type == "active": 
        # Keep only incomplete tasks 
        filtered = [t for t in tasks if t["status"] == "incomplete"]
    elif filter_type == "complete": 
        # Keep only completed tasks 
        filtered = [t for t in tasks if t["status"] == "complete"]
    elif filter_type in PRIORITY_STONES: 
    # Keep only taks with matching priority 
        filtered = [t for t in tasks if t ["priority"] == filter_type]
    
    # Handle case where filter returns no results
    if not filtered: 
        print("\nNo tasks match this filter.") 
        return
    
    # Print header 
    print("\n" + "=" * 60)
    print("THE INFINITY GAUNTLET - Your tasks")
    print("=" * 60)

    # Loop through each task and sdisplay it
    # enumerate() gives us borth the index (i) and the item (task)
    # Starting at 1 makes the numbering user-friendly
    for i, task in enumerate (filtered, 1): 

        # Choose status icon based on completion 
        if task["status"] == "complete": 
            status_icon = "[DONE]" 
        else: 
            status_icon = "[    ]"

        # Get the display name for this priority
        # .get() returns a default value if key not found 
        stone = PRIORITY_STONES.get(task["priority"], "UNKNOW") 


        # Calculate days remaining and get status message 
        days = get_days_remaining(task['due_date'])
        time_status = get_time_status(days)

        # Print tasks details 
        # \n create a blank line for spacing 
        print(f"\n{i} {status_icon} {task['title']})")
        print(f" Stone: {stone}")
        print(f" Due: {task['due_date']} ({time_status})")
        print(f" Description: {task['description']}")


    # Print footer 
    print("\n" + "=" * 60) 

    # Calculate and display statistics 
    total = len(tasks) 
    complete = len([t for t in tasks if t["status"] == "complete"])

    # Avoid division by zero 
    if total > 0:
        percentage = int(complete / total * 100) 
    else: 
        percentage = 0 
    print(f"Progress: {complete}/{total} tasks complete ({percentage}%)")


# Create Function 

# This fucntion handles creating new tasks 

def create_task(tasks): 
    """
    Create a new ask and add it to the list. 

    How it works: 
    1. Get task details from user input
    2. Validate the input (especially the date) 
    3. Create a task dictionary with all properties 
    4. Add to the list and save to file

    Args: 
        tasks (list): The list of tasks (will be modified) 
    """

    print("\n" + "=" * 40) 
    print("FORGE NEW TASK") 
    print("=" * 40)

    # Get title - this is required 
    # .strip() removes leading/trailing whitespace
    title = input("\n Task title: ").strip()
    

    # Validate title is not empty 
    if not title: 
        print("Error: A task without a name no purpose in this unverse.")
        return # Exit the function early
    
    # Get description - this is optional
    description = input("Description: ").strip()
    if not description: 
        description = "No description provided" 
    
    # Get priority using our helper function 
    priority = select_priority()

    # Get due date with validation loop
    #Keep asking until user gives valid date format
    while True:
        due_date = input("\nDue date (YYYY-MM-DD): ").strip()

        try: 
            # Try to parse the date = if it fails, we catch the error 
            datetime.strptime(due_date, "%Y-%m-%d)")
            break # Valid date - exit the loop 
        except ValueError: 
            # Invalid format = show error and loop again
            print("Invalid date format.  The Tiem Stone requires YYYY-MM-DD." )

    # Create the task dictionary
    # This contains all the properties for one task
    new_task = {
        # Unique ID based on timestamp
        "id": datetime.now().strftime("%Y%m%d%H%M%S"), 
        "title": title, 
        "description": description, 
        "priority": priority, 
        "due_date": due_date, 
        "status": "incomplete", 
        # Record when the task was created 
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   }
    
    # Add the new task to the list
    tasks.append(new_task) 

    # Save to file immediately
    save_tasks(tasks) 

    # Confirm to user 
    print(f"\n'{title}' has been added to the Gauntlet!")
    print(f"Infinity Stone: {PRIORITY_STONES[priority]}")


# UPDATE FUNCTION

# This fucntion handles modifying existing tasks

def update_task(tasks): 
    """
    Update an existing tasks. 

    How it works: 
    1. Display all tasks so user can see the numbers
    2. Get user's selection 
    3. For each field, show current value and ask for new value
    4. Only update fields where user provides new input 
    5. Save changes to file

    Args: 
        tasks (list): The list of tasks (will be modified)
    """
    # Check if there are any tasks to update 
    if not tasks: 
        print("\nNo tasks exist to alter.")
        return
    
    #  Show current tasks so user can pick one 
    display__tasks(tasks) 

    # Get task selection with error handling 
    try: 
        # Subtract 1 because list indices start at 0
        # but we displayed starting at 1 for user-friendliness
        index = int(input("\nEnter task number to modify: ")) - 1

        # Validate the index is in range 
        if index < 0 or index >= len(tasks): 
            print("That task does not exist in this reallity.") 
            return
    except ValueError: 
        # User entered something that's not a number 
        print("Invalid input. Enter a number.")
        return
    # Get the task to modify
    task = tasks[index]
    
    print(f"\nALTERING: {task['title']}")
    print("(Press Enter to keep  current value)\n") 

    # Get new values for each field 
    # We show current value in brackets as a hint
    new_title = input(f"Title [{task['title']}]: ").strip()
    new_desc = input(f"Description [{task['description']}]: ").strip()

    # Priority change requires extra confirmation 
    print(f"\nCurrent Stone: {PRIORITY_STONES[task['priority']]}")
    change_stone = input("Chnage Infinity Stone? (y/n): ").strip().lower()

    # Only show priority meni if user wants to change it
    if change_stone == "y": 
        new_priority = select_priority()
    else: 
        new_priority = None
    
    new_due = input(f"\nDue date [{task['due_date']}]: ").strip()

    # Status change 
    print(f"\nCurrent Status: {task['status'].upper()}")
    new_status = input("Mark as complete? (y/n):) ").strip().lower()

    # Apply changes only if user provided new values 
    # Empty string is "falsy" in Python, so "if new_title:" is False for ""
    if new_title: 
        task["description"] = new_title

    if new_desc: 
        task["priority"] = new_priority 
    
    # Validate new due date if provided
    if new_due: 
        try: 
            datetime.strptime(new_due, "%Y-%m-%d")
            task["due_date"] = new_due
        except ValueError: 
            print("Invalid date format. Keeping original.") 
    
    # Handle status change 
    if new_status == "y": 
        task["status"] = "complete"
    elif new_status == "n": 
        task["status"] = "incomplete"
    # If neither y nor n, keep current status


    # Add modification timestamp
    task["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save changes 
    save_tasks(tasks) 

    print("\nReality has been altered. Task updated!")



# Delete Function 

# This fucntion handles removing tasks 

def delete_task(tasks): 
    """
    Delete a task from the list. 

    How it works: 
    1. Display all tasks 
    2. Get user's selection 
    3. Ask for confirmation  (user must type SNAP) 
    4. Remove from list and save

    Args:
        tasks (list): The list of tasks (will be modified) 
    """
    # Check if there are any tasks to delete
    if not tasks: 
        print("\nThe Gauntlet is already empty.") 
        return
    
    # Show current tasks
    display__tasks(tasks) 

    # Get task selection with error handling 
    try: 
        index = int(input("\nEnter task number to SNAP: ")) - 1 

        if index < 0 or index >= len(tasks): 
            print("That task does not exist.") 
            return
    except ValueError: 
        print("Invalid input.") 
        return
    
    # Store the task naem before deleting (for confirmation message) 
    task_name = tasks[index]["title"]
    
    # Require confirmation - this prevents accidental deletes
    print(f"\nYou are about to snap '{task_name}' out of existance.") 
    confirm = input("Type 'SNAP' to cofirm: ").strip()

    # Check for exatch match 
    if  confirm == "SNAP": 
        # .pop() removes and returns the item at the given index
        tasks.pop(index) 
        save_tasks(tasks) 
        print(f"\n*snap* '{task_name}' has been erased from existance.")

    else: 
        print("The task has been spared.") 
    

# EXTRA FEATURE FUNCTIONS

# These add additional functionality beyond basic CRUD

def snap_completed(tasks): 
    """
    Delete all completed tasks at once. 

    How it works: 
    1. Count how many completed tasks at once. 
    2. Ask for confirmation 
    3. Remove all completed tasks and save

    Args: 
        tasks (list): The list of tasks (will be modified) 
    """
    # Find all completed tasks 
    completed = [t for t in tasks if t["status"] == "complete"]

    # Check if there are any to delete
    if not completed: 
        print("\nNo completed tasks to snap.")
        return
    
    # Show warning and ask for confirmation 
    print(f"\nYou are about to snap {len(completed)} completed tasks.") 
    confirm = input("Type 'SNAP' to confirm: ").strip()

    if confirm == "SNAP": 
        # This syntax modifies the list in-place 
        # tasks[:] = ... replaces the contents of the original list
        # This is important because we're modifying the list passed by reference 
        tasks[:] = [t for t in tasks if t["status"] != "complete"]
        save_tasks(tasks) 
        print(f"\n*SNAP* {len(completed)} task erased. Perfectly balanced.") 
    else: 
        print("The tasks have been spared.") 


def view_by_stone(tasks):
    """
    Filter and display tasks by Infinity Stone priority. 

    Args: 
        tasks (list): The list of tasks 
    """
    print("\n--- FILTER BY INFINITY STONE ---") 

    # Use our helper function to get priority choice
    priority = select_priority()
    
    # Call display_tasks with the filter
    display__tasks(tasks, filter_type=priority) 



# Menu Function 

# Displays the main menu options 

def main_menu(): 
    """
    Display the main menu options. 

    This is separated into its own function to keep main() clean
    and to make it easy to modify the menu appearance. 
    """

    print("\n" + "=" * 40) 
    print("T.H.A.N.O.S. COMMAND CENTER") 
    print("=" * 40)
    print("[1] View All Tasks") 
    print("[2] Forge New Task (Create)")
    print("[3] Alter Task (Update)") 
    print("[4] Snap Task (Delete)") 
    print("[5] Filter by Infinity Stone") 
    print("[6] View Active Tasks Only") 
    print("[7] View Completed Tasks Only") 
    print("[8] Snap All Completed Tasks") 
    print("[9] Exit") 
    print("=" * 40) 


# Main Function 

# This is the entry pointt and main loop of the program 

def main(): 
    """
    Main porgam loop. 

    How it works: 
    1. Display welcome banner 
    2. Load existing tasks from file 
    3. Enter main loop: 
        a. Show menu
        b. Get user choice 
        c. Call appropriate function 
        d. Repeat unti user chooses exit
    """

    #Welcome message 
    print("\n" + "=" * 60)
    print("Welcome to T.H.A.N.O.S.") 
    print("Task Handling And Notification Organization System") 
    print("=" * 60) 
    print('\n Fun isn\t something one considers when balancing tasks.')
    print(' But this... does put a smile on my face."')

    # Load existing tasks from the JSON file 
    tasks = load_tasks() 

    # Main program loop - runs until user chooses to exit
    while True: 
        # Show the menu
        main_menu() 

        # Get user's choice 
        choice = input("\nEnter command (1-9): ").strip() 

        # Route to appropriate function based on choice 
        # Using if/elif chain to handle each option 
        if choice == "1": 
            display__tasks(tasks) 
        
        elif choice == "2": 
            create_task(tasks) 
        
        elif choice == "3": 
            update_task(tasks) 

        elif choice == "4": 
            delete_task(tasks) 

        elif choice == "5": 
            view_by_stone(tasks) 
        
        elif choice == "6": 
            # Pass filter_type to show only incomplete tasks
            display__tasks(tasks, filter_type="active")
        
        elif choice == "7": 
            # Pass filter_type to show only completed tasks 
            display__tasks(tasks, filter_type="complete") 
        
        elif choice == "8": 
            snap_completed(tasks) 
        
        elif choice == "9": 
            # Exit the program
            print("\n" + "=" * 40) 
            print('"I am... inevitable."') 
            print("=" * 40) 
            print("Your tasks have been saved to the vault.") 
            print("Unitl next time, T.H.A.N.O.S. signing off.\n")
            break # Exist the while loop 
        
        else: 
            # Invalid choice = show error
            print("Invalid command. Choose wisely (1-9).")


# Program Entry Point 

# This is a Python convention that checks if this file is being run directly
# (as opposed to being imported as a module by another file) 

if __name__ == "__main__": 
    #Only run main() if this file is executed directly
    main()






