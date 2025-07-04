import fitz  # PyMuPDF
import re
import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta
import pandas as pd

# Intervalo de datas
start_date = datetime(2025, 6, 20)
end_date = datetime(2025, 7, 19)

# Regex para "Estágio" com variações
estagio_pattern = re.compile(r"est[aáâã]g[ií]o", re.IGNORECASE)
datetime_pattern = re.compile(r"(\\d{1,2}/\\d{1,2}/\\d{4})\\s+(\\d{1,2}:\\d{2})", re.IGNORECASE)
duration_pattern = re.compile(r"(\\d{1,2}):h", re.IGNORECASE)

def parse_duration(text):
    match = duration_pattern.search(text)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2)) if match.group(2) else 0
        return timedelta(hours=hours, minutes=minutes)
    return timedelta(0)

def extract_events_from_pdf(file_path):
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

def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Selecione os arquivos PDF do calendário", filetypes=[("PDF files", "*.pdf")])
    return file_paths

# Execução principal
file_paths = select_files()
all_events = []
for path in file_paths:
    all_events.extend(extract_events_from_pdf(path))

df = pd.DataFrame(all_events)
total_hours = sum((event["Duração"] for event in all_events), timedelta())

# Cálculo de horas esperadas
expected_hours = timedelta()
current = start_date
while current <= end_date:
    if current.weekday() < 5:
        expected_hours += timedelta(hours=6)
    current += timedelta(days=1)

# Resultados
print("Eventos encontrados:")
print(df[["Nome", "Data-Hora", "Duração"]])
print(f"\nTotal de horas realizadas: {total_hours}")
print(f"Total de horas esperadas no período: {expected_hours}")
