# app/routes.py
from flask import Blueprint, render_template, request, session, redirect, url_for
import os
from .logic import parse_time_string, format_seconds

main = Blueprint('main', __name__)

USERNAME = os.environ.get("LOGIN_USERNAME", "defaultuser")
PASSWORD = os.environ.get("LOGIN_PASSWORD", "defaultpass")

@main.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("main.tracker"))
    return render_template("login.html")

@main.route("/tracker", methods=["GET", "POST"])
def tracker():
    if not session.get("logged_in"):
        return redirect(url_for("main.login"))

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

    return render_template("tracker.html",
                           result=result,
                           alicia_total=alicia_total,
                           wanwei_total=wanwei_total)

@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


