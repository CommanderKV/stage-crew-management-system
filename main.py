"""
This program will:
    "Add student" button pressed:
        - add a student to a save file with all of the details required

    "Schedule event" button pressed:
        - Get students who have not done many events
        - Get the appropriate ammount of students for the event
        - Show user

"""




import tkinter

def main():
    window = tkinter.Tk()

    WIN_WIDTH = window.winfo_screenwidth()
    WIN_HEIGHT = window.winfo_screenheight()
    window.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")



    window.mainloop()

if __name__ == "__main__":
    main()
