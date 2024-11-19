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

def CreateExpotKey (dir_files : list = os.listdir(),
                    save_path: str = os.getcwd(),
                    file_name :str = 'export_ssids_key_all.bat',
                    dir_export :str = 'ssid-key') -> dict[str, str, str, str]:
    script :str = f'netsh wlan export profile key=clear folder={save_path}\{dir_export}'

    data :dict ={
        'validation': False, 
        'fileName':file_name,
        'dir_export': dir_export
        }

    if(file_name in dir_files and dir_export in dir_files):
        data['validation'] = True
        return data

    try:
        if(dir_export not in dir_files):
            os.mkdir(dir_export)
            print(f'Criado "{dir_export}"')

        with open (file_name, 'w', encoding='utf-8') as file:
            file.write(script)

        data['validation'] = True

    except Exception as e:
        print(f'Erro durante "CreateExpotKey", Criar log para (CreateExpotKey, erro: {e})')

    return data

def ExecuteExportBat() -> bool:
    chk_dir = CreateExpotKey()

    if (chk_dir.get('validation') and chk_dir.get('fileName') != None):
        os.system(chk_dir.get('fileName'))
        
        wifi_files : list = os.listdir(chk_dir.get('dir_export'))

        if wifi_files:
            print('Redes encontradas: ' + fn.Listar(wifi_files))
            if(Validar.SimNao(message="Deseja gerar QRCode das redes encontradas: [S/N]: ", loop=True).get('Validation')):
                for i in wifi_files :
                    with open(chk_dir.get('dir_export')+'/' + i, 'r' ) as f:
                        xml = minidom.parse(f)
                        ssid = xml.getElementsByTagName('name')
                        security_type = xml.getElementsByTagName('authentication')
                        password = xml.getElementsByTagName('keyMaterial')

                        _data: object = Dados.Wifi()
                        _data.ssid = ssid[0].firstChild.data,
                        _data.key = password[0].firstChild.data,
                        _data.type_s = security_type[0].firstChild.data.replace('PSK', ''),
                        _data.fileName = _data.ssid
                        _data.update_composedPath()
                       
                        try:
                            QR_Code.url(_data)
                        except Exception as e:
                            print(e)

        return True
    
    
    return False


def SetUP()-> None:
    fn.LimparConsole()

    if('image') not in os.listdir():
        os.mkdir('image')

# @Decorator.exibeInicioFim ## TARTAR import circular
def run() -> None:
    SetUP()
    opcoes : list= [
        '[0] - Cancelar',
        '[1] - QROCDE de URL',
        '[2] - QRCODE de WI-FI',
        '[3] - Exportar todas as redes WIFI',
        # '[4] - INFO'

    ]
    msg :str ='Opcoes disponiveis: ' + fn.Listar(opcoes) + '\nDigite uma das opcoes: '

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
            # recebido = RecebeDadosURL()
            ExecuteExportBat()

    except Exception as e:
        print(Messages.mErroGenerico())

        _m: str = f'Erro durante a execucao: {choice};\n excecao: {e}'
        Logs.log_to_file(_m)

        
class Teste :
    def TesteCreateExpotKey():
        CreateExpotKey()

    def TesteExectuteExportBat():
        ExecuteExportBat()


if __name__ == '__main__':
    run()
    