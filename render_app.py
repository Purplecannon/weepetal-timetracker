from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "super-secret-password"

USERNAME = "alicia"
PASSWORD = "wanweitime"

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


@app.route("/tracker")
def tracker():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return TRACKER_TEMPLATE


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
