from abc import ABC, abstractmethod

# Component: The base class for all employees
class Employee(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def show_details(self):
        pass

# Leaf: Worker class
class Worker(Employee):
    def show_details(self):
        pass  # Display logic to be implemented later

    def quit(self):
        pass  # logic to be implemented later

# Composite: Supervisor class (can have subordinates)
class Supervisor(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.subordinates = []  # List to store subordinate workers
        self.maxSubordinates = 5

    def hire_employee(self):
        pass  # Logic for hiring to be implemented later

    def layoff_employee(self):
        pass  # Logic for laying off to be implemented later

    def fire_employee(self):
        pass  # Logic for firing to be implemented later

    def quit(self):
        pass  # logic to be implemented later

    def show_details(self):
        pass  # Display logic to be implemented later

# Composite: VicePresident class (can have supervisors)
class VicePresident(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.subordinates = []  # List to store subordinate supervisors
        self.maxSubordinates = 3

    def promote_employee(self):
        pass  # Logic for promoting to be implemented later

    def layoff_employee(self):
        pass  # Logic for laying off to be implemented later

    def fire_employee(self):
        pass  # Logic for firing to be implemented later
    
    def transfer_employee(self):
        pass  # Logic for transferring to be implemented later

    def quit(self):
        pass  # logic to be implemented later

    def show_details(self):
        pass  # Display logic to be implemented later

# Composite: President class (can have vice presidents)
class President(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.subordinates = []  # List to store subordinate vice presidents
        self.maxSubordinates = 2  # List to store subordinate workers

    def promote_employee(self):
        pass  # Logic for promoting to be implemented later
    
    def layoff_employee(self):
        pass  # Logic for laying off to be implemented later

    def fire_employee(self):
        pass  # Logic for firing to be implemented later

    def show_details(self):
        pass  # Display logic to be implemented later