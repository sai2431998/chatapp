import json
from re import S
from flask import Flask, jsonify, request, Response
from flask_restful import Resource, Api
import mysql.connector
from flask_cors import CORS
import datetime

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="Sai@1234",
database="riktam"
)

mycursor = mydb.cursor()


app=Flask(__name__)
api=Api(app)
CORS(app)

def make_cors_resp(j):
    resp=Response(json.dumps(j))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"]="Content-Type, Content-Length, Access-Control-Allow-Headers, Access-Control-Allow-Origin"
    resp.headers["Content-Type"]="application/json"
    return resp

@app.route("/")
def hello_world():
    return "Hello!!!"


@app.route("/create_schema")
def create_schema():

    mycursor.execute("DROP TABLE IF EXISTS Users")
    print("If table exist dropped..")
    mycursor.execute("CREATE TABLE Users (user VARCHAR(255) PRIMARY KEY, user_type VARCHAR(255), password VARCHAR(255))")
    print("Users Table Created")
    mycursor.execute("INSERT INTO users(user, user_type, password) VALUES ('Sai', 'Admin', '1234')")
    mydb.commit()


    mycursor.execute("DROP TABLE IF EXISTS GroupData")
    print("If table exist dropped..")
    mycursor.execute("CREATE TABLE GroupData (group_name VARCHAR(255), user VARCHAR(255))")
    print("Groups Table Created")


    mycursor.execute("DROP TABLE IF EXISTS Messages")
    print("If table exist dropped..")
    mycursor.execute("CREATE TABLE Messages (group_name VARCHAR(255), user VARCHAR(255), content VARCHAR(255), time VARCHAR(255))")
    print("Messages Table Created")

    return "Schema Created Successfully!!!"

@app.route("/create_user", methods=["POST","OPTIONS"])
def create_user():
    data=request.json

    mycursor.execute("""select user from Users""")
    myresult = mycursor.fetchall()
    user_ids = [row[0] for row in myresult]

    select_query="""select user from Users where user_type = %s"""
    mycursor.execute(select_query,("Admin",))
    myresult = mycursor.fetchall()
    admin_ids = [row[0] for row in myresult]


    if data["created_by"] not in admin_ids:
        return "You are not an admin!!"
    if data["user"] in user_ids:
        return "User already Exists....User Another User!"
    else:
        sql = "INSERT INTO Users (user, user_type, password) VALUES (%s, %s, %s)"
        val = (data["user"],data["user_type"],data["password"])
        mycursor.execute(sql, val)
        mydb.commit()
        print(user_ids,admin_ids)

    return "User Added Successfully"


@app.route("/edit_user", methods=["POST","OPTIONS"])
def edit_user():
    data=request.json
    print(data)

    select_query="""select user from Users where user_type = %s"""
    mycursor.execute(select_query,("Admin",))
    myresult = mycursor.fetchall()
    admin_ids = [row[0] for row in myresult]


    if data["updated_by"] not in admin_ids:
        return "You are not an admin!!"

    mycursor.execute("""select user from Users""")
    myresult = mycursor.fetchall()
    user_ids = [row[0] for row in myresult]

    if data["user"] not in user_ids:
        return "User Not Found!!!!!"

    select_query="""select * from Users where user = %s"""
    mycursor.execute(select_query,(data["user"],))
    old_data = mycursor.fetchall()


    if "updated_user" in data:
        if data["updated_user"] in user_ids:
            return "Username you want to edit was already exists!!!"
        else:
            updated_user=data["updated_user"]
    else:
        updated_user=old_data[0][0]
    if "updated_user_type" in data:
        updated_user_type=data["updated_user_type"]
    else:
        updated_user_type=old_data[0][1]
    if "updated_password" in data:
        updated_password=data["updated_password"]
    else:
        updated_password=old_data[0][2]

    sql = "UPDATE users SET user = %s, user_type=%s, password=%s WHERE user = %s"
    val = (updated_user,updated_user_type,updated_password,data["user"])
    mycursor.execute(sql, val)
    mydb.commit()


    return "User Edited Successfully"

@app.route("/authorize_user", methods=["POST","OPTIONS"])
def authorize_user():
    if request.method=="OPTIONS":
        return make_cors_resp({})
    data=request.json

    
    mycursor.execute("""select user,password from Users""")
    myresult = mycursor.fetchall()
    user_ids = [row[0] for row in myresult]

    if data["user"] not in user_ids:
        return "User Not Found!!!!!"

    select_query="""select user,password from Users where user = %s"""
    mycursor.execute(select_query,(data["user"],))
    myresult = mycursor.fetchall()

    if data["password"]==myresult[0][1]:
        return data
    else:
        return ("Incorrect Password...Try Again..",400)



@app.route("/create_group", methods=["POST","OPTIONS"])
def create_group():
    data=request.json

    sql = "INSERT INTO GroupData (group_name, user) VALUES (%s, %s)"
    val = (data["group_name"],data["user"])
    mycursor.execute(sql, val)
    mydb.commit()

    return "Group Created Successfully"


@app.route("/check_group", methods=["POST","OPTIONS"])
def check_group():
    if request.method=="OPTIONS":
        return make_cors_resp({})
        
    data=request.json

    select_query="""select user from groupData where group_name = %s"""
    mycursor.execute(select_query,(data["group"],))
    myresult = mycursor.fetchall()
    user_ids = [row[0] for row in myresult]

    if data["user"] in user_ids:
        return "Found"
    else:
        return ("User not in group",400)

@app.route('/get_group_message/', methods=['GET'])
def query_records():
    group_name = request.args.get('group_name')
    select_query="""select user,content from messages where group_name = %s order by time DESC LIMIT 5"""
    mycursor.execute(select_query,(group_name,))
    myresult = mycursor.fetchall()

    return jsonify(myresult)



@app.route("/send_msg", methods=["POST","OPTIONS"])
def send_msg():
    if request.method=="OPTIONS":
        return make_cors_resp({})
        
    data=request.json
    now = datetime.datetime.now()

    
    sql = "INSERT INTO messages (group_name, user, content,time) VALUES (%s, %s, %s,%s)"
    val = (data["grp"],data["user"],data["content"],now.timestamp())
    mycursor.execute(sql, val)

    mydb.commit()

    return "Message sent Successfully!!!!!!!"







# class CreateUser(Resource):
#     def get(self,creator,user_id,password,user_type):
#         sql = "INSERT INTO Users (user, user_type, password) VALUES (%s, %s, %s)"
#         val = (user_id,user_type,password
#         mycursor.execute(sql, val)
#         return "User added Successfully!!!"
# api.add_resource(CreateUser,"/create_user/<creator>/<user_id>/<password>/<user_type>")



if __name__ == "__main__":
    app.run()
