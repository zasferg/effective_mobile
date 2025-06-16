from datetime import datetime, timedelta


def get_delta_date_minus(days):
    return datetime.now().date() - timedelta(days=days)