""" Specifies routing for the application"""
from flask import render_template, request, jsonify, session
from app import app
from app import database as db_helper

#Something about session data
#View schedule page
@app.route("/view_schedule", methods=['POST', 'GET'])
@app.route("/view_schedule:<schedule_id>", methods=['POST', 'GET'])
@app.route("/view_schedule:<schedule_id>:<isFriends>")
def view_schedules(schedule_id=None, isFriends=0):
    print("view_schedules page")
    #Display the schedules of netid, the schedules of the friends of netid, and the classes in the schedule
    #assume we have some session variable called netid i guess
    data = request.get_json()
    course_data = []
    viewingName = ""
    totalCredits = 0
    if schedule_id is not None:
        crns = db_helper.fetch_courses_by_schedule(schedule_id)
        for crn in crns:
            course_data.append(db_helper.show_details_by_crn(crn))

        scheduleName = db_helper.get_schedule_name(schedule_id)

        totalCredits = db_helper.fetch_total_credits(schedule_id)

        if len(scheduleName) > 0 and len(scheduleName[0]) > 0:
            viewingName = scheduleName[0][0]


        print("COURSE DATA")
        print(course_data)

    student_schedules = []
    friend_schedules = []
    if "netid" in session:
        netid = session["netid"]
        student_schedules = db_helper.fetch_schedules(netid)
        friend_schedules = db_helper.fetch_friend_schedules(netid)

    sorted_course_data = []
    for i in range(5):
        sorted_course_data.append([])

    for course in course_data:
        split = course['time'].split('-')
        course['start_time'] = int(split[0])
        course['end_time'] = int(split[1])

        if 'M' in course['day']:
            sorted_course_data[0].append(course)
        if 'T' in course['day']:
            sorted_course_data[1].append(course)
        if 'W' in course['day']:
            sorted_course_data[2].append(course)
        if 'R' in course['day']:
            sorted_course_data[3].append(course)
        if 'F' in course['day']:
            sorted_course_data[4].append(course)

    hour_sorted_course_data = []
    for i in range(len(sorted_course_data)):
        newDay = sorted(sorted_course_data[i], key = lambda i: i['start_time'])
        hour_sorted_course_data.append(newDay)



    return render_template("View-Schedules.html", sched=student_schedules[:9], fsched=friend_schedules, cdata=course_data, viewID=schedule_id, viewName=viewingName, sortedCData=hour_sorted_course_data, tCredits=totalCredits, friendSchedule=isFriends)

@app.route("/delete:<schedule_id>:<crn>", methods=['POST', 'GET'])
def delete_class_from_schedule(schedule_id=None, crn=None):
    if schedule_id is None or crn is None:
        return view_schedules()

    db_helper.delete_class_from_schedule(schedule_id, crn)

    return view_schedules(schedule_id)


#Generate schedule page
@app.route("/gen_schedule", methods=['POST', 'GET'])
def gen_schedule():
    print("gen schedule page")
    #Display major reqs, time constraints, and resulting searches
    #Retrieve the requirements attached to the major of the student
    reqnames = []
    if 'netid' in session:
        netid = session['netid']
        reqnames = db_helper.fetch_reqs_by_netid(netid)
    #Display the current time constraints on the schedule
    data = request.get_json()
    tc = []
    if 'sid' in session:
        schedule_id = session['sid']
        tc = db_helper.fetch_time_constraints_by_schedule(schedule_id)

    rc = []
    #Display the filtered search results
    if data is not None:
        if 'req' in data:
            print(data['req'], 'req')
            reqid = data['req']
            session['req'] = reqid
        if 'filter_s' in data:
            session['filter_s'] = data['filter_s']
        if 'filter_t' in data:
            session['filter_t'] = data['filter_t']

    if data and 'req' in data and data['req'] == '' and (('filter_s' in data and data['filter_s'] != '') or ('filter_t' in data and data['filter_t'] != '')):
        session.pop('req', None)

    if data and ('filter_s' in data and data['filter_s'] != '') and ('filter_t' in data and data['filter_t'] == ''):
        session.pop('filter_t', None)

    if data and ('filter_s' in data and data['filter_s'] == '') and ('filter_t' in data and data['filter_t'] != ''):
        session.pop('filter_s', None)


    if 'req' in session:
        print(session['req'])
        rc = db_helper.fetch_course_by_req(session['req'])

    if 'filter_s' in session and session['filter_s']:
        print(session['filter_s'])
        rc = db_helper.fetch_courses_by_subject_like(session['filter_s'])

    if 'filter_t' in session and session['filter_t']:
        print(session['filter_t'])
        rc = db_helper.fetch_courses_by_title(session['filter_t'])


    rce = []
    for entry in rc:
        rce.append(db_helper.show_details_by_crn(entry))

    if 'filter_s' in session and session['filter_s']:
        print(session['filter_s'], 'filter_s')
        rce = db_helper.filter_courses_by_subject(rce, session['filter_s'])
    if 'filter_t' in session and session['filter_t']:
        print(session['filter_t'], 'filter_t')
        rce = db_helper.filter_courses_by_title(rce, session['filter_t'])

    if len(tc) != 0:
        print("tc")
        rce = db_helper.filter_courses_by_tc(rce, tc)


    #print(rce)
    return render_template("Generate-a-Schedule.html", reqs=reqnames, timec=tc, reqc=rce)

#Homepage
@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def home():
    print("homepage")
    netid = ""
    if "netid" in session:
        netid = session['netid']

    return render_template("Home.html", netid=netid)


#Add constraint button
@app.route("/add_constraint", methods=['POST'])
def add_constraint():
    print("adding constraint")
    result = {'success': False, 'response': 'create constraint unsuccessful'}
    data = request.get_json()
    if 'stime' in data and 'etime' in data:
        stime = int(data['stime'])
        etime = int(data['etime'])
        if 'sid' in session:
            scheduleid = session['sid']
            db_helper.create_time_constraint(scheduleid, stime, etime)
            result = {'success': True, 'response': 'create constraint successful'}

    return jsonify(result)

#Delete constraint button
@app.route("/delete_constraint", methods=['POST'])
def delete_constraint():
    print("deleting constraint")
    result = {'success': False, 'response': 'delete constraint unsuccessful'}
    data = request.get_json()
    if 'constraintid' in data:
        constraintid = data['constraintid']
        if 'sid' in session:
            scheduleid = session['sid']
            db_helper.delete_time_constraint(scheduleid, constraintid)
            result = {'success': True, 'response': 'delete constraint successful'}

    return jsonify(result)

#Login button
@app.route("/login", methods=['POST'])
def login():
    print("login request")
    result = {'success': False, 'response': 'Login unsuccessful'}
    data = request.get_json()
    if 'netid' in data and 'pw' in data:
        #Should be the hashed password, probably
        netid = data['netid']
        hashed_pass = data['pw']
        #Check if student in db
        existence = db_helper.is_student_in_db(netid)
        if not existence:
            print("creating user")
            #Create user and login
            major = data['mj']
            creation_status = db_helper.create_user(netid, major, hashed_pass)
            if creation_status == True:
                session['netid'] = netid
                result = {'success': True, 'response': 'Successfully created account'}

        else:
            print("logging in existing user")
            #Attempt login
            login_status = db_helper.verify_hashed_login(netid, hashed_pass)
            if login_status == True:
                session['netid'] = netid
                result = {'success': True, 'response': 'Successfully logged in'}

    return jsonify(result)

#Set favorite schedule
@app.route("/setfav", methods=['POST'])
def setfav():
    result = {'success': False, 'response': 'setfav unsuccessful'}
    data = request.get_json()
    netid = session['netid']
    if 'sid' in data:
        schedule_id = data['sid']
        db_helper.set_favorite_schedule(netid, schedule_id)
        result = {'success': True, 'response': 'setfav successful'}

    return jsonify(result)

#Generate and link schedule button
@app.route("/new_schedule", methods=['POST'])
def create_schedule():
    result = {'success': False, 'response': 'create schedule unsuccessful'}
    data = request.get_json()
    if 'sname' in data:
        sname = data['sname']
        netid = session['netid']
        session['sid'] = db_helper.create_schedule(netid, sname)
        result = {'success': True, 'response': 'create schedule successful'}

    return jsonify(result)

@app.route("/edit_schedule", methods=['POST'])
def edit_schedule():
    result = {'success': False, 'response': 'edit schedule unsuccessful'}
    data = request.get_json()
    if 'sname' in data:
        sname = data['sname']
        netid = session['netid']
        session['sid'] = db_helper.find_schedule(netid, sname)
        result = {'success': True, 'response': 'edit schedule successful'}

    return jsonify(result)


#Add friend to pending friends list
@app.route("/add_friend", methods=['POST'])
def add_friend():
    result = {'success': False, 'response': 'pending friend unsuccessful'}
    data = request.get_json()
    netid = session['netid']
    if 'friend' in data:
        friendid = data['friend']
        db_helper.add_pending_friend(netid, friendid)
        db_helper.eval_friend_request(netid, friendid)
        result = {'success': True, 'response': 'pending friend successful'}

    return jsonify(result)

#Add course taken to the netid
@app.route("/course_taken", methods=['POST'])
def add_course_taken():
    result = {'success': False, 'response': 'add course taken unsuccessful'}
    data = request.get_json()
    netid = session['netid']
    if 'crn' in data:
        crn = data['crn']
        db_helper.add_course_taken(netid, crn)
        result = {'success': True, 'response': 'add course taken successful'}

    return jsonify(result)

#Add course to schedule
@app.route("/add_to_schedule", methods=['POST'])
def add_to_schedule():
    result = {'success': False, 'response': 'add course taken unsuccessful'}
    data = request.get_json()
    if 'crn' in data and 'sid' in session:
        sid = session['sid']
        crn = data['crn']
        db_helper.add_course_to_schedule(sid, crn)
        result = {'success': True, 'response': 'add course taken successful'}

    return jsonify(result)

#Logout
@app.route("/logout", methods=['POST'])
def logout():
    result = {'success': False, 'response': 'logout error'}
    if 'netid' in session:
        session.pop('netid')
        result = {'success': True, 'response': 'logout successful'}
    return jsonify(result)


#STAGE 4 DEPRECATED  BELOW
#------------------------------------------------------------


# @app.route("/delete/<int:task_id>", methods=['POST'])
# def delete(task_id):
#     """ recieved post requests for entry delete """

#     try:
#         db_helper.remove_task_by_id(task_id)
#         result = {'success': True, 'response': 'Removed task'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)

# @app.route("/search/<reqname>", methods=['POST', 'GET'])
# def searchByReqName(reqname):
#     print(reqname)
#     data = request.get_json()
#     items = None
#     try:
#         items = db_helper.fetch_reqs_by_name(reqname)
#         result = {'success': True, 'response': 'Search complete'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     #return jsonify(result)
#     return render_template("index.html", items=items)

# @app.route("/advsearch/<reqid>", methods=['POST', 'GET'])
# def advSearch(reqid):
#     print(reqid)
#     data = request.get_json()
#     items2 = None
#     try:
#         items2 = db_helper.students_with_req(reqid)
#         result = {'success': True, 'response': 'Search complete'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     #return jsonify(result)
#     return render_template("index.html", items2=items2)

#This one right here
# @app.route("/edit", methods=['POST'])
# def edit():
#     print("EDIT")
#     data = request.get_json()
#     try:
#         if 'reqid' in data:
#             db_helper.edit_or_create(data['reqid'], data['reqname'], data['numcredits'], data['numcourses'])
#             result = {'success': True, 'response': 'Nice'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)

# @app.route("/delete", methods=['POST'])
# def delete_req():
#     print("DELETE")
#     data = request.get_json()
#     try:
#         if 'reqid' in data:
#             db_helper.delete(data['reqid'])
#             result = {'success': True, 'response': 'Nice'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)

# @app.route("/link", methods=['POST'])
# def link():
#     print("LINK")
#     data = request.get_json()
#     try:
#         if 'reqid' in data:
#             db_helper.link(data['reqid'], data['crn'])
#             result = {'success': True, 'response': 'Nice'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)


# @app.route("/edit/<int:task_id>", methods=['POST'])
# def update(task_id):
#     """ recieved post requests for entry updates """

#     data = request.get_json()

#     try:
#         if "status" in data:
#             db_helper.update_status_entry(task_id, data["status"])
#             result = {'success': True, 'response': 'Status Updated'}
#         elif "description" in data:
#             db_helper.update_task_entry(task_id, data["description"])
#             result = {'success': True, 'response': 'Task Updated'}
#         else:
#             result = {'success': True, 'response': 'Nothing Updated'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)


# @app.route("/create", methods=['POST'])
# def create():
#     """ recieves post requests to add new task """
#     data = request.get_json()
#     db_helper.insert_new_task(data['description'])
#     result = {'success': True, 'response': 'Done'}
#     return jsonify(result)


# @app.route("/")
# def homepage():
#     """ returns rendered homepage """
#     items = None
#     if 'results' in session:
#         print("found")
#         items = session['results']
#     if items:
#         result = render_template("index.html", items=items)
#     else:
#         result = render_template("index.html")
#     return result
