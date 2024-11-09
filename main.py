import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os


# Function to log real-time activities or past activities
def log_activity(activity, start_time, end_time):
    # Calculate the duration in minutes
    duration = (end_time - start_time).seconds / 60
    entry = {
        'Date': start_time.date(),
        'Activity': activity,
        'Start Time': start_time.strftime('%H:%M'),
        'End Time': end_time.strftime('%H:%M'),
        'Duration (min)': duration
    }

    df = pd.DataFrame([entry])

    # Check if the file exists to avoid header duplication
    file_exists = os.path.isfile('time_diary.csv')

    df.to_csv('time_diary.csv', mode='a', header=not file_exists, index=False)
    print(f"Logged: {activity} for {duration} minutes.")


# Function to start an activity in real-time
def start_activity(activity):
    start_time = datetime.now()
    input(f"Press Enter to stop {activity}...")
    end_time = datetime.now()

    log_activity(activity, start_time, end_time)


# Function to log a past activity
def log_past_activity():
    activity = input("Enter the activity: ")
    date_str = input("Enter the date of activity (YYYY-MM-DD) or press Enter for today's date: ")
    start_time_str = input("Enter start time (HH:MM): ")
    end_time_str = input("Enter end time (HH:MM): ")

    # Use today's date if no date is provided
    if date_str == '':
        date = datetime.today().date()
    else:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    # Parse the time inputs
    try:
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()
    except ValueError:
        print("Invalid time format. Please use HH:MM.")
        return

    # Combine date with time to get full datetime objects
    start_time = datetime.combine(date, start_time)
    end_time = datetime.combine(date, end_time)

    # Log the activity
    log_activity(activity, start_time, end_time)


# Function to generate reports (daily, weekly, monthly)
def generate_report(time_period='weekly'):
    try:
        df = pd.read_csv('time_diary.csv', parse_dates=['Date'])
    except FileNotFoundError:
        print("No activity data found. Please log some activities first.")
        return None

    if df.empty:
        print("No data in CSV file.")
        return None

    # Generate report based on the time period
    if time_period == 'daily':
        report = df.groupby(['Date', 'Activity'])['Duration (min)'].sum()
    elif time_period == 'weekly':
        df['Week'] = df['Date'].dt.isocalendar().week
        report = df.groupby(['Week', 'Activity'])['Duration (min)'].sum()
    elif time_period == 'monthly':
        df['Month'] = df['Date'].dt.month
        report = df.groupby(['Month', 'Activity'])['Duration (min)'].sum()

    print(report)
    return report


# Function to visualize the report
def visualize_report(report):
    if report is None or report.empty:
        print("No report data to visualize.")
        return

    # Create a bar chart
    report.unstack().plot(kind='bar', stacked=True)
    plt.title('Time Spent on Activities')
    plt.xlabel('Time Period')
    plt.ylabel('Duration (minutes)')
    plt.show()


# Main menu to interact with the user
def menu():
    while True:
        print("\n1. Start an activity")
        print("2. Log a past activity")
        print("3. Generate a daily report")
        print("4. Generate a weekly report")
        print("5. Generate a monthly report")
        print("0. Exit")

        choice = input("\nChoose an option: ")
        if choice == '1':
            activity = input("Enter the activity name: ")
            start_activity(activity)
        elif choice == '2':
            log_past_activity()
        elif choice == '3':
            report = generate_report('daily')
            visualize_report(report)
        elif choice == '4':
            report = generate_report('weekly')
            visualize_report(report)
        elif choice == '5':
            report = generate_report('monthly')
            visualize_report(report)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

menu()
