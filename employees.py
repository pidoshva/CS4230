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

# Composite: Supervisor class (can have subordinates)
class Supervisor(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.subordinates = []  # List to store subordinate workers
        self.maxSubordinates = 5

    def add(self):
        pass  # Logic to add subordinates to be implemented later

    def remove(self):
        pass  # Logic to remove subordinates to be implemented later

    def show_details(self):
        pass  # Display logic to be implemented later

# Composite: VicePresident class (can have supervisors)
class VicePresident(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.subordinates = []  # List to store subordinate supervisors
        self.maxSubordinates = 3

    def add(self):
        pass  # Logic to add subordinates to be implemented later

    def remove(self):
        pass  # Logic to remove subordinates to be implemented later

    def show_details(self):
        pass  # Display logic to be implemented later

# Composite: President class (can have vice presidents)
class President(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.subordinates = []  # List to store subordinate vice presidents
        self.maxSubordinates = 2  # List to store subordinate workers

    def add(self):
        pass  # Logic to add subordinates to be implemented later

    def remove(self):
        pass  # Logic to remove subordinates to be implemented later

    def show_details(self):
        pass  # Display logic to be implemented later
