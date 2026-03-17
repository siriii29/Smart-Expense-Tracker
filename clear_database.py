"""
This script clears all data from the database.
WARNING: This action cannot be undone!
"""
from utils.database import clear_all_data

def main():
    print("WARNING: This will delete ALL data from the database!")
    confirm = input("Are you sure you want to continue? (yes/no): ")
    
    if confirm.lower() == 'yes':
        if clear_all_data():
            print("✅ All data has been successfully deleted from the database.")
        else:
            print("❌ An error occurred while clearing the database.")
    else:
        print("Operation cancelled. No data was deleted.")

if __name__ == "__main__":
    main()
