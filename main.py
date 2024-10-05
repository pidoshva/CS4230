"""
Project #4
The Dysfunctional Organization System
[Vadim Pidoshva, Trajan Clark, Jessica Adams, Cameron Seppi]
"""
import sys
import employees

# Global Hash Set that contains all currently used unique employee names
employee_names_used = set()

# Counters for employees during read_organization
pres_count = 0
vp_count = 0
supervisor_count = 0
worker_count = 0

# Flag for organization read success or failure
read_organization_success = True

def check_employee_name_uniqueness(name):
    """
    Check if the employee name is unique (not already used in the organization).
    """
    if name in employee_names_used:
        return False
    employee_names_used.add(name)
    return True

def display_organization(president):
    """
    Utility function to display the organization hierarchy.
    """
    president.display()

def read_organization(filename='organization.txt'):
    """
    Utility function to create the organization from a file.

    Reads the organization structure from a file and creates the employee hierarchy.
    """
    global read_organization_success

    with open(filename, 'r') as f:
        lines = f.readlines()

    president = None
    current_vp = None
    current_supervisor = None

    global pres_count, vp_count, supervisor_count, worker_count

    for line in lines:
        if line.strip():
            parts = line.strip().split(': ')
            role = parts[0]
            name = parts[1]

            if role == "President":
                pres_count += 1
                if not check_employee_name_uniqueness(name) or pres_count > 1:
                    read_organization_success = False
                    break
                president = employees.President(name)

            elif role == "Vice President":
                vp_count += 1
                if not check_employee_name_uniqueness(name) or vp_count > 2:
                    read_organization_success = False
                    break
                vp = employees.VicePresident(name)
                president.hire(vp)
                current_vp = vp

            elif role == "Supervisor":
                supervisor_count += 1
                if not check_employee_name_uniqueness(name) or supervisor_count > 4:
                    read_organization_success = False
                    break
                supervisor = employees.Supervisor(name)
                current_vp.hire(supervisor)
                current_supervisor = supervisor

            elif role == "Worker":
                worker_count += 1
                if not check_employee_name_uniqueness(name) or worker_count > 10:
                    read_organization_success = False
                    break
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
    Handle quitting employees. Employees who quit are removed from the organization.
    """
    role = input("Enter role to quit (worker, supervisor, vp): ").strip().lower()
    name = input("Enter name of person quitting: ").strip()

    if role == "worker":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                for worker in supervisor.workers:
                    if worker.name == name:
                        employee_names_used.discard(name)
                        worker.quit(supervisor)
                        print(f"Worker {name} quit")
                        save_organization(president)
                        return
        print(f"Worker {name} not found")

    elif role == "supervisor":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == name:
                    employee_names_used.discard(name)
                    supervisor.quit(vp)
                    print(f"Supervisor {name} quit")
                    save_organization(president)
                    return
        print(f"Supervisor {name} not found")

    elif role == "vp":
        for vp in president.vice_presidents:
            if vp.name == name:
                employee_names_used.discard(name)
                vp.quit(president)
                print(f"Vice President {name} quit")
                save_organization(president)
                return
        print(f"Vice President {name} not found")

def handle_firing(president):
    """
    Handle firing employees and promote their replacements.
    """
    role = input("Enter role to fire (worker, supervisor, vp): ").strip().lower()
    name = input("Enter name to fire: ").strip()

    if role == "worker":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                for worker in supervisor.workers:
                    if worker.name == name:
                        employee_names_used.discard(name)
                        supervisor.fire(worker)
                        print(f"Fired worker {name}")
                        save_organization(president)
                        return
        print(f"Worker {name} not found")

    elif role == "supervisor":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == name:
                    employee_names_used.discard(name)
                    vp.fire(supervisor)
                    print(f"Fired Supervisor {name}")
                    save_organization(president)
                    return
        print(f"Supervisor {name} not found")

    elif role == "vp":
        for vp in president.vice_presidents:
            if vp.name == name:
                employee_names_used.discard(name)
                president.fire(vp)
                print(f"Fired Vice President {name}")
                save_organization(president)
                return
        print(f"Vice President {name} not found")

def handle_layoff(president):
    """
    Handle laying off employees.
    Based on the role (worker, supervisor, vp), the employee is laid off, and then moved to the same position if available
    """
    while True:
        role = input("Enter role to layoff (worker, supervisor, vp): ").strip().lower()
        if role == "worker" or role == "supervisor" or role == "vp":
            break
    name = input("Enter name to layoff: ").strip()
    employee_initiating_layoff = ""
    saved_employee = None
    transfered = False
    # Fire Worker
    if role == "worker":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                for worker in supervisor.workers:
                    if worker.name == name:
                        employee_names_used.discard(name)
                        saved_employee = worker
                        supervisor.fire(worker)
                        employee_initiating_layoff = supervisor.name
                        print(f"Fired worker {name}")
                        save_organization(president)
        # Attempt to move worker somewhere else
        if employee_initiating_layoff != "":
            # Attempt to hire in same supervisory area
            for vp in president.vice_presidents:
                if transfered == True:
                    break
                for supervisor in vp.supervisors:
                    if transfered == True:
                        break
                    if supervisor.name == employee_initiating_layoff:
                        # 4 Becuase you cannot relocate to the original position so 5-1
                        if len(supervisor.workers) >= 4:
                            break
                        else:
                            supervisor.hire(saved_employee)
                            transfered = True
            # Attempt to hire in different supervisory area
            for vp in president.vice_presidents:
                if transfered == True:
                    break
                for supervisor in vp.supervisors:
                    if transfered == True:
                        break
                    if supervisor.name != employee_initiating_layoff:
                        # 4 Becuase you cannot relocate to the original position so 5-1
                        if len(supervisor.workers) >= 5:
                            break
                        else:
                            supervisor.hire(saved_employee)
                            transfered = True
            if transfered:
                print("Employee Relocated")
                save_organization(president)
                return
            else:
                print("Employee laid off and unable to be relocated")
                save_organization(president)
                return
            
        print(f"Worker {name} not found")
    elif role == "supervisor":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == name:
                    employee_names_used.discard(name)
                    saved_employee = supervisor
                    vp.fire(supervisor)
                    employee_initiating_layoff = vp.name
                    print(f"Fired Supervisor {name}")
                    save_organization(president)
        # Attempt to move worker somewhere else
        if employee_initiating_layoff != "":
            # Attempt to hire in same supervisory area
            for vp in president.vice_presidents:
                if transfered == True:
                    break
                if vp.name == employee_initiating_layoff:
                    # 4 Becuase you cannot relocate to the original position so 2-1
                    if len(vp.supervisors) >= 1:
                        break
                    else:
                        vp.hire(saved_employee)
                        transfered = True
            # Attempt to hire in different supervisory area
            for vp in president.vice_presidents:
                if transfered == True:
                    break
                if vp.name != employee_initiating_layoff:
                    if len(vp.supervisors) >= 2:
                        break
                    else:
                        vp.hire(saved_employee)
                        transfered = True
            if transfered:
                print("Employee Relocated")
                save_organization(president)
                return
            else:
                print("Employee laid off and unable to be relocated")
                save_organization(president)
                return
        print(f"Supervisor {name} not found")
    elif role == "vp":
        for vp in president.vice_presidents:
            if vp.name == name:
                employee_names_used.discard(name)
                saved_employee = vp
                president.fire(vp)
                employee_initiating_layoff = president.name
                print(f"Fired Vice President {name}")
                save_organization(president)
        # Attempt to move VP to other VP position
        if employee_initiating_layoff != "":
            if len(president.vice_presidents) > 0:
                pass
            else:
                president.hire(saved_employee)
                transfered = True
        if transfered:
            print("Employee Relocated")
            return
        elif transfered != True:
            print("Employee laid off and unable to be relocated")
            return
        print(f"Vice President {name} not found.")


def relocate_employee(president, employee, role):
    """
    Relocate an employee to a new position, if available.
    """
    for vp in president.vice_presidents:
        if role == "worker":
            for supervisor in vp.supervisors:
                if len(supervisor.workers) < 5:
                    supervisor.hire(employee)
                    return True
        elif role == "supervisor" and len(vp.supervisors) < 3:
            vp.hire(employee)
            return True

    return False

def handle_promotion(president):
    """
    Handle promotions for workers and supervisors.
    """
    role = input("Enter role to promote (worker, supervisor): ").strip().lower()
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

def handle_hiring(president):
    """
    Handle hiring new employees (workers, supervisors, or vice presidents).
    """
    role = input("Enter role (worker, supervisor, vp): ").strip().lower()
    name = input("Enter name: ").strip()

    if role == "worker":
        supervisor_name = input("Enter supervisor's name: ").strip()
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == supervisor_name:
                    if not check_employee_name_uniqueness(name):
                        print("Name is not unique, hiring failed.")
                        return
                    worker = employees.Worker(name)
                    supervisor.hire(worker)
                    save_organization(president)
                    return
        print(f"Supervisor {supervisor_name} not found.")

    elif role == "supervisor":
        vp_name = input("Enter VP's name: ").strip()
        for vp in president.vice_presidents:
            if vp.name == vp_name:
                if not check_employee_name_uniqueness(name):
                    print("Name is not unique, hiring failed.")
                    return
                supervisor = employees.Supervisor(name)
                vp.hire(supervisor)
                save_organization(president)
                return
        print(f"Vice President {vp_name} not found.")

    elif role == "vp":
        if not check_employee_name_uniqueness(name):
            print("Name is not unique, hiring failed.")
            return
        vp = employees.VicePresident(name)
        president.hire(vp)
        save_organization(president)

def command_loop(president):
    """
    Command loop for interaction with the organization.
    """
    while True:
        command = input("Enter command (hire, fire, promote, quit, display, layoff, q): ").strip().lower()
        if command == "display":
            display_organization(president)
        elif command == "hire":
            handle_hiring(president)
        elif command == "fire":
            handle_firing(president)
        elif command == "promote":
            handle_promotion(president)
        elif command == "layoff":
            handle_layoff(president)
        elif command == "quit":
            handle_quit(president)
        elif command == "q":
            break
        else:
            print("Invalid command.")

def main():
    """
    Main function: Read organization and start command loop.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <organization_file>")
        sys.exit(1)

    organization_file = sys.argv[1]
    president = read_organization(organization_file)

    if read_organization_success:
        print("Organization read from file is valid")
        command_loop(president)
    else:
        print("Organization read from file is invalid, Exiting Program...")
        sys.exit(1)

if __name__ == "__main__":
    main()
