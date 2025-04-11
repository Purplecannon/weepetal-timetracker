# app/routes.py
from flask import Blueprint, render_template, request, session, redirect, url_for
import os
import logging
from .logic import (
    parse_time_string,
    format_seconds,
    load_balance,
    save_balance,
    log_history,
    load_history,
    reset_history,
)


logging.basicConfig(level=logging.INFO)

main = Blueprint("main", __name__)

USERNAME = os.environ.get("LOGIN_USERNAME", "defaultuser")
PASSWORD = os.environ.get("LOGIN_PASSWORD", "defaultpass")


@main.route("/", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        submitted_user = request.form["username"]
        submitted_pass = request.form["password"]

        if submitted_user == USERNAME and submitted_pass == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("main.tracker"))
        else:
            message = "❌ Incorrect username or password."

    return render_template("login.html", message=message)


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

            log_history(alicia_seconds, wanwei_seconds, new_balance)

        except Exception as e:
            result = f"⚠️ Error: {str(e)}"

    history = load_history()

    # Always calculate balance display and render template, even for GET
    balance_text = (
        f"Wanwei owes Alicia {format_seconds(current_balance)}"
        if current_balance > 0
        else f"Alicia owes Wanwei {format_seconds(-current_balance)}"
        if current_balance < 0
        else "⚖️ No one owes time!"
    )

    alicia_sum = sum(parse_time_string(entry["alicia"]) for entry in history)
    wanwei_sum = sum(parse_time_string(entry["wanwei"]) for entry in history)

    return render_template(
        "tracker.html",
        result=result,
        alicia_total=alicia_total,
        wanwei_total=wanwei_total,
        balance_text=balance_text,
        last_updated=last_updated,
        current_balance=current_balance,
        history=history,
        alicia_sum=format_seconds(alicia_sum),
        wanwei_sum=format_seconds(wanwei_sum),
    )


@main.route("/reset", methods=["POST"])
def reset():
    if not session.get("logged_in"):
        return redirect(url_for("main.login"))

    reset_history()
    return redirect(url_for("main.tracker"))


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))
