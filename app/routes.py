# app/routes.py
from flask import Blueprint, render_template, request, session, redirect, url_for
import os
from .logic import parse_time_string, format_seconds
from .logic import load_balance, save_balance


main = Blueprint("main", __name__)

USERNAME = os.environ.get("LOGIN_USERNAME", "defaultuser")
PASSWORD = os.environ.get("LOGIN_PASSWORD", "defaultpass")


@main.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        submitted_user = request.form["username"]
        submitted_pass = request.form["password"]

        print(f"🔐 Attempting login: {submitted_user} / {submitted_pass}")

        if submitted_user == USERNAME and submitted_pass == PASSWORD:
            session["logged_in"] = True
            print("✅ Login successful!")
            return redirect(url_for("main.tracker"))
        else:
            print("❌ Login failed.")

    return render_template("login.html")


@main.route("/tracker", methods=["GET", "POST"])
def tracker():
    if not session.get("logged_in"):
        return redirect(url_for("main.login"))

    alicia_total = wanwei_total = result = None
    current_balance, last_updated = load_balance()

    if request.method == "POST":
        alicia_entries = request.form.getlist("alicia_time")
        wanwei_entries = request.form.getlist("wanwei_time")

        try:
            alicia_seconds = sum(parse_time_string(e) for e in alicia_entries if e)
            wanwei_seconds = sum(parse_time_string(e) for e in wanwei_entries if e)

            diff = alicia_seconds - wanwei_seconds
            new_balance = current_balance + diff
            timestamp = save_balance(new_balance)

            alicia_total = format_seconds(alicia_seconds)
            wanwei_total = format_seconds(wanwei_seconds)

            result = (
                f"💰 {'Wanwei owes Alicia' if new_balance > 0 else 'Alicia owes Wanwei' if new_balance < 0 else 'No one owes time'} "
                f"{format_seconds(abs(new_balance))} (updated {timestamp})"
            )

            current_balance = new_balance
            last_updated = timestamp

        except Exception as e:
            result = f"⚠️ Error: {str(e)}"

    # Always calculate balance display and render template, even for GET
    balance_text = (
        f"Wanwei owes Alicia {format_seconds(current_balance)}"
        if current_balance > 0
        else f"Alicia owes Wanwei {format_seconds(-current_balance)}"
        if current_balance < 0
        else "⚖️ No one owes time!"
    )

    return render_template(
        "tracker.html",
        result=result,
        alicia_total=alicia_total,
        wanwei_total=wanwei_total,
        balance_text=balance_text,
        last_updated=last_updated,
        current_balance=current_balance,
    )


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))
