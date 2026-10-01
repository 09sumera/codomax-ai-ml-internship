import json
import os 

habits=[]
completed=[]
if os.path.exists("habits.json"):
    with open("habits.json", "r") as file:
        data = json.load(file)
        habits = data["habits"]
        completed = data["completed"]
def save_data():
    data = {
        "habits": habits,
        "completed": completed
    }

    with open("habits.json", "w") as file:
        json.dump(data, file, indent=4)
while True :
    print("==== SMART DAILY HABIT TRACKER ====")
    print("1. Add Habit")
    print("2. View Habit ")
    print("3. Mark Habit Complete")
    print("4. View Progress ")
    print("5. Delete Habit ")
    print("6. Exit ")
    choice = int(input("Enter Choice :" ))
    if choice ==1:
        add=input("Enter habit u want to add :")
        habits.append(add)
        save_data()
        print("Habit added successfully!")
    elif choice==2:
        if not habits :
            print("No habits Available ")
        else:
            print("Your Habits :")
            for n,h  in enumerate(habits, start=1):
                print(f"{n}.{h}")
    elif choice==3:
        if not habits  :
            print("No habits available  ")
        else:
            for n,h in enumerate(habits,start=1):
                print(f"{n}.{h}")
            number=int(input("Enter habit number :"))
            selected_habit=habits[number-1]
            if selected_habit in completed:
                print("⚠️ Habit is already completed!")
            else:
                completed.append(selected_habit)
                save_data()
                print("✅", selected_habit, "marked as completed!")
    elif choice==4:
        if not habits:
            print("No habits available ")
        else:
            habitslen=len(habits)
            completedlen=len(completed)
            remaining=habitslen-completedlen
            print("Total Habits:",habitslen)
            print("Completed:",completedlen)
            print("Remaining:",remaining)
    elif  choice==5:
        if not habits :
            print("No habits available ")
        else:
            for n,h in enumerate(habits,start=1):
                print(f"{n}.{h}")
            habitnumber=int(input("Enter a habit to delete: "))
            selected_habit = habits[habitnumber - 1]
            habits.remove(selected_habit)
            if selected_habit in completed:
                completed.remove(selected_habit)
            save_data()
            print("✅", selected_habit, "deleted successfully!")
    elif choice == 6:
        print("Good Bye ")
        break 
    else:
        print("Invalid choice ")
