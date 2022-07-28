"""
This program will:
    "Add student" button pressed:
        - add a student to a save file with all of the details required
            - Full name
            - Email
            - Grade
            - Specialzation
            - How many events attended - default 0

        - Show review content page before saving and option to edit values
        - save person


    "Show students" button pressed:
        - Show the student in a list viewer


    "Schedule event" button pressed:
        - Get students who have not done many events
        - Get the appropriate ammount of students for the event
        - Show user events that have been scheduled


    attending_list = []
    while x_needed != 0:
        find person with x specilazation
            put in temp list

        go through temp list
            find person with least amount of events attended
            add person to attending list

        x_needed -= 1



"""




import tkinter


def submit_student(fname, lname, email, events):
    global add_student_window
    print(f"{fname} {lname} {email} {events}")
    add_student_window.destroy()
    add_student_window = None
    main()


def add_student():
    global window, add_student_window
    window.destroy ()

    add_student_window = tkinter.Tk()
    add_student_window.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")


    # ------------------------
    #   Student input fields
    # ------------------------
    studentInputFrame = tkinter.Frame(add_student_window)

    # -----------------
    #   Students name
    # -----------------
    fname_label = tkinter.Label(
        studentInputFrame,
        text="First name:",
        font=("Comic Sans MS", 12, "bold")
    )
    fname_label.grid (row = 0, column = 0)

    fname = tkinter.Entry(studentInputFrame)
    fname.grid(row=0, column=1)

    lname_label = tkinter.Label(
        studentInputFrame,
        text="Last name:",
        font=("Comic Sans MS", 12, "bold")
    )
    lname_label.grid (row=1, column=0)

    lname = tkinter.Entry(studentInputFrame)
    lname.grid(row=1, column=1)


    # ------------------
    #   Students email
    # ------------------
    email_label = tkinter.Label(
        studentInputFrame,
        text="Email:",
        font=("Comic Sans MS", 12, "bold")
    )
    email_label.grid (row=2, column=0)

    email = tkinter.Entry(studentInputFrame)
    email.grid(row=2, column=1)


    # -----------------------------
    #   Number of events attended
    # -----------------------------
    events_label = tkinter.Label(
        studentInputFrame,
        text="Amount of events attended:",
        font=("Comic Sans MS", 12, "bold")
    )
    events_label.grid (row=3, column=0)

    events = tkinter.Entry(studentInputFrame)
    events.grid(row=3, column=1)


    # ---------------------------------
    #   Button for submitting student
    # ---------------------------------
    submit_button = tkinter.Button(
        studentInputFrame,
        text="Submit",
        command=lambda: submit_student(fname.get(), lname.get(), email.get(), events.get())
    )
    submit_button.grid(row=4, column=1)

    studentInputFrame.pack()



    # ----------------
    #   Start window
    # ----------------
    studentInputFrame.grid(row=0, column=0)
    add_student_window.mainloop()



def create_event():
    global window
    window.destroy()

    create_event_window = tkinter.Tk()
    create_event_window.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")



    create_event_window.mainloop()



def main():
    global window, WIN_WIDTH, WIN_HEIGHT, add_student_window, create_event_window
    if add_student_window != None:
        add_student_window.destroy()

    if create_event_window != None:
        create_event_window.destroy()


    window = tkinter.Tk()

    WIN_WIDTH = 1000
    WIN_HEIGHT = 500
    window.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")

    add_student_button = tkinter.Button(
        window,
        text="Add a student",
        command=add_student
    )
    add_student_button.grid(row=0, column=0)

    window.mainloop()

if __name__ == "__main__":
    global add_student_window, create_event_window

    create_event_window = None
    add_student_window = None
    main()
