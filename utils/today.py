from datetime import datetime, timedelta, timezone


def get_today():
    today_date = datetime.today().astimezone(
        timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    return today_date
