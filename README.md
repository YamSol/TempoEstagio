# Análise de Eventos "Estágio" em PDFs de Calendário (Alpha 0.1)
Este projeto analisa arquivos PDF de calendários e extrai eventos relacionados a **"Estágio"**. Ele calcula e compara o total de horas realizadas com o esperado (30 horas semanais).
## Utilização

1. Criar e ativar um ambiente virtual:
    - Windows:
      ```sh
      python -m venv venv
      .\\venv\\Scripts\\activate
      ```
    - macOS/Linux:
      ```sh
      python3 -m venv venv
      source venv/bin/activate
      ```
2. Instalar as dependências:
      ```sh
      pip install -r requirements.txt
      ```
3. Executar o script:
      ```sh
      python src/analisar_estagios.py
      ```

O script permite selecionar os PDFs, extrai os eventos de estágio e mostra um resumo das horas realizadas.
