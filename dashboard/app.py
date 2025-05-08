from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "070945290b6f890447deae9f1e05c42b142e4a9d2cf8028cbc7a024a9fe02d40"
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "employee_monitoring"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
activity_collection = db["employee_activity"]
work_hours_collection = db["emp_work_hours"]

def create_admin():
    if users_collection.count_documents({"username": "admin"}) == 0:
        hashed_password = generate_password_hash("admin123")
        users_collection.insert_one({"username": "admin", "password": hashed_password})

create_admin()

#Login Route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users_collection.find_one({"username": username})

        if user:
            print(f"Stored Password: {user['password']}") 
            print(f"Entered Password: {password}")

        if user and password == user["password"]: 
            session["admin"] = username
            return redirect(url_for("dashboard"))

        return "Invalid credentials, try again!"

    return render_template("login.html")



#Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("login"))

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    search_query = request.args.get("search", "").strip().lower()

    query = {}

    if from_date and to_date:
        query["timestamp"] = {
            "$gte": f"{from_date} 00:00:00",
            "$lte": f"{to_date} 23:59:59"
        }

    records = list(activity_collection.find(query, {"_id": 0}).sort("timestamp", -1))

    if search_query:
        records = [
            record for record in records
            if search_query in record.get("employee_id", "").lower()
            or search_query in record.get("employee_name", "").lower()
            or search_query in ("working" if record.get("working") else "not working")
        ]

    return render_template("dashboard.html", records=records)

#Logout Route
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

#Fetch Top 10 Employees
@app.route("/top_employees")
def top_employees():
    pipeline = [
        {"$match": {"working": True}},
        {"$group": {"_id": "$employee_id", "total_hours": {"$sum": 1}}},
        {"$sort": {"total_hours": -1}},
        {"$limit": 10}
    ]

    top_10 = list(activity_collection.aggregate(pipeline))
    return jsonify([{"employee_id": emp["_id"], "total_hours": emp["total_hours"]} for emp in top_10])

#Reports Page
@app.route("/reports")
def reports():
    if "admin" not in session:
        return redirect(url_for("login"))
    return render_template("reports.html")

#Change Password (Now Hashed)
@app.route("/change_password", methods=["POST"])
def change_password():
    if "admin" not in session:
        return redirect(url_for("login"))

    new_password = request.form["new_password"]
    hashed_password = generate_password_hash(new_password)

    users_collection.update_one({"username": "admin"}, {"$set": {"password": hashed_password}})
    flash("Password changed successfully!", "success")

    return redirect(url_for("settings"))

#View Unknown Faces
@app.route("/unknown_faces")
def unknown_faces():
    if "admin" not in session:
        return redirect(url_for("login"))

    unknown_folder = "unknown_faces/"
    unknown_images = [secure_filename(img) for img in os.listdir(unknown_folder) if img.endswith((".png", ".jpg", ".jpeg"))]

    return render_template("unknown_faces.html", images=unknown_images)

#Download Reports as CSV
@app.route("/download_report", methods=["POST"])
def download_report():
    if "admin" not in session:
        return redirect(url_for("login"))

    report_type = request.form["report_type"]
    days = 7 if report_type == "weekly" else 30
    start_date = datetime.datetime.utcnow() - timedelta(days=days)

    records = list(activity_collection.find({"timestamp": {"$gte": start_date}}, {"_id": 0, "employee_id": 1, "employee_name": 1, "timestamp": 1, "working": 1}))

    if not records:
        return Response("No data available for the selected report type.", mimetype="text/plain")

    csv_output = "Employee ID,Employee Name,Timestamp,Status\n"
    for record in records:
        csv_output += f"{record.get('employee_id', '')},{record.get('employee_name', '')},{record.get('timestamp', '')},{'Working' if record.get('working') else 'Not Working'}\n"

    response = Response(csv_output, mimetype="text/csv")
    response.headers.set("Content-Disposition", f"attachment; filename={report_type}_report.csv")

    return response

#Auto Logout After 30 Minutes
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

@app.before_request
def make_session_permanent():
    session.permanent = True

#Settings Route
@app.route("/settings")
def settings():
    if "admin" not in session:
        return redirect(url_for("login"))
    return render_template("settings.html")

#Fetch Work Hours
@app.route("/work_hours")
def work_hours():
    data = list(work_hours_collection.find({}, {"_id": 0, "employee_id": 1, "total_hours": 1}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
