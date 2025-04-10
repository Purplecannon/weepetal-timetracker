from flask import Flask, request, session, redirect, url_for, render_template_string
import os
from time_debt_tracker import parse_time_string, format_seconds

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "temporary-secret")

USERNAME = os.environ.get("LOGIN_USERNAME", "defaultuser")
PASSWORD = os.environ.get("LOGIN_PASSWORD", "defaultpass")


LOGIN_TEMPLATE = """
<h2>Login</h2>
<form method="post">
  <input name="username" placeholder="Username" required><br>
  <input name="password" type="password" placeholder="Password" required><br>
  <button type="submit">Login</button>
</form>
"""

TRACKER_TEMPLATE = """
<h2>Time Debt Tracker</h2>
<p>This is your secret app!</p>
<a href="/logout">Logout</a>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form["username"] == USERNAME
            and request.form["password"] == PASSWORD
        ):
            session["logged_in"] = True
            return redirect(url_for("tracker"))
    return LOGIN_TEMPLATE


@app.route("/tracker", methods=["GET", "POST"])
def tracker():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    alicia_total = wanwei_total = result = None

    if request.method == "POST":
        alicia_entries = request.form["alicia_time"].split()
        wanwei_entries = request.form["wanwei_time"].split()

        try:
            alicia_seconds = sum(parse_time_string(e) for e in alicia_entries if e)
            wanwei_seconds = sum(parse_time_string(e) for e in wanwei_entries if e)
            alicia_total = format_seconds(alicia_seconds)
            wanwei_total = format_seconds(wanwei_seconds)

            diff = alicia_seconds - wanwei_seconds
            if diff == 0:
                result = "⚖️ Neither owes time! It’s a perfect match."
            elif diff > 0:
                result = f"💰 Wanwei owes Alicia {format_seconds(diff)}."
            else:
                result = f"💰 Alicia owes Wanwei {format_seconds(-diff)}."

        except Exception as e:
            result = f"⚠️ Error: {str(e)}"

    return render_template_string(
        TRACKER_TEMPLATE,
        result=result,
        alicia_total=alicia_total,
        wanwei_total=wanwei_total,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
