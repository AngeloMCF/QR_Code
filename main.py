# (Optional) python -m venv venv
# (Optional) ./venv/Scripts/Activate.ps1

# pip install requirements.txt
# pip freeze > requirements.txt

# https://pypi.org/project/qrcode/

# pip install qrcode

# url = 'WIFI:S:<SSID>;T:WPA<ENCRYPTION_TYPE>;P:<KEY>;H:<HIDDEN_SSID(true/false)>;'
#        ^    ^        ^                      ^       ^
#        |    |        |                      |       +-- hidden SSID (true/false)
#        |    |        |                      +-- WPA KEY       
#        |    |        +-- encryption type       
#        |    +-- ESSID       
#        +-- Code Type   

import os
import os.path
from PIL import Image
from xml.dom import minidom 

from config import save_path
from util import functions as fn, Validar, Logs
from dados import Dados
from mensagens import Messages
from makeqrcode import QR_Code
from exportwifi import ExportWIFI


def SetUP()-> None:
    fn.LimparConsole()

    if('image') not in os.listdir():
        os.mkdir('image')

# @Decorator.exibeInicioFim ## TARTAR import circular
def run() -> None:
    SetUP()
    print(Messages.mInicioExecucao())
    opcoes : list= [
        '[0] - Cancelar',
        '[1] - QROCDE de URL',
        '[2] - QRCODE de WI-FI',
        '[3] - Exportar todas as redes WIFI',
        # '[4] - INFO'

    ]
    msg :str ='Opcoes disponiveis: ' + fn.Listar(opcoes, sep='\n\t') + '\nDigite uma das opcoes: '

    choice :int= -1

    try:
        choice =int(input(msg))
        if choice == 0:
            print(Messages.mFimExecucao())
        
        if choice == 1: #URL
            data = Dados.Url()
            recebido = data.EntradaDados()
            img = QR_Code.url(recebido)
            QR_Code.Show(img)

        if choice == 2: #WI-FI
            data = Dados.Wifi()
            recebido = data.EntradaDados()
            img = QR_Code.url(recebido)
            QR_Code.Show(img)

        if choice == 3: #WI-FI EXPORT
            ExportWIFI().export_wifi()

    except Exception as e:
        print(Messages.mErroGenerico())

        _m: str = f'Erro durante a execucao: {choice};\n excecao: {e}'
        Logs.log_to_file(_m)

if __name__ == '__main__':
    run()
    