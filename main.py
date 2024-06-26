import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
import schedule
import time
from threading import Thread
from datetime import datetime, timedelta
import pygame.mixer

twilio_number = '+18334691315'
your_phone_number = '+x'

account_sid = "y" #replace with your own account sid
auth_token  = "x" #replace with your own auth token

client = Client(account_sid, auth_token)

def send_sms(message):
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=your_phone_number
    )

def notify_break(break_type, start_time):
    message = f"{break_type} break started at {start_time.strftime('%H:%M')}"
    tk.messagebox.showinfo("Break Notification", message)
    pygame.mixer.init()
    pygame.mixer.music.load('C:\\Users\\kyra\\OneDrive\\Desktop\\Web Development Projects\\water-intake\\assets\\alarmsound.mp3')
    pygame.mixer.music.play()
    send_sms(message)

def brain_break():
    notify_break("Brain", datetime.now())

def break_break():
    notify_break("Break", datetime.now())

def schedule_breaks(start_time, end_time):
    work_interval = timedelta(minutes=2)
    short_break_interval = timedelta(minutes=5)
    long_break_interval = timedelta(minutes=15)
    current_time = start_time

    while current_time < end_time:
        # Work period
        current_time += work_interval
        if current_time >= end_time:
            break
        schedule.every().day.at(current_time.strftime("%H:%M")).do(brain_break)

        # Short break period
        current_time += short_break_interval
        if current_time >= end_time:
            break

        # Work period
        current_time += work_interval
        if current_time >= end_time:
            break
        schedule.every().day.at(current_time.strftime("%H:%M")).do(break_break)

        # Long break period
        current_time += long_break_interval
        if current_time >= end_time:
            break

def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_alarm():
    start_time_str = start_time_entry.get()
    end_time_str = end_time_entry.get()
    
    try:
        start_time = datetime.strptime(start_time_str, "%H:%M")
        end_time = datetime.strptime(end_time_str, "%H:%M")
    except ValueError:
        messagebox.showerror("Invalid time format", "Please enter time in HH:MM format")
        return
    
    schedule_breaks(start_time, end_time)
    Thread(target=start_scheduler, daemon=True).start()
    messagebox.showinfo("Alarm Set", "Alarms have been set successfully!")

app = tk.Tk()
app.title("CodeClock")

tk.Label(app, text="Start Time (HH:MM)").grid(row=0, column=0)
start_time_entry = tk.Entry(app)
start_time_entry.grid(row=0, column=1)

tk.Label(app, text="End Time (HH:MM)").grid(row=1, column=0)
end_time_entry = tk.Entry(app)
end_time_entry.grid(row=1, column=1)

start_button = tk.Button(app, text="Start", command=start_alarm)
start_button.grid(row=2, columnspan=2)

app.mainloop()
