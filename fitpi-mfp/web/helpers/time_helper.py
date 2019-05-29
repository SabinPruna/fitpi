from datetime import datetime, timezone, timedelta

def get_local_datetime():
    utc_dt = datetime.now(timezone.utc) # UTC time
    dt = utc_dt + timedelta(hours=3) # local time
    
    return dt.strftime("%Y-%m-%d-%H-%M")

def get_local_date():
    utc_dt = datetime.now(timezone.utc) # UTC time
    dt = utc_dt + timedelta(hours=3) # local time
    
    return dt.strftime("%Y-%m-%d")

def get_local_date_numbers():
    utc_dt = datetime.now(timezone.utc) # UTC time
    dt = utc_dt + timedelta(hours=3) # local time

    return [dt.year, dt.month, dt.day]