import schedule
import time
from datetime import datetime
import tkinter as tk
from threading import Thread

# 📝 Function to display sticky-note-style reminder
def show_sticky_note(title, message):
    root = tk.Tk()
    root.title(title)
    root.geometry("300x150+100+100")
    root.configure(bg="#fff8b0")  # Sticky note yellow
    root.attributes("-topmost", True)  # Stay on top

    label = tk.Label(root, text=message, bg="#fff8b0", font=("Helvetica", 14), wraplength=280, justify="left")
    label.pack(padx=10, pady=20)

    root.mainloop()

# 📌 Reminder message
def plan_tomorrow_reminder():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📅 Reminder: Plan tomorrow’s work.")
    Thread(target=show_sticky_note, args=("🗓️ Work Planner", "Take 5 mins to plan your tasks for tomorrow.")).start()

# ⏰ Set schedule for 21:05
schedule.every().day.at("21:05").do(plan_tomorrow_reminder)

print("🕔 Planning reminder is running... Waiting for 21:05... Press Ctrl+C to stop.")

# 🔁 Keep script running
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Reminder stopped by user.")
