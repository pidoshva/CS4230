"""
Project #4
The Dysfunctional Organization System
[Vadim Pidoshva, Trajan Clark, Jessica Adams, Cameron Seppi]
"""
import employees

def display_organization(president):
    """Utility function to display the organization hierarchy"""
    president.display()


def read_organization(filename='organization.txt'):
    """Utility function to create the organization from a file"""
    with open(filename, 'r') as f:
        lines = f.readlines()

    president = None
    current_vp = None
    current_supervisor = None

    for line in lines:
        parts = line.strip().split(': ')
        role = parts[0]
        name = parts[1]

        if role == "President":
            president = President(name)
        elif role == "Vice President":
            vp = VicePresident(name)
            president.hire(vp)
            current_vp = vp
        elif role == "Supervisor":
            supervisor = Supervisor(name)
            current_vp.hire(supervisor)
            current_supervisor = supervisor
        elif role == "Worker":
            worker = Worker(name)
            current_supervisor.hire(worker)

    return president

def save_organization(president, filename='organization.txt'):
    """Utility function to save the organization to a file"""
    with open(filename, 'w') as f:
        # Write the president
        f.write(f"President: {president.name}\n")
        # Write each vice president, supervisor, and worker in the organization
        for vp in president.vice_presidents:
            f.write(f"Vice President: {vp.name}\n")
            for supervisor in vp.supervisors:
                f.write(f"Supervisor: {supervisor.name}\n")
                for worker in supervisor.workers:
                    f.write(f"Worker: {worker.name}\n")

