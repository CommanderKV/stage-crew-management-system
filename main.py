"""
This program will:
    "Add student" button pressed:
        - add a student to a save file with all of the details required

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

def main():
    window = tkinter.Tk()

    WIN_WIDTH = window.winfo_screenwidth()
    WIN_HEIGHT = window.winfo_screenheight()
    window.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")

    add_student = tkinter.Button(
        window,
        text="Add student"
    )
    add_student.grid(row=0,column=0)

    window.mainloop()

if __name__ == "__main__":
    main()
