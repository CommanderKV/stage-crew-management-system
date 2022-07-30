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



db format:
{
    "student #": {
        "first name": "",
        "last name": "",
        "email": "",
        "events": 0
    },
    "student #": {
        "first name": "",
        "last name": "",
        "email": "",
        "events": 0
    },
}



"""



import os
import tkinter
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import date as date_year
import json

# Initialize Firebase
cred = credentials.Certificate(os.path.join(os.getcwd(), "stage-crew-event-manager-firebase-adminsdk-ed2pg-b047e32b38.json"))
DB_CONNECTION = firebase_admin.initialize_app(cred, {"databaseURL": "https://stage-crew-event-manager-default-rtdb.firebaseio.com"})
DB_REFERENCE = db.reference("/")




# \\\\\\\\\\\\\\\\\\\\\\\\\\
#     Database functions
# \\\\\\\\\\\\\\\\\\\\\\\\\\

def save_student_info(fname: str, lname: str, email: str, events: str, ref: db.reference, update_students: bool=False) -> bool:
    ref_data = ref.get()

    if ref_data is None:
        ref.set({"Students": {}})

    elif "Students" not in ref_data.keys():
        ref_data["Students"] = {}
        ref.set(ref_data)

    ref = db.reference("/Students")

    data = {
        "first name": fname,
        "last name": lname,
        "email": email,
        "events": int (events)
    }

    try:
        items = ref.get()
        if items is not None:
            for item in items:
                if items[item]["email"] == email:
                    if update_students:
                        ref.child(item).update(data)
                        return True
                    else:
                        return False
        
        else:
            ref.push().set(data)
            return True

    except Exception as e:
        print(e)
        return False


def get_students(ref) -> list or None:
    if ref.get() is None:
        ref.set({"Students": {}})
    ref = db.reference("/Students")
    
    students = []
    items = ref.get()
    for item in items:
        students.append(items[item])

    if len(students) <= 0:
        return None
    else:
        return students


def save_event_info(name: str, date: str, start_time: str, end_time: str, sound: bool, mics: bool, lights: bool, projector: bool, ref: db.reference, update_events: bool=False) -> bool:
    # -------------------------
    #    Check if directory 
    #   exists if not make it
    # -------------------------
    ref_data = ref.get()

    if ref_data is None:
        ref.set({"Events": {}})

    elif "Events" not in ref_data.keys():
        ref_data["Events"] = {}
        ref.set(ref_data)

    ref = db.reference("/Events")


    # --------------------------
    #   Create data dictionary
    # --------------------------
    data = {
        "name": name,
        "date": date,
        "start time": start_time,
        "end time": end_time,
        "sound": sound,
        "mics": mics,
        "lights": lights,
        "projector": projector
    }

    # -------------------------
    #   Add event to database
    # -------------------------
    #try:
    if True:
        items = ref.get()
        if items is not None:
            print (items)
            for item in items:
                if items[item]["name"] == name:
                    if update_events:
                        ref.child(item).update(data)
                        return True

                    else:
                        return False
        else:
            ref.push().set(data)
            return True

    # except Exception as e:
    #     print(e)
    #     return False


# \\\\\\\\\\\\\\\\\\\\\\\\\\\
#     Main code functions
# \\\\\\\\\\\\\\\\\\\\\\\\\\\

def check_time(time: str) -> bool:
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if len(time) == 5:
        if time[2] == ":":
            if time[0] in numbers and time[1] in numbers and time[3] in numbers and time[4] in numbers:
                if int(time[0:2]) < 24 and int(time[3:5]) < 60:
                    return True
                    
                else:
                    return False

            else:
                return False

        else:
            return False

    else:
        return False

def check_date(date: str) -> bool:
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if len(date) == 10:
        if date[4] == "-" and date[7] == "-":
            if date[0] in numbers and date[1] in numbers and date[2] in numbers and date[3] in numbers and date[5] in numbers and date[6] in numbers and date[8] in numbers and date[9] in numbers:
                if int(date[0:4]) >= date_year.today().year and int(date[5:7]) < 13 and int(date[8:10]) < 32:
                    return True

                else:
                    return False

            else:
                return False

        else:
            return False

    else:
        return False


def submit_student(fname, lname, email, events):
    global add_student_window, error_label_add_students
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    if fname != "":
        if lname != "":
            if email != "" and "@" in email and "tdsb.on.ca" in email:
                if events != "" and all(char in numbers for char in events):
                    if not save_student_info(fname, lname, email, events, DB_REFERENCE):
                        error_label_add_students.config(text="Error adding student or student already exists.")
                        return False

                    else:
                        error_label_add_students.configure(text="")
                        add_student_window.destroy()
                        add_student_window = None
                        main()
                        return True

                else:
                    error_label_add_students.configure(text="Amount of events must be entered.")
            else:
                error_label_add_students.configure(text="Email must be filled and must be a tdsb email.")
        else:
            error_label_add_students.configure(text="Last name must be filled.")
    else:    
        error_label_add_students.configure(text="First name must be filled.")


def add_student():
    global window, add_student_window, error_label_add_students
    window.destroy ()

    add_student_window = tkinter.Tk()
    add_student_window.geometry("400x200")


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

    # ---------------
    #   Error label
    # ---------------

    error_label_add_students = tkinter.Label(
        add_student_window,
        text="",
        font=("Comic Sans MS", 12),
        fg="red"
    )
    error_label_add_students.grid(row=1, column=0)

    # ---------------
    #   Back button
    # ---------------
    back = tkinter.Button(
        add_student_window,
        text="Back",
        command=lambda: main()
    )
    back.grid(row=2, column=0)


    # ----------------
    #   Start window
    # ----------------
    studentInputFrame.grid(row=0, column=0)
    add_student_window.mainloop()


def submit_event(name: str, date: str, time: str, end_time: str, teacher_contact:str, sound: bool, mics: bool, lights: bool, projector: bool, ref: db.reference) -> bool:
    global crate_event_error_message
    if name != "" and name != "Event name" and name.replace(" ", "") != "":
        if date != "" and date != "yyyy-mm-dd" and date.replace(" ", "") != "" and len(date) == 10 and check_date(date):
            if time != "" and time != "hh:mm" and time.replace(" ", "") != "" and len(time) == 5 and check_time(time):
                if end_time != "" and end_time != "hh:mm" and end_time.replace(" ", "") != "" and len(end_time) == 5 and check_time(end_time):
                    if teacher_contact != "" and teacher_contact.replace(" ", "") != "" and "tdsb.on.ca" in teacher_contact and "@" in teacher_contact and len(teacher_contact) >= 20:
                        crate_event_error_message.configure(text="")
                        if not save_event_info(name, date, time, end_time, sound, mics, lights, projector, ref):
                            crate_event_error_message.configure(text="Error uploading event or event already exists.")
                            return False

                        else:
                            main()
                            return True
                    
                    else:
                        crate_event_error_message.configure(text="Teacher contact must be filled.")
                        return False

                else:
                    crate_event_error_message.configure(text="End time must be filled.")
                    return False

            else:
                crate_event_error_message.configure(text="Start time must be filled.")
                return False

        else:
            crate_event_error_message.configure(text="Date must be filled.")
            return False
    else:
        crate_event_error_message.configure(text="Event name must be filled.")
        return False


def create_event():
    global window, create_event_window, crate_event_error_message

    # -----------------------
    #   Destroy main window 
    #   and create new one
    # -----------------------
    window.destroy()

    create_event_window = tkinter.Tk()
    create_event_window.geometry("800x540")

    mainframe = tkinter.Frame(create_event_window)

    # ----------------------
    #   Create event label
    # ----------------------
    create_event_label = tkinter.Label(
        mainframe,
        text="Create event",
        font=("Comic Sans MS", 30, "bold")
    )
    create_event_label.grid(row=0, column=0)

    text_input_frame = tkinter.Frame(mainframe)

    # --------------------------
    #   Setting text font size
    # --------------------------
    text_font_size = 18

    # --------
    #   Name
    # --------
    name_label = tkinter.Label(
        text_input_frame,
        text="Name:",
        font=("Comic Sans MS", text_font_size, "bold")
    )
    name_label.grid(row=0, column=0)

    name = tkinter.Entry(text_input_frame)
    name.insert(0, "Event name")
    name.grid(row=0, column=1)


    # --------
    #   Date 
    # --------
    date_label = tkinter.Label(
        text_input_frame,
        text="Date:",
        font=("Comic Sans MS", text_font_size, "bold")
    )
    date_label.grid(row=1, column=0)

    date = tkinter.Entry(text_input_frame)
    date.insert(0, "YYYY-MM-DD")
    date.grid(row=1, column=1)


    # --------------
    #   Start time
    # --------------
    time_label = tkinter.Label(
        text_input_frame,
        text="Start time:",
        font=("Comic Sans MS", text_font_size, "bold")
    )
    time_label.grid(row=2, column=0)

    time = tkinter.Entry(text_input_frame)
    time.insert(0, "HH:MM")
    time.grid(row=2, column=1)


    # ------------
    #   End time
    # ------------
    end_time_label = tkinter.Label(
        text_input_frame,
        text="End time:",
        font=("Comic Sans MS", text_font_size, "bold")
    )
    end_time_label.grid(row=3, column=0)

    end_time = tkinter.Entry(text_input_frame)
    end_time.insert(0, "HH:MM")
    end_time.grid(row=3, column=1)


    # -------------------
    #   Teacher contact
    # -------------------
    teacher_contact_label = tkinter.Label(
        text_input_frame,
        text="Teacher contact:",
        font=("Comic Sans MS", text_font_size, "bold")
    )
    teacher_contact_label.grid(row=4, column=0)

    teacher_contact = tkinter.Entry(text_input_frame)
    teacher_contact.grid(row=4, column=1)


    # ---------
    #   Sound
    # ---------
    sound_label = tkinter.Label(
        text_input_frame,
        text="Sound:",
        font=("Comic Sans MS", text_font_size, "bold")
    )
    sound_label.grid(row=5, column=0)

    soundvar = tkinter.IntVar()
    sound = tkinter.Checkbutton(text_input_frame, variable=soundvar, onvalue=1, offvalue=0)
    sound.grid(row=5, column=1)

    # --------
    #   Mics
    # --------
    mics_label = tkinter.Label(
        text_input_frame,
        text="Mics:",
        font=("Comic Sans MS", text_font_size, "bold")
    )
    mics_label.grid(row=6, column=0)

    micsvar = tkinter.IntVar()
    mics = tkinter.Checkbutton(text_input_frame, variable=micsvar, onvalue=1, offvalue=0)
    mics.grid(row=6, column=1)

    # ----------
    #   Lights
    # ----------
    lights_label = tkinter.Label(
        text_input_frame,
        text="Lights:",
        font=("Comic Sans MS", text_font_size, "bold")
    )
    lights_label.grid(row=7, column=0)

    lightsvar = tkinter.IntVar()
    lights = tkinter.Checkbutton(text_input_frame, variable=lightsvar, onvalue=1, offvalue=0)
    lights.grid(row=7, column=1)


    # -------------
    #   Projector
    # -------------
    projector_label = tkinter.Label(
        text_input_frame,
        text="Projector:",
        font=("Comic Sans MS", text_font_size, "bold")
    )
    projector_label.grid(row=8, column=0)

    projectorvar = tkinter.IntVar()
    projector = tkinter.Checkbutton(text_input_frame, variable=projectorvar, onvalue=1, offvalue=0)
    projector.grid(row=8, column=1)


    # -----------------
    #   Submit button
    # -----------------
    submit_button = tkinter.Button(
        text_input_frame,
        text="Submit",
        command=lambda: submit_event(
            name.get(), 
            date.get(), 
            time.get(), 
            end_time.get(), 
            teacher_contact.get(),
            True if soundvar.get() == 1 else False,
            True if micsvar.get() == 1 else False, 
            True if lightsvar.get() == 1 else False, 
            True if projectorvar.get() == 1 else False,
            DB_REFERENCE
        )
    )
    submit_button.grid(row=9, column=1)


    # -----------------
    #   Error message
    # -----------------
    crate_event_error_message = tkinter.Label(
        text_input_frame,
        text="",
        font=("Comic Sans MS", text_font_size, "bold"),
        fg="red"
    )
    crate_event_error_message.grid(row=10, column=1)


    # ---------------
    #   Back button
    # ---------------
    back = tkinter.Button(
        mainframe,
        text="Back",
        command=lambda: main()
    )
    back.grid(row=2, column=0)


    # ----------
    #   Spacer
    # ----------
    spacer = tkinter.Label(
        create_event_window,
        text="",
        width=10
    )
    spacer.grid(row=0, column=0)


    # -------------------
    #   Start main loop
    # -------------------
    text_input_frame.grid(row=1, column=0)
    mainframe.grid(row=0, column=1)
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


    # -------------------
    #   Main menu label
    # -------------------
    main_menu_label = tkinter.Label(
        window,
        text="Main menu",
        font=("Comic Sans MS", 20, "bold")
    )
    main_menu_label.grid(row=0, column=0)


    # ----------------
    #   Button frame
    # ----------------
    button_frame = tkinter.Frame(window)


    # ----------------------
    #   Add student button
    # ----------------------
    add_student_button = tkinter.Button(
        button_frame,
        text="Add a student",
        command=add_student
    )
    add_student_button.grid(row=0, column=0)


    # -----------------------
    #   Create event button
    # -----------------------
    create_event_button = tkinter.Button(
        button_frame,
        text="Create an event",
        command=create_event
    )
    create_event_button.grid(row=0, column=1)


    # -------------------
    #   Start main loop
    # -------------------
    button_frame.grid(row=1, column=0)
    window.mainloop()


if __name__ == "__main__":
    global add_student_window, create_event_window

    create_event_window = None
    add_student_window = None
    main()
