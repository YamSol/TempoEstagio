# Análise de Eventos "Estágio" em PDFs de Calendário (Alpha 0.1) (BROKEN LIB fitz)
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

Existem dois scripts principais neste projeto:

- **Selecionador de PDFs (`selecionar_pdfs.py`)**: Ao executar este script, uma janela será aberta para que você possa arrastar e soltar os arquivos PDF que deseja analisar. Após a seleção, os arquivos são processados automaticamente para extrair os eventos de estágio e gerar o resumo das horas realizadas.

- **Editor de Entrada (`editor_entrada.py`)**: Basta rodar este script para que o arquivo `input.txt` seja aberto em um editor de código. Faça as edições necessárias e salve o arquivo; o programa será executado automaticamente após o salvamento, processando os dados inseridos.

Ambos os scripts facilitam a análise dos eventos de estágio de acordo com a sua preferência de uso.
