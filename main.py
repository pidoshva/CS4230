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

def handle_quit(president):
    """Handles quitting"""
    role = input("Enter role to quit (worker, supervisor, vp): ").strip().lower()
    name = input("Enter name of person quitting: ").strip()
    if role == "worker":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                for worker in supervisor.workers:
                    if worker.name == name:
                        supervisor.fire(worker)
                        print(f"{name} has quit.")
                        save_organization(president)
                        return
    elif role == "supervisor":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == name:
                    vp.fire(supervisor)
                    print(f"{name} has quit.")
                    save_organization(president)
                    return
    elif role == "vp":
        for vp in president.vice_presidents:
            if vp.name == name:
                president.fire(vp)
                print(f"{name} has quit.")
                save_organization(president)
                return
    print(f"{name} not found.")

def handle_layoff(president):
    """Handles layoffs"""
    role = input("Enter role to lay off (worker, supervisor, vp): ").strip().lower()
    name = input("Enter name to lay off: ").strip()
    if role == "worker":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                for worker in supervisor.workers:
                    if worker.name == name:
                        supervisor.fire(worker)
                        print(f"{name} has been laid off.")
                        relocate_worker(president, worker)
                        save_organization(president)
                        return
    print(f"{name} not found.")

def relocate_worker(president, worker):
    """Relocates workers"""
    for vp in president.vice_presidents:
        for supervisor in vp.supervisors:
            if len(supervisor.workers) < 5:
                supervisor.hire(worker)
                print(f"{worker.name} relocated to {supervisor.name}.")
                return
    print(f"No vacancies for {worker.name}. Layoff is final.")

def transfer_employee(president):
    """Moves employees"""
    role = input("Enter role to transfer (worker, supervisor): ").strip().lower()
    name = input("Enter name to transfer: ").strip()
    if role == "worker":
        source_supervisor = input("Enter current supervisor's name: ").strip()
        destination_supervisor = input("Enter new supervisor's name: ").strip()
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == source_supervisor:
                    for worker in supervisor.workers:
                        if worker.name == name:
                            supervisor.fire(worker)
                            for vp_dest in president.vice_presidents:
                                for sup_dest in vp_dest.supervisors:
                                    if sup_dest.name == destination_supervisor:
                                        sup_dest.hire(worker)
                                        print(f"Transferred {name} from {source_supervisor} to {destination_supervisor}.")
                                        save_organization(president)
                                        return
    print(f"Transfer failed. {name} not found or destination unavailable.")

def handle_hiring(president):
    """Handles hiring"""
    role = input("Enter role (worker, supervisor, vp): ").strip().lower()
    name = input("Enter name: ").strip()
    if role == "worker":
        supervisor_name = input("Enter supervisor's name: ").strip()
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == supervisor_name:
                    worker = Worker(name)
                    supervisor.hire(worker)
                    print(f"Hired worker {name} under Supervisor {supervisor_name}")
                    save_organization(president)
                    return
    elif role == "supervisor":
        vp_name = input("Enter VP's name: ").strip()
        for vp in president.vice_presidents:
            if vp.name == vp_name:
                supervisor = Supervisor(name)
                vp.hire(supervisor)
                print(f"Hired Supervisor {name} under Vice President {vp_name}")
                save_organization(president)
                return
    elif role == "vp":
        if len(president.vice_presidents) < 2:
            vp = VicePresident(name)
            president.hire(vp)
            print(f"Hired Vice President {name} under President {president.name}")
            save_organization(president)
        else:
            print("No space to hire another VP.")

def handle_firing(president):
    """Handles firing"""
    role = input("Enter role to fire (worker, supervisor, vp): ").strip().lower()
    name = input("Enter name to fire: ").strip()
    if role == "worker":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                for worker in supervisor.workers:
                    if worker.name == name:
                        supervisor.fire(worker)
                        print(f"Fired worker {name}")
                        save_organization(president)
                        return
    elif role == "supervisor":
        for vp in president.vice_presidents:
            for supervisor in vp.supervisors:
                if supervisor.name == name:
                    supervisor.handle_firing(vp)
                    print(f"Fired supervisor {name}")
                    save_organization(president)
                    return
    elif role == "vp":
        for vp in president.vice_presidents:
            if vp.name == name:
                vp.handle_firing(president)
                president.fire(vp)
                print(f"Fired VP {name}")
                save_organization(president)
                return

def handle_promotion(president):
    """Handles promotions"""
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
                                vp.hire(promoted_supervisor)
                                print(f"Promoted {name} to Supervisor under VP {vp.name}")
                                save_organization(president)
                                return
    elif role == "supervisor":
        vp_name = input("Enter current VP's name: ").strip()
        for vp in president.vice_presidents:
            if vp.name == vp_name:
                promoted_vp = vp.promote(Supervisor(name))
                if promoted_vp:
                    president.hire(promoted_vp)
                    print(f"Promoted {name} to Vice President")
                    save_organization(president)

def command_loop(president):
    """Input collection system"""
    while True:
        command = input("Enter command (hire, fire, promote, quit, layoff, transfer, display, q): ").strip().lower()
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
        elif command == "layoff":
            handle_layoff(president)
        elif command == "transfer":
            transfer_employee(president)
        elif command == "q":
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    """Main"""
    president = read_organization()
    command_loop(president)
