import os
import re
import tkinter as tk
from tkinter import filedialog
from subprocess import call
from datetime import datetime, timedelta
import fitz  # PyMuPDF
import pandas as pd
from tkinterdnd2 import TkinterDnD, DND_FILES

# === CONSTANTS ===
INPUT_FILE = "input.txt"
WORK_HOURS_PER_DAY = 6
WORK_DAYS_PER_WEEK = 5
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

def process_pdfs(file_paths):
    today = datetime.now()
    start_date = find_start_date(today)
    end_date = find_end_date(today)

    all_events = []
    for file in file_paths:
        all_events.extend(extract_events_from_pdf(file, start_date, end_date))

    df = pd.DataFrame(all_events)
    total_hours = sum((event["Duração"] for event in all_events), timedelta())

    # Cálculo de horas esperadas
    expected_hours = timedelta()
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:
            expected_hours += timedelta(hours=WORK_HOURS_PER_DAY)
        current += timedelta(days=1)

    # Resultados
    print("\n=== RESULTADOS DA ANÁLISE ===")
    print("Eventos encontrados:")
    if not df.empty:
        print(df[["Nome", "Data-Hora", "Duração"]].to_string(index=False))
    else:
        print("Nenhum evento encontrado.")
    print(f"\nTotal de horas realizadas: {total_hours}")
    print(f"Total de horas esperadas no período: {expected_hours}")
    print("\n=============================")

def extract_events_from_pdf(file_path, start_date, end_date):
    estagio_pattern = re.compile(r"est[aáâã]g[ií]o", re.IGNORECASE)
    datetime_pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}:\d{2})", re.IGNORECASE)
    duration_pattern = re.compile(r"(\d{1,2}):h", re.IGNORECASE)

    def parse_duration(text):
        match = duration_pattern.search(text)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2)) if match.group(2) else 0
            return timedelta(hours=hours, minutes=minutes)
        return timedelta(0)

    events = []
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text()
        if estagio_pattern.search(text):
            for match in estagio_pattern.finditer(text):
                context = text[max(0, match.start()-100):match.end()+100]
                date_match = datetime_pattern.search(context)
                duration = parse_duration(context)
                if date_match:
                    date_str = date_match.group(1)
                    time_str = date_match.group(2)
                    try:
                        dt = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
                        if start_date <= dt <= end_date:
                            events.append({
                                "Nome": "Estágio",
                                "Data-Hora": dt,
                                "Duração": duration
                            })
                    except ValueError:
                        continue
    return events

def edit_input_file():
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w") as f:
            f.write("# Insira os dados no formato: horas,minutos\n")

    call(['vim', INPUT_FILE])

    # Após sair do vim, processar e exibir os resultados
    total_minutes = parse_time_entries(INPUT_FILE)
    total_hours = timedelta(minutes=total_minutes)

    today = datetime.now()
    start_date = find_start_date(today)
    end_date = find_end_date(today)

    expected_hours_until_today = timedelta()
    current = start_date
    while current <= today:
        if current.weekday() < WORK_DAYS_PER_WEEK:
            expected_hours_until_today += timedelta(hours=WORK_HOURS_PER_DAY)
        current += timedelta(days=1)

    expected_hours_until_end_date = timedelta()
    current = start_date
    while current <= end_date:
        if current.weekday() < WORK_DAYS_PER_WEEK:
            expected_hours_until_end_date += timedelta(hours=WORK_HOURS_PER_DAY)
        current += timedelta(days=1)

    delta_until_today = total_hours - expected_hours_until_today
    delta_until_end_date = total_hours - expected_hours_until_end_date

    print("\n=== RESULTADOS DA EDIÇÃO ===")
    # Converter timedelta para horas decimais (ex: 1.5h)
    def timedelta_to_decimal_hours(td):
        return td.total_seconds() / 3600

    print(f"Total Previsto: {timedelta_to_decimal_hours(expected_hours_until_end_date):.2f} horas (Delta: {timedelta_to_decimal_hours(delta_until_end_date):+.2f} horas)")
    print(f"Total já realizado: {timedelta_to_decimal_hours(total_hours):.2f} horas")
    print(f"Esperado até hoje: {timedelta_to_decimal_hours(expected_hours_until_today):.2f} horas (Delta: {timedelta_to_decimal_hours(delta_until_today):+.2f} horas)")
    print("\n=============================")

def main():
    # Executar análise diretamente sem GUI
    print("Executando análise de estágio sem GUI...")

    # Processar arquivo de entrada
    if os.path.exists(INPUT_FILE):
        total_minutes = parse_time_entries(INPUT_FILE)
        total_hours = timedelta(minutes=total_minutes)

        today = datetime.now()
        start_date = find_start_date(today)
        end_date = find_end_date(today)

        expected_hours_until_today = timedelta()
        current = start_date
        while current <= today:
            if current.weekday() < WORK_DAYS_PER_WEEK:
                expected_hours_until_today += timedelta(hours=WORK_HOURS_PER_DAY)
            current += timedelta(days=1)

        expected_hours_until_end_date = timedelta()
        current = start_date
        while current <= end_date:
            if current.weekday() < WORK_DAYS_PER_WEEK:
                expected_hours_until_end_date += timedelta(hours=WORK_HOURS_PER_DAY)
            current += timedelta(days=1)

        delta_until_today = total_hours - expected_hours_until_today
        delta_until_end_date = total_hours - expected_hours_until_end_date

        print("\n=== RESULTADOS DA ANÁLISE ===")
        def timedelta_to_decimal_hours(td):
            return td.total_seconds() / 3600

        print(f"Total Previsto: {timedelta_to_decimal_hours(expected_hours_until_end_date):.2f} horas (∆ = {timedelta_to_decimal_hours(delta_until_end_date):+.2f} horas)")
        print(f"Total já realizado: {timedelta_to_decimal_hours(total_hours):.2f} horas")
        print(f"Esperado até hoje: {timedelta_to_decimal_hours(expected_hours_until_today):.2f} horas (∆ = {timedelta_to_decimal_hours(delta_until_today):+.2f} horas)")
        print("\n=============================")
    else:
        print(f"Arquivo de entrada '{INPUT_FILE}' não encontrado. Por favor, crie o arquivo e insira os dados no formato correto.")

if __name__ == "__main__":
    main()
