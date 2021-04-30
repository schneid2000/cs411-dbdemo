"""Defines all the functions related to the database"""
from app import db
import hashlib

#What needs to be done with the database

#Use hashing for login
#Returns true if the hashed password matches the stored hash for the user, false otherwise
def verify_login(username, password):
    conn = db.connect()
    if not safe_input(username):
        return False
    query = 'SELECT Password FROM Student WHERE NetID = "{}";'.format(username)
    query_results = conn.execute(query).fetchall()
    conn.close()
    #Would be a weird issue, but return none to be safe if duplicates
    if len(query_results) != 1:
        return False

    hashed_pass = query_results[0]
    hasher = hashlib.sha3_256
    hasher.update(password.encode())
    if hasher.hexdigest() == hashed_pass:
        return True

    return False

def verify_hashed_login(username, hashed_pass):
    conn = db.connect()
    if not safe_input(username):
        return False
    query = 'SELECT Hashed FROM Student WHERE NetID = "{}";'.format(username)
    query_results = conn.execute(query).fetchall()
    conn.close()
    #Would be a weird issue, but return none to be safe if duplicates
    if len(query_results) != 1:
        return False

    password = query_results[0][0]
    print(type(password))
    print(password)
    print(hashed_pass)

    if hashed_pass == password:
        print("Correct password")
        return True

    print("Incorrect password")
    return False


#Returns true if the input contains 0 unsafe chars, false otherwise
def safe_input(input):
    unsafe_chars = ["'", '"', '/', '#', ';']
    if type(input) != str:
        return True

    for val in input:
        if val in unsafe_chars:
            return False
    return True


#Create a new user
#Returns true if the operation was successful, false otherwise
def create_user(netid, major, password):
    if not safe_input(netid) or not safe_input(major) or not safe_input(password):
        return False

    #hasher = hashlib.sha3_256
    #hasher.update(password.encode())
    #hashed_pass = hasher.hexdigest()

    conn = db.connect()
    query = 'INSERT INTO Student (NetID, Major, Password, Hashed) VALUES ("{}", "{}", 12345, "{}")'.format(netid, major, password)

    #Not sure how to check if there was an error in the query but that would go here

    conn.execute(query)
    conn.close()
    return True


def set_favorite_schedule(netid, scheduleid):
    if not safe_input(netid) or not safe_input(scheduleid):
        return False
    conn = db.connect()
    query = 'UPDATE Student SET FavoriteSchedule = {} WHERE NetID = "{}"'.format(scheduleid, netid)
    query_results = conn.execute(query).fetchall()
    conn.close()
    return True

def create_schedule(netid):
    if not safe_input(netid):
        print("not safe input (create_schedule)")
        return False
    conn = db.connect()
    query = 'SELECT MAX(ScheduleID) FROM Schedule ORDER BY ScheduleID'
    query_results = conn.execute(query).fetchall()
    max_val = int(query_results[0][0])
    new_val = max_val + 1
    query = 'INSERT INTO Schedule (ScheduleID, Student) VALUES ({}, "{}")'.format(new_val, netid)
    conn.execute(query)
    conn.close()

    return True

def link_schedule(netid, scheduleid):
    if not safe_input(netid) or not safe_input(scheduleid):
        return False
    conn = db.connect()
    query = 'INSERT INTO SavedSchedule (NetID, ScheduleID) VALUES ("{}", {})'.format(netid, scheduleid)
    query_results = conn.execute(query).fetchall()
    conn.close()
    return True

#Returns uncompleted prereq CRNs, returns None if all prereqs are taken
def check_course_for_prereq(crn, netid):
    if not safe_input(netid) or not safe_input(crn):
        return False
    conn = db.connect()
    query = 'SELECT PrereqCRN FROM SELECT CRN FROM CoursesTaken WHERE NetID = {} as taken, SELECT PrereqCRN FROM Prereqs WHERE ClassCRN = {} as required WHERE PrereqCRN NOT IN taken'.format(netid, crn)
    query_results = conn.execute(query).fetchall()
    conn.close()

    #The query will return a row for each uncompleted prereq
    if len(query_results) > 0:
        prereqs = []
        for row in query_results:
            crn = row[0]
            prereqs.append(crn)
        return prereqs

    return None

#Returns a course given a subject, number, or both
#Returns just the CRN for now
def fetch_course_by_subject(subject):
    return fetch_course_by_subject_number(subject, -1)

def fetch_course_by_number(number):
    return fetch_course_by_subject_number("", number)

def fetch_course_by_subject_number(subject, number):
    use_subject = not (subject == "")
    use_number = not (number == -1)
    if not safe_input(subject) or not safe_input(number):
        return False
    conn = db.connect()
    query = ""
    if use_subject and use_number:
        query = 'SELECT CRN FROM Class WHERE Subject = "{}" AND Number = {}'.format(subject, number)
    elif use_subject and not use_number:
        query = 'SELECT CRN FROM Class WHERE Subject = "{}"'.format(subject)
    elif not use_subject and use_number:
        query = 'SELECT CRN FROM Class WHERE Number = {}'.format(number)
    else:
        return None
    query_results = conn.execute(query).fetchall()
    conn.close()
    if len(query_results) == 0:
        return None

    output = []
    for row in query_results:
        output.append(row[0])

    return output


#Returns a class from a CRN
#Just returns the CRN for now, will include more details later
def fetch_course_by_crn(crn):
    if not safe_input(crn):
        return False

    conn = db.connect()
    query = 'SELECT CRN FROM Class WHERE CRN = {}'.format(crn)
    query_results = conn.execute(query).fetchall()
    conn.close()
    if len(query_results) != 1:
        return None

    return query_results[0][0]


#Add a friend to the Pending Friend list
def add_pending_friend(requestnetid, pendingnetid):
    if not safe_input(requestnetid) or not safe_input(pendingnetid):
        return False

    conn = db.connect()
    query = 'INSERT INTO PendingFriends (FriendNetID, FriendsWithNetID) VALUES ("{}", "{}")'.format(requestnetid, pendingnetid)
    query_results = conn.execute(query).fetchall()
    conn.close()

    return True

def del_friend_request(netid, requesternetid):
    if not safe_input(netid) or not safe_input(requesternetid):
        return False

    conn = db.connect()
    query = 'DELETE FROM PendingFriends WHERE FriendNetID = "{}" AND FriendsWithNetID = "{}"'.format(requesternetid, netid)
    query_results = conn.execute(query).fetchall()
    conn.close()

    return True

def eval_friend_request(firstnetid, secondnetid):
    if not safe_input(firstnetid) or not safe_input(secondnetid):
        return False

    conn = db.connect()
    query = 'SELECT * FROM PendingFriends WHERE FriendNetID = "{}" AND FriendsWithNetID = "{}"'.format(firstnetid, secondnetid)
    query_results = conn.execute(query).fetchall()
    query = 'SELECT * FROM PendingFriends WHERE FriendNetID = "{}" AND FriendsWithNetID = "{}"'.format(secondnetid, firstnetid)
    query_results_2 = conn.execute(query).fetchall()
    if len(query_results) == 1 and len(query_results_2) == 1:
        query = 'INSERT INTO Friends (FriendNetID, FriendsWithNetID) VALUES ("{}","{}")'.format(firstnetid, secondnetid)
        conn.execute(query)
        query = 'INSERT INTO Friends (FriendNetID, FriendsWithNetID) VALUES ("{}","{}")'.format(secondnetid, firstnetid)
        conn.execute(query)
        conn.close()
        return True
    conn.close()
    return False

def add_course_taken(netid, crn):
    if not safe_input(netid) or not safe_input(crn):
        return False

    conn = db.connect()
    query = 'INSERT INTO CoursesTaken (NetID, CRN) VALUES ("{}", {})'.format(netid, crn)
    conn.execute(query)
    conn.close()

    return True

def add_course_to_schedule(scheduleid, crn):
    if not safe_input(scheduleid) or not safe_input(crn):
        return False

    conn = db.connect()
    query = 'INSERT INTO WithinSchedule (ScheduleID, CRN) VALUES ({}, {})'.format(scheduleid, crn)
    conn.execute(query)
    conn.close()

    return True

def add_constraint_to_schedule(scheduleid, constraintid):
    if not safe_input(scheduleid) or not safe_input(crn):
        return False

    conn = db.connect()
    query = 'INSERT INTO ScheduleConstraints (ScheduleID, ConstraintID) VALUES ({}, {})'.format(scheduleid, constraintid)
    conn.execute(query)
    conn.close()

    return True

#Returns true if the selected major exists
def validate_major(major):
    if not safe_input(major):
        return False

    conn = db.connect()
    query = 'SELECT * FROM MajorRequirements WHERE Major = "{}"'.format(major)
    query_results = conn.execute(query).fetchall()
    conn.close()
    if len(query_results) == 0:
        return False

    return True

#Fetch the CRNs associated with a given requirement
def show_req_courses(reqid):
    if not safe_input(reqid):
        print("reqid was not safe (show_req_courses)")
        return None

    conn = db.connect()
    query = 'SELECT CRN FROM CourseReqs WHERE ReqID = {}'.format(reqid)
    query_results = conn.excute(query).fetchall()
    conn.close()
    results = []
    for result in query_results:
        course = {
            "crn": result[0]
        }
        results.append(course)
    return results


#Fetch relevant course details given a crn
#This will probably break because of how numbers work in mysql
def show_details_by_crn(crn):
    if not safe_input(crn):
        print("crn was not safe (show_details_by_crn)")
        return None

    conn = db.connect()
    query = 'SELECT CRN, Subject, Number, Title, Type, Section, Time, EndTime, Days, Location FROM Class WHERE CRN = {}'.format(crn)
    query_results = conn.execute(query).fetchall()
    conn.close()
    results = []
    for result in query_results:
        course_details = {
            "crn": result[0],
            "class": result[1] + " " + str(result[2]),
            "title": result[3],
            "type": result[4],
            "section": result[5],
            "time": str(result[6]) + "-" + str(result[7]),
            "day": result[8],
            "location": result[9]
        }
        results.append(course_details)
    return results


def debug_query_results(query_results):
    print("This query returned", len(query_results), "rows")

#Create a new time constraint
def create_time_constraint(scheduleid, constraintid, start_time, end_time):
    if not safe_input(start_time) or not safe_input(end_time):
        print("start_time or end_time were not safe (create_time_constraint)")
        return False

    conn = db.connect()
    query = 'INSERT INTO Constraints (ConstraintID, ScheduleID, StartTime, EndTime, Days) VALUES ({}, {}, {}, {}, "MTWRF")'.format(constraintid, scheduleid, start_time, end_time)
    query_results = conn.execute(query).fetchall()
    conn.close()

    return True

def delete_time_constraint(scheduleid, constraintid):
    if not safe_input(scheduleid) or not safe_input(constraintid):
        print("Not safe input (delete_time_constraint)")
        return False

    conn = db.connect()
    query = 'DELETE FROM Constraints WHERE ConstraintID = {} AND ScheduleID = {}'.format(constraintid, scheduleid)
    query_results = conn.execute(query).fetchall()
    conn.close()

    return True

#Filter out courses by a searched phrase in the title
def filter_courses_by_title(prev_results, filter_substring):
    results = []
    for prev_result in prev_results:
        if "title" not in prev_result:
            print("title not found in previous result object")
            return None

        course_title = prev_result["title"]
        if filter_substring.lower() in course_title.lower():
            results.append(prev_result)

    return results

#Filter out courses by a given subject
def filter_courses_by_subject(prev_results, subject):
    results = []
    for prev_result in prev_results:
        if "class" not in prev_result:
            print("class not found in previous result object")
            return None

        course = prev_result["class"]
        if subject.lower() in course.lower():
            results.append(prev_result)

    return results

#Fetch schedules
def fetch_schedules(netid):
    if not safe_input(netid):
        print("not safe input (fetch_schedules)")
        return None

    conn = db.connect()
    query = 'SELECT ScheduleName, IsFavorite, TotalCredits, ScheduleID FROM Schedule WHERE Student like "{}"'.format(netid)
    query_results = conn.execute(query).fetchall()
    conn.close()
    results = []
    for result in query_results:
        schedule_data = {
            "name": result[0],
            "is_favorite": result[1],
            "total_credits": result[2],
            "schedule_id": result[3]
        }
        results.append(schedule_data)
    return results


def fetch_friend_schedules(netid):
    if not safe_input(netid):
        print("not safe input (fetch_schedules)")
        return None

    conn = db.connect()
    query = 'SELECT ScheduleName, TotalCredits, Student, ScheduleID FROM Schedule WHERE Schedule.Student IN (SELECT FriendsWithNetID From Friends WHERE FriendNetID = "{}" AND IsFavorite = 1)'.format(netid)
    query_results = conn.execute(query).fetchall()
    conn.close()
    results = []
    for result in query_results:
        schedule_data = {
            "name": result[0],
            "total_credits": result[1],
            "friend_netID": result[2],
            "schedule_ID": result[3]
        }
        results.append(schedule_data)
    return results

#Get the crns associated with a given schedule
def fetch_courses_by_schedule(scheduleid):
    if not safe_input(scheduleid):
        print("not safe input (fetch_courses_by_schedule)")
        return None

    conn = db.connect()
    query = 'SELECT CRN FROM WithinSchedule WHERE ScheduleID = {}'.format(scheduleid)
    query_results = conn.execute(query).fetchall()
    results = []
    for result in query_results:
        course = {
            "crn": result[0]
        }
        results.append(course)
    return results

#Get the requirements associated with the major of the student with the netid
def fetch_reqs_by_netid(netid):
    if not safe_input(netid):
        print("not safe input (fetch_reqs_by_netid)")
        return None

    conn = db.connect()
    query = 'SELECT Name FROM Requirement WHERE ReqID in (SELECT ReqID FROM InternalMajorReqs WHERE Major IN (SELECT Major FROM Student WHERE NetID = "{}"))'.format(netid)
    query_results = conn.execute(query).fetchall()
    conn.close()
    results = []
    for result in query_results:
        name = {
            "name": result[0]
        }
        results.append(name)
    return results

def fetch_time_constraints_by_schedule(scheduleid):
    if not safe_input(scheduleid):
        print("not safe input (fetch_time_constraints_by_schedule)")
        return None

    conn = db.connect()
    query = 'SELECT ConstraintID, StartTime, EndTime FROM Constraints WHERE ScheduleID = {}'.format(scheduleid)
    query_results = conn.execute(query).fetchall()
    conn.close()
    results = []
    for result in query_results:
        cid = result[0]
        stime = result[1]
        etime = result[2]
        tcstr = str(stime) + "-" + str(etime)
        results.append(tcstr)
    return results

def fetch_course_by_req(reqid):
    if not safe_input(reqid):
        print("not safe input (fetch_req_by_id)")
        return None

    conn = db.connect()
    query = 'SELECT CRN FROM CourseReqs WHERE ReqID = {}'.format(reqid)
    query_results = conn.execute(query).fetchall()
    conn.close()
    results = []
    for result in query_results:
        course = {
            "crn": result[0]
        }
        results.append(course)
    return results

def is_student_in_db(netid):
    if not safe_input(netid):
        print("not safe input (is_student_in_db)")
        return False

    conn = db.connect()
    query = 'SELECT * FROM Student WHERE NetID = "{}"'.format(netid)
    query_results = conn.execute(query).fetchall()
    conn.close()
    if len(query_results) == 0:
        return False

    return True

#STAGE 4 DEPRECATED BELOW
#--------------------------------------------------------
# def fetch_reqs_by_name(reqname) -> dict:
#     """Reads all tasks listed in the todo table

#     Returns:
#         A list of dictionaries
#     """
#     conn = db.connect()
#     query = 'SELECT * FROM Requirement WHERE Name = "{}";'.format(reqname)
#     print(query)
#     query_results = conn.execute(query).fetchall()
#     conn.close()
#     todo_list = []
#     for result in query_results:
#         item = {
#             "id": result[0],
#             "name": result[1],
#             "numcredits": result[3],
#             "numcourses": result[2]
#         }
#         todo_list.append(item)
#     print(type(todo_list))
#     return todo_list

# def students_with_req(reqid) -> dict:
#     """Reads all tasks listed in the todo table

#     Returns:
#         A list of dictionaries
#     """
#     conn = db.connect()
#     query = 'SELECT NetID FROM (SELECT NetID, currentStatus.ReqID FROM (SELECT NetID, SUM(Credits) AS creditsToward, COUNT(CRN) AS numToward, ReqID FROM CourseReqs NATURAL JOIN CoursesTaken NATURAL JOIN Class GROUP BY NetID, ReqID) as currentStatus, (SELECT ReqID, ChooseN, RequiredCredits FROM Requirement) AS Required WHERE numToward >= Required.ChooseN AND creditsToward >= Required.RequiredCredits AND Required.ReqID = currentStatus.ReqID ORDER BY NetID, currentStatus.ReqID) as temp WHERE temp.ReqID = {};'.format(reqid)
#     print(query)
#     query_results = conn.execute(query).fetchall()
#     conn.close()
#     results = []
#     for result in query_results:
#         item = {
#             "netid": result[0]
#         }
#         results.append(item)
#     print(type(results))
#     return results

# def fetch_search_results():
#     return global_items

# def fetch_todo() -> dict:
#     conn = db.connect()
#     query_results = conn.execute("SELECT * FROM Requirement;").fetchall()
#     conn.close()
#     todo_list = []
#     for result in query_results:
#         item = {
#             "id": result[0],
#             "name": result[3],
#             "numcredits": result[1],
#             "numcourses": result[2]
#         }
#         todo_list.append(item)

#     return todo_list

# def edit_or_create(reqid, reqname, numcredits, numcourses):
#     print("Editing")
#     useCourses = True
#     useCredits = True
#     if numcourses == '':
#         useCourses = False
#     if numcredits == '':
#         useCredits = False


#     conn = db.connect()
#     # initial_results = conn.execute("SELECT MAX(ReqID) FROM Requirement")
#     # print(initial_results[0][0])
#     query_results = None
#     try:
#         query_results = conn.execute("SELECT * FROM Requirement WHERE ReqID = {};".format(reqid)).fetchall()
#     except:
#         print("Hello world!")

#     if (len(query_results)) == 0:
#         #Create the requirement
#         if useCourses and useCredits:
#             conn.execute("INSERT INTO Requirement VALUES ({}, '{}', {}, {});".format(reqid, reqname, numcourses, numcredits))
#         elif useCourses and not useCredits:
#             conn.execute("INSERT INTO Requirement VALUES ({}, '{}', {}, NULL);".format(reqid, reqname, numcourses))
#         elif useCredits and not useCourses:
#             conn.execute("INSERT INTO Requirement VALUES ({}, '{}', NULL, {});".format(reqid, reqname, numcredits))
#     else:
#         #Update the requirement
#         conn.execute("UPDATE Requirement SET Name = '{}' WHERE ReqID = {};".format(reqname, reqid))
#         if useCourses:
#             conn.execute("UPDATE Requirement SET ChooseN = {} WHERE ReqID = {};".format(numcourses, reqid))
#         if useCredits:
#             conn.execute("UPDATE Requirement SET RequiredCredits = {} WHERE ReqID = {};".format(numcredits, reqid))
#     conn.close()

# def delete(reqid):
#     conn = db.connect()
#     conn.execute("DELETE FROM Requirement WHERE ReqID = {}".format(reqid))
#     conn.close()

# def link(reqid, crn):
#     conn = db.connect()
#     conn.execute("INSERT INTO CourseReqs VALUES ({}, {});".format(crn, reqid))
#     conn.close()

# def update_task_entry(task_id: int, text: str) -> None:
#     """Updates task description based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated description

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


# def update_status_entry(task_id: int, text: str) -> None:
#     """Updates task status based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated status

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


# def insert_new_task(text: str) ->  int:
#     """Insert new task to todo table.

#     Args:
#         text (str): Task description

#     Returns: The task ID for the inserted entry
#     """

#     conn = db.connect()
#     query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
#         text, "Todo")
#     conn.execute(query)
#     query_results = conn.execute("Select LAST_INSERT_ID();")
#     query_results = [x for x in query_results]
#     task_id = query_results[0][0]
#     conn.close()

#     return task_id


# def remove_task_by_id(task_id: int) -> None:
#     """ remove entries based on task ID """
#     conn = db.connect()
#     query = 'Delete From tasks where id={};'.format(task_id)
#     conn.execute(query)
#     conn.close()
