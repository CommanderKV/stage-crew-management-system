import tkinter
from students import Students


def main():

    def back():
        add_student_window.destroy()
        raise Exception("Back")

    def submit_student():
        def is_number(string: str) -> bool:
            numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            for char in string:
                if char not in numbers:
                    return False
            
            return True

        
        for key in inputs.keys():
            if key != "version":
                item = inputs[key]
                label = item[0].cget("text")
                entry = item[1]

                if str(entry.get()) == "":
                    # entry is empty
                    error_label_add_students.config(text="Fill in all fields", fg="red")
                    break

                value = str(students_connection.template[key]).upper()
                if str(entry.get()).upper() != value:
                    if is_number(value):
                        if not is_number(entry.get()):
                            # entry is not a number
                            error_label_add_students.config(text="Enter a number for {}".format(label), fg="red")
                            break

                        elif int(entry.get()) < int(value):
                            # entry is less than value
                            error_label_add_students.config(text="Enter a number greater than {} for {}".format(value, label), fg="red")
                            break

                        elif label == "Grade":
                            if int(entry.get()) > 12:
                                # entry is greater than 12
                                error_label_add_students.config(text="Enter a number less than 13 for {}".format(label), fg="red")
                                break

                            elif int(entry.get()) < 9:
                                # entry is less than 9
                                error_label_add_students.config(text="Enter a number greater than 8 for {}".format(label), fg="red")
                                break
                    
                    elif label == "Email":
                        email = entry.get().replace(" ", "")
                        if "@" not in email:
                            # entry is not an email
                            error_label_add_students.config(text="Enter a valid email for {}".format(label), fg="red")
                            break

                        elif "." not in email:
                            # entry is not an email
                            error_label_add_students.config(text="Enter a valid email for {}".format(label), fg="red")
                            break

                        elif "tdsb.on.ca" not in email:
                            # entry is not an email
                            error_label_add_students.config(text="Enter a valid email for {}".format(label), fg="red")
                            break

                        elif len(email) < 15:
                            # entry is not an email
                            error_label_add_students.config(text="Enter a valid email for {}".format(label), fg="red")
                            break
                
                elif str(entry.get()).upper() == value:
                    # entry is the same as value
                    error_label_add_students.config(text="Change default value for {}".format(label), fg="red")
                    break


        # ----------------------------------------
        #   If there is no error attmept adding. 
        #       Otherwise throw that error.
        # ----------------------------------------
        if error_label_add_students.cget("text") == "":
            # no error
            student = student_template.copy()
            for key, item in inputs.items():
                student[key] = item[1].get()

            if students_connection.add_student(student):
                back()

            else:
                error_label_add_students.config(text="Error adding student", fg="red")
                error_label_add_students.after(9000, lambda: error_label_add_students.config(text="", fg="black"))
        
        else:
            # error
            error_label_add_students.after(9000, lambda: error_label_add_students.config(text="", fg="black"))

        students_connection.get_student_struct()


    add_student_window = tkinter.Tk()


    # ------------------------
    #   Student input fields
    # ------------------------
    student_input_frame = tkinter.Frame(add_student_window)


    students_connection = Students()
    student_template = students_connection.get_student_struct()

    inputs = {}
    for row, key in enumerate(student_template.keys()):
        if key != "version":
            inputs[key] = [
                tkinter.Label(
                    student_input_frame, 
                    text=str(key)[1:].capitalize(),
                    font=("Comic Sans MS", 12, "bold")
                ),
                tkinter.Entry(
                    student_input_frame,
                    width=50
                )
            ]
            inputs[key][0].grid(row=row, column=0)

            inputs[key][1].insert(0, str(student_template[key]).capitalize())
            inputs[key][1].grid(row=row, column=1)



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


    # ---------------------------------
    #   Button for submitting student
    # ---------------------------------
    submit_button = tkinter.Button(
        add_student_window,
        text="Submit",
        command=submit_student
    )
    submit_button.grid(row=2, column=0, columnspan=2, sticky="nsew")


    # ---------------
    #   Back button
    # ---------------
    back_button = tkinter.Button(
        add_student_window,
        text="Back",
        command=back
    )
    back_button.grid(row=3, column=0, sticky="nsew")


    # ----------------
    #   Start window
    # ----------------
    student_input_frame.grid(row=0, column=0)
    add_student_window.mainloop()


if __name__ == "__main__":
    main()