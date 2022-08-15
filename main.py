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
from tkinter import ttk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import date as date_year
from datetime import datetime
from tkcalendar import Calendar

# Initialize Firebase
cred = credentials.Certificate(os.path.join(os.getcwd(), "stage-crew-event-manager-firebase-adminsdk-ed2pg-b047e32b38.json"))
DB_CONNECTION = firebase_admin.initialize_app(cred, {"databaseURL": "https://stage-crew-event-manager-default-rtdb.firebaseio.com"})
DB_REFERENCE = db.reference("/")



# \\\\\\\\\\\\\\\\\\\\\\\\\\
#     Database functions
# \\\\\\\\\\\\\\\\\\\\\\\\\\

def save_student_info(fname: str, lname: str, email: str, events: str, grade: str, update_students: bool=False) -> bool:
    ref = db.reference("/")
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
        "events": int(events),
        "grade": int(grade),
        "version": 1.1
    }

    try:
        items = ref.get()
        if items is not None:
            for item in items:
                if items[item]["email"] == email:
                    if update_students:
                        db.reference("/Students/"+item).transaction(lambda value: data if value == items[item] else value)
                        return True
                    
                    else:
                        return False
        
        else:
            ref.push().set(data)
            return True

        version_updater(ref)

    except Exception as e:
        print(e)
        return False


def get_students() -> list or None:
    ref = db.reference("/")
    ref_data = ref.get()

    if ref_data is None:
        ref.set({"Students": {}})
    
    elif "Students" not in ref_data.keys():
        ref_data["Students"] = {}
        ref.set(ref_data)

    ref = db.reference("/Students")
    
    students = []
    items = ref.get()
    for item in items:
        students.append(items[item])

    if len(students) <= 0:
        return None
    else:
        return students


def save_event_info(name: str, date: str, start_time: str, end_time: str, sound: bool, mics: bool, lights: bool, projector: bool, teacher_email: str, update_event: bool=False) -> bool:
    # -------------------------
    #    Check if directory 
    #   exists if not make it
    # -------------------------
    ref = db.reference("/")
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
        "projector": projector,
        "teacher contact": teacher_email,
        "version": 1.1
    }

    # -------------------------
    #   Add event to database
    # -------------------------
    try:
        items = ref.get()
        if items is not None:
            for key, item in items.items():
                past_item = item.copy()
                if item["name"].lower() == name.lower():
                    if update_event:
                        for key2, value in data.items():
                            if key2 not in item.keys():
                                items[key][key2] = value
                            
                            if value != items[key][key2]:
                                items[key][key2] = value
                        ref = db.reference("/Events/"+key)
                        ref.transaction(lambda value2: items[key] if past_item == value2 else value2)
                        return True
                    
                    else:
                        print("Update event not active canceling push")
                        return False

        else:
            ref.push().set(data)
            return True
        
        version_updater(ref)

    except Exception as e:
        print(e)
        return False


def get_all_events():
    ref = db.reference("/")
    ref_data = ref.get()

    if ref_data is None:
        ref.set({"Events": {}})

    elif "Events" not in ref_data.keys():
        ref_data["Events"] = {}
        ref.set(ref_data)
    
    ref = db.reference("/Events")
    
    data = ref_data["Events"]
    results = []
    for key, value in data.items():
        value["key"] = key
        results.append(value)
    
    return results


def get_all_students():
    ref = db.reference("/")
    ref_data = ref.get()

    if ref_data is None:
        ref.set({"Students": {}})

    elif "Students" not in ref_data.keys():
        ref_data["Students"] = {}
        ref.set(ref_data)
    
    ref = db.reference("/Students")
    
    data = ref_data["Students"]
    results = []
    for key, value in data.items():
        value["key"] = key
        results.append(value)
    
    return results


def version_updater(ref: db.reference):
    section = ref.path
    ref_data = ref.get()
    past_ref_value = db.reference(section).get()

    temp = db.reference("/Version").get()

    if "/" == section or section is None:
        print("No data")
        return False
    
    elif "Students" in section:
        current_version = int(temp["Students"]["v"])

    elif "Events" in section:
        current_version = int(temp["Events"]["v"])

    updated = False

    # each dict
    for key, value in ref_data.items():
        # each student/event in dict
        if "version" not in value.keys():
            value["version"] = 0

        if value["version"] < current_version:
            template = db.reference("/Version"+section+"/template").get()

            # Find missing keys and add them
            if template.keys() != value.keys():
                for key2 in template.keys():
                    if key2 not in value.keys():
                        ref_data[key][key2] = template[key2]

            value["version"] = current_version
            updated = True

    if updated:
        # Add everything to the database
        ref = db.reference(section)
        ref.transaction(lambda value: value if past_ref_value != value else ref_data)

        ref = db.reference("/Version" + section + "/v")
        ref.transaction(lambda value: value + .1 if value < current_version+.1 else value)
        if ref.get() > current_version+.1:
            version_updater(db.reference(section))
        else:
            return True


def remove_student_info(email: str):
    ref = db.reference("/Students")
    items = ref.get()
    for key, value in items.items():
        if value["email"] == email:
            ref.child(key).remove()
            return True

    return False


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


def submit_student(fname, lname, email, events, grade: str, error_message, update: bool=False):
    global add_student_window, error_label_add_students
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    if fname != "":
        if lname != "":
            if email != "" and "@" in email and "tdsb.on.ca" in email:
                if events != "" and all(char in numbers for char in events):
                    if grade != "" and 12 >= int(grade) >= 9:
                        if not save_student_info(fname, lname, email, events, grade, update):
                            error_message.config(text="Error adding student or student already exists.")
                            return False

                        else:
                            error_message.configure(text="")
                            add_student_window.destroy()
                            add_student_window = None
                            return True
                    else:
                        error_message.configure(text="Grade must be either 9, 10, 11, or 12.")

                else:
                    error_message.configure(text="Amount of events must be entered.")
            else:
                error_message.configure(text="Email must be filled and must be a tdsb email.")
        else:
            error_message.configure(text="Last name must be filled.")
    else:    
        error_message.configure(text="First name must be filled.")


def add_student():
    global window, add_student_window, error_label_add_students
    window.destroy ()

    add_student_window = tkinter.Tk()
    #add_student_window.geometry("400x200")


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

    # --------------------
    #   Grade of student
    # --------------------
    grade_label = tkinter.Label(
        studentInputFrame,
        text="Grade:",
        font=("Comic Sans MS", 12, "bold")
    )
    grade_label.grid (row=4, column=0)

    grade = tkinter.Entry(studentInputFrame)
    grade.grid(row=4, column=1)


    # ---------------------------------
    #   Button for submitting student
    # ---------------------------------
    submit_button = tkinter.Button(
        studentInputFrame,
        text="Submit",
        command=lambda: main() if submit_student(
            fname.get(), 
            lname.get(), 
            email.get(), 
            events.get(), 
            grade.get(), 
            error_label_add_students
        ) else False
    )
    submit_button.grid(row=5, column=0, columnspan=2, sticky="nsew")


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
    back.grid(row=2, column=0, sticky="nsew")


    # ----------------
    #   Start window
    # ----------------
    studentInputFrame.grid(row=0, column=0)
    add_student_window.mainloop()


def submit_event(name: str, date: str, time: str, end_time: str, teacher_contact:str, sound: bool, mics: bool, lights: bool, projector: bool, error_box, update_event: bool=False) -> bool:
    if name != "" and name != "Event name" and name.replace(" ", "") != "":
        if date != "" and date != "yyyy-mm-dd" and date.replace(" ", "") != "" and len(date) == 10 and check_date(date):
            if time != "" and time != "hh:mm" and time.replace(" ", "") != "" and len(time) == 5 and check_time(time):
                if end_time != "" and end_time != "hh:mm" and len(end_time) == 5 and check_time(end_time):
                    if teacher_contact != "" and teacher_contact.replace(" ", "") != "" and "tdsb.on.ca" in teacher_contact and "@" in teacher_contact and len(teacher_contact) >= 15:
                        error_box.configure(text="")
                        if not save_event_info(name, date, time, end_time, sound, mics, lights, projector, teacher_contact, update_event=update_event):
                            error_box.configure(text="Error uploading event or event already exists.")
                            return False

                        else:
                            return True
                    
                    else:
                        error_box.configure(text="Teacher contact must be filled.")
                        return False

                else:
                    error_box.configure(text="End time must be filled.")
                    return False

            else:
                error_box.configure(text="Start time must be filled.")
                return False

        else:
            error_box.configure(text="Date must be filled.")
            return False

    else:
        error_box.configure(text="Event name must be filled.")
        return False


def create_event():
    global window, create_event_window

    # -----------------------
    #   Destroy main window 
    #   and create new one
    # -----------------------
    window.destroy()

    create_event_window = tkinter.Tk()
    # create_event_window.geometry("800x540")

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

    name = tkinter.Entry(text_input_frame, width=40)
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

    date = tkinter.Entry(text_input_frame, width=40)
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

    time = tkinter.Entry(text_input_frame, width=40)
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

    end_time = tkinter.Entry(text_input_frame, width=40)
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

    teacher_contact = tkinter.Entry(text_input_frame, width=40)
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
        command=lambda: main() if submit_event(
            name.get(), 
            date.get(), 
            time.get(), 
            end_time.get(), 
            teacher_contact.get(),
            True if soundvar.get() == 1 else False,
            True if micsvar.get() == 1 else False, 
            True if lightsvar.get() == 1 else False, 
            True if projectorvar.get() == 1 else False,
            create_event_error_message, 
        ) else False
    )
    submit_button.grid(row=9, column=1)


    # -----------------
    #   Error message
    # -----------------
    create_event_error_message = tkinter.Label(
        text_input_frame,
        text="",
        font=("Comic Sans MS", text_font_size, "bold"),
        fg="red"
    )
    create_event_error_message.grid(row=10, column=0, columnspan=2)


    # ---------------
    #   Back button
    # ---------------
    back = tkinter.Button(
        create_event_window,
        text="Back",
        command=lambda: main()
    )
    back.grid(row=1, column=0, columnspan=4, sticky="nsew")


    # ----------
    #   Spacer
    # ----------
    spacer = tkinter.Label(
        create_event_window,
        text="",
        width=2
    )
    spacer.grid(row=0, column=0)

    spacer2 = tkinter.Label(
        create_event_window,
        text="",
        width=2
    )
    spacer2.grid(row=0, column=3)


    # -------------------
    #   Start main loop
    # -------------------
    text_input_frame.grid(row=1, column=0)
    mainframe.grid(row=0, column=1)
    create_event_window.mainloop()


def view_events():
    global window, view_events_window, EVENTS, current_event
    window.destroy()

    current_event = 0

    # ------------------------------------
    #   Get all events from the calendar
    # ------------------------------------
    received_events = get_all_events()


    def update_displayed_events(cal: Calendar):
        # ------------------------------------------
        #   Add all received events to the calendar
        # ------------------------------------------
        for event in received_events:

            displayed_month, displayed_year = cal.get_displayed_month_year()
            if int(event["date"].split("-")[1]) == displayed_month and int(event["date"].split("-")[0]) == displayed_year:
                time = datetime.strptime(event["date"], "%Y-%m-%d")
                details = f'{event["name"]}|{event["date"]}|{event["start time"]}|{event["end time"]}|{event["mics"]}|{event["lights"]}|{event["projector"]}|{event["sound"]}|{event["teacher contact"]}|{event["key"]}'
                cal.calevent_create(time, details, "Message")
        
        cal.tag_config("Message", background="blue", foreground="black")




    class CustomCalendar(Calendar):
        def _next_month(self):
            Calendar._next_month(self)
            self.event_generate("<<CalendarMonthChanged>>")
            update_displayed_events(self)


        def _prev_month(self):
            Calendar._prev_month(self)
            self.event_generate("<<CalendarMonthChanged>>")
            update_displayed_events(self)


        def _next_year(self):
            Calendar._next_year(self)
            self.event_generate("<<CalendarMonthChanged>>")
            update_displayed_events(self)


        def _prev_year(self):
            Calendar._prev_year(self)
            self.event_generate("<<CalendarMonthChanged>>")
            update_displayed_events(self)


        def get_displayed_month_year(self):
            return self._date.month, self._date.year



    view_events_window = tkinter.Tk()
    EVENTS = []

    def cal_day_selected(_=None):
        global EVENTS
        if cal.get_calevents(cal.selection_get()):
            events = cal.get_calevents(cal.selection_get())
            if EVENTS != events:
                EVENTS = [[event, 0] for event in events]
                EVENTS[0][1] = 1
                display_event(EVENTS[0][0])
        else:
            display_event(None)


    def display_event(event_id):
        if event_id is not None:
            text = cal.calevent_cget(event_id, "text")
            text = text.split("|")
        else:
            text = ["","","","","","","","",""]

        # -------------------------------------------
        #   Set up all labels according to the text
        # -------------------------------------------
        entrys = [
            (event_name_label, text[0]),
            (date_label, text[1]),
            (start_time_label, text[2]),
            (end_time_label, text[3]),
            (teacher_contact_label, text[8])
        ]

        checks = [
            (mics_checkbutton_value, text[4]),
            (lights_checkbutton_value, text[5]),
            (projector_checkbutton_value, text[6]),
            (sound_checkbutton_value, text[7])
        ]

        for entry, text in entrys:
            entry.delete(0, tkinter.END)
            entry.insert(0, text)


        for check, text in checks:
            if text == "True":
                check.set(1)

            else:
                check.set(0)

        event_count_label.config(text=f"Event {current_event}/{len(EVENTS)}")


    def next_event():
        global EVENTS, current_event
        if len(EVENTS) > 0:
            starting_pos = None
            for pos, event in enumerate(EVENTS):
                if event[1] == 1:
                    starting_pos = pos
                    break

            EVENTS[starting_pos][1] = 0
            
            if starting_pos != None:
                pos = starting_pos
                pos += 1
                if pos > len(EVENTS)-1:
                    pos = 0
                    current_event = 0

                if EVENTS[pos][1] == 0:
                    current_event += 1
                    display_event(EVENTS[pos][0])
                    EVENTS[pos][1] = 1


    def back_event():
        global EVENTS, current_event
        if len(EVENTS) > 0:
            starting_pos = None
            for pos, event in enumerate(EVENTS):
                if event[1] == 1:
                    starting_pos = pos
                    break
            
            EVENTS[starting_pos][1] = 0

            if starting_pos != None:
                pos = starting_pos
                pos -= 1
                if pos < 0:
                    pos = len(EVENTS)-1
                    current_event = len(EVENTS)-1
                    
                if EVENTS[pos][1] == 0:
                    current_event += 1
                    display_event(EVENTS[pos][0])
                    EVENTS[pos][1] = 1
                    current_event += 1


    def save():
        if len(EVENTS) > 0 and cal.get_calevents(cal.selection_get()):
            if submit_event(
                name=event_name_label.get(),
                date=date_label.get(),
                time=start_time_label.get(),
                end_time=end_time_label.get(),
                teacher_contact=teacher_contact_label.get(),
                sound=True if sound_checkbutton_value.get() == 1 else False,
                mics=True if mics_checkbutton_value.get() == 1 else False,
                lights=True if lights_checkbutton_value.get() == 1 else False,
                projector=True if projector_checkbutton_value.get() == 1 else False,
                error_box=error_message, 
                update_event=True
            ):
                error_message.configure(text="Event updated", fg="lime green")
                error_message.after(9000, lambda: error_message.configure(text="", fg="red"))

        else:
            error_message.configure(text="No event selected", fg="red")



    # -------------------
    #   Custom calendar
    # -------------------
    cal = CustomCalendar(view_events_window, selectmode="day")
    cal.bind("<<CalendarSelected>>", cal_day_selected)


    # ---------------------------
    #   Calender events counter
    # ---------------------------
    event_count_label = tkinter.Label(view_events_window, text="Events: 0/0")
    event_count_label.grid(row=1, column=0)

    update_displayed_events(cal)


    # -----------------------
    #   Event details frame
    # -----------------------
    event_details_frame = tkinter.Frame(view_events_window)


    # -----------------------
    #   Event details label
    # -----------------------
    event_details = tkinter.Label(
        event_details_frame, 
        text="Event details",
        font=("Comic Sans MS", 18, "bold")
    )
    event_details.grid(row=0, column=0, columnspan=2)


    # --------------------
    #   Event name label
    # --------------------
    event_name = tkinter.Label(event_details_frame, text="Event name:")
    event_name.grid(row=1, column=0)


    # --------------------------
    #   Event name entry label
    # --------------------------
    event_name_label = tkinter.Entry(event_details_frame)
    event_name_label.grid(row=1, column=1)


    # --------
    #   Date
    # --------
    date = tkinter.Label(event_details_frame, text="Date:")
    date.grid(row=2, column=0)


    # --------------------
    #   Date entry label
    # --------------------
    date_label = tkinter.Entry(event_details_frame)
    date_label.grid(row=2, column=1)


    # --------------
    #   Start time
    # --------------
    start_time = tkinter.Label(event_details_frame, text="Start time:")
    start_time.grid(row=3, column=0)


    # --------------------------
    #   Start time entry label
    # --------------------------
    start_time_label = tkinter.Entry(event_details_frame)
    start_time_label.grid(row=3, column=1)


    # ------------
    #   End time
    # ------------
    end_time = tkinter.Label(event_details_frame, text="End time:")
    end_time.grid(row=4, column=0)


    # ------------------------
    #   End time entry label
    # ------------------------
    end_time_label = tkinter.Entry(event_details_frame)
    end_time_label.grid(row=4, column=1)


    # -------------------
    #   Teacher contact
    # -------------------
    teacher_contact = tkinter.Label(event_details_frame, text="Teacher contact:")
    teacher_contact.grid(row=5, column=0)


    # -------------------------------
    #   Teacher contact entry label
    # -------------------------------
    teacher_contact_label = tkinter.Entry(event_details_frame, width=40)
    teacher_contact_label.grid(row=5, column=1)


    # ---------
    #   Sound
    # ---------
    sound = tkinter.Label(event_details_frame, text="Sound:")
    sound.grid(row=6, column=0)


    # ---------------------------
    #   Sound entry checkbutton
    # ---------------------------
    sound_checkbutton_value = tkinter.IntVar()
    sound_checkbutton = tkinter.Checkbutton(
        event_details_frame,
        variable=sound_checkbutton_value, 
        onvalue=1, 
        offvalue=0
    )
    sound_checkbutton.grid(row=6, column=1)


    # --------
    #   Mics 
    # --------
    mics = tkinter.Label(event_details_frame, text="Mics:")
    mics.grid(row=7, column=0)


    # --------------------------
    #   Mics entry checkbutton
    # --------------------------
    mics_checkbutton_value = tkinter.IntVar()
    mics_checkbutton = tkinter.Checkbutton(
        event_details_frame,
        variable=mics_checkbutton_value,
        onvalue=1,
        offvalue=0
    )
    mics_checkbutton.grid(row=7, column=1)


    # ----------
    #   Lights
    # ----------
    lights = tkinter.Label(event_details_frame, text="Lights:")
    lights.grid(row=8, column=0)


    # ----------------------------
    #   Lights entry checkbutton
    # ----------------------------
    lights_checkbutton_value = tkinter.IntVar()
    lights_checkbutton = tkinter.Checkbutton(
        event_details_frame,
        variable=lights_checkbutton_value,
        onvalue=1,
        offvalue=0
    )
    lights_checkbutton.grid(row=8, column=1)


    # -------------
    #   Projector
    # -------------
    projector = tkinter.Label(event_details_frame, text="Projector:")
    projector.grid(row=9, column=0)


    # -------------------------------
    #   Projector entry checkbutton
    # -------------------------------
    projector_checkbutton_value = tkinter.IntVar()
    projector_checkbutton = tkinter.Checkbutton(
        event_details_frame,
        variable=projector_checkbutton_value,
        onvalue=1,
        offvalue=0
    )
    projector_checkbutton.grid(row=9, column=1)


    # ---------------
    #   Next button
    # ---------------
    next_button = tkinter.Button(
        event_details_frame,
        text="Next Event",
        command=next_event
    )
    next_button.grid(row=10, column=1, sticky="nsew")


    # ----------------------
    #   Back button events
    # ----------------------
    back_button = tkinter.Button(
        event_details_frame,
        text="Previous event",
        command=back_event
    )
    back_button.grid(row=10, column=0, sticky="nsew")


    # ---------------
    #   Save button
    # ---------------
    save_button = tkinter.Button(
        event_details_frame,
        text="Save",
        command=save
    )
    save_button.grid(row=11, column=0, columnspan=2, sticky="nsew")


    # -----------------------
    #   Error message label
    # -----------------------
    error_message = tkinter.Label(view_events_window, text="", fg="red", font=("comic sans", 14))
    error_message.grid(row=3, column=0, columnspan=4)


    # ---------------
    #   Back button
    # ---------------
    back_button_main = tkinter.Button(
        view_events_window,
        text="Back",
        command=lambda: main()
    )
    back_button_main.grid(row=5, column=0, columnspan=4, sticky="nsew")


    # -------------------------------
    #   view_events_window mainloop
    # -------------------------------
    cal.grid(row=0, column=0, columnspan=2)
    event_details_frame.grid(row=0, column=3)
    view_events_window.mainloop()


def view_students():
    global window

    window.destroy()

    version_updater(db.reference("/Students"))

    student_view_window = tkinter.Tk()


    def show(student):
        first_name_entry.delete(0, tkinter.END)
        first_name_entry.insert(0, student["first name"].capitalize())

        last_name_entry.delete(0, tkinter.END)
        last_name_entry.insert(0, student["last name"].capitalize())

        email_entry.delete(0, tkinter.END)
        email_entry.insert(0, student["email"])

        grade_entry.delete(0, tkinter.END)
        grade_entry.insert(0, str(student["grade"]))

        events_attended_entry.delete(0, tkinter.END)
        events_attended_entry.insert(0, str(student["events"]))    


    def save_students():
        if save_student_info(
            first_name_entry.get(), 
            last_name_entry.get(), 
            email_entry.get(), 
            events_attended_entry.get(),
            grade_entry.get(),
            update_students=True, 
        ):
            view_students_error_message.configure(text="Student updated successfully!", fg="lime green")
            view_students_error_message.after(9000, lambda: view_students_error_message.configure(text="", fg="red"))
            refresh_list()
            return True
        
        refresh_list()


    def remove_student():
        if email_entry.get() != "":
            if remove_student_info(email_entry.get()):
                refresh_list()
                view_students_error_message.configure(text="Student removed successfully!", fg="lime green")
                view_students_error_message.after(9000, lambda: view_students_error_message.configure(text="", fg="red"))
                refresh_list()
                return True
            
            else:
                view_students_error_message.configure(text="Student not found!", fg="red")
                view_students_error_message.after(9000, lambda: view_students_error_message.configure(text="", fg="red"))
                refresh_list()
                return False
        else:
            view_students_error_message.configure(text="Please select a student!", fg="red")
            view_students_error_message.after(9000, lambda: view_students_error_message.configure(text="", fg="red"))
            refresh_list()
            return False
        

    def refresh_list():
        # -----------------------------------
        #   Add all students to scroll list
        # -----------------------------------
        for row, student in enumerate(get_all_students()):
            student_name = f'{student["first name"].capitalize()} {student["last name"].capitalize()}'
            student_events = f'Events attended: {student["events"]}'

            student_frame = ttk.Frame(scrollable_frame)
            
            student_label = ttk.Label(student_frame, text=student_name, width=30, background="light gray" if row%2 != 0 else "white")
            student_label.grid(row=0, column=0)

            student_label_2 = ttk.Label(student_frame, text=student_events, width=18, background="light gray" if row%2 != 0 else "white")
            student_label_2.grid(row=0, column=1)
            
            student_button = ttk.Button(
                student_frame, 
                text="Remove",
                command=lambda: show(student)
            )
            student_button.grid(row=0, column=2)

            student_frame.grid(row=row, column=0, sticky="nsew")


    container = ttk.Frame(student_view_window)
    canvas = tkinter.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)


    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    refresh_list()


    # -----------------
    #   Details frame
    # -----------------
    student_details_frame = ttk.Frame(student_view_window)


    # --------------
    #   First name
    # --------------
    first_name = tkinter.Label(student_details_frame, text="First name:")
    first_name.grid(row=0, column=0)
    first_name_entry = tkinter.Entry(student_details_frame, width=50)
    first_name_entry.grid(row=0, column=1)


    # -------------
    #   Last name
    # -------------
    last_name = tkinter.Label(student_details_frame, text="Last name:")
    last_name.grid(row=1, column=0)
    last_name_entry = tkinter.Entry(student_details_frame, width=50)
    last_name_entry.grid(row=1, column=1)


    # ---------
    #   Email
    # ---------
    email = tkinter.Label(student_details_frame, text="Email:")
    email.grid(row=2, column=0)
    email_entry = tkinter.Entry(student_details_frame, width=50)
    email_entry.grid(row=2, column=1)


    # ---------
    #   Grade
    # ---------
    grade = tkinter.Label(student_details_frame, text="Grade:")
    grade.grid(row=3, column=0)
    grade_entry = tkinter.Entry(student_details_frame, width=50)
    grade_entry.grid(row=3, column=1)


    # -----------------------------
    #   Amount of events attended
    # -----------------------------
    events_attended = tkinter.Label(student_details_frame, text="Events attended:")
    events_attended.grid(row=4, column=0)
    events_attended_entry = tkinter.Entry(student_details_frame, width=50)
    events_attended_entry.grid(row=4, column=1)

    # ---------------
    #   Save button
    # ---------------
    save_button = tkinter.Button(
        student_details_frame,
        text="Save",
        command=save_students
    )
    save_button.grid(row=5, column=1, sticky="nsew")


    # ----------------------
    #   Schedule for event
    # ----------------------
    schedule_button = tkinter.Button(
        student_details_frame,
        text="Schedule",
        command=lambda: True
    )
    schedule_button.grid(row=5, column=0, sticky="nsew")


    # ------------------
    #   Delete student
    # ------------------
    delete_button = tkinter.Button(
        student_details_frame,
        text="Delete",
        command=remove_student
    )
    delete_button.grid(row=6, column=0, sticky="nsew")


    # ------------------
    #   Refresh button
    # ------------------
    refresh_button = tkinter.Button(
        student_details_frame,
        text="Refresh",
        command=refresh_list
    )
    refresh_button.grid(row=6, column=1, sticky="nsew")



    # -----------------
    #   Error message
    # -----------------
    view_students_error_message = tkinter.Label(
        student_details_frame, 
        text="",
        fg="red",
        font=("comic sans", 14)
    )
    view_students_error_message.grid(row=90, column=0, columnspan=2)



    container.grid(row=0, column=0)
    student_details_frame.grid(row=0, column=1)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    student_view_window.mainloop()



def main():
    global window, WIN_WIDTH, WIN_HEIGHT, add_student_window, create_event_window, view_events_window, student_view_window
    if add_student_window != None:
        add_student_window.destroy()
        add_student_window = None

    if create_event_window != None:
        create_event_window.destroy()
        create_event_window = None
    
    if view_events_window != None:
        view_events_window.destroy()
        view_events_window = None
    
    if student_view_window != None:
        student_view_window.destroy()
        student_view_window = None


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


    # ----------------------
    #   View events button
    # ----------------------
    view_events_button = tkinter.Button(
        button_frame,
        text="View events",
        command=view_events,
    )
    view_events_button.grid(row=0, column=2)


    # ------------------------
    #   View students button
    # ------------------------
    view_students_button = tkinter.Button(
        button_frame,
        text="View students",
        command=view_students,
    )
    view_students_button.grid(row=0, column=3)


    # -------------------
    #   Start main loop
    # -------------------
    button_frame.grid(row=1, column=0)
    window.mainloop()


if __name__ == "__main__":
    global add_student_window, create_event_window, view_events_window, student_view_window

    create_event_window = None
    add_student_window = None
    view_events_window = None
    student_view_window = None
    main()
