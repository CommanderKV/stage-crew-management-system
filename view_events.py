import tkinter
from events import Events
from datetime import datetime
from tkcalendar import Calendar
import json


def main():
    global EVENTS, inputs
    events_connection = Events()


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


    def back():
        view_events_window
        raise Exception("Back")


    def update_displayed_events(cal: CustomCalendar):
        # ------------------------------------------
        #   Add all received events to the calendar
        # ------------------------------------------
        displayed_month, displayed_year = cal.get_displayed_month_year()

        events = events_connection.get_events_by_month()
        term = "date"
        for key in events_connection.template.keys():
            if "date" in str(key).lower():
                term = key
                break

        for month in events:
            if int(month) == displayed_month:
                for event in events[month]:
                    if events[month][event][term].split("-")[0] == str(displayed_year):
                        time = datetime.strptime(events[month][event][term], "%Y-%m-%d")
                        details = events[month][event]
                        details["temporary id"] = event
                        cal.calevent_create(time, details, "Message")
        
        cal.tag_config("Message", background="orange", foreground="black")


    def save():
        """
        Save / update the event
        """
        global EVENTS

        def is_number(string: str) -> bool:
            numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            for char in string:
                if char not in numbers:
                    return False

            return True


        for key in events_connection.template.keys():
            if key != "version":
                label = inputs[key][0].cget("text")

                if str(events_connection.template[key]).upper() == "TRUE OR FALSE":
                    entry = inputs[key][2].get()

                else:
                    entry = inputs[key][1].get()

                    if entry == "":
                        # entry is empty
                        error_message.config(text="Fill in all fields", fg="red")
                        break

                    value = str(events_connection.template[key]).upper()
                    if str(entry).upper() == str(value).upper():
                        # entry is same as default
                        error_message.config(text="Enter a different value for {}".format(label), fg="red")
                        break


                    elif "TIME" in str(label).upper():
                        if len(entry) != 5:
                            # entry is not a time
                            error_message.config(text="Enter a valid time for {}".format(label), fg="red")
                            break

                        elif entry[2] != ":":
                            # entry is not a time
                            error_message.config(text="Enter a valid time for {}".format(label), fg="red")
                            break

                        elif is_number(entry[0:2]) == False or is_number(entry[3:5]) == False:
                            # entry is not a time
                            error_message.config(text="Enter a valid time for {}".format(label), fg="red")
                            break


                    elif "DATE" in str(label).upper():
                        if len(entry) != 10:
                            # entry is not a date
                            error_message.config(text="Enter a valid date for {} format: yyyy-mm-dd".format(label), fg="red")
                            break

                        elif entry[4] != "-" or entry[7] != "-":
                            # entry is not a date
                            error_message.config(text="Enter a valid date for {} format: yyyy-mm-dd".format(label), fg="red")
                            break

                        elif is_number(entry[0:4]) == False or is_number(entry[5:7]) == False or is_number(entry[8:10]) == False:
                            # entry is not a date
                            error_message.config(text="Enter a valid date for {} format: yyyy-mm-dd".format(label), fg="red")
                            break

                        elif datetime.strptime(entry, "%Y-%m-%d") < datetime.now():
                            # entry is not a date
                            error_message.config(text="{} must be in the future".format(label), fg="red")
                            break

                    
                    elif "contact" in label:
                        email = entry.replace(" ", "")
                        if "@" not in email:
                            # entry is not an email
                            error_message.config(text="Enter a valid email for {}".format(label), fg="red")
                            break

                        elif "." not in email:
                            # entry is not an email
                            error_message.config(text="Enter a valid email for {}".format(label), fg="red")
                            break

                        elif "tdsb.on.ca" not in email:
                            # entry is not an email
                            error_message.config(text="Enter a valid email for {}".format(label), fg="red")
                            break

                        elif len(email) < 15:
                            # entry is not an email
                            error_message.config(text="Enter a valid email for {}".format(label), fg="red")
                            break


        if error_message["text"] == "":
            event = {}
            for key in inputs:
                if key != "version":
                    if str(events_connection.template[key]).upper() == "TRUE OR FALSE":
                        event[key] = inputs[key][2].get()

                    else:
                        event[key] = inputs[key][1].get()
            
            event["version"] = events_connection.template["version"]


            # -------------------------------------------------------------------------
            #   If there are no errors then we will find the database id of the event
            #   then we will edit that event if there is an event selected otherwise 
            #                       we will create a new one 
            # -------------------------------------------------------------------------
            if cal.get_calevents(cal.get_date()):
                for events in EVENTS:
                    if events[1] == 1:
                        event_database_id = cal.calevent_cget(events[0], "text")["temporary id"]

                if events_connection.edit_event(event_database_id, event):
                    back()
                
                else:
                    error_message.config(text="Error adding event", fg="red")
            
            else:
                if events_connection.add_event(event):
                    back()
                
                else:
                    error_message.config(text="Error adding event", fg="red")
        
        else:
            error_message.after(9000, lambda: error_message.config(text="", fg="black"))


    view_events_window = tkinter.Tk()
    EVENTS = [0, 1]

    def cal_day_selected(_=None):
        """
        Displays the selected day and 
        updates the events in the EVENTS list
        """
        global EVENTS
        if cal.get_calevents(cal.selection_get()):
            events = cal.get_calevents(cal.selection_get())
            if EVENTS != events:
                EVENTS = [[event, 0] for event in events]
                EVENTS[0][1] = 1
                display_event(EVENTS[0][0])
        
        else:
            display_event(None)


    def display_event(event_id: int):
        """
        Used to display a specific event

        Args:
            event_id (int): event_id according to tkcalander
        """


        global inputs

        if event_id is not None:
            event = cal.calevent_cget(event_id, "text")

            for key in inputs:
                if key != "version":
                    values = inputs[key]
                    if len(values) == 3:
                        values[2].set(event[key])

                    else:
                        values[1].delete(0, tkinter.END)
                        values[1].insert(0, event[key])
            
        else:
            event = None

            template = events_connection.get_event_struct()

            for key in inputs:
                values = inputs[key]
                if len(values) == 3:
                    values[2].set(False)
                
                else:
                    values[1].delete(0, tkinter.END)
                    values[1].insert(0, template[key])


    def next_event():
        """
        Used to switch up which event is being displayed
        """
        global EVENTS
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

                if EVENTS[pos][1] == 0:
                    display_event(EVENTS[pos][0])
                    EVENTS[pos][1] = 1


    def back_event():
        """
        Used to switch up which event is being displayed
        """
        global EVENTS
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

                if EVENTS[pos][1] == 0:
                    display_event(EVENTS[pos][0])
                    EVENTS[pos][1] = 1



    # -------------------
    #   Custom calendar
    # -------------------
    cal = CustomCalendar(
        view_events_window, 
        selectmode="day",
        weekenddays=[1, 7],
        showweeknumbers=False, 
        firstweekday="sunday"
    )
    cal.bind("<<CalendarSelected>>", cal_day_selected)

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


    # ------------------------------
    #   Get all of the entrys from 
    #   the template and add them
    # ------------------------------
    event_template = events_connection.get_event_struct()
    inputs = {}
    for row, key in enumerate(event_template):
        if key != "version":
            if str(events_connection.template[key]).upper() == "TRUE OR FALSE":
                check_buttons = tkinter.BooleanVar()
                inputs[key] = [
                    tkinter.Label(
                        event_details_frame, 
                        text=str(key)[1:].capitalize(),
                        font=("comic sans ms", 12),
                        width=20
                    ),
                    tkinter.Checkbutton(
                        event_details_frame,
                        variable=check_buttons,
                        onvalue=True,
                        offvalue=False
                    ),
                    check_buttons
                ]

            else:
                inputs[key] = [
                    tkinter.Label(
                        event_details_frame,
                        text=str(key)[1:].capitalize(),
                        font=("comic sans ms", 12),
                        width=20
                    ),
                    tkinter.Entry(
                        event_details_frame,
                        width=50
                    )
                ]
            
            inputs[key][0].grid(row=row+1, column=0)
            inputs[key][1].grid(row=row+1, column=1)


    # ---------------
    #   Next button
    # ---------------
    next_button = tkinter.Button(
        event_details_frame,
        text="Next Event",
        command=next_event
    )
    next_button.grid(row=100, column=1, sticky="nsew")


    # ----------------------
    #   Back button events
    # ----------------------
    back_button = tkinter.Button(
        event_details_frame,
        text="Previous event",
        command=back_event
    )
    back_button.grid(row=100, column=0, sticky="nsew")


    # ---------------
    #   Save button
    # ---------------
    save_button = tkinter.Button(
        event_details_frame,
        text="Save",
        command=save
    )
    save_button.grid(row=110, column=0, columnspan=2, sticky="nsew")


    # -----------------------
    #   Error message label
    # -----------------------
    error_message = tkinter.Label(view_events_window, text="", fg="red", font=("comic sans", 14))
    error_message.grid(row=3, column=0, columnspan=7)


    # ---------------
    #   Back button
    # ---------------
    back_button_main = tkinter.Button(
        view_events_window,
        text="Back",
        command=lambda: main()
    )
    back_button_main.grid(row=5, column=0, columnspan=7, sticky="nsew")


    # -----------
    #   Spacing
    # -----------
    spacing1 = tkinter.Label(
        view_events_window,
        width=10
    )
    spacing1.grid(row=0, column=0)

    spacing2 = tkinter.Label(
        view_events_window,
        width=10
    )
    spacing2.grid(row=0, column=6)


    # -------------------------------
    #   view_events_window mainloop
    # -------------------------------
    display_event(None)
    cal.grid(row=0, column=2, columnspan=2)
    event_details_frame.grid(row=0, column=4)
    view_events_window.mainloop()


if __name__ == "__main__":
    main()