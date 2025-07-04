from datetime import datetime, timedelta

# === CONSTANTS ===
INPUT_FILE = "input.txt"
WORK_HOURS_PER_DAY = 6
WORK_DAYS_PER_WEEK = 5
WORK_HOURS_PER_WEEK = WORK_HOURS_PER_DAY * WORK_DAYS_PER_WEEK
PERIOD_START_DAY = 20
PERIOD_END_DAY = 19

# === FUNCTIONS ===

def parse_time_entries(filename):
    total_minutes = 0
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                try:
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    total_minutes += hours * 60 + minutes
                except ValueError:
                    continue  # skip lines with invalid numbers
    return total_minutes

def find_start_date(today):
    if today.day < PERIOD_START_DAY:
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_year = today.year - 1 if today.month == 1 else today.year
        return today.replace(day=PERIOD_START_DAY, month=prev_month, year=prev_year)
    else:
        return today.replace(day=PERIOD_START_DAY, month=today.month, year=today.year)

def find_end_date(today):
    if today.day < PERIOD_START_DAY:
        return today.replace(day=PERIOD_END_DAY, month=today.month, year=today.year)
    else:
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year + 1 if today.month == 12 else today.year
        return today.replace(day=PERIOD_END_DAY, month=next_month, year=next_year)

def working_days_between(start, end):
    days = 0
    current = start
    while current < end:
        if current.weekday() < WORK_DAYS_PER_WEEK:  # Monday to Friday
            days += 1
        current += timedelta(days=1)
    return days

def main():
    # Read total minutes from input file
    total_minutes = parse_time_entries(INPUT_FILE)
    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60

    print(f"Total time: {total_hours} hours and {remaining_minutes} minutes ({total_minutes / 60:.2f} hours)")

    today = datetime.now()
    start_date = find_start_date(today)
    end_date = find_end_date(today)

    # Calculate expected working hours
    total_working_days = working_days_between(start_date, end_date)
    expected_hours_to_end = total_working_days * WORK_HOURS_PER_DAY

    working_days_until_now = working_days_between(start_date, today + timedelta(days=1))
    expected_hours_until_now = working_days_until_now * WORK_HOURS_PER_DAY

    print(f"Expected hours until now: {expected_hours_until_now}")
    print(f"Expected hours to end: {expected_hours_to_end}")

    # === DELTAS ===
    delta_until_now = total_hours + remaining_minutes / 60 - expected_hours_until_now
    delta_to_end = total_hours + remaining_minutes / 60 - expected_hours_to_end

    print(f"Delta until now: {delta_until_now:.2f} hours")
    print(f"Delta to end: {delta_to_end:.2f} hours")

if __name__ == "__main__":
    main()
