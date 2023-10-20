from json import loads
from time import sleep
from urllib3 import PoolManager
import os
import sys
import mysql.connector
import psutil
import platform
from datetime import datetime

# Configurações de conexão com o banco de dados
config = {
    'user': 'user_conway',
    'password': 'urubu100',
    'host': 'localhost',
    'database': 'ConWay',
}
conexao = mysql.connector.connect(**config)
cursor = conexao.cursor()

#Cores no terminal
vermelho = "\033[91m"
verde = "\033[92m"
amarelo = "\033[93m"
ciano = "\033[96m"
padrao = "\033[0m"

global idtotem
idtotem = 1

#Função para retirar , e colocar .
def conversor(valor):
    return float(valor[0:4].replace(",", '.'))

# Função para o usuario digitar um valor inválido
def msgErro():
    print(f"\n{vermelho}+--------------------------------------------+")
    print(f"|           {amarelo}DIGITE UM VALOR VÁLIDO!          {vermelho}|")
    print(f"+--------------------------------------------+{padrao}\n")

# Função para encerrar o programa
def encerrar():
    print(f"\n{vermelho}+--------------------------------------------+")
    print(f"|    {ciano}Obrigada por usar Air Way!    {vermelho}|")
    print(f"+--------------------------------------------+\n")
    sleep(3)
    sys.exit()

def limparTela():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix (Linux, macOS)
        os.system('clear')

def aplicacao():
    rodar = True
    while (rodar):
        print(f"{vermelho}+--------------------------------------------+")
        print(f"|                 {ciano}Air Way                    {vermelho}|")
        print(f"+--------------------------------------------+")
        print(f"| {padrao}Seleciona abaixo a opção que lhe agrada    {vermelho}|")
        print(f"|                                            |")
        print(f"|  {ciano}[1]{padrao} Ao vivo - Memoria, CPU e Disco        {vermelho}|")
        print(f"|  {ciano}[2]{padrao} Histórico - Memoria, CPU e Disco      {vermelho}|")
        print(f"|  {ciano}[3]{padrao} Encerrar Programa                     {vermelho}|")
        print(f"|                                            |")
        resposta = int(input(f"+--------------------------------------------+{padrao}\n\n"))

        limparTela()

        if(resposta == 1):
            temps()
        elif(resposta == 2):
            historico()
        elif(resposta == 3):
            encerrar()
        else:
            msgErro()

def historico():
    cursor.execute(f"SELECT DATE_FORMAT(data, '%Y-%m') as data  FROM vw_RegistroEstruturado as r JOIN Totem as t ON r.id = t.idTotem AND t.idTotem = {1} group by DATE_FORMAT(data, '%Y-%m')")
    resultados = cursor.fetchall()

    print(f"{vermelho}+--------------------------------------------+")
    print(f"|                 {ciano}Air Way                    {vermelho}|")
    print(f"+--------------------------------------------+")
    print(f"| {padrao}Selecione abaixo o mês que deseja ver      {vermelho}|")
    print(f"|                                            |")
    print(f"|  {ciano}[0]{padrao} Voltar                                {vermelho}|")
   
    for i in range(len(resultados)):
        print(f"|  {ciano}[{i+1}]{padrao} Data: {resultados[i][0]}                         {vermelho}|")

    print(f"|                                            |")
    resposta = int(input(f"+--------------------------------------------+{padrao}\n\n"))

    limparTela()

    cont = 0
    for i in range(len(resultados)):
        cont+=1
        if(resposta == cont):
            exibirInfos(resultados[i][0])
    
    if (resposta == 0):
        aplicacao()
            
    

def exibirInfos(data):
    idtotem = 1
    cursor.execute(f"SELECT DATE_FORMAT(data, '%h:%i:%s') as data, cpu, memoria, disco FROM vw_RegistroEstruturado WHERE id = {idtotem} AND data like '{data}%'")
    resultados = cursor.fetchall()

    print(f"{vermelho}+--------------------------------------------+")
    print(f"|                 {ciano}Air Way                    {vermelho}|")
    print(f"+--------------------------------------------+")
    print(f"| {padrao}Exibindo histórico de {data}              {vermelho}|")
    print(f"|                                            |")
    print(f"|  {ciano}[0]{padrao} Voltar                                {vermelho}|")

    for i in range(len(resultados)):
        print(f"|  {ciano}Hora: {resultados[i][0]}                            {vermelho}|")
        print(f"|        CPU: {resultados[i][1]}                          {vermelho}|")
        print(f"|        Memória: {resultados[i][2]}                      {vermelho}|")
        print(f"|        Disco: {resultados[i][3]}                        {vermelho}|")

    print(f"|                                            |")
    resposta = int(input(f"+--------------------------------------------+{padrao}\n\n"))

    limparTela()

    if(resposta == 0):
        aplicacao()
    else:
        msgErro()
    


def temps():    

    cont = 0

    qtd_core = psutil.cpu_count(logical=False)
    cpu_um_speed_max = psutil.cpu_freq().max / pow(10,3)
    ram_um_total = (psutil.virtual_memory().total) / pow(10,9)
    so = platform.system()
    if (so == 'Windows'):
        disco_um_total = psutil.disk_usage('C:\\').total / pow(10,9)
    elif (so == 'Linux'):
        disco_um_total = psutil.disk_usage('/bin').total / pow(10,9)

    while True:
            
        data = datetime.now()
        data = data.strftime('%Y/%m/%d %H:%M:%S')
        cpu_m1 = psutil.cpu_percent(interval=1)
        cpu_m1_speed = psutil.cpu_freq().current / pow(10,3)
        ram_m1_used = (psutil.virtual_memory().used) / pow(10,9)
        ram_m1 = psutil.virtual_memory().percent
        if (so == 'Windows'):
            disco_m1 = psutil.disk_usage('C:\\').percent
        elif (so == 'Linux'):
            disco_m1 = psutil.disk_usage('/bin').percent
                                               
        limparTela()

        print(f"{vermelho}+--------------------------------------------+")
        print(f"|                 {ciano}Air Way                    {vermelho}|")
        print(f"+--------------------------------------------+")
        print(f"| {padrao}Para sair, aguarde o tempo 10              {vermelho}|")
        print(f"| {padrao}Tempo: {cont+1}s                                  {vermelho}|")
        print(f"|                                            |")
        print(f"|  {ciano}[CPU]{padrao} Atual usada é de: {(cpu_m1)} °C           {vermelho}|")
        print(f"|  {ciano}[Memória]{padrao} Atual usada é de: {(ram_m1)} %        {vermelho}|")
        print(f"|  {ciano}[Disco]{padrao} Atual usada é de: {(disco_m1)} %          {vermelho}|")
        print(f"|                                            |")
        print(f"+--------------------------------------------+{padrao}\n")

        cont += 1

        if(cont >= 10):
            limparTela()
            aplicacao()

aplicacao()