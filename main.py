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
import qrcode
from PIL import Image
from xml.dom import minidom 

from util import functions as fn, Validar


save_path :str = './image/'

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
            print('Rede encontradas: ' + fn.Listar(wifi_files))
            if(Validar.SimNao(message="Deseja gerar QRCode das redes encontradas: [S/N]: ", loop=True).get('Validation')):
                for i in wifi_files :
                    with open(chk_dir.get('dir_export')+'/' + i, 'r' ) as f:
                        xml = minidom.parse(f)
                        ssid = xml.getElementsByTagName('name')
                        security_type = xml.getElementsByTagName('authentication')
                        password = xml.getElementsByTagName('keyMaterial')

                        data :dict = {
                            'ssid' : ssid[0].firstChild.data,
                            'password': password[0].firstChild.data,
                            'security_type': security_type[0].firstChild.data.replace('PSK', ''),
                            'fileName':'',
                            'fileExtension':'.png'                    
                        }
                        
                        try:
                            MakeWIFICode(
                                ssid=data.get('ssid'),
                                key=data.get('password'), 
                                type_s=data.get('security_type'), 
                                )
                        except Exception as e:
                            print(e)

        return True
    
    
    return False


def RecebeDadosURL() -> dict[str, str, str, str, str, str]:
    url :str =''
    fileName :str = 'QRCODE_'
    fileExtension :str = '.png'
    savepath :str = save_path

    msg :str = 'Digite a url: '
    url = input(msg)
    fileName += fn.ReplaceURL(url)
    changeFileName :str = input(f'Deseja renomear o arquivo final ({fileName}{fileExtension}) [S/N]: ')
    if (changeFileName[0].lower() == 's'):
        fileName = input('Digite o nome do arquivo com extensao: ')
        fileExtension = fileName[fileName.find('.')::]
        fileName = fileName.replace(fileExtension, '')

    _send :dict = {
        'url' : url,
        'fileName' : fileName,
        'fileExtension' : fileExtension,
        'savepath' : savepath
    }

    return _send

def RecebeDadosWIFI() -> dict[str, str, str, str, str, str]:
    ssid :str = ''
    key :str = ''
    type_s :str = ''
    hidden :str = 'False'
    fileName :str = 'QRCode_WI-FI-'
    fileExtension :str = '.png'
    savePath :str = save_path

    listaTiposSeguranca :list= [
        '    [1] (WPA) Wi-Fi Protected Access (Padrao)',
        '    [2] (WEP) Wired Equivalent Privacy',
        '    [3] (WPA 2) Wi-Fi Protected Access 2',
        '    [4] (WPA 3) Wi-Fi Protected Access 3',
    ]

    TipoSegurancaValoresAceitos :list = [str(i).strip()[1] for i in listaTiposSeguranca]
    VarloTiposSeguranca :dict[str, str]= {}

    for i in listaTiposSeguranca:
        i  = str(i).strip().replace(" ", '')
        VarloTiposSeguranca[i[1]] = i[i.index('(') +1: i.index(')')]


    msgs :dict = {
        'ssid' :  'Digite o nome da rede (SSID): ',
        'key' :  'Digite o senha da rede (Key/Password): ',
        'type_s' : f'Tipos de seguraca disponiveis: {fn.Listar(listaTiposSeguranca)} \nDigite o tipo de seguranca: ' 
    }

    ssid  = input(msgs.get('ssid'))
    key  = input(msgs.get('key'))
    i_type_s  = input(msgs.get('type_s'))

    try:
        type_s = VarloTiposSeguranca.get(i_type_s) if(i_type_s in TipoSegurancaValoresAceitos) else VarloTiposSeguranca.get('1')
    except:
        type_s = VarloTiposSeguranca.get('1')


    msg_validar :str =  f'Deseja renomear o arquivo final ({fileName + ssid + fileExtension}) [S/N]: '
    if (Validar.SimNao(message= msg_validar, loop=True).get('Validation')):
        file :dict= fn.RenomearArquivoFinal(fileName= fileName, fileExtension= fileExtension)
        fileName = file.get('fileName')
        fileExtension = file.get('fileExtension')

    data :dict = {
        'ssid' :ssid,
        'key' : key ,
        'type_s' : type_s, 
        'hidden' : hidden ,
        'fileName' :fileName, 
        'fileExtension' : fileExtension,
        'savePath' : savePath
    }
    return data

def MakeURLCode (url :str, fileName :str='QRCode_', fileExtension :str = '.png', savePath :str = save_path, tipo :int= 0) -> None:
    img = qrcode.make(url)
    composedPath :str = ''

    if(tipo == 1 ): #WI-FI
        composedPath = fileName
    else: 
        composedPath = save_path + fileName.replace(' ', '_') + fileExtension

    img.save(composedPath)
    print(f'URL Gerada: {url}')
    print(f'Arquivo salvo em: {composedPath}')
    ShowImage(composedPath)

def MakeWIFICode( ssid :str, key :str, type_s :str,
                 hidden :str = 'false',
                 fileName :str='QRCODE_WI-FI_',
                 fileExtension :str='.png',
                 savePath :str = save_path) -> None: 
    
    hidden = hidden.lower()

    composedPath :str= savePath + (fileName + ssid).replace(' ', '_') + fileExtension

    wifi_url :str = f'WIFI:S:{ssid};T:{type_s};P:{key};H:{hidden};'

    MakeURLCode(url =wifi_url, fileName= composedPath, tipo=1)

def ShowImage(path :str )-> None:
    img = Image.open(path)
    img.show()

def ListarDisponiveis()-> None:
    dir

def SetUP()-> None:
    fn.LimparConsole()
    if('image') not in os.listdir():
        os.mkdir('image')

def __init__() -> None:
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
            print('Encerrando Execucao..')
        
        if choice == 1: #URL
            recebido = RecebeDadosURL()
            MakeURLCode(url=recebido.get('url'), fileName=recebido.get('fileName'))

        if choice == 2: #WI-FI
            recebido = RecebeDadosWIFI()
            MakeWIFICode(ssid=recebido.get('ssid'),key=recebido.get('key'), type_s=recebido.get('type_s'), fileName=recebido.get('fileName'),fileExtension=recebido.get('fileExtension'))

        if choice == 3: #WI-FI EXPORT
            # recebido = RecebeDadosURL()
            ExecuteExportBat()

    except Exception as e:
        print('Erro...')

        with open('logExecution.txt', 'w') as file:
            file.write(f'Erro durante a execucao: {choice};\n excecao: {e}')
        
class Teste :
    def TesteCreateExpotKey():
        CreateExpotKey()

    def TesteExectuteExportBat():
        ExecuteExportBat()

    def TesteListar():
        fn.Listar([''])

    def TeteReplaceURL():
        fn.ReplaceURL('www.google.com')

    def TesteRecebeDadosURL():
        RecebeDadosURL()

    def TesteRecebeDadosWIFI():
        RecebeDadosWIFI()


if __name__ == '__main__':
    __init__()
    