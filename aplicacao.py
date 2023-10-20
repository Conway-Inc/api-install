import psutil
from datetime import datetime
import mysql.connector
import platform
import time
 
conexao = mysql.connector.connect(user='user_conway', password='urubu100', host='localhost', database='ConWay', auth_plugin = 'mysql_native_password')

cursor = conexao.cursor()

def rudge_ramos():
    cont = 0
    isExibiuAlerta = False
    isExibiuCritico = False
    
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
        
            

        cursor.execute(f"INSERT INTO Registro (valor, dataHora, fkComponente, fkTotem) VALUES ({cpu_m1}, NOW(), 1, 1), ({ram_m1}, NOW(), 2, 1),({disco_m1}, NOW(), 3, 1);")
            
        conexao.commit()

        if (ram_m1 >= 85) and (ram_m1 < 95):
            if (isExibiuAlerta == False):
                cursor.execute(f"INSERT INTO Alerta (tipo, descricao, fkRegistro) VALUES (1,{ram_m1},(SELECT idRegistro FROM Registro WHERE fkTotem = 1 AND fkComponente = 2 ORDER BY dataHora DESC LIMIT 1));")
                conexao.commit()
                isExibiuAlerta = True 
                isExibiuCritico = False
        elif (ram_m1 >= 95):
            if (isExibiuCritico == False):
                cursor.execute(f"INSERT INTO Alerta (tipo, descricao, fkRegistro) VALUES (2,{ram_m1},(SELECT idRegistro FROM Registro WHERE fkTotem = 1 AND fkComponente = 2 ORDER BY dataHora DESC LIMIT 1));")
                conexao.commit()
                isExibiuAlerta = False 
                isExibiuCritico = True 
        else: 
            isExibiuAlerta = False 
            isExibiuCritico = False

        if (cpu_m1 >= 85) and (cpu_m1 < 95):
            if (isExibiuAlerta == False):
                cursor.execute(f"INSERT INTO Alerta (tipo, descricao, fkRegistro) VALUES (1,{cpu_m1},(SELECT idRegistro FROM Registro WHERE fkTotem = 1 AND fkComponente = 1 ORDER BY dataHora DESC LIMIT 1));")
                conexao.commit()
                isExibiuAlerta = True 
                isExibiuCritico = False
        elif (cpu_m1 >= 95):
            if (isExibiuCritico == False):
                cursor.execute(f"INSERT INTO Alerta (tipo, descricao, fkRegistro) VALUES (2,{cpu_m1},(SELECT idRegistro FROM Registro WHERE fkTotem = 1 AND fkComponente = 1 ORDER BY dataHora DESC LIMIT 1));")
                conexao.commit()
                isExibiuAlerta = False 
                isExibiuCritico = True 
        else: 
            isExibiuAlerta = False 
            isExibiuCritico = False
        cont+=1
        print(cont)
        # time.sleep(1)
 
if (conexao.is_connected()):
    print("A Conexão ao MySql foi iniciada ")
    rudge_ramos()
else:
    print("Houve erro ao conectar")