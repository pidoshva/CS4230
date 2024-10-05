# CS4230
Software Test and Quality Engineering.  

Project #4

![Project_4-1](https://github.com/user-attachments/assets/5cdc815e-8714-4a37-9250-b48f1c3cb6a5)
![Project_4-2](https://github.com/user-attachments/assets/699caedc-60fb-47e2-a2d0-75f0840bc9da)

# Manual Tests for Validation

## 1. Organization Hierarchy Tests

### Test Case 1.1
**Verify that only one president can exist in the organization.**  
**Input:** Create an organization and hire a second president.  
**Expected Outcome:** An error message

### Test Case 1.2
**Verify that the president can hire up to two vice presidents.**  
**Input:** Hire two vice presidents.  
**Expected Outcome:** Both vice presidents are hired successfully.

### Test Case 1.3
**Verify that hiring a third vice president fails.**  
**Input:** Attempt to hire a third vice president.  
**Expected Outcome:** An error message indicating the limit has been reached.

### Test Case 1.4
**Verify that each vice president can oversee up to three supervisors.**  
**Input:** Hire three supervisors under one vice president.  
**Expected Outcome:** All supervisors are hired successfully.

### Test Case 1.5
**Verify that hiring a fourth supervisor fails under the same vice president.**  
**Input:** Attempt to hire a fourth supervisor.  
**Expected Outcome:** An error message indicating the limit has been reached.

### Test Case 1.6
**Verify that each supervisor can oversee up to five workers.**  
**Input:** Hire five workers under one supervisor.  
**Expected Outcome:** All workers are hired successfully.

### Test Case 1.7
**Verify that hiring a sixth worker fails under the same supervisor.**  
**Input:** Attempt to hire a sixth worker.  
**Expected Outcome:** An error message indicating the limit has been reached.

---

## 2. Employee Name Uniqueness Tests

### Test Case 2.1
**Verify that no two employees can have the same name.**  
**Input:** Hire two workers with the same name.  
**Expected Outcome:** An error message indicating the name is already taken.

---

## 3. Hiring Tests

### Test Case 3.1
**Verify that an immediate supervisor can hire someone.**  
**Input:** A vice president hires a supervisor.  
**Expected Outcome:** The supervisor is hired successfully.

### Test Case 3.2
**Verify that an immediate supervisor cannot hire someone if there is no vacancy.**  
**Input:** Attempt to hire another supervisor when the limit is reached.  
**Expected Outcome:** An error message indicating no vacancy.

---

## 4. Firing Tests

### Test Case 4.1
**Verify that an employee can be fired by their immediate supervisor.**  
**Input:** A supervisor fires a worker.  
**Expected Outcome:** The worker is removed from the organization.

### Test Case 4.2
**Verify that the president cannot be fired.**  
**Input:** Attempt to fire the president.  
**Expected Outcome:** An error message indicating the president cannot be fired.

### Test Case 4.3
**Verify that firing leaves a vacancy.**  
**Input:** Fire a worker and check the supervisor’s list of workers.  
**Expected Outcome:** The worker is removed from the supervisor’s list.

---

## 5. Quitting Tests

### Test Case 5.1
**Verify that an employee can quit.**  
**Input:** A worker quits.  
**Expected Outcome:** The worker is removed from the organization.

### Test Case 5.2
**Verify that the president cannot quit.**  
**Input:** Attempt to quit the president.  
**Expected Outcome:** An error message indicating the president cannot quit.

---

## 6. Layoff Tests

### Test Case 6.1
**Verify that a laid-off worker can be moved to a comparable opening.**  
**Input:** Lay off a worker with a comparable position available.  
**Expected Outcome:** The worker is moved to the new position.

### Test Case 6.2
**Verify that if no comparable position is available, the worker remains in limbo (or similar logic).**  
**Input:** Lay off a worker with no available positions.  
**Expected Outcome:** An appropriate message indicating no placement available.

---

## 7. Transfer Tests

### Test Case 7.1
**Verify that a vice president can transfer a worker to another supervisor within their organization.**  
**Input:** A vice president transfers a worker from one supervisor to another.  
**Expected Outcome:** The worker is transferred successfully.

### Test Case 7.2
**Verify that a transfer fails if there is no vacancy in the destination.**  
**Input:** Attempt to transfer a worker to a position with no vacancy.  
**Expected Outcome:** An error message indicating no vacancy.

---

## 8. Promotion Tests

### Test Case 8.1
**Verify that a supervisor can promote a worker to a supervisor position.**  
**Input:** A supervisor promotes a worker.  
**Expected Outcome:** The worker is promoted successfully, and a vacancy is created in the worker's position.

### Test Case 8.2
**Verify that promotions cannot be made if there is no vacancy.**  
**Input:** Attempt to promote a worker when there’s no vacancy.  
**Expected Outcome:** An error message indicating no vacancy.

### Test Case 8.3
**Verify that a worker cannot be promoted to a position where they would supervise their former peers.**  
**Input:** Promote a worker who has peers in their previous group.  
**Expected Outcome:** An error message indicating the promotion is not valid.

---

## 9. File Input Tests

### Test Case 9.1
**Verify that the organization can be initialized from a file.**  
**Input:** Load the organization from a valid file.  
**Expected Outcome:** The organization is set up correctly as per the file’s contents.

### Test Case 9.2
**Verify error handling when loading from an invalid file.**  
**Input:** Attempt to load an invalid or improperly formatted file.  
**Expected Outcome:** An error message indicating the file cannot be loaded.

---

## 10. Display Tests

### Test Case 10.1
**Verify that the organization can be displayed correctly.**  
**Input:** Call the display function after several hires and promotions.  
**Expected Outcome:** The organization hierarchy is displayed correctly.

### Test Case 10.2
**Verify that vacancies are shown correctly.**  
**Input:** Fire a supervisor and check the display output.  
**Expected Outcome:** The display indicates the supervisor position is vacant.

### Test Case 10.3
**Verify that worker vacancies do not affect the supervisor display if the entire organization below is vacant.**  
**Input:** Fire all workers under a supervisor and display.  
**Expected Outcome:** The supervisor’s position does not show as vacant if all positions below are also vacant.
