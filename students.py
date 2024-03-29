from database import Database

class Students(Database):

    def __init__(self):
        """
        Create an outline and conection 
        used to connect to the database.
        """
        super().__init__()
        self.path = "/"
        self.set_path(self.path)
        self.get_student_struct()


    def get_student_struct(self) -> dict:
        """
        Get student structure from database
        
        Returns:
            dictionary: student structure
        """
        self.set_path("/Version/Students/template")
        template = self.get_db_data()
    
        self.set_path("/Version/Students/")
        version = self.get_db_data()["v"]
    
        template["version"] = int(version)
        self.template = template
        return template


    def get_students(self) -> dict:
        """
        Get students from database
        
        Returns:
            dictionary: students
        """
        self.set_path("/Students/")
        return self.get_db_data()


    def get_student(self, student_id: str) -> False or dict:
        """
        Get student from database
        
        Args:
            student_id (string): Student id / random id generated by database
            
        Returns:
            dictionary: student
        """
        if self.get_students().keys().__contains__(student_id):
            self.set_path("/Students/" + student_id)
            return self.get_db_data()
        
        else:
            return False


    def get_student_by_email(self, email: str) -> False or dict:
        """
        Get student from database by email
        
        Args:
            email (string): Email of student
            
        Returns:
            dictionary: student
        """
        students = self.get_students()
        for student in students:
            if students[student]["email"] == email:
                return students[student]

        return False


    def get_student_by_name(self, name: str) -> False or dict:
        """
        Get student from database by name
        
        Args:
            name (string): Name of student
            
        Returns:
            dictionary: student
        """
        students = self.get_students()
        for student in students:
            if students[student]["name"] == name:
                return students[student]

        return False


    def get_students_by_grade(self) -> dict:
        """
        Get students from database by grade
        
        Args:
            grade (string): Grade of student
            
        Returns:
            dictionary: students
        """
        students = self.get_students()
        students_by_grade = {}
        for key, student in students.items():
            if int(student["dgrade"]) not in students_by_grade.keys():
                students_by_grade[student["dgrade"]] = {key: student}
            
            else:
                students_by_grade[student["dgrade"]].update({key: student})

        return students_by_grade


    def add_student(self, student: dict) -> bool:
        """
        Add student to database
        
        Args:
            student (dictionary): Student to be added to database
            
        Returns:
            bool: Did process succeed?
        """
        if self.get_student_by_email(student["cemail"]) == False:
            student = self.check_data(student)
            self.set_path("/Students/")
            self.append_db(student)
            return True
        
        else:
            return False


    def update_student(self, student_id: str, student: dict) -> bool:
        """
        Update student in database
        
        Args:
            student_id (string): Student id / random id generated by database
            student (dictionary): Student to be updated
            
        Returns:
            bool: Did process succeed?
        """
        if self.get_student(student_id) != False:
            student = self.check_data(student)
            self.set_path("/Students/" + student_id)
            self.update_db(student)
            return True
        
        else:
            return False


    def remove_student(self, student_id: str) -> bool:
        """
        Remove student from database
        
        Args:
            student_id (string): Student id / random id generated by database
            
        Returns:
            bool: Did process succeed?
        """
        if self.get_student(student_id) != False:
            self.set_path("/Students/" + student_id)
            if self.remove_db():
                return True
            
            else:
                return False
        
        else:
            return False


    def check_data(self, student: dict) -> dict:
        """
        Check data of student
        
        Args:
            student (dictionary): Student to be checked
            
        Returns:
            dictionary: Student with checked data
        """
        data_updated = student

        self.get_student_struct()

        if not self._check_version(student["version"]):
            if student["version"] > self.template["version"]:
                # self template out of date
                new_struct = self.template.copy()
                for key in student.keys():
                    if key not in new_struct.keys():
                        new_struct[key] = ""
                
                # Update the database with new structure
                self.set_path("/Version/Events/")
                self.update_db(new_struct)
                self.set_path("/Version/")
                version_data = self.get_db_data()
                version_data["v"] = int(student["version"])
                self.update_db(version_data)
                self.get_student_struct()

                data_updated = student
                
            elif student["version"] < self.template["version"]:
                # student template out of date
                updated_student = self.template.copy()
                updated_student.update(student)

        return data_updated


    def _check_version(self, version: int) -> bool:
        """
        Check version of student structure
        
        Args:
            version (int): Version of student structure
            
        Returns:
            bool: Did process succeed?
        """
        if version == self.template["version"]:
            return True
        
        else:
            return False


    def _check_template(self, data: dict) -> bool:
        """
        Check template of student structure
        
        Args:
            data (dictionary): Template of student structure
            
        Returns:
            bool: Did process succeed?
        """
        for key in self.template.keys():
            if key not in data.keys():
                return False
        
        return True



if __name__ == "__main__":
    students = Students()
    print(students.get_students())
    print(students.get_students_by_grade())


