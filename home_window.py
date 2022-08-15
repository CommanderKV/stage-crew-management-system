import tkinter

def add_student():
    raise Exception("add_student")

def create_event():
    raise Exception("create_event")

def view_events():
    raise Exception("view_events")

def view_students():
    raise Exception("view_students")

home_window = tkinter.Tk()


# -------------------
#   Main menu label
# -------------------
main_menu_label = tkinter.Label(
    home_window,
    text="Main menu",
    font=("Comic Sans MS", 20, "bold")
)
main_menu_label.grid(row=0, column=0)


# ----------------
#   Button frame
# ----------------
button_frame = tkinter.Frame(home_window)
button_height = 2
button_width = 20


# ----------------------
#   Add student button
# ----------------------
add_student_button = tkinter.Button(
    button_frame,
    text="Add a student",
    command=add_student,
    height=button_height,
    width=button_width,
    font=("comic sans", 14)
)
add_student_button.grid(row=0, column=0, sticky="nsew")


# -----------------------
#   Create event button
# -----------------------
create_event_button = tkinter.Button(
    button_frame,
    text="Create an event",
    command=create_event,
    height=button_height,
    width=button_width,
    font=("comic sans", 14)
)
create_event_button.grid(row=1, column=0, sticky="nsew")


# ----------------------
#   View events button
# ----------------------
view_events_button = tkinter.Button(
    button_frame,
    text="View events",
    command=view_events,
    height=button_height,
    width=button_width,
    font=("comic sans", 14)
)
view_events_button.grid(row=1, column=1, sticky="nsew")


# ------------------------
#   View students button
# ------------------------
view_students_button = tkinter.Button(
    button_frame,
    text="View students",
    command=view_students,
    height=button_height,
    width=button_width,
    font=("comic sans", 14)
)
view_students_button.grid(row=0, column=1, sticky="nsew")


# -------------------
#   Start main loop
# -------------------
button_frame.grid(row=1, column=0)
home_window.mainloop()