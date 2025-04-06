import sqlite3
import sys
from datetime import datetime, timedelta

def connect_db():
    return sqlite3.connect("XYZGym.sqlite")

def get_class_attendance(class_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name FROM Member m
            JOIN ClassAttendance ca ON m.memberId = ca.memberId
            WHERE ca.classId = ?;
        """, (class_id,))
        rows = cursor.fetchall()
        print("Members attending class", class_id)
        for row in rows:
            print("-", row[0])

def list_equipment_by_type(equipment_type):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM Equipment
            WHERE type = ?;
        """, (equipment_type,))
        rows = cursor.fetchall()
        print("Equipment of type:", equipment_type)
        for row in rows:
            print("-", row[0])

def expired_memberships():
    today = datetime.today().strftime('%Y-%m-%d')
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name FROM Member m
            JOIN Membership ms ON m.memberId = ms.memberId
            WHERE ms.endDate < ?;
        """, (today,))
        rows = cursor.fetchall()
        print("Members with expired memberships:")
        for row in rows:
            print("-", row[0])

def classes_by_instructor(instructor_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.name, i.phone, c.className, c.classType, c.duration, c.capacity
            FROM Instructor i
            JOIN Class c ON i.instructorId = c.instructorId
            WHERE i.instructorId = ?;
        """, (instructor_id,))
        rows = cursor.fetchall()
        print("Classes taught by instructor", instructor_id)
        for row in rows:
            print(f"Instructor: {row[0]}, Phone: {row[1]}, Class: {row[2]}, Type: {row[3]}, Duration: {row[4]} mins, Capacity: {row[5]}")

def average_member_ages():
    today = datetime.today().strftime('%Y-%m-%d')
    with connect_db() as conn:
        cursor = conn.cursor()

        # Active members
        cursor.execute("""
            SELECT dob FROM Member
            WHERE memberId IN (
                SELECT memberId FROM Membership WHERE endDate >= ?
            );
        """, (today,))
        active = cursor.fetchall()

        # Expired members
        cursor.execute("""
            SELECT dob FROM Member
            WHERE memberId IN (
                SELECT memberId FROM Membership WHERE endDate < ?
            );
        """, (today,))
        expired = cursor.fetchall()

        def avg_age(dobs):
            total = 0
            for (dob,) in dobs:
                age = (datetime.today() - datetime.strptime(dob, "%Y-%m-%d")).days // 365
                total += age
            return total / len(dobs) if dobs else 0

        print("Average age of active members:", round(avg_age(active), 2))
        print("Average age of expired members:", round(avg_age(expired), 2))

def top_instructors():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.name, COUNT(c.classId) as total_classes
            FROM Instructor i
            JOIN Class c ON i.instructorId = c.instructorId
            GROUP BY i.instructorId
            ORDER BY total_classes DESC
            LIMIT 3;
        """)
        rows = cursor.fetchall()
        print("Top 3 instructors by number of classes taught:")
        for row in rows:
            print(f"{row[0]}: {row[1]} classes")

def members_attended_all_of_type(class_type):
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT classId FROM Class WHERE classType = ?;", (class_type,))
        target_classes = {row[0] for row in cursor.fetchall()}

        cursor.execute("SELECT DISTINCT memberId FROM ClassAttendance;")
        member_ids = [row[0] for row in cursor.fetchall()]
        qualified = []

        for mid in member_ids:
            cursor.execute("SELECT classId FROM ClassAttendance WHERE memberId = ?;", (mid,))
            attended = {row[0] for row in cursor.fetchall()}
            if target_classes.issubset(attended):
                cursor.execute("SELECT name FROM Member WHERE memberId = ?;", (mid,))
                qualified.append(cursor.fetchone()[0])

        print(f"Members who attended all classes of type '{class_type}':")
        for name in qualified:
            print("-", name)

def recent_attendance_summary():
    today = datetime.today()
    one_month_ago = today - timedelta(days=30)
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name, c.className, c.classType
            FROM ClassAttendance ca
            JOIN Member m ON m.memberId = ca.memberId
            JOIN Class c ON c.classId = ca.classId
            WHERE attendanceDate >= ?;
        """, (one_month_ago.strftime('%Y-%m-%d'),))
        rows = cursor.fetchall()

        summary = {}
        for name, className, classType in rows:
            if name not in summary:
                summary[name] = {'classes': set(), 'types': set()}
            summary[name]['classes'].add(className)
            summary[name]['types'].add(classType)

        print("Recent Class Attendance:")
        print("Member Name | Total Classes | Classes Attended | Class Types")
        print("="*80)
        for name, data in summary.items():
            print(f"{name:<12} | {len(data['classes']):<14} | {', '.join(data['classes'])} | {', '.join(data['types'])}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python gym_queries.py <option> [args...]")
        return

    option = sys.argv[1]

    if option == "3":
        get_class_attendance(sys.argv[2])
    elif option == "4":
        list_equipment_by_type(sys.argv[2])
    elif option == "5":
        expired_memberships()
    elif option == "6":
        classes_by_instructor(sys.argv[2])
    elif option == "7":
        average_member_ages()
    elif option == "8":
        top_instructors()
    elif option == "9":
        members_attended_all_of_type(sys.argv[2])
    elif option == "10":
        recent_attendance_summary()
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
