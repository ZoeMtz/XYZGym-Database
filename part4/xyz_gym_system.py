import sqlite3
import sys
import datetime

DB_FILE = ""

def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_input(prompt, default=None):
    val = input(prompt).strip()
    return val if val else default

def valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

def validate_enum(value, allowed):
    return value in allowed

# ---------- Members ----------
def list_members():
    db = connect()
    rows = db.execute("SELECT * FROM Member").fetchall()
    db.close()
    for r in rows: print(dict(r))

def add_member():
    print("\n[ Add Member ]")
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    address = input("Address: ").strip()
    age = int(input("Age: "))
    start = input("Membership Start Date (YYYY-MM-DD): ")
    end = input("Membership End Date (YYYY-MM-DD): ")
    if age < 15 or not valid_date(start) or not valid_date(end) or end < start:
        print("Invalid input.")
        return
    db = connect()
    db.execute("""INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (name, email, phone, address, age, start, end))
    db.commit()
    db.close()
    print("✓ Member added.\n")

# ---------- Membership Plan ----------
def list_plans():
    db = connect()
    rows = db.execute("SELECT * FROM MembershipPlan").fetchall()
    db.close()
    for r in rows: print(dict(r))

def add_plan():
    planType = input("Plan Type (Monthly/Annual): ")
    cost = float(input("Cost: "))
    if planType not in ["Monthly", "Annual"]:
        print("Invalid plan type.")
        return
    db = connect()
    db.execute("INSERT INTO MembershipPlan (planType, cost) VALUES (?, ?)", (planType, cost))
    db.commit()
    db.close()
    print("✓ Plan added.")

# ---------- Instructors ----------
def list_instructors():
    db = connect()
    rows = db.execute("SELECT * FROM Instructor").fetchall()
    db.close()
    for r in rows: print(dict(r))

# ---------- Classes ----------
def list_classes():
    db = connect()
    rows = db.execute("SELECT * FROM Class").fetchall()
    db.close()
    for r in rows: print(dict(r))

def class_attendance_counts():
    db = connect()
    rows = db.execute("""
        SELECT C.classId, C.className, COUNT(A.memberId) AS attendees
        FROM Class C
        LEFT JOIN Attends A ON C.classId = A.classId
        GROUP BY C.classId, C.className
    """).fetchall()
    db.close()
    print("\n-- Class Attendance --")
    for r in rows:
        print(f"{r['classId']} | {r['className']} | {r['attendees']} attendee(s)")

def add_class():
    name = input("Class Name: ")
    ctype = input("Type (Yoga/Zumba/HIIT/Weights): ")
    duration = int(input("Duration (min): "))
    capacity = int(input("Capacity: "))
    instructorId = input("Instructor ID: ")
    gymId = input("Gym ID: ")
    db = connect()
    db.execute("""INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId)
                  VALUES (?, ?, ?, ?, ?, ?)""",
                  (name, ctype, duration, capacity, instructorId, gymId))
    db.commit()
    db.close()
    print("✓ Class added.")

def update_class():
    list_classes()
    cid = input("Class ID to update: ")
    db = connect()
    row = db.execute("SELECT * FROM Class WHERE classId=?", (cid,)).fetchone()
    if not row:
        print("Class not found.")
        return
    name = get_input(f"Name ({row['className']}): ", row['className'])
    ctype = get_input(f"Type ({row['classType']}): ", row['classType'])
    dur = get_input(f"Duration ({row['duration']}): ", row['duration'])
    cap = get_input(f"Capacity ({row['classCapacity']}): ", row['classCapacity'])
    iid = get_input(f"Instructor ID ({row['instructorId']}): ", row['instructorId'])
    gid = get_input(f"Gym ID ({row['gymId']}): ", row['gymId'])
    db.execute("""UPDATE Class SET className=?, classType=?, duration=?, classCapacity=?, instructorId=?, gymId=?
                  WHERE classId=?""", (name, ctype, dur, cap, iid, gid, cid))
    db.commit()
    db.close()
    print("✓ Class updated.")

def delete_class():
    list_classes()
    cid = input("Class ID to delete: ")
    db = connect()
    count = db.execute("SELECT COUNT(*) FROM Attends WHERE classId=?", (cid,)).fetchone()[0]
    if count > 0:
        print(f"Class has {count} registered members.")
        new_cid = input("Move members to which new class ID? ")
        db.execute("UPDATE Attends SET classId=? WHERE classId=?", (new_cid, cid))
    db.execute("DELETE FROM Class WHERE classId=?", (cid,))
    db.commit()
    db.close()
    print("✓ Class deleted.")

def find_members_by_class():
    cid = input("Enter Class ID: ")
    db = connect()
    rows = db.execute("""
        SELECT M.memberId, M.name
        FROM Member M
        JOIN Attends A ON M.memberId = A.memberId
        WHERE A.classId = ?
    """, (cid,)).fetchall()
    db.close()
    print(f"\n-- Members in Class {cid} --")
    for r in rows:
        print(f"{r['memberId']}: {r['name']}")

# ---------- Equipment ----------
def list_equipment():
    db = connect()
    rows = db.execute("SELECT * FROM Equipment").fetchall()
    db.close()
    for r in rows: print(dict(r))

def add_equipment():
    name = input("Name: ")
    etype = input("Type (Cardio/Strength/Flexibility/Recovery): ")
    qty = int(input("Quantity: "))
    gymId = input("Gym ID: ")
    db = connect()
    db.execute("INSERT INTO Equipment (name, type, quantity, gymId) VALUES (?, ?, ?, ?)", (name, etype, qty, gymId))
    db.commit()
    db.close()

def update_equipment():
    list_equipment()
    eid = input("Equipment ID: ")
    db = connect()
    row = db.execute("SELECT * FROM Equipment WHERE equipmentId=?", (eid,)).fetchone()
    if not row:
        print("Not found.")
        return
    name = get_input(f"Name ({row['name']}): ", row['name'])
    etype = get_input(f"Type ({row['type']}): ", row['type'])
    qty = get_input(f"Quantity ({row['quantity']}): ", row['quantity'])
    gymId = get_input(f"Gym ID ({row['gymId']}): ", row['gymId'])
    db.execute("UPDATE Equipment SET name=?, type=?, quantity=?, gymId=? WHERE equipmentId=?",
               (name, etype, qty, gymId, eid))
    db.commit()
    db.close()
    print("✓ Equipment updated.")

def delete_equipment():
    list_equipment()
    eid = input("Equipment ID to delete: ")
    db = connect()
    db.execute("DELETE FROM Equipment WHERE equipmentId=?", (eid,))
    db.commit()
    db.close()
    print("✓ Equipment deleted.")

# ---------- Main Menu ----------
def main_menu():
    while True:
        print("\n=== XYZ Gym Management ===")
        print("[1] Members")
        print("[2] Membership Plans")
        print("[3] Instructors")
        print("[4] Classes")
        print("[5] Attendance & Reports")
        print("[6] Equipment")
        print("[0] Exit")
        cmd = input("> ")
        if cmd == '1':
            list_members(); add_member()
        elif cmd == '2':
            list_plans(); add_plan()
        elif cmd == '3':
            list_instructors()
        elif cmd == '4':
            class_menu()
        elif cmd == '5':
            attendance_reports()
        elif cmd == '6':
            equipment_menu()
        elif cmd == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

# ---------- Class Submenu ----------
def class_menu():
    while True:
        print("\n-- Class Menu --")
        print("[1] List Classes")
        print("[2] Add Class")
        print("[3] Update Class")
        print("[4] Delete Class")
        print("[5] Find Members by Class")
        print("[6] Attendance Count Per Class")
        print("[0] Back")
        ch = input("> ")
        if ch == '1': list_classes()
        elif ch == '2': add_class()
        elif ch == '3': update_class()
        elif ch == '4': delete_class()
        elif ch == '5': find_members_by_class()
        elif ch == '6': class_attendance_counts()
        elif ch == '0': break

# ---------- Equipment Submenu ----------
def equipment_menu():
    while True:
        print("\n-- Equipment Menu --")
        print("[1] List Equipment")
        print("[2] Add Equipment")
        print("[3] Update Equipment")
        print("[4] Delete Equipment")
        print("[0] Back")
        ch = input("> ")
        if ch == '1': list_equipment()
        elif ch == '2': add_equipment()
        elif ch == '3': update_equipment()
        elif ch == '4': delete_equipment()
        elif ch == '0': break

# ---------- Attendance Menu ----------
def attendance_reports():
    while True:
        print("\n-- Attendance Reports --")
        print("[1] Attendance Count Per Class")
        print("[2] Find Members by Class")
        print("[0] Back")
        ch = input("> ")
        if ch == '1': class_attendance_counts()
        elif ch == '2': find_members_by_class()
        elif ch == '0': break

# ---------- Start ----------
def startup():
    global DB_FILE
    DB_FILE = input("Enter SQLite database filename (e.g., xyz_gym.db): ").strip()
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.close()
        print(f"✓ Connected to {DB_FILE}\n")
        main_menu()
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == '__main__':
    startup()
