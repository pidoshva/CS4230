from abc import ABC, abstractmethod

class Employee(ABC): #abstract
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def hire(self, employee):
        pass

    @abstractmethod
    def fire(self, employee):
        pass

    @abstractmethod
    def display(self, indent=0):
        pass

    @abstractmethod
    def promote(self, employee):
        pass

class Worker(Employee):
    def hire(self, employee):
        raise Exception("Cannot hire under a worker")

    def fire(self, employee):
        raise Exception("Cannot fire under a worker")

    def display(self, indent=0):
        print(" " * indent + f"Worker: {self.name}")

    def promote(self, employee):
        raise Exception("Cannot promote a worker")

class Supervisor(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.workers = []  # A supervisor can manage up to 5 workers

    def hire(self, worker):
        for w in self.workers:
            if w.name == worker.name:
                print(f"Worker {worker.name} already exists under Supervisor {self.name}")
                return
        if len(self.workers) < 5:
            self.workers.append(worker)
        else:
            print(f"No space to hire under Supervisor {self.name}")

    def fire(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)
        else:
            print(f"{worker.name} is not under Supervisor {self.name}")

    def display(self, indent=0):
        print(" " * indent + f"Supervisor: {self.name}")
        for worker in self.workers:
            worker.display(indent + 2)

    def promote(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)
            promoted_supervisor = Supervisor(worker.name)
            print(f"Promoted {worker.name} to Supervisor.")
            return promoted_supervisor
        else:
            print(f"Cannot promote {worker.name}, they are not under Supervisor {self.name}.")
            return None

    def handle_firing(self, vp):
        """Handle Supervisor firing - promote a worker"""
        if len(self.workers) > 0:
            new_supervisor = self.workers.pop(0)
            vp.hire(Supervisor(new_supervisor.name))
            print(f"Promoted Worker {new_supervisor.name} to Supervisor.")
        else:
            print(f"No Workers left to promote under Supervisor {self.name}")

class VicePresident(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.supervisors = []  # A VP can manage up to 3 supervisors

    def hire(self, supervisor):
        if len(self.supervisors) < 3:
            self.supervisors.append(supervisor)
        else:
            print(f"No space to hire under Vice President {self.name}")

    def fire(self, supervisor):
        if supervisor in self.supervisors:
            self.supervisors.remove(supervisor)
        else:
            print(f"{supervisor.name} is not under Vice President {self.name}")

    def display(self, indent=0):
        print(" " * indent + f"Vice President: {self.name}")
        for supervisor in self.supervisors:
            supervisor.display(indent + 2)

    def promote(self, supervisor):
        if supervisor in self.supervisors:
            self.supervisors.remove(supervisor)
            promoted_vp = VicePresident(supervisor.name)
            print(f"Promoted {supervisor.name} to Vice President.")
            return promoted_vp
        else:
            print(f"Cannot promote {supervisor.name}, they are not under Vice President {self.name}.")
            return None

    def handle_firing(self, president):
        """Handle VP firing - promote a supervisor"""
        if len(self.supervisors) > 0:
            new_vp = self.supervisors.pop(0)
            president.hire(VicePresident(new_vp.name))
            print(f"Promoted Supervisor {new_vp.name} to Vice President.")
        else:
            print(f"No Supervisors left to promote under Vice President {self.name}")

class President(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.vice_presidents = []  # The president can manage up to 2 VPs

    def hire(self, vice_president):
        if len(self.vice_presidents) < 2:
            self.vice_presidents.append(vice_president)
        else:
            print(f"No space to hire under President {self.name}")

    def fire(self, vice_president):
        if vice_president in self.vice_presidents:
            vice_president.handle_firing(self)  # Promote one of their supervisors
            self.vice_presidents.remove(vice_president)
        else:
            print(f"{vice_president.name} is not under President {self.name}")

    def display(self, indent=0):
        print(" " * indent + f"President: {self.name}")
        for vp in self.vice_presidents:
            vp.display(indent + 2)

    def promote(self, vp):
        raise Exception("Cannot promote a Vice President to President!")
