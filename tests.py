import unittest
from unittest.mock import MagicMock, patch
import main

class TestOrganizationSystem(unittest.TestCase):
    def setUp(self):
        # Mock the employees and their hierarchy
        self.mock_president = MagicMock()
        self.mock_vp = MagicMock()
        self.mock_supervisor = MagicMock()
        self.mock_worker = MagicMock()

        # Set up hierarchy
        self.mock_president.name = "Manny"
        self.mock_president.vice_presidents = [self.mock_vp]
        self.mock_vp.name = "Ted"
        self.mock_vp.supervisors = [self.mock_supervisor]
        self.mock_supervisor.name = "Wolfgang"
        self.mock_supervisor.workers = []  # Use a real list
        self.mock_worker.name = "Daniel1"
        self.mock_supervisor.workers.append(self.mock_worker)  # Add worker

        # Mock behaviors
        self.mock_president.hire = MagicMock(return_value=True)
        self.mock_vp.hire = MagicMock(return_value=True)
        self.mock_supervisor.hire = MagicMock(return_value=True)
        self.mock_supervisor.fire = MagicMock()
        self.mock_vp.fire = MagicMock()
        self.mock_president.fire = MagicMock()

        # Patch the employees module
        patcher = patch("employees.President", return_value=self.mock_president)
        self.addCleanup(patcher.stop)
        self.mock_president_class = patcher.start()

        # Clear global state
        main.employee_names_used.clear()
        main.employee_names_used.add("Daniel1")

    @patch("main.save_organization")
    def test_display_organization(self, mock_save_organization):
        main.display_organization(self.mock_president)
        self.mock_president.display.assert_called_once()

    @patch("builtins.open", create=True)
    def test_read_organization(self, mock_open):
        # Simulate valid file contents
        mock_open.return_value.__enter__.return_value.readlines.return_value = [
            "President: Manny\n",
            "Vice President: Ted\n",
            "Supervisor: Wolfgang\n",
            "Worker: Daniel1\n",
            "Worker: Daniel2\n",
        ]

        president = main.read_organization("mock_file.txt")
        self.assertEqual(president, self.mock_president)
        self.assertTrue(main.read_organization_success)

    @patch("builtins.open", create=True)
    def test_save_organization(self, mock_open):
        main.save_organization(self.mock_president, "mock_file.txt")
        mock_open.assert_called_with("mock_file.txt", "w")
        mock_open.return_value.__enter__().write.assert_called()

    @patch("builtins.input", side_effect=["worker", "Daniel1"])
    @patch("main.save_organization")
    def test_handle_quit_worker(self, mock_save_organization, mock_input):
        main.handle_quit(self.mock_president)
        self.assertNotIn(self.mock_worker, self.mock_supervisor.workers)

    @patch("builtins.input", side_effect=["vp", "Ted"])
    @patch("main.save_organization")
    def test_handle_firing_vp(self, mock_save_organization, mock_input):
        main.handle_firing(self.mock_president)
        self.mock_president.fire.assert_called_with(self.mock_vp)

    @patch("builtins.input", side_effect=["supervisor", "Wolfgang", "Ted"])
    @patch("main.save_organization")
    def test_handle_promotion_supervisor(self, mock_save_organization, mock_input):
        main.handle_promotion(self.mock_president)
        self.mock_president.promote.assert_called_with(self.mock_supervisor, self.mock_vp)

    @patch("builtins.input", side_effect=["worker", "Daniel1", "Wolfgang"])
    @patch("main.save_organization")
    def test_handle_hiring_worker(self, mock_save_organization, mock_input):
        main.employee_names_used = set()  # Ensure names are unique
        main.handle_hiring(self.mock_president)
        self.mock_supervisor.hire.assert_called()

    @patch("builtins.input", side_effect=["worker", "Daniel1"])
    @patch("main.save_organization")
    def test_handle_layoff_worker(self, mock_save_organization, mock_input):
        main.handle_layoff(self.mock_president)
        self.assertNotIn(self.mock_worker, self.mock_supervisor.workers)

    @patch("builtins.input", side_effect=["worker", "Daniel1"])
    @patch("main.save_organization")
    def test_handle_transfer_worker(self, mock_save_organization, mock_input):
        main.handle_transfer(self.mock_president)
        self.assertNotIn(self.mock_worker, self.mock_supervisor.workers)

    def test_check_employee_name_uniqueness(self):
        main.employee_names_used = {"Daniel1"}
        self.assertFalse(main.check_employee_name_uniqueness("Daniel1"))
        self.assertTrue(main.check_employee_name_uniqueness("New Worker"))


if __name__ == "__main__":
    unittest.main()
