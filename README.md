# Análise de Eventos "Estágio" em PDFs de Calendário

Este projeto permite analisar arquivos PDF de calendários e extrair eventos relacionados a **"Estágio"**, mesmo com variações ortográficas. Ele calcula o total de horas realizadas e compara com o total esperado (30 horas semanais, de segunda a sexta-feira) dentro de um intervalo de datas.

## 📁 Estrutura do Projeto

- `src/analisar_estagios.py`: Script principal para análise dos PDFs.
- `requirements.txt`: Lista de dependências do projeto.
- `README.md`: Instruções de uso.

## ▶️ Como usar

### 1. Criar ambiente virtual

No terminal, execute:

```bash
python -m venv .venv

# Linux
source .venv/bin/activate

# Windows: 
.venv\\Scripts\\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o script

```bash
python src/analisar_estagios.py
```

### 4. O que o script faz

- Abre uma janela para você selecionar arquivos PDF.
- Lê os PDFs e busca eventos com o nome "Estágio" (mesmo com erros ou variações).
- Extrai nome, data-hora e duração dos eventos.
- Calcula o total de horas realizadas e o total esperado no intervalo.
- Exibe uma tabela com os eventos encontrados e um resumo final.