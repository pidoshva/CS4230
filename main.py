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

def command_loop(president):
    """Command loop to interact with the system"""
    while True:
        command = input("Enter command (hire, fire, promote, display, quit): ").strip().lower()
        if command == "display":
            display_organization(president)
        elif command == "hire":
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
                            save_organization(president)  # Save after hiring
                            display_organization(president)  # Display updated organization
            elif role == "supervisor":
                vp_name = input("Enter VP's name: ").strip()
                for vp in president.vice_presidents:
                    if vp.name == vp_name:
                        supervisor = Supervisor(name)
                        vp.hire(supervisor)
                        print(f"Hired Supervisor {name} under Vice President {vp_name}")
                        save_organization(president)  # Save after hiring
                        display_organization(president)  # Display updated organization
            elif role == "vp":
                if len(president.vice_presidents) < 2:
                    vp = VicePresident(name)
                    president.hire(vp)
                    print(f"Hired Vice President {name} under President {president.name}")
                    save_organization(president)  # Save after hiring
                    display_organization(president)  # Display updated organization
                else:
                    print("No space to hire another VP.")
        elif command == "fire":
            role = input("Enter role to fire (worker, supervisor, vp): ").strip().lower()
            name = input("Enter name to fire: ").strip()
            if role == "worker":
                for vp in president.vice_presidents:
                    for supervisor in vp.supervisors:
                        for worker in supervisor.workers:
                            if worker.name == name:
                                supervisor.fire(worker)
                                print(f"Fired worker {name}")
                                save_organization(president)  # Save after firing
                                display_organization(president)  # Display updated organization
            elif role == "supervisor":
                for vp in president.vice_presidents:
                    for supervisor in vp.supervisors:
                        if supervisor.name == name:
                            vp.fire(supervisor)
                            print(f"Fired supervisor {name}")
                            save_organization(president)  # Save after firing
                            display_organization(president)  # Display updated organization
            elif role == "vp":
                for vp in president.vice_presidents:
                    if vp.name == name:
                        president.fire(vp)
                        print(f"Fired VP {name}")
                        save_organization(president)  # Save after firing
                        display_organization(president)  # Display updated organization
        elif command == "promote":
            role = input("Enter role to promote (worker, supervisor): ").strip().lower()
            name = input("Enter name to promote: ").strip()
            if role == "worker":
                supervisor_name = input("Enter current supervisor's name: ").strip()
                # Search for the correct supervisor and worker for promotion
                promoted_supervisor = None
                for vp in president.vice_presidents:
                    for supervisor in vp.supervisors:
                        if supervisor.name == supervisor_name:
                            for worker in supervisor.workers:
                                if worker.name == name:
                                    promoted_supervisor = supervisor.promote(worker)
                                    if promoted_supervisor:
                                        vp.hire(promoted_supervisor)
                                        print(f"Promoted {name} to Supervisor under VP {vp.name}")
                                        save_organization(president)  # Save after promotion
                                        display_organization(president)  # Display updated organization
                                        break
                            else:
                                print(f"Worker {name} not found under Supervisor {supervisor_name}")
            elif role == "supervisor":
                vp_name = input("Enter current VP's name: ").strip()
                for vp in president.vice_presidents:
                    if vp.name == vp_name:
                        promoted_vp = vp.promote(Supervisor(name))
                        if promoted_vp:
                            president.hire(promoted_vp)
                            print(f"Promoted {name} to Vice President")
                            save_organization(president)  # Save after promotion
                            display_organization(president)  # Display updated organization
        elif command == "quit":
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    """Main"""
    
    president = read_organization() # Load initial organization struct from file

    command_loop(president) # Calling command loop
