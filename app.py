import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, time as dt_time
from database import create_tables, db_name

app = Flask(__name__)
app.secret_key = "dev"

create_tables()

@app.route("/")
def index():
    return render_template("homepage.html")



#----events-----
@app.route("/events")
def list_events():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT event_id, title, start_time, end_time, description FROM Event ORDER BY start_time")
    events = cur.fetchall()
    conn.close()

    return render_template("events.html", event=events)


#----create event-----
@app.route("/events/new", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        title = request.form.get("title")
        start_time = datetime.fromisoformat(request.form.get("start_time"))
        end_time =datetime.fromisoformat(request.form.get("end_time"))
        description = request.form.get("description")
        start_iso = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_iso   = end_time.strftime("%Y-%m-%d %H:%M:%S")

        if start_time >= end_time:
            flash("Start time must be before end time.")
            return redirect(url_for("create_event"))

        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Event (title, start_time, end_time, description) VALUES (?, ?, ?, ?)",
            (title, start_iso, end_iso, description),
        )
        con.commit()
        con.close()

        flash("Event created")
        return redirect(url_for("list_events"))

    return render_template("event_form.html")


#----edit event-----

@app.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute("SELECT * FROM Event WHERE event_id = ?", (event_id,))
    event = cur.fetchone()

    if not event:
        flash("Event not found.")
        return redirect(url_for("list_events"))

    if request.method == "POST":
        title = request.form.get("title")
        start_time = datetime.fromisoformat(request.form.get("start_time"))
        end_time = datetime.fromisoformat(request.form.get("end_time"))
        description = request.form.get("description")


        if start_time >= end_time:
            flash("Start time must be before end time.")
            con.close()
            return redirect(url_for("edit_event", event_id=event_id))

        cur.execute("""
            UPDATE Event SET title=?, start_time=?, end_time=?, description=?
            WHERE event_id=?
        """, (title, start_time, end_time, description, event_id))

        con.commit()
        con.close()

        flash("Event updated")
        return redirect(url_for("list_events"))

    con.close()
    return render_template("event_form.html", event=event)


#----delete event-----

@app.route("/events/<int:event_id>/delete")
def delete_event(event_id):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("DELETE FROM EventResourceAllocation WHERE event_id = ?", (event_id,))
    cur.execute("DELETE FROM Event WHERE event_id = ?", (event_id,))

    conn.commit()
    conn.close()

    flash("Event deleted")
    return redirect(url_for("list_events"))


#----resource----
@app.route("/resources")
def list_resources():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Resource ORDER BY resource_name")
    resources = cur.fetchall()

    conn.close()
    return render_template("resources.html", resources=resources)


#-----create resource-----

@app.route("/resources/new", methods=["GET", "POST"])
def create_resource():
    if request.method == "POST":
        name = request.form.get("resource_name")
        rtype = request.form.get("resource_type")

        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        cur.execute("INSERT INTO Resource (resource_name, resource_type) VALUES (?, ?)", (name, rtype))

        conn.commit()
        conn.close()

        flash("Resource added")
        return redirect(url_for("list_resources"))

    return render_template("resource_form.html", resource=None)


#------edit resource-----

@app.route("/resources/<int:resource_id>/edit", methods=["GET", "POST"])
def edit_resource(resource_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute("SELECT * FROM Resource WHERE resource_id = ?", (resource_id,))
    resource = cur.fetchone()

    if not resource:
        flash("Resource not found.")
        con.close()
        return redirect(url_for("list_resources"))

    if request.method == "POST":
        name = request.form.get("resource_name")
        rtype = request.form.get("resource_type")

        cur.execute("""
            UPDATE Resource SET resource_name=?, resource_type=? 
            WHERE resource_id=?
        """, (name, rtype, resource_id))

        con.commit()
        con.close()

        flash("Resource updated.")
        return redirect(url_for("list_resources"))

    con.close()
    return render_template("resource_form.html", resource=resource)


#----delete resource-----
@app.route("/resources/<int:resource_id>/delete")
def delete_resource(resource_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute("DELETE FROM EventResourceAllocation WHERE resource_id=?", (resource_id,))
    cur.execute("DELETE FROM Resource WHERE resource_id=?", (resource_id,))

    con.commit()
    con.close()

    flash("Resource deleted")
    return redirect(url_for("list_resources"))


#----allocate------.
@app.route("/events/<int:event_id>/allocate", methods=["GET", "POST"])
def allocate_resources(event_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    #get event
    cur.execute("SELECT * FROM Event WHERE event_id = ?", (event_id,))
    event = cur.fetchone()
    if not event:
        flash("Event not found.")
        con.close()
        return redirect(url_for("list_events"))

    #get resources
    cur.execute("SELECT * FROM Resource ORDER BY resource_name")
    resources = cur.fetchall()

    #get current allocations
    cur.execute("SELECT * FROM EventResourceAllocation WHERE event_id = ?", (event_id,))
    current_allocs = cur.fetchall()
    current_map = {a[2]: a for a in current_allocs}
    

    event_start = datetime.fromisoformat(event[2])
    event_end = datetime.fromisoformat(event[3])


    availability = {}

    for r in resources:
        res_id = r[0]

        cur.execute("""
            SELECT e.start_time, e.end_time
            FROM EventResourceAllocation a
            JOIN Event e ON a.event_id = e.event_id
            WHERE a.resource_id = ? AND e.event_id != ?
        """, (res_id, event_id))

        rows = cur.fetchall()

        free = True
        for s, e in rows:
            s_dt = datetime.fromisoformat(s)
            e_dt = datetime.fromisoformat(e)

            if event_start < e_dt and s_dt < event_end:
                free = False
                break

        availability[res_id] = free


    if request.method == "POST":
        conflicts = []

        for r in resources:
            res_id = r[0]
            selected = request.form.get(f"use_{res_id}")

            if selected:
                if res_id in current_map:
                    continue

                if not availability[res_id]:
                    conflicts.append(r)
                    continue

                cur.execute(
                    "INSERT INTO EventResourceAllocation (event_id, resource_id) VALUES (?, ?)",
                    (event_id, res_id)
                )

            else:
                if res_id in current_map:
                    cur.execute(
                        "DELETE FROM EventResourceAllocation WHERE allocation_id = ?",
                        (current_map[res_id][0],)
                    )

        con.commit()

        

        con.close()
        flash("Resources updated.")
        return redirect(url_for("list_events"))



    con.close()
    return render_template(
        "allocations.html",
        event=event,
        resources=resources,
        current_allocs=current_allocs,
        current_map=current_map,
        availability=availability,
        conflicts=[]
    )

#-----report------
@app.route("/report", methods=["GET", "POST"])
def report():
    report_data = []
    start_str =  ""
    end_str = ""

    if request.method == "POST":
        start_str = request.form.get("start_date")
        end_str = request.form.get("end_date")

        if not start_str or not end_str:
            flash("Please choose dates.")
            return render_template("report.html", report_data=[])

        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
        end_date = datetime.combine(end_date, dt_time.max)

        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        cur.execute("SELECT * FROM Resource ORDER BY resource_name")
        resources = cur.fetchall()

        for r in resources:
            res_id = r[0]

            #allocations
            cur.execute("""
                SELECT e.start_time, e.end_time, e.title
                FROM EventResourceAllocation a
                JOIN Event e ON a.event_id = e.event_id
                WHERE a.resource_id=?
            """, (res_id,))
            rows = cur.fetchall()

            total_hours = 0
            upcoming = []

            for s, e, title in rows:
                ev_s = datetime.fromisoformat(s)
                ev_e = datetime.fromisoformat(e)
                overlap_start = max(ev_s, start_date)
                overlap_end = min(ev_e, end_date)

                if overlap_end > overlap_start:
                    total_hours += (overlap_end - overlap_start).total_seconds() / 3600

                if ev_s >= datetime.now():
                    upcoming.append((title, s, e))

            report_data.append({
                "resource_name": r[1],
                "resource_type": r[2],
                "total_hours": round(total_hours),
                "upcoming": upcoming
            })

        conn.close()
    return render_template("report.html", report_data=report_data)

def overlaps(s1, e1, s2, e2):
    return s1 < e2 and s2 < e1

if __name__ == "__main__":
    app.run(debug=True)
