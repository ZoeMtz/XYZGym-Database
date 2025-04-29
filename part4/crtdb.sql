DROP TABLE IF EXISTS Attends;
DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Equipment;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS Instructor;
DROP TABLE IF EXISTS GymFacility;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS MembershipPlan;

CREATE TABLE Member (
    memberId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    address TEXT,
    age INTEGER CHECK(age >= 15),
    membershipStartDate TEXT NOT NULL,
    membershipEndDate TEXT NOT NULL,
    CHECK (membershipEndDate >= membershipStartDate)
);

CREATE TABLE Instructor (
    instructorId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT,
    phone TEXT,
    email TEXT
);

CREATE TABLE GymFacility (
    gymId INTEGER PRIMARY KEY AUTOINCREMENT,
    managerId INTEGER,
    location TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE Equipment (
    equipmentId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT CHECK(type IN ('Cardio', 'Strength', 'Flexibility', 'Recovery')),
    quantity INTEGER CHECK(quantity >= 0),
    gymId INTEGER,
    FOREIGN KEY (gymId) REFERENCES GymFacility(gymId) ON DELETE SET NULL
);

CREATE TABLE Class (
    classId INTEGER PRIMARY KEY AUTOINCREMENT,
    className TEXT NOT NULL,
    classType TEXT CHECK(classType IN ('Yoga', 'Zumba', 'HIIT', 'Weights')),
    duration INTEGER CHECK(duration > 0),
    classCapacity INTEGER CHECK(classCapacity > 0),
    instructorId INTEGER,
    gymId INTEGER,
    FOREIGN KEY (instructorId) REFERENCES Instructor(instructorId) ON DELETE SET NULL,
    FOREIGN KEY (gymId) REFERENCES GymFacility(gymId) ON DELETE SET NULL
);

CREATE TABLE MembershipPlan (
    planId INTEGER PRIMARY KEY AUTOINCREMENT,
    planType TEXT CHECK(planType IN ('Monthly', 'Annual')),
    cost REAL CHECK(cost >= 0)
);

CREATE TABLE Payment (
    paymentId INTEGER PRIMARY KEY AUTOINCREMENT,
    memberId INTEGER NOT NULL,
    planId INTEGER NOT NULL,
    amountPaid REAL CHECK(amountPaid >= 0),
    paymentDate TEXT NOT NULL,
    FOREIGN KEY (memberId) REFERENCES Member(memberId) ON DELETE CASCADE,
    FOREIGN KEY (planId) REFERENCES MembershipPlan(planId) ON DELETE CASCADE
);

CREATE TABLE Attends (
    attendanceId INTEGER PRIMARY KEY AUTOINCREMENT,
    memberId INTEGER NOT NULL,
    classId INTEGER NOT NULL,
    attendanceDate TEXT NOT NULL,
    FOREIGN KEY (memberId) REFERENCES Member(memberId) ON DELETE CASCADE,
    FOREIGN KEY (classId) REFERENCES Class(classId) ON DELETE CASCADE
);
