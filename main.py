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
    role = input("Enter role to quit (worker, supervisor, vp): ").strip().lower()
    name = input("Enter name of person quitting: ").strip()
    handle_firing(president, role, name)

def handle_firing(president, role=None, name=None):
    """
    Handle firing employees and promote their replacements.

    Based on the role (worker, supervisor, vp), the employee is fired, and promotions are done
    to maintain the hierarchy.
    """
    if not role:
        role = input("Enter role to fire (worker, supervisor, vp): ").strip().lower()
    if not name:
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

    # Firing a Supervisor
    elif role == "supervisor":
        for vp in president.vice_presidents:
            supervisor_to_fire = None
            for supervisor in vp.supervisors:
                if supervisor.name == name:
                    supervisor_to_fire = supervisor
                    break

            if supervisor_to_fire:
                # Promote a worker to supervisor
                if supervisor_to_fire.workers:
                    promoted_worker = supervisor_to_fire.workers.pop(0)
                    promoted_supervisor = employees.Supervisor(promoted_worker.name)
                    promoted_supervisor.workers = supervisor_to_fire.workers
                    vp.supervisors[vp.supervisors.index(supervisor_to_fire)] = promoted_supervisor
                    print(f"Promoted Worker {promoted_worker.name} to Supervisor and replaced {supervisor_to_fire.name}")
                else:
                    vp.supervisors.remove(supervisor_to_fire)
                    print(f"Fired Supervisor {name}")
                save_organization(president)
                return
            else:
                print(f"Supervisor {name} not found under Vice President {vp.name}.")

    # Firing a Vice President
    elif role == "vp":
        vp_to_fire = None
        for vp in president.vice_presidents:
            if vp.name == name:
                vp_to_fire = vp
                break

        if vp_to_fire:
            # Promote the first supervisor to VP
            if vp_to_fire.supervisors:
                promoted_supervisor = vp_to_fire.supervisors.pop(0)
                promoted_vp = employees.VicePresident(promoted_supervisor.name)

                # Promote the first worker to Supervisor
                if promoted_supervisor.workers:
                    promoted_worker = promoted_supervisor.workers.pop(0)
                    new_supervisor = employees.Supervisor(promoted_worker.name)
                    new_supervisor.workers = promoted_supervisor.workers
                    promoted_vp.supervisors.append(new_supervisor)
                
                promoted_vp.supervisors += vp_to_fire.supervisors
                president.vice_presidents[president.vice_presidents.index(vp_to_fire)] = promoted_vp
                print(f"Promoted Supervisor {promoted_supervisor.name} to Vice President.")
            else:
                president.vice_presidents.remove(vp_to_fire)
                print(f"Fired Vice President {name}")
            save_organization(president)
            return
        else:
            print(f"Vice President {name} not found.")

def handle_promotion(president):
    """
    Handle promotions for workers and supervisors.

    Promote a worker to supervisor or a supervisor to vice president.
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
                            promoted_supervisor = supervisor.promote(worker)
                            if promoted_supervisor:
                                vp.supervisors.append(promoted_supervisor)
                                print(f"Promoted {name} to Supervisor under VP {vp.name}")
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
                        promoted_vp = vp.promote(supervisor)
                        if promoted_vp:
                            president.vice_presidents.append(promoted_vp)
                            print(f"Promoted {name} to Vice President.")
                            save_organization(president)
                            return
                print(f"Supervisor {name} not found under VP {vp_name}")
                return
        print(f"Vice President {vp_name} not found.")

def handle_hiring(president):
    """Handle hiring new employees (workers, supervisors, or vice presidents)"""
    role = input("Enter role (worker, supervisor, vp): ").strip().lower()
    name = input("Enter name: ").strip()
    if role == "worker":
        supervisor_name = input("Enter supervisor's name: ").strip()
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == supervisor_name:
                    worker = employees.Worker(name)
                    supervisor.hire(worker)
                    print(f"Hired worker {name} under Supervisor {supervisor_name}")
                    save_organization(president)
                    return
    elif role == "supervisor":
        vp_name = input("Enter VP's name: ").strip()
        for vp in president.vice_presidents:
            if vp.name == vp_name:
                supervisor = employees.Supervisor(name)
                vp.hire(supervisor)
                print(f"Hired Supervisor {name} under Vice President {vp_name}")
                save_organization(president)
                return
    elif role == "vp":
        if len(president.vice_presidents) < 2:
            vp = employees.VicePresident(name)
            president.hire(vp)
            print(f"Hired Vice President {name} under President {president.name}")
            save_organization(president)
        else:
            print("No space to hire another VP.")

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
