# db_interface.py

from abc import ABC, abstractmethod


class IDatabase(ABC):

    @abstractmethod
    def connect(self):
        """connect database"""

    # @abstractmethod
    # def disconnect(self):
    #     """disconnect database"""

    # CARS
    @abstractmethod
    def create_vehicle(self):
        """creates record that are saved into the database"""

    @abstractmethod
    def read_vehicles(self):
        """views record in database"""

    @abstractmethod
    def update_vehicle(self):
        """updates record in database"""

    @abstractmethod
    def delete_vehicle(self):
        """deletes record from database"""

    # BATTERIES
    @abstractmethod
    def create_batteries(self):
        """creates record that are saved into the database"""

    @abstractmethod
    def read_batteries(self):
        """views record in database"""

    @abstractmethod
    def update_batteries(self):
        """updates record in database"""

    @abstractmethod
    def delete_batteries(self):
        """deletes record from database"""

    # CHARGES
    @abstractmethod
    def create_charges(self):
        """creates record that are saved into the database"""

    @abstractmethod
    def read_charges(self):
        """views record in database"""

    @abstractmethod
    def update_charges(self):
        """updates record in database"""

    @abstractmethod
    def delete_charges(self):
        """deletes record from database"""

    # CLINIC
    @abstractmethod
    def create_clinic(self):
        """creates record that are saved into the database"""

    @abstractmethod
    def read_clinic(self):
        """views record in database"""

    @abstractmethod
    def update_clinic(self):
        """updates record in database"""

    @abstractmethod
    def delete_clinic(self):
        """deletes record from database"""

    # PAYMENT
    @abstractmethod
    def create_payment(self):
        """creates record that are saved into the database"""

    @abstractmethod
    def read_payment(self):
        """views record in database"""

    @abstractmethod
    def update_payment(self):
        """updates record in database"""

    @abstractmethod
    def delete_payment(self):
        """deletes record from database"""

    @abstractmethod
    def signup(self):
        """signup user"""

    @abstractmethod
    def login(self):
        """login user"""