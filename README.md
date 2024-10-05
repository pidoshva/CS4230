# Dysfunctional Organization System

## Project Overview
This project is a command-line application designed to manage an organization's employee hierarchy, including roles such as President, Vice President, Supervisor, and Worker. Users can perform operations like hiring, firing, promoting, quitting, laying off, transferring employees, and displaying the organization structure.

### Contributors
- Vadim Pidoshva
- Trajan Clark
- Jessica Adams
- Cameron Seppi

## Getting Started

### Prerequisites
Make sure you have Python 3.x installed on your machine. You can check your Python version by running:
```bash
python --version
```

## Installation

Clone the repository to your local machine:

```bash
git clone <repository_url>
cd <repository_directory>
```

## Running the Program

To run the application, use the following command:

```bash
python main.py <organization_file>
```

Replace <organization_file> with the path to your organization file, for example, organization.txt.

## Organization File Structure

The organization file must follow a specific format for the hierarchy to be read correctly. Here’s an example:

```bash
President: John Doe
Vice President: Jane Smith
Vice President: Alice Johnson
Supervisor: Bob Brown
Worker: Charlie Black
Worker: David White
```

## Commands

Once the program is running, you can use the following commands in the command loop:

- **display**: Show the current organization hierarchy.
- **hire**: Hire a new employee (worker, supervisor, or vice president).
- **fire**: Fire an existing employee.
- **promote**: Promote a worker or supervisor to a higher position.
- **quit**: Remove an employee who is quitting.
- **layoff**: Lay off an employee and attempt to relocate them.
- **transfer**: Transfer an employee to another supervisory group.
- **q**: Quit the program.

## User Input

The program will prompt the user for input during the command loop. It is important to note that the input must match the specified commands exactly and is case-sensitive. Ensure that you enter commands and other inputs precisely as instructed to avoid errors.

## Error Handling

If there are issues reading the organization file, the program will print an error message and exit. Ensure the file format is correct and follows the specifications above.
