import csv
import time
from datetime import datetime
import serial  # Importa a biblioteca para comunicação serial

# Caminho dos arquivos CSV e HTML
csv_filename = 'X:\\dados_irrigacao.csv'
html_filename = 'X:\\dados.html'

# Configurar a porta serial para o Arduino (alterar 'COM3' para a porta correta)
arduino = serial.Serial('COM3', 9600)  # Define a porta e a velocidade de comunicação

# Função para salvar dados no CSV
def salvar_dados(umidade, status_bomba):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([data_hora, umidade, status_bomba])

# Função para atualizar o HTML com os dados do CSV e aplicar estilo CSS
def atualizar_html():
    with open(csv_filename, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        linhas = list(reader)

    # Gerar conteúdo HTML com CSS embutido
    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Dados de Irrigação</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #005f73;
            text-align: center;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0 auto;
            font-size: 16px;
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #005f73;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #e0f7fa;
        }
        tr:hover {
            background-color: #d1e7dd;
        }
    </style>
</head>
<body>
    <h1>Registro de Irrigação</h1>
    <table>
        <tr>
            <th>Data e Hora</th>
            <th>Umidade</th>
            <th>Status da Bomba</th>
        </tr>"""

    # Preencher as linhas da tabela com os dados do CSV
    for linha in linhas[1:]:  # Ignorar cabeçalho
        html_content += f"""
        <tr>
            <td>{linha[0]}</td>
            <td>{linha[1]}</td>
            <td>{linha[2]}</td>
        </tr>"""

    html_content += """
    </table>
</body>
</html>"""

    # Salvar HTML no diretório especificado
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

# Adicionar cabeçalho ao CSV
with open(csv_filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Data e Hora', 'Umidade', 'Status da Bomba'])

# Loop para ler dados do Arduino e atualizar HTML periodicamente
try:
    while True:
        if arduino.in_waiting > 0:  # Verifica se há dados para ler
            # Lê e decodifica os dados do Arduino
            linha = arduino.readline().decode('utf-8').strip()
            umidade = int(linha)  # Converte o valor de umidade recebido para inteiro
            status_bomba = "Ativa" if umidade < 500 else "Inativa"
            
            salvar_dados(umidade, status_bomba)
            atualizar_html()
            print(f"Data e Hora: {datetime.now()}, Umidade: {umidade}, Status da Bomba: {status_bomba}")
        
        time.sleep(5)  # Intervalo de atualização de 5 segundos
except KeyboardInterrupt:
    print("Encerrado pelo usuário.")
finally:
    arduino.close()  # Fecha a porta serial ao encerrar

# Simulação de dados para testes sem Arduino (comente o bloco abaixo ao usar com Arduino)
'''
import random
try:
    while True:
        umidade = random.randint(300, 700)
        status_bomba = "Ativa" if umidade < 500 else "Inativa"
        
        salvar_dados(umidade, status_bomba)
        atualizar_html()
        print(f"Data e Hora: {datetime.now()}, Umidade: {umidade}, Status da Bomba: {status_bomba}")
        
        time.sleep(5)
except KeyboardInterrupt:
    print("Encerrado pelo usuário.")
'''
