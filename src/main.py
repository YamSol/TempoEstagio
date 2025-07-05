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
    print("Eventos encontrados:")
    print(df[["Nome", "Data-Hora", "Duração"]])
    print(f"\nTotal de horas realizadas: {total_hours}")
    print(f"Total de horas esperadas no período: {expected_hours}")

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

    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    call(['vim', INPUT_FILE])
    root.deiconify()  # Mostra a janela principal novamente

def main():
    root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop functionality
    root.title("Análise de Estágio")

    # Set window size and position
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def open_input():
        edit_input_file()

    def on_drop(event):
        file_paths = root.tk.splitlist(event.data)
        print("Arquivos arrastados:")
        for file in file_paths:
            print(file)
        process_pdfs(file_paths)

    drag_drop_frame = tk.Frame(root, width=window_width - 50, height=window_height - 100, bg="lightgray")
    drag_drop_frame.pack(pady=20)
    drag_drop_frame.pack_propagate(False)
    tk.Label(drag_drop_frame, text="Analisar Calendario(s)", bg="lightgray", fg="black").pack(expand=True)

    drag_drop_frame.drop_target_register("DND_Files")
    drag_drop_frame.dnd_bind("<<Drop>>", on_drop)

    tk.Button(root, text="Inserir via texto", command=open_input).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
