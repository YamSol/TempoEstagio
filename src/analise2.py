total_minutes = 0

with open("input.txt", "r") as f:
    for line in f:
        parts = line.strip().split(',')
        if len(parts) >= 2:
            try:
                hours = int(parts[0])
                minutes = int(parts[1])
                total_minutes += hours * 60 + minutes
            except ValueError:
                continue  # skip lines with invalid numbers

total_hours = total_minutes // 60
remaining_minutes = total_minutes % 60

print(f"Total time: {total_hours} hours and {remaining_minutes} minutes ({total_minutes/ 60:.2f} hours)")

# Logica para achar o tempo previsto. Trabalho 30 horas por semana, 6 horas por dia, de segunda a sexta. 
# Conto as horas entre os dias 19/X e 20/X+1. Deve se considerar a data atual.
from datetime import datetime, timedelta

today = datetime.now()

def find_start_date(today):
    if today.day < 20:
        return today.replace(day=20, month=today.month - 1 if (today.month > 1) else 12, year=today.year - (1 if today.month == 1 else 0))
    else:
        return today.replace(day=19, month=today.month, year=today.year)

def find_end_date(today):
    if today.day < 20:
        return today.replace(day=19, month=today.month, year=today.year - (1 if today.month == 1 else 0))
    else:
        return today.replace(day=20, month=today.month + 1 if (today.month < 12) else 1, year=today.year + (1 if today.month == 12 else 0))

start_date = find_start_date(today)
end_date = find_end_date(today)
# Calculate expected working hours between start_date and end_date (full period)
def working_days_between(start, end):
    days = 0
    current = start
    while current < end:
        if current.weekday() < 5:  # Monday to Friday
            days += 1
        current += timedelta(days=1)
    return days

# Total expected hours in the period
total_working_days = working_days_between(start_date, end_date)
expected_hours_to_end = hours=total_working_days * 6.0  # 6 hours per working day

# Expected hours until now (from start_date to today)
working_days_until_now = working_days_between(start_date, today + timedelta(days=1))
expected_hours_until_now = working_days_until_now * 6.0  # 6 hours per working day

# Deltas
# actual_time = timedelta(minutes=total_minutes)
# delta_until_now = actual_time - expected_hours_until_now
# delta_to_end = actual_time - expected_hours_to_end

print(f"Expected hours until now: {expected_hours_until_now}")
print(f"Expected hours to end: {expected_hours_to_end}")


