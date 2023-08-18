import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def show_message_box():
    messagebox.showinfo("Message", "This is a message box!")

def on_scale_change(scale_value):
    scale_label.config(text=f"Scale Value: {scale_value}")

root = tk.Tk()
root.title("tkinter Widgets Example")

# Checkbutton
check_var = tk.BooleanVar()
check_button = ttk.Checkbutton(root, text="Check me", variable=check_var)
check_button.pack(pady=10)

# Scrollbar
scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
for i in range(1, 21):
    listbox.insert(tk.END, f"Item {i}")
listbox.pack(side=tk.LEFT, padx=10, pady=10)
scrollbar.config(command=listbox.yview)

# Messagebox
message_button = ttk.Button(root, text="Show Message", command=show_message_box)
message_button.pack(pady=10)

# Scale
scale_label = ttk.Label(root, text="Scale Value: 0")
scale_label.pack(pady=5)
scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=on_scale_change)
scale.pack(pady=5)

# Radiobutton
radio_var = tk.StringVar()
radio_var.set("option1")
radio_button1 = ttk.Radiobutton(root, text="Option 1", variable=radio_var, value="option1")
radio_button2 = ttk.Radiobutton(root, text="Option 2", variable=radio_var, value="option2")
radio_button1.pack()
radio_button2.pack()

# Menu
def open_file():
    messagebox.showinfo("Menu", "Open File selected")

def save_file():
    messagebox.showinfo("Menu", "Save File selected")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

root.mainloop()

