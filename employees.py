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
        found = False
        layoff = None
        for worker in self.subordinates:
            if worker.name == name:
                found = True
                layoff = self.subordinates.pop(worker)
            
        if not found:
            print(str.format("Worker {} not found", name))

        overseer = self.overseer
        while overseer is not None:
            for supervisor in overseer.subordinates:
                if isinstance(supervisor, Supervisor) and supervisor.name != self.name:
                    if len(supervisor.subordinates) < supervisor.maxSubordinates:
                        supervisor.subordinates.append(layoff)
                        layoff.setOverseer(supervisor)
                        return
                elif isinstance(supervisor, VicePresident):
                    for worker in supervisor.subordinates:
                        if len(worker.subordinates) < worker.maxSubordinates:
                            worker.subordinates.append(layoff)
                            layoff.setOverseer(worker)
                            return
            overseer = overseer.overseer

    def fire_employee(self, worker):
        self.subordinates.remove(worker)

    def quit(self):
        self.overseer.fire_employee(self)

    def show_details(self):
        if self.name != "":
            print(f"Supervisor: {self.name}")
            for subordinate in self.subordinates:
                subordinate.show_details()
        else:
            for subordinate in self.subordinates:
                subordinate.show_details()

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
        vacancy = False
        if len(self.subordinates) < self.maxSubordinates:
            vacancy = True
        else:
            for supervisor in self.subordinates:
                if supervisor.name == "":
                    vacancy = True

        if vacancy:
            for supervisor in self.subordinates:
                for worker in supervisor.subordinates:
                    if worker.name == name:
                        supervisor.subordinates.remove(worker)
                        self.hire_employee(worker)
            
        pass  # Logic for promoting to be implemented later

    def hire_employee(self, supervisor):
        if supervisor.name == "":
            self.subordinates.append(supervisor)
            return
        elif len(self.subordinates) < self.maxSubordinates:
            self.subordinates.append(supervisor)
            supervisor.setOverseer(self)
            return
        else:
            for supervisor in self.subordinates:
                if supervisor.name == "":
                    supervisor.name = supervisor.name
                    return
            print(str.format("Unable to hire new supervisors. Max workers for Vice President {} already reached", self.name))

    def layoff_employee(self, name):
        found = False
        layoff = None
        for supervisor in self.subordinates:
            if supervisor.name == name:
                found = True
                layoff = Supervisor(name)
                supervisor.name = ""
            
        if not found:
            print(str.format("Worker {} not found", name))

        overseer = self.overseer
        while overseer is not None:
            for vp in overseer.subordinates:
                if vp.name != self.name:
                    if len(vp.subordinates) < vp.maxSubordinates:
                        vp.subordinates.append(layoff)
                        layoff.setOverseer(vp)
                        return
                    else:
                        for supervisor in vp.subordinates:
                            if supervisor.name == "":  # If supervisor is not hired
                                supervisor.name = layoff.name
                                return
            overseer = overseer.overseer

    def fire_employee(self, supervisor):
        for person in self.subordinates:
            if person.name == supervisor.name:
                person.name = ""
                return
    
    def transfer_employee(self, name):
        transfer = None
        found = False
        pass  # Logic for transferring to be implemented later

    def quit(self):
        self.overseer.fire_employee(self)

    def show_details(self):
        if self.name != "":
            print(f"Vice President: {self.name}")
            for subordinate in self.subordinates:
                subordinate.show_details()
        else:
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
        for person in self.subordinates:
            if person.name == vicePresident.name:
                person.name = ""
                return

    def show_details(self):
        print(f"President: {self.name}")
        for subordinate in self.subordinates:
            subordinate.show_details()
        pass  # Display logic to be implemented later
