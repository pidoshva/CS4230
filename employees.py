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
    def quit(self,overseer):
        pass

    @abstractmethod
    def display(self, indent=0):
        pass

    @abstractmethod
    def promote(self, employee, overseer):
        pass

class Worker(Employee):
    def hire(self, employee):
        raise Exception("Cannot hire under a worker")

    def fire(self, employee):
        raise Exception("Cannot fire under a worker")

    def quit(self, supervisor):
        supervisor.fire(self)

    def display(self, indent=0):
        print(" " * indent + f"Worker: {self.name}")

    def promote(self, employee, overseer):
        raise Exception("Cannot promote under a worker")

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
            print(f"Hired worker {worker.name} under Supervisor {self.name}")
        else:
            print(f"No space to hire under Supervisor {self.name}")

    def fire(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)
        else:
            print(f"{worker.name} is not under Supervisor {self.name}")

    def quit(self, vp):
        vp.fire(self)

    def display(self, indent=0):
        print(" " * indent + f"Supervisor: {self.name}")
        for worker in self.workers:
            worker.display(indent + 2)

    def promote(self, employee, overseer):
        """Promotes a worker to supervisor after supervisor is promoted to vp"""
        if len(self.workers) > 0:
            worker_to_promote = self.workers.pop(0)
            new_supervisor = Supervisor(worker_to_promote.name)
            for current_worker in self.workers:
                new_supervisor.hire(current_worker)
            return new_supervisor
        return None

    def remove_employee(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)

class VicePresident(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.supervisors = []  # A VP can manage up to 3 supervisors

    def hire(self, supervisor):
        if len(self.supervisors) < 3:
            self.supervisors.append(supervisor)
            print(f"Hired Supervisor {supervisor.name} under Vice President {self.name}")
        else:
            print(f"No space to hire under Vice President {self.name}")

    def fire(self, supervisor):
        if supervisor in self.supervisors:
            self.supervisors.remove(supervisor)
        else:
            print(f"{supervisor.name} is not under Vice President {self.name}")

    def quit(self, president):
        president.fire(self)

    def display(self, indent=0):
        print(" " * indent + f"Vice President: {self.name}")
        for supervisor in self.supervisors:
            supervisor.display(indent + 2)

    def promote(self, worker, supervisor):
        if len(self.supervisors) < 3:
            new_supervisor = Supervisor(worker.name)
            supervisor.remove_employee(worker)
            self.supervisors.append(new_supervisor)
            print(f"Promoted Worker {new_supervisor.name} to Supervisor under Vice President {self.name}")

        else:
            print(f"No space to promote under Vice President {self.name}")

    def handle_promote(self, supervisor):
        """Handle supervisor promotion to vp - promote a new supervisor"""
        if supervisor in self.supervisors:
            new_supervisor = supervisor.promote(None, None)
            self.supervisors.remove(supervisor)
            if new_supervisor:
                self.supervisors.append(new_supervisor)


class President(Employee):
    def __init__(self, name):
        super().__init__(name)
        self.vice_presidents = []  # The president can manage up to 2 VPs

    def hire(self, vice_president):
        if len(self.vice_presidents) < 2:
            self.vice_presidents.append(vice_president)
            print(f"Hired Vice President {vice_president.name} under President {self.name}")
        else:
            print(f"No space to hire under President {self.name}")

    def fire(self, vice_president):
        if vice_president in self.vice_presidents:
            self.vice_presidents.remove(vice_president)
        else:
            print(f"{vice_president.name} is not under President {self.name}")

    def quit(self, overseer):
        raise Exception("President can't quit")

    def display(self, indent=0):
        print(" " * indent + f"President: {self.name}")
        for vp in self.vice_presidents:
            vp.display(indent + 2)

    def promote(self, supervisor, vp):
        if len(self.vice_presidents) < 2:
            new_vp = VicePresident(supervisor.name)
            vp.handle_promote(supervisor)
            self.vice_presidents.append(new_vp)
            print(f"Promoted Supervisor {new_vp.name} to Vice President under President {self.name}")

        else:
            print(f"No space to promote under President {self.name}")
