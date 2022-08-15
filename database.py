import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db




class Database:

    def __init__(self):
        self.cred = credentials.Certificate(
            os.path.join(
                os.getcwd(), 
                "stage-crew-event-manager-firebase-adminsdk-ed2pg-b047e32b38.json"
            )
        )
        self.app = firebase_admin.initialize_app(
            self.cred, 
            {
                "databaseURL": "https://stage-crew-event-manager-default-rtdb.firebaseio.com"
            }
        )
        

        self.path = "/"
        self.db = firebase_db.reference(self.path)

    
    def set_path(self, path: str) -> bool:
        """
        Set path in database

        Args:
            path (string): Path in database
        """
        try:
            self.path = path
            self.db = firebase_db.reference(self.path)
            return True
        
        except:
            return False


    def get_path(self) -> str:
        """
        Get path in database
            
        Returns:
            string: Path in database
        """
        return self.path


    def get_db_data(self) -> dict:
        """
        Get data from database

        Returns:
            dictionary: database data
        """
        return self.db.get()


    def update_db(self, data: dict) -> bool:
        """
        Set data in database

        Args:
            data (dictionary): Data to be added to database

        Returns:
            bool: Did process succeed?
        """
        for _ in range(5):
            self.db.transaction(lambda x: data if x == self.db.get() else x)
            if self.get_db_data() == data:
                return True
        
        else:
            return False


    def append_db(self, data: dict) -> bool:
        """
        Append data to database
        
        Args:
            data (dictionary): Data to be added to database
        """
        try:
            self.db.push().set(data)
            return True
        
        except:
            return False


    def remove_db(self) -> bool:
        """
        Remove data from database
        """
        try:
            self.db.delete()
            return True
        
        except:
            return False


if __name__ == "__main__":
    db = Database()
    print(db.db.get())
    