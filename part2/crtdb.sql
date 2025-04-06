-- crtdb.sql

DROP TABLE IF EXISTS ClassAttendance;
DROP TABLE IF EXISTS Membership;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS Instructor;
DROP TABLE IF EXISTS Equipment;

CREATE TABLE Member (
    memberId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dob DATE NOT NULL,
    phone TEXT,
    email TEXT
);

CREATE TABLE Membership (
    membershipId INTEGER PRIMARY KEY,
    memberId INTEGER,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    FOREIGN KEY (memberId) REFERENCES Member(memberId)
);

CREATE TABLE Instructor (
    instructorId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
);

CREATE TABLE Class (
    classId INTEGER PRIMARY KEY,
    className TEXT NOT NULL,
    classType TEXT NOT NULL,
    duration INTEGER NOT NULL,
    capacity INTEGER NOT NULL,
    instructorId INTEGER,
    FOREIGN KEY (instructorId) REFERENCES Instructor(instructorId)
);

CREATE TABLE ClassAttendance (
    attendanceId INTEGER PRIMARY KEY,
    memberId INTEGER,
    classId INTEGER,
    attendanceDate DATE,
    FOREIGN KEY (memberId) REFERENCES Member(memberId),
    FOREIGN KEY (classId) REFERENCES Class(classId)
);

CREATE TABLE Equipment (
    equipmentId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    purchaseDate DATE
);
