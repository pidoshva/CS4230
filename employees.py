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
    def __init__(self, name):
        super().__init__(name)
        self.overseer = None

    def setOverseer(self, overseer):
        self.overseer = overseer

    def show_details(self):
        print(f"Worker: {self.name}")
        pass  # Display logic to be implemented later

    def quit(self):
        self.overseer.fire_employee(self)

# Composite: Supervisor class (can have subordinates)
class Supervisor(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.subordinates = []  # List to store subordinate workers
        self.maxSubordinates = 5
        self.overseer = None

    def setOverseer(self, overseer):
        self.overseer = overseer

    def hire_employee(self, worker):
        if worker.name == "":
            self.subordinates.append(worker)
        elif len(self.subordinates) < self.maxSubordinates:
            self.subordinates.append(worker)
            worker.setOverseer(self)
        else:
            print(str.format("Unable to hire new workers. Max workers for Supervisor {} already reached",self.name))

    def layoff_employee(self, name):
        pass  # Logic for laying off to be implemented later

    def fire_employee(self, worker):
        self.subordinates.remove(worker)

    def quit(self):
        self.overseer.fire_employee(self)

    def show_details(self):
        print(f"Supervisor: {self.name}")
        for subordinate in self.subordinates:
            subordinate.show_details()
        pass  # Display logic to be implemented later

# Composite: VicePresident class (can have supervisors)
class VicePresident(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.subordinates = []  # List to store subordinate supervisors
        self.maxSubordinates = 3
        self.overseer = None

    def setOverseer(self, overseer):
        self.overseer = overseer

    def promote_employee(self, name):
        pass  # Logic for promoting to be implemented later

    def hire_employee(self, supervisor):
        if supervisor.name == "":
            self.subordinates.append(supervisor)
        elif len(self.subordinates) < self.maxSubordinates:
            self.subordinates.append(supervisor)
            supervisor.setOverseer(self)
        else:
            print(str.format("Unable to hire new supervisors. Max workers for Vice President {} already reached", self.name))

    def layoff_employee(self):
        pass  # Logic for laying off to be implemented later

    def fire_employee(self, supervisor):
        self.subordinates.remove(supervisor)
    
    def transfer_employee(self, name):
        pass  # Logic for transferring to be implemented later

    def quit(self):
        self.overseer.fire_employee(self)

    def show_details(self):
        print(f"Vice President: {self.name}")
        for subordinate in self.subordinates:
            subordinate.show_details()
        pass  # Display logic to be implemented later

# Composite: President class (can have vice presidents)
class President(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.subordinates = []  # List to store subordinate vice presidents
        self.maxSubordinates = 2  # List to store subordinate workers
        self.overseer = None

    def setOverseer(self, overseer):
        self.overseer = overseer

    def promote_employee(self, name):
        pass  # Logic for promoting to be implemented later

    def hire_employee(self, vicePresident):
        if vicePresident.name == "":
            self.subordinates.append(vicePresident)
        elif len(self.subordinates) < self.maxSubordinates:
            self.subordinates.append(vicePresident)
            vicePresident.setOverseer(self)
        else:
            print(str.format("Unable to hire new Vice Presidents. Max workers for President {} already reached",self.name))
    
    def layoff_employee(self, name):
        pass  # Logic for laying off to be implemented later

    def fire_employee(self, vicePresident):
        self.subordinates.remove(vicePresident)

    def show_details(self):
        print(f"President: {self.name}")
        for subordinate in self.subordinates:
            subordinate.show_details()
        pass  # Display logic to be implemented later
