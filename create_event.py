import tkinter
from events import Events
from datetime import datetime

def main():

    def back():
        create_event_window.destroy()
        raise Exception("Back")

    def submit_event():

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
                        create_event_error_message.config(text="Fill in all fields", fg="red")
                        break

                    value = str(events_connection.template[key]).upper()
                    if str(entry).upper() == str(value).upper():
                        # entry is same as default
                        create_event_error_message.config(text="Enter a different value for {}".format(label), fg="red")
                        break


                    elif "TIME" in str(label).upper():
                        if len(entry) != 5:
                            # entry is not a time
                            create_event_error_message.config(text="Enter a valid time for {}".format(label), fg="red")
                            break

                        elif entry[2] != ":":
                            # entry is not a time
                            create_event_error_message.config(text="Enter a valid time for {}".format(label), fg="red")
                            break

                        elif is_number(entry[0:2]) == False or is_number(entry[3:5]) == False:
                            # entry is not a time
                            create_event_error_message.config(text="Enter a valid time for {}".format(label), fg="red")
                            break


                    elif "DATE" in str(label).upper():
                        if len(entry) != 10:
                            # entry is not a date
                            create_event_error_message.config(text="Enter a valid date for {} format: yyyy-mm-dd".format(label), fg="red")
                            break

                        elif entry[4] != "-" or entry[7] != "-":
                            # entry is not a date
                            create_event_error_message.config(text="Enter a valid date for {} format: yyyy-mm-dd".format(label), fg="red")
                            break

                        elif is_number(entry[0:4]) == False or is_number(entry[5:7]) == False or is_number(entry[8:10]) == False:
                            # entry is not a date
                            create_event_error_message.config(text="Enter a valid date for {} format: yyyy-mm-dd".format(label), fg="red")
                            break

                        elif datetime.strptime(entry, "%Y-%m-%d") < datetime.now():
                            # entry is not a date
                            create_event_error_message.config(text="{} must be in the future".format(label), fg="red")
                            break

                    
                    elif "contact" in label:
                        email = entry.replace(" ", "")
                        if "@" not in email:
                            # entry is not an email
                            create_event_error_message.config(text="Enter a valid email for {}".format(label), fg="red")
                            break

                        elif "." not in email:
                            # entry is not an email
                            create_event_error_message.config(text="Enter a valid email for {}".format(label), fg="red")
                            break

                        elif "tdsb.on.ca" not in email:
                            # entry is not an email
                            create_event_error_message.config(text="Enter a valid email for {}".format(label), fg="red")
                            break

                        elif len(email) < 15:
                            # entry is not an email
                            create_event_error_message.config(text="Enter a valid email for {}".format(label), fg="red")
                            break


        if create_event_error_message["text"] == "":
            event = {}
            for key in inputs:
                if key != "version":
                    if str(events_connection.template[key]).upper() == "TRUE OR FALSE":
                        event[key] = inputs[key][2].get()

                    else:
                        event[key] = inputs[key][1].get()
            
            event["version"] = events_connection.template["version"]

            # no errors
            if events_connection.add_event(event):
                back()
            
            else:
                create_event_error_message.config(text="Error adding event", fg="red")
        
        else:
            create_event_error_message.after(9000, lambda: create_event_error_message.config(text="", fg="black"))






    create_event_window = tkinter.Tk()
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


    # ---------------------------
    #   Create text input frame
    # ---------------------------
    text_input_frame = tkinter.Frame(mainframe)

    # --------------------------
    #   Setting text font size
    # --------------------------
    text_font_size = 18


    # ------------------------------------------
    #   Dynamically creating text input fields
    # ------------------------------------------
    events_connection = Events()
    event_template = events_connection.get_event_struct()

    inputs = {}
    for row, key in enumerate(event_template.keys()):
        if key != "version":
            if str(event_template[key]).upper() == "TRUE OR FALSE":
                checkbutton_value = tkinter.BooleanVar()
                inputs[key] = [
                    tkinter.Label(
                        text_input_frame,
                        text=str(key)[1:].capitalize(),
                        font=("Comic Sans MS", text_font_size, "bold"),
                        width=20
                    ),
                    tkinter.Checkbutton(
                        text_input_frame,
                        variable=checkbutton_value,
                        onvalue=True,
                        offvalue=False
                    ),
                    checkbutton_value
                ]
            else:
                inputs[key] = [
                    tkinter.Label(
                        text_input_frame, 
                        text=str(key)[1:].capitalize(),
                        font=("Comic Sans MS", text_font_size, "bold"),
                        width=20
                    ),
                    tkinter.Entry(
                        text_input_frame,
                        width=50
                    )
                ]
            
            inputs[key][0].grid(row=row, column=0)

            if str(event_template[key]).upper() != "TRUE OR FALSE":
                inputs[key][1].insert(0, str(event_template[key]).capitalize())

            inputs[key][1].grid(row=row, column=1)


    # -----------------
    #   Error message
    # -----------------
    create_event_error_message = tkinter.Label(
        create_event_window,
        text="",
        font=("Comic Sans MS", text_font_size, "bold"),
        fg="red"
    )
    create_event_error_message.grid(row=1, column=0, columnspan=4, sticky="nsew")


    # -----------------
    #   Submit button
    # -----------------
    submit_button = tkinter.Button(
        create_event_window,
        text="Submit",
        command=submit_event,
        font=("Comic Sans MS", text_font_size),
        height=1
    )
    submit_button.grid(row=2, column=0, columnspan=4, sticky="nsew")


    # ---------------
    #   Back button
    # ---------------
    back_button = tkinter.Button(
        create_event_window,
        text="Back",
        command=back,
        font=("Comic Sans MS", text_font_size),
        height=1
    )
    back_button.grid(row=3, column=0, columnspan=4, sticky="nsew")


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


if __name__ == "__main__":
    main()