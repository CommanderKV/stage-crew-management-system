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

def add_student():
    global window, add_student_window
    window.destroy ()

    add_student_window = tkinter.Tk()
    add_student_window.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")

    ask_name = tkinter.Label(
        add_student_window,
        text="Enter student's full name here:",
        font=("Comic Sans MS", 15, "bold")
    )
    ask_name.grid (row = 0, column = 0)

    student_name = tkinter.Entry(add_student_window)
    student_name.grid(row = 1, column = 0)


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

    WIN_WIDTH = window.winfo_screenwidth()
    WIN_HEIGHT = window.winfo_screenheight()
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
