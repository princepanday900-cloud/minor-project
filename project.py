import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- 1. DATABASE LOGIC ---
def connect_db():
    conn = sqlite3.connect('student_data.db')
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS students 
                    (roll INTEGER PRIMARY KEY, name TEXT, email TEXT, 
                     gender TEXT, dept TEXT, admission TEXT, contact TEXT)''')
    conn.commit()
    conn.close()

def save_to_db():
    if roll_var.get() == "" or name_var.get() == "":
        messagebox.showerror("Error", "Sari details bhariye!")
        return
    try:
        conn = sqlite3.connect('student_data.db')
        curr = conn.cursor()
        curr.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?)", 
                     (roll_var.get(), name_var.get(), email_var.get(), 
                      gender_var.get(), dept_var.get(), admission_var.get(), contact_var.get()))
        conn.commit()
        conn.close()
        fetch_data()
        clear_fields()
        messagebox.showinfo("Success", "Record Add Ho Gaya!")
    except:
        messagebox.showerror("Error", "Roll No pehle se hai!")

def fetch_data():
    conn = sqlite3.connect('student_data.db')
    curr = conn.cursor()
    curr.execute("SELECT * FROM students")
    rows = curr.fetchall()
    student_table.delete(*student_table.get_children())
    for row in rows:
        student_table.insert('', tk.END, values=row)
    conn.close()

def delete_data():
    if roll_var.get() == "":
        messagebox.showerror("Error", "Record select karein!")
        return
    conn = sqlite3.connect('student_data.db')
    curr = conn.cursor()
    curr.execute("DELETE FROM students WHERE roll=?", (roll_var.get(),))
    conn.commit()
    conn.close()
    fetch_data()
    clear_fields()
    messagebox.showinfo("Success", "Data Delete Ho Gaya!")

def update_data():
    if roll_var.get() == "":
        messagebox.showerror("Error", "Select record to update!")
        return
    conn = sqlite3.connect('student_data.db')
    curr = conn.cursor()
    curr.execute("UPDATE students SET name=?, email=?, gender=?, dept=?, admission=?, contact=? WHERE roll=?",
                 (name_var.get(), email_var.get(), gender_var.get(), dept_var.get(), 
                  admission_var.get(), contact_var.get(), roll_var.get()))
    conn.commit()
    conn.close()
    fetch_data()
    messagebox.showinfo("Success", "Record Updated!")

def search_data():
    conn = sqlite3.connect('student_data.db')
    curr = conn.cursor()
    curr.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search_var.get() + '%',))
    rows = curr.fetchall()
    student_table.delete(*student_table.get_children())
    for row in rows:
        student_table.insert('', tk.END, values=row)
    conn.close()

def clear_fields():
    roll_var.set("")
    name_var.set("")
    email_var.set("")
    gender_var.set("")
    dept_var.set("")
    admission_var.set("")
    contact_var.set("")

def get_cursor(event):
    cursor_row = student_table.focus()
    content = student_table.item(cursor_row)
    row = content['values']
    if row:
        roll_var.set(row[0])
        name_var.set(row[1])
        email_var.set(row[2])
        gender_var.set(row[3])
        dept_var.set(row[4])
        admission_var.set(row[5])
        contact_var.set(row[6])

# --- 2. MAIN WINDOW ---
root = tk.Tk()
root.title("CST Student Management Pro")
root.geometry("1350x720")
root.configure(bg="#f4f7f6")

roll_var, name_var, email_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
gender_var, dept_var, admission_var, contact_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
search_var = tk.StringVar()

# Header
header = tk.Frame(root, bg="#2c3e50", height=60)
header.pack(side=tk.TOP, fill=tk.X)
tk.Label(header, text="STUDENT MANAGEMENT SYSTEM PRO", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="white").pack(pady=10)

# --- 3. LEFT PANEL ---
Left_Panel = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
Left_Panel.place(x=20, y=80, width=410, height=620)

tk.Label(Left_Panel, text="Registration Form", font=("Helvetica", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=5)

# Entry Helper Function
def create_input(lbl, var):
    frame = tk.Frame(Left_Panel, bg="white")
    frame.pack(fill=tk.X, padx=30, pady=1)
    tk.Label(frame, text=lbl, font=("Helvetica", 9, "bold"), bg="white").pack(anchor="w")
    tk.Entry(frame, textvariable=var, font=("Helvetica", 11), bd=1, relief="solid").pack(fill=tk.X, ipady=1)

create_input("Roll Number", roll_var)
create_input("Student Name", name_var)
create_input("Email ID", email_var)

# Gender Dropdown
gender_frame = tk.Frame(Left_Panel, bg="white")
gender_frame.pack(fill=tk.X, padx=30, pady=1)
tk.Label(gender_frame, text="Gender", font=("Helvetica", 9, "bold"), bg="white").pack(anchor="w")
gender_combo = ttk.Combobox(gender_frame, textvariable=gender_var, font=("Helvetica", 11), state="readonly")
gender_combo['values'] = ("Male", "Female", "Other")
gender_combo.pack(fill=tk.X)

# Department Dropdown (YE RAHA AUTOMATIC LIST)
dept_frame = tk.Frame(Left_Panel, bg="white")
dept_frame.pack(fill=tk.X, padx=30, pady=1)
tk.Label(dept_frame, text="Department", font=("Helvetica", 9, "bold"), bg="white").pack(anchor="w")
dept_combo = ttk.Combobox(dept_frame, textvariable=dept_var, font=("Helvetica", 11), state="readonly")
dept_combo['values'] = ("Computer Science", "Mechanical", "Civil", "Electrical", "Electronics", "Information Technology")
dept_combo.pack(fill=tk.X)

create_input("Admission Year", admission_var)
create_input("Contact No", contact_var)

# Buttons
btn_frame = tk.Frame(Left_Panel, bg="white")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="SUBMIT", command=save_to_db, bg="#27ae60", fg="white", width=13, font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="DELETE", command=delete_data, bg="#e74c3c", fg="white", width=13, font=("Helvetica", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="UPDATE", command=update_data, bg="#2980b9", fg="white", width=13, font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="CLEAR", command=clear_fields, bg="#f39c12", fg="white", width=13, font=("Helvetica", 10, "bold")).grid(row=1, column=1, padx=5, pady=5)

# --- 4. RIGHT PANEL ---
Right_Panel = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
Right_Panel.place(x=450, y=80, width=870, height=620)

search_frame = tk.Frame(Right_Panel, bg="#ecf0f1")
search_frame.pack(fill=tk.X, padx=10, pady=10)
tk.Label(search_frame, text="Search Name:", font=("Helvetica", 10, "bold"), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
tk.Entry(search_frame, textvariable=search_var, width=25, font=("Helvetica", 11)).pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="SEARCH", command=search_data, bg="#34495e", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="SHOW ALL", command=fetch_data, bg="#34495e", fg="white", width=10).pack(side=tk.LEFT, padx=5)

# Table
cols = ("roll", "name", "email", "gender", "dept", "adm", "contact")
student_table = ttk.Treeview(Right_Panel, columns=cols, show='headings')
style = ttk.Style()
style.theme_use("clam")

for col in cols:
    student_table.heading(col, text=col.upper())
    student_table.column(col, width=120, anchor="center")

student_table.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
student_table.bind("<ButtonRelease-1>", get_cursor)

connect_db()
fetch_data()
root.mainloop()