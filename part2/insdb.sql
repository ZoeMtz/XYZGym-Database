-- insdb.sql

-- Members
INSERT INTO Member VALUES (1, 'Alice', '1995-04-10', '1234567890', 'alice@example.com');
INSERT INTO Member VALUES (2, 'Bob', '1990-06-15', '0987654321', 'bob@example.com');
INSERT INTO Member VALUES (3, 'Charlie', '1985-11-22', '5555555555', 'charlie@example.com');
INSERT INTO Member VALUES (4, 'Diana', '2000-01-01', '4444444444', 'diana@example.com');
INSERT INTO Member VALUES (5, 'Evan', '1992-09-09', '3333333333', 'evan@example.com');

-- Memberships
INSERT INTO Membership VALUES (1, 1, '2024-01-01', '2024-12-31');
INSERT INTO Membership VALUES (2, 2, '2023-01-01', '2023-12-31');
INSERT INTO Membership VALUES (3, 3, '2024-02-15', '2025-02-15');
INSERT INTO Membership VALUES (4, 4, '2023-05-01', '2024-05-01');
INSERT INTO Membership VALUES (5, 5, '2024-03-01', '2024-09-01');

-- Instructors
INSERT INTO Instructor VALUES (1, 'Coach A', '1111111111', 'a@gym.com');
INSERT INTO Instructor VALUES (2, 'Coach B', '2222222222', 'b@gym.com');
INSERT INTO Instructor VALUES (3, 'Coach C', '3333333333', 'c@gym.com');

-- Classes
INSERT INTO Class VALUES (1, 'Yoga', 'Flexibility', 60, 20, 1);
INSERT INTO Class VALUES (2, 'Zumba', 'Cardio', 45, 25, 2);
INSERT INTO Class VALUES (3, 'Body Pump', 'Strength', 50, 15, 1);
INSERT INTO Class VALUES (4, 'Pilates', 'Flexibility', 60, 10, 3);
INSERT INTO Class VALUES (5, 'HIIT', 'Cardio', 30, 20, 2);

-- Class Attendance
INSERT INTO ClassAttendance VALUES (1, 1, 1, '2024-03-01');
INSERT INTO ClassAttendance VALUES (2, 2, 2, '2024-03-03');
INSERT INTO ClassAttendance VALUES (3, 1, 3, '2024-03-05');
INSERT INTO ClassAttendance VALUES (4, 3, 4, '2024-03-07');
INSERT INTO ClassAttendance VALUES (5, 4, 5, '2024-03-09');

-- Equipment
INSERT INTO Equipment VALUES (1, 'Treadmill', 'Cardio', '2022-05-01');
INSERT INTO Equipment VALUES (2, 'Elliptical', 'Cardio', '2022-06-15');
INSERT INTO Equipment VALUES (3, 'Dumbbell Set', 'Strength', '2023-01-10');
INSERT INTO Equipment VALUES (4, 'Yoga Mats', 'Flexibility', '2023-03-20');
INSERT INTO Equipment VALUES (5, 'Kettlebells', 'Strength', '2023-08-08');
