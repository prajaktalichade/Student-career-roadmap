
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ---------------- DATABASE ----------------

def create_database():
    conn = sqlite3.connect("career_roadmap.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            career TEXT,
            skills TEXT,
            progress REAL
        )
    """)

    conn.commit()
    conn.close()


def save_progress():
    name = name_entry.get().strip()
    career = career_box.get()
    skills = skills_entry.get().strip()

    if name == "":
        messagebox.showwarning(
            "Warning",
            "Please enter your name."
        )
        return

    if career == "":
        messagebox.showwarning(
            "Warning",
            "Please select a career."
        )
        return

    progress = progress_bar["value"]

    conn = sqlite3.connect("career_roadmap.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, career, skills, progress)
        VALUES (?, ?, ?, ?)
    """, (name, career, skills, progress))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Your progress has been saved successfully!"
    )


def view_saved_data():

    conn = sqlite3.connect("career_roadmap.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    conn.close()

    if not records:
        messagebox.showinfo(
            "Saved Data",
            "No saved records found."
        )
        return

    data_window = tk.Toplevel(root)
    data_window.title("Saved Student Data")
    data_window.geometry("700x400")

    title = tk.Label(
        data_window,
        text="Saved Student Records",
        font=("Arial", 18, "bold")
    )

    title.pack(pady=15)

    columns = (
        "ID",
        "Name",
        "Career",
        "Skills",
        "Progress"
    )

    table = ttk.Treeview(
        data_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)

    table.column("ID", width=50)
    table.column("Name", width=100)
    table.column("Career", width=150)
    table.column("Skills", width=200)
    table.column("Progress", width=80)

    for record in records:
        table.insert("", tk.END, values=record)

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


# ---------------- CAREERS ----------------

careers = {

    "Python Developer": [
        "Python",
        "SQL",
        "DSA",
        "Django",
        "Git & GitHub"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git & GitHub"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Pandas",
        "Power BI"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Pandas",
        "Machine Learning"
    ],

    "Machine Learning Engineer": [
        "Python",
        "SQL",
        "Statistics",
        "Machine Learning",
        "Deep Learning"
    ],

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git & GitHub"
    ],

    "Backend Developer": [
        "Python",
        "SQL",
        "Django",
        "REST API",
        "Git & GitHub"
    ],

    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Python",
        "SQL"
    ],

    "Software Engineer": [
        "Python",
        "DSA",
        "OOP",
        "SQL",
        "Git & GitHub"
    ]
}
# ---------------- GENERATE ROADMAP ----------------

def generate_roadmap():

    career = career_box.get()

    if career == "":
        messagebox.showwarning(
            "Warning",
            "Please select a career."
        )
        return

    skills_text = skills_entry.get().lower()

    if skills_text.strip() == "":
        user_skills = []
    else:
        user_skills = [
            skill.strip()
            for skill in skills_text.split(",")
        ]

    required_skills = careers[career]

    completed = []
    missing = []

    for skill in required_skills:

        if skill.lower() in user_skills:
            completed.append(skill)
        else:
            missing.append(skill)

    total = len(required_skills)
    completed_count = len(completed)

    progress = (completed_count / total) * 100

    # Clear old results
    completed_text.delete("1.0", tk.END)
    missing_text.delete("1.0", tk.END)
    roadmap_text.delete("1.0", tk.END)

    # ---------------- COMPLETED SKILLS ----------------

    if completed:

        for skill in completed:
            completed_text.insert(
                tk.END,
                "✓ " + skill + "\n"
            )

    else:

        completed_text.insert(
            tk.END,
            "No skills completed yet."
        )

    # ---------------- MISSING SKILLS ----------------

    if missing:

        for skill in missing:
            missing_text.insert(
                tk.END,
                "→ " + skill + "\n"
            )

    else:

        missing_text.insert(
            tk.END,
            "🎉 All skills completed!"
        )

    # ---------------- LEARNING ROADMAP ----------------

    if missing:

        roadmap_text.insert(
            tk.END,
            f"Career Goal: {career}\n\n"
        )

        roadmap_text.insert(
            tk.END,
            "Recommended Learning Path:\n\n"
        )

        for i, skill in enumerate(missing, start=1):

            roadmap_text.insert(
                tk.END,
                f"Step {i}: Learn {skill}\n"
            )

        roadmap_text.insert(
            tk.END,
            "\n💡 Tip: Practice each skill and build projects "
            "before moving to the next step."
        )

    else:

        roadmap_text.insert(
            tk.END,
            "🎉 Congratulations!\n\n"
            "You have completed all the required skills "
            f"for {career}.\n\n"
            "Now focus on building real-world projects "
            "and preparing for interviews."
        )

    # ---------------- PROGRESS ----------------

    progress_bar["value"] = progress

    progress_label.config(
        text=f"Progress: {progress:.0f}%"
    )


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Student Career Roadmap Generator")

root.geometry("750x680")

root.resizable(False, False)


# ---------------- SCROLLABLE AREA ----------------

canvas = tk.Canvas(root)

scrollbar = ttk.Scrollbar(
    root,
    orient="vertical",
    command=canvas.yview
)

scrollable_frame = ttk.Frame(canvas)


scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)


canvas_window = canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)


def resize_frame(event):
    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    resize_frame
)


canvas.configure(
    yscrollcommand=scrollbar.set
)


canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ---------------- MOUSE WHEEL ----------------

def on_mousewheel(event):
    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    on_mousewheel
)


# ---------------- TITLE ----------------

title_label = tk.Label(
    scrollable_frame,
    text="🎓 Student Career Roadmap Generator",
    font=("Arial", 22, "bold")
)

title_label.pack(pady=15)


subtitle_label = tk.Label(
    scrollable_frame,
    text="Build your personalized career roadmap",
    font=("Arial", 12)
)

subtitle_label.pack(pady=5)


# ---------------- NAME ----------------

name_label = tk.Label(
    scrollable_frame,
    text="Student Name:",
    font=("Arial", 12, "bold")
)

name_label.pack(pady=(15, 5))


name_entry = tk.Entry(
    scrollable_frame,
    width=40,
    font=("Arial", 11)
)

name_entry.pack()


# ---------------- CAREER ----------------

career_label = tk.Label(
    scrollable_frame,
    text="Select Career:",
    font=("Arial", 12, "bold")
)

career_label.pack(pady=(15, 5))


career_box = ttk.Combobox(
    scrollable_frame,
    values=list(careers.keys()),
    state="readonly",
    width=35
)

career_box.pack()


# ---------------- SKILLS ----------------

skills_label = tk.Label(
    scrollable_frame,
    text="Enter your skills:",
    font=("Arial", 12, "bold")
)

skills_label.pack(pady=(15, 5))


skills_entry = tk.Entry(
    scrollable_frame,
    width=50,
    font=("Arial", 11)
)

skills_entry.pack()


skills_hint = tk.Label(
    scrollable_frame,
    text="Example: Python, SQL",
    font=("Arial", 9)
)

skills_hint.pack(pady=5)


# ---------------- BUTTON ----------------

generate_button = tk.Button(
    scrollable_frame,
    text="🚀 Generate Roadmap",
    command=generate_roadmap,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8
)

generate_button.pack(pady=10)


# ---------------- PROGRESS ----------------

progress_label = tk.Label(
    scrollable_frame,
    text="Progress: 0%",
    font=("Arial", 12, "bold")
)

progress_label.pack(pady=5)


progress_bar = ttk.Progressbar(
    scrollable_frame,
    length=500,
    mode="determinate",
    maximum=100
)

progress_bar.pack(pady=5)


# ---------------- RESULTS ----------------

result_frame = tk.Frame(
    scrollable_frame
)

result_frame.pack(pady=15)


# ---------------- COMPLETED ----------------

completed_frame = tk.Frame(
    result_frame
)

completed_frame.grid(
    row=0,
    column=0,
    padx=15
)


completed_label = tk.Label(
    completed_frame,
    text="✓ Completed Skills",
    font=("Arial", 12, "bold")
)

completed_label.pack()


completed_text = tk.Text(
    completed_frame,
    width=25,
    height=7,
    font=("Arial", 10)
)

completed_text.pack()


# ---------------- MISSING ----------------

missing_frame = tk.Frame(
    result_frame
)

missing_frame.grid(
    row=0,
    column=1,
    padx=15
)


missing_label = tk.Label(
    missing_frame,
    text="→ Skills To Learn",
    font=("Arial", 12, "bold")
)

missing_label.pack()


missing_text = tk.Text(
    missing_frame,
    width=25,
    height=7,
    font=("Arial", 10)
)

missing_text.pack()


# ---------------- LEARNING ROADMAP ----------------

roadmap_label = tk.Label(
    scrollable_frame,
    text="📚 Learning Roadmap",
    font=("Arial", 18, "bold")
)

roadmap_label.pack(
    pady=(20, 10)
)


roadmap_text = tk.Text(
    scrollable_frame,
    width=65,
    height=12,
    font=("Arial", 11),
    wrap="word"
)

roadmap_text.pack(
    pady=10
)


# ---------------- SAVE BUTTON ----------------

save_button = tk.Button(
    scrollable_frame,
    text="💾 Save Progress",
    command=save_progress,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=7
)

save_button.pack(pady=8)


# ---------------- VIEW DATA BUTTON ----------------

view_button = tk.Button(
    scrollable_frame,
    text="📋 View Saved Data",
    command=view_saved_data,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=7
)

view_button.pack(pady=5)


# ---------------- EXIT BUTTON ----------------

exit_button = tk.Button(
    scrollable_frame,
    text="❌ Exit",
    command=root.destroy,
    font=("Arial", 11, "bold"),
    padx=20,
    pady=7
)

exit_button.pack(pady=10)


# ---------------- CREATE DATABASE ----------------

create_database()


# ---------------- START APPLICATION ----------------

root.mainloop()