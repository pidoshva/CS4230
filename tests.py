# President:
# - Cannot have greater than two vice presidents
# - Cannot hire if subordinates is equal to two
# - Hiring should correctly add 1 to the total of subordinates
# - Firing should remove the subordinates
# Vice President:
# - Cannot have greater than three supervisors
# - Cannot hire if subordinates is equal to three
# - Hiring should correctly add 1 to the total of subordinates
# Supervisors:
# - Cannot have greater than five workers
# - Cannot hire if subordinates is equal to five
# - Hiring should correctly add 1 to the total of subordinates


# Hiring an employee:
# Each employee must have a unique name, add utils that check name before an employee is hired with a try catch, test this

import unittest
from io import StringIO
import sys
from main import (check_employee_name_uniqueness, handle_layoff, display_organization)
import employees

class TestDysfunctionalOrganization(unittest.TestCase):

    def setUp(self):
        # Create a fresh organization for each test
        self.president = employees.President("Bob")
        self.vp1 = employees.VicePresident("VP1")
        self.vp2 = employees.VicePresident("VP2")
        self.president.hire(self.vp1)
        self.president.hire(self.vp2)

        self.supervisor1 = employees.Supervisor("Supervisor1")
        self.vp1.hire(self.supervisor1)

        self.worker1 = employees.Worker("Worker1")
        self.supervisor1.hire(self.worker1)

        self.worker2 = employees.Worker("Worker2")
        self.supervisor1.hire(self.worker2)

    def tearDown(self):
        # Clear the employee names set after each test to ensure state isolation
        employees.employee_names_used.clear()

    def test_hierarchy(self):
        # Test hierarchy levels
        self.assertIsInstance(self.president, employees.President)
        self.assertIsInstance(self.vp1, employees.VicePresident)
        self.assertIsInstance(self.supervisor1, employees.Supervisor)
        self.assertIsInstance(self.worker1, employees.Worker)

    def test_name_uniqueness(self):
        # Test name uniqueness
        self.assertTrue(check_employee_name_uniqueness("Alice"))  # Should be unique
        self.assertFalse(check_employee_name_uniqueness("Worker1"))  # Should be false, already exists

    def test_hiring_logic(self):
        # Test hiring logic
        supervisor2 = employees.Supervisor("Supervisor2")
        self.vp1.hire(supervisor2)
        self.assertEqual(len(self.vp1.supervisors), 2)  # Should have 2 supervisors now

        worker3 = employees.Worker("Worker3")
        self.supervisor1.hire(worker3)
        self.assertEqual(len(self.supervisor1.workers), 3)  # Should have 3 workers now

        # Attempt to hire a worker with the same name
        worker_duplicate = employees.Worker("Worker1")
        self.supervisor1.hire(worker_duplicate)  # Should not hire due to name conflict
        self.assertEqual(len(self.supervisor1.workers), 3)  # Should still have 3 workers

    def test_firing_logic(self):
        self.assertEqual(len(self.supervisor1.workers), 2)  # Should have 2 workers
        self.supervisor1.fire(self.worker1)  # Fire Worker1
        self.assertEqual(len(self.supervisor1.workers), 1)  # Should have 1 worker after firing

    def test_promotion_logic(self):
        # Promote Worker1 to Supervisor
        self.vp1.promote(self.worker1, self.supervisor1)  
        self.assertEqual(len(self.supervisor1.workers), 1)  # Supervisor1 should now have Worker2
        self.assertEqual(len(self.vp1.supervisors), 2)  # VP1 should have 2 supervisors now

    def test_layoff_logic(self):
        self.assertEqual(len(self.supervisor1.workers), 2)  # Ensure 2 workers exist
        self.supervisor1.fire(self.worker1)  # Lay off Worker1
        self.assertEqual(len(self.supervisor1.workers), 1)  # Only Worker2 should remain

    def test_display_organization(self):
        # Capture the output of display_organization
        captured_output = StringIO()
        sys.stdout = captured_output
        display_organization(self.president)
        sys.stdout = sys.__stdout__

        # Check the captured output against expected structure
        output = captured_output.getvalue().strip()
        expected_output = (
            "President: Bob\n"
            "  Vice President: VP1\n"
            "    Supervisor: Supervisor1\n"
            "      Worker: Worker1\n"
            "      Worker: Worker2\n"
            "  Vice President: VP2"
        ).strip()

        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
