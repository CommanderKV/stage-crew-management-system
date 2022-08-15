import tkinter
from events import Events
from datetime import datetime
from tkcalendar import Calendar
import json


def main():
    global EVENTS, inputs
    events_connection = Events()
    current_event = 0


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
                        cal.calevent_create(time, details, "Message")
        
        cal.tag_config("Message", background="orange", foreground="black")


    view_events_window = tkinter.Tk()
    EVENTS = [0, 1]

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
                        width=30
                    )
                ]
            
            inputs[key][0].grid(row=row+1, column=0)
            inputs[key][1].grid(row=row+1, column=1)


    """
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
    """

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



main()