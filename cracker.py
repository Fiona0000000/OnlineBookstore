import tkinter as tk
from tkinter import ttk
import time
import threading

def crack_password():
    user_id = entry.get().strip()
    status_label.config(text="Cracking.", foreground="#00FFFF")
    get_button.config(state="disabled")

    def cracking_animation():
        dots = 0
        for _ in range(5):
            dots = (dots % 3) + 1
            status_label.config(text="Cracking" + "." * dots)
            time.sleep(1)

    def delayed_crack():
        cracking_animation()

        found = False
        try:
            with open("data.txt", "r") as file:
                for line in file:
                    stored_id, stored_pass = line.strip().split(":")
                    if stored_id == user_id:
                        found = True
                        result = f"Password: {stored_pass}"
                        break
            if not found:
                result = "User ID not found."
        except FileNotFoundError:
            result = "data.txt file not found."

        root.after(0, show_result, result)

    threading.Thread(target=delayed_crack).start()

def show_result(result):
    if "Password:" in result:
        status_label.config(text=result, foreground="#00FF00")
    else:
        status_label.config(text=result, foreground="#FF5555")
    get_button.config(state="normal")

def enter_pressed(event=None):
    crack_password()

# GUI Setup
root = tk.Tk()
root.title("PASSHUNTER - Password Cracker")
root.geometry("500x300")
root.configure(bg="#1e1e1e")
root.resizable(True, True)  # Allow resizing
root.minsize(400, 250)
root.maxsize(700, 400)

# Custom Styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Consolas", 12))
style.configure("TEntry", font=("Consolas", 12), padding=5)
style.configure("TButton", font=("Consolas", 12), padding=6)

# Title
title = ttk.Label(root, text="ðŸ” PASSHUNTER", font=("Consolas", 16, "bold"), foreground="#00FFFF")
title.pack(pady=(20, 10))

# Entry field
ttk.Label(root, text="Enter User ID:").pack(pady=(10, 5))
entry = ttk.Entry(root, width=30)
entry.pack(pady=(0, 10))
entry.bind("<Return>", enter_pressed)  # Bind Enter key

# Button
get_button = ttk.Button(root, text="Get Password", command=crack_password)
get_button.pack(pady=10)

# Status Label
status_label = ttk.Label(root, text="", font=("Consolas", 12, "italic"))
status_label.pack(pady=15)

root.mainloop()
