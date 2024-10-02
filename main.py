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
    """
    Utility function to create the organization from a file.

    Reads the organization structure from a file and creates the employee hierarchy.
    """
    print(f"Creating company organization from file {filename}\n")
    with open(filename, 'r') as f:
        lines = f.readlines()

    president = None
    current_vp = None
    current_supervisor = None

    for line in lines:
        if line != "" and line != '\n':
            parts = line.strip().split(': ')
            role = parts[0]
            name = parts[1]
            if role == "President":
                # Create the President
                president = employees.President(name)
            elif role == "Vice President":
                # Create and assign Vice President to the President
                vp = employees.VicePresident(name)
                president.hire(vp)
                current_vp = vp
            elif role == "Supervisor":
                # Create and assign Supervisor to the Vice President
                supervisor = employees.Supervisor(name)
                current_vp.hire(supervisor)
                current_supervisor = supervisor
            elif role == "Worker":
                # Create and assign Worker to the Supervisor
                worker = employees.Worker(name)
                current_supervisor.hire(worker)
    return president

def save_organization(president, filename='organization.txt'):
    """
    Utility function to save the organization to a file.

    Writes the current structure of the organization to a file for persistence.
    """
    with open(filename, 'w') as f:
        f.write(f"President: {president.name}\n")
        for vp in president.vice_presidents:
            f.write(f"Vice President: {vp.name}\n")
            for supervisor in vp.supervisors:
                f.write(f"Supervisor: {supervisor.name}\n")
                for worker in supervisor.workers:
                    f.write(f"Worker: {worker.name}\n")

def handle_quit(president):
    """
    Handle quitting employees.

    When an employee quits, it is handled in a similar way as firing them.
    """
    while True:
        role = input("Enter role to quit (worker, supervisor, vp): ").strip().lower()
        if role == "worker" or role == "supervisor" or role == "vp":
            break

    name = input("Enter name of person quitting: ").strip()

    # Worker quits
    if role == "worker":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                for worker in supervisor.workers:
                    if worker.name == name:
                        worker.quit(supervisor)
                        print(f"Worker {name} quit")
                        save_organization(president)
                        return

        print(f"Worker {name} not found")

    # Supervisor quits
    elif role == "supervisor":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == name:
                    supervisor.quit(vp)
                    print(f"Supervisor {name} quit")
                    save_organization(president)
                    return

        print(f"Supervisor {name} not found")

    # Vice President quits
    elif role == "vp":
        for vp in president.vice_presidents:
            if vp.name == name:
                vp.quit(president)
                print(f"Vice President {name} quits")
                save_organization(president)
                return

        print(f"Vice President {name} not found.")

def handle_firing(president):
    """
    Handle firing employees and promote their replacements.

    Based on the role (worker, supervisor, vp), the employee is fired, and all employees under them are also fired
    """
    while True:
        role = input("Enter role to fire (worker, supervisor, vp): ").strip().lower()
        if role == "worker" or role == "supervisor" or role == "vp":
            break

    name = input("Enter name to fire: ").strip()

    # Firing a Worker
    if role == "worker":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                for worker in supervisor.workers:
                    if worker.name == name:
                        supervisor.fire(worker)
                        print(f"Fired worker {name}")
                        save_organization(president)
                        return

        print(f"Worker {name} not found")

    # Firing a Supervisor
    elif role == "supervisor":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == name:
                    vp.fire(supervisor)
                    print(f"Fired Supervisor {name}")
                    save_organization(president)
                    return

        print(f"Supervisor {name} not found")

    # Firing a Vice President
    elif role == "vp":
        for vp in president.vice_presidents:
            if vp.name == name:
                president.fire(vp)
                print(f"Fired Vice President {name}")
                save_organization(president)
                return

        print(f"Vice President {name} not found.")

def handle_promotion(president):
    """
    Handle promotions for workers and supervisors.

    Promote a worker to supervisor or a supervisor to vice president.
    """
    while True:
        role = input("Enter role to promote (worker, supervisor): ").strip().lower()
        if role == "worker" or role == "supervisor":
            break

    name = input("Enter name to promote: ").strip()

    if role == "worker":
        supervisor_name = input("Enter current supervisor's name: ").strip()
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == supervisor_name:
                    for worker in supervisor.workers:
                        if worker.name == name:
                            vp.promote(worker, supervisor)
                            save_organization(president)
                            return
                    print(f"Worker {name} not found under Supervisor {supervisor_name}")
                    return
        print(f"Supervisor {supervisor_name} not found.")

    elif role == "supervisor":
        vp_name = input("Enter current VP's name: ").strip()
        for vp in president.vice_presidents:
            if vp.name == vp_name:
                for supervisor in vp.supervisors:
                    if supervisor.name == name:
                        president.promote(supervisor, vp)
                        save_organization(president)
                        return
                print(f"Supervisor {name} not found under VP {vp_name}")
                return
        print(f"Vice President {vp_name} not found.")

def handle_hiring(president):
    """Handle hiring new employees (workers, supervisors, or vice presidents)"""
    while True:
        role = input("Enter role (worker, supervisor, vp): ").strip().lower()
        if role == "worker" or role == "supervisor" or role == "vp":
            break

    name = input("Enter name: ").strip()

    if role == "worker":
        supervisor_name = input("Enter supervisor's name: ").strip()
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == supervisor_name:
                    worker = employees.Worker(name)
                    supervisor.hire(worker)
                    save_organization(president)
                    return
            print(f"Supervisor {supervisor_name} not found")
    elif role == "supervisor":
        vp_name = input("Enter VP's name: ").strip()
        for vp in president.vice_presidents:
            if vp.name == vp_name:
                supervisor = employees.Supervisor(name)
                vp.hire(supervisor)
                save_organization(president)
                return
        print(f"Vice President {vp_name} not found")
    elif role == "vp":
        vp = employees.VicePresident(name)
        president.hire(vp)
        save_organization(president)

def command_loop(president):
    """Command loop for interaction with the organization"""
    while True:
        command = input("Enter command (hire, fire, promote, quit, display, q): ").strip().lower()
        if command == "display":
            display_organization(president)
        elif command == "hire":
            handle_hiring(president)
        elif command == "fire":
            handle_firing(president)
        elif command == "promote":
            handle_promotion(president)
        elif command == "quit":
            handle_quit(president)
        elif command == "q":
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    """Main program: Read organization and start command loop"""
    president = read_organization()
    command_loop(president)
