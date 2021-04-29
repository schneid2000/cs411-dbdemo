""" Specifies routing for the application"""
from flask import render_template, request, jsonify, session
from app import app
from app import database as db_helper

#Something about session data
#View schedule page
@app.route("/view_schedule", methods=['POST', 'GET'])
def view_schedules():
    print("view_schedules page")
    #Display the schedules of netid, the schedules of the friends of netid, and the classes in the schedule
    #assume we have some session variable called netid i guess
    data = request.get_json()
    course_data = []
    if 'sid' in data:
        schedule_id = data['sid']
        crns = db_helper.fetch_courses_by_schedule(schedule_id)
        for crn in crns:
            course_data.append(db_helper.show_details_by_crn(crn))

    netid = session["netid"]
    student_schedules = db_helper.fetch_schedules(netid)
    friend_schedules = db_helper.fetch_friend_schedules(netid)
      
    return render_template("View_Schedules.html", sched=student_schedules, fsched=friend_schedules, cdata=course_data)

#Generate schedule page
@app.route("/gen_schedule", methods=['POST', 'GET'])
def gen_schedule():
    print("gen schedule page")
    #Display major reqs, time constraints, and resulting searches
    #Retrieve the requirements attached to the major of the student
    netid = session['netid']
    reqnames = fetch_reqs_by_netid(netid)
    #Display the current time constraints on the schedule
    data = request.get_json()
    tc = []
    if 'sid' in data:
        schedule_id = data['sid']
        tc = fetch_time_constraints_by_schedule(schedule_id)
    
    rc = []
    #Display the filtered search results
    if 'req' in data:
        reqid = data['req']
        rc = fetch_course_by_req(reqid)
        if 'filter_s' in data:
            rc = filter_courses_by_subject(rc, data['filter_s'])
        if 'filter_t' in data:
            rc = filter_courses_by_title(rc, data['filter_t'])
    
    return render_template("Generate-a-Schedule.html", reqs=reqnames, timec=tc, reqc=rc)

#Homepage
@app.route("/home", methods=['POST', 'GET'])
def home():
    netid = ""
    if "netid" in session:
        netid = session['netid']

    return render_template("Home.html", netid=netid)

#Login button
@app.route("/login", methods=['POST'])
def login():
    result = {'success': False, 'response': 'Login unsuccessful'}
    data = request.get_json()
    if 'netid' in data and 'pw' in data:
        #Should be the hashed password, probably
        netid = data['netid']
        hashed_pass = data['pw']
        #Check if student in db
        existence = is_student_in_db(netid)
        if not existence:
            #Create user and login
            major = data['mj']
            creation_status = create_user(netid, major, password)
            if creation_status == True:
                session['netid'] = netid
                result = {'success': True, 'response': 'Successfully created account'}

        else:
            #Attempt login
            login_status = verify_hashed_login(netid, hashed_pass)
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
        set_favorite_schedule(netid, schedule_id)
        result = {'success': True, 'response': 'setfav successful'}

    return jsonify(result)

#Generate and link schedule button
@app.route("/new_schedule", methods=['POST'])
def create_schedule():
    result = {'success': False, 'response': 'create schedule unsuccessful'}
    netid = session['netid']
    create_schedule(netid)
    result = {'success': True, 'response': 'create schedule successful'}
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