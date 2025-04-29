
-- Sample Members
INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate) VALUES
('Alice Smith', 'alice@example.com', '1234567890', '123 Elm St', 28, '2024-01-01', '2024-12-31'),
('Bob Johnson', 'bob@example.com', '2345678901', '456 Oak St', 35, '2024-02-01', '2025-01-31');

-- Sample Instructors
INSERT INTO Instructor (name, specialty, phone, email) VALUES
('John Trainer', 'HIIT', '1112223333', 'john@xyzgym.com'),
('Sarah Coach', 'Yoga', '4445556666', 'sarah@xyzgym.com');

-- Sample Gym Facilities
INSERT INTO GymFacility (managerId, location, phone) VALUES
(1, 'Downtown Gym', '5551234567'),
(2, 'Westside Gym', '5557654321');

-- Sample Equipment
INSERT INTO Equipment (name, type, quantity, gymId) VALUES
('Treadmill', 'Cardio', 5, 1),
('Dumbbells', 'Strength', 10, 1),
('Yoga Mats', 'Flexibility', 20, 2);

-- Sample Classes
INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId) VALUES
('Morning Yoga', 'Yoga', 60, 15, 2, 1),
('Evening HIIT', 'HIIT', 45, 10, 1, 2);

-- Sample Membership Plans
INSERT INTO MembershipPlan (planType, cost) VALUES
('Monthly', 50.00),
('Annual', 500.00);

-- Sample Payments
INSERT INTO Payment (memberId, planId, amountPaid, paymentDate) VALUES
(1, 1, 50.00, '2024-01-01'),
(2, 2, 500.00, '2024-02-01');

-- Sample Attendance
INSERT INTO Attends (memberId, classId, attendanceDate) VALUES
(1, 1, '2024-04-01'),
(2, 2, '2024-04-02');
