from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def hire(self, employee):
        pass

    @abstractmethod
    def fire(self, employee):
        pass

    @abstractmethod
    def quit(self, overseer):
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
        if len(self.workers) < 5:
            self.workers.append(worker)
            print(f"Hired worker {worker.name} under Supervisor {self.name}")
        else:
            print(f"No space to hire under Supervisor {self.name}")

    def fire(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)
            print(f"Fired worker {worker.name} from Supervisor {self.name}")
        else:
            print(f"{worker.name} is not under Supervisor {self.name}")

    def quit(self, vp):
        vp.fire(self)

    def display(self, indent=0):
        print(" " * indent + f"Supervisor: {self.name}")
        for worker in self.workers:
            worker.display(indent + 2)

    def promote(self, employee, overseer):
        """Promote the first worker under this supervisor to a supervisor"""
        if len(self.workers) > 0:
            promoted_worker = self.workers.pop(0)
            new_supervisor = Supervisor(promoted_worker.name)
            new_supervisor.workers = self.workers
            print(f"Promoted Worker {promoted_worker.name} to Supervisor.")
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
            if supervisor.workers:
                # Promote the first worker to Supervisor
                promoted_worker = supervisor.workers.pop(0)
                new_supervisor = Supervisor(promoted_worker.name)

                # Transfer remaining workers to the new supervisor
                new_supervisor.workers = supervisor.workers
                supervisor.workers = []

                # Replace the old supervisor with the new one
                self.supervisors[self.supervisors.index(supervisor)] = new_supervisor
                print(f"Promoted Worker {promoted_worker.name} to Supervisor and replaced {supervisor.name}.")
            else:
                # If no workers, simply remove the supervisor
                self.supervisors.remove(supervisor)
                print(f"Fired Supervisor {supervisor.name}.")
        else:
            print(f"{supervisor.name} is not under Vice President {self.name}.")


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
            print(f"Promoted Worker {worker.name} to Supervisor under Vice President {self.name}")
        else:
            print(f"No space to promote under Vice President {self.name}")

    def handle_promote(self, supervisor):
        """Handle supervisor promotion to VP - promote a new supervisor"""
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
            if vice_president.supervisors:
                # Promote the first supervisor to VP
                promoted_supervisor = vice_president.supervisors.pop(0)
                new_vp = VicePresident(promoted_supervisor.name)

                # Check if the promoted supervisor has workers to promote to a supervisor
                if promoted_supervisor.workers:
                    promoted_worker = promoted_supervisor.workers.pop(0)
                    new_supervisor = Supervisor(promoted_worker.name)  # New Supervisor instance for promoted worker
                    new_supervisor.workers = promoted_supervisor.workers  # Transfer workers to the new supervisor
                    new_vp.supervisors.append(new_supervisor)  # Add the new supervisor under the new VP
                    vice_president.supervisors = []
                    print(f"Promoted Worker {promoted_worker.name} to Supervisor and replaced {promoted_supervisor.name}.")
                else:
                    print(f"No workers to promote under Supervisor {promoted_supervisor.name}.")

                new_vp.supervisors += vice_president.supervisors  # Transfer remaining supervisors under the new VP
                self.vice_presidents[self.vice_presidents.index(vice_president)] = new_vp
                print(f"Promoted Supervisor {new_vp.name} to Vice President and replaced {vice_president.name}.")
            else:
                # If no supervisors, just remove the VP
                self.vice_presidents.remove(vice_president)
                print(f"Fired Vice President {vice_president.name}.")
        else:
            print(f"{vice_president.name} is not under President {self.name}.")


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
