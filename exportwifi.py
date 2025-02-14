import os

from xml.dom import minidom 

from util import functions as fn, Logs, Validar, Decorator
from mensagens import Messages
from dados import Dados
from makeqrcode import QR_Code


class ExportWIFI():

    def __init__(self, 
                dir_files : list = os.listdir(),
                save_path: str = os.getcwd(),
                file_name :str = 'export_ssids_key_all.bat',
                dir_export :str = 'ssid-key'
                ):
        self.dir_files = dir_files
        self.save_path = save_path
        self.file_name = file_name
        self.dir_export = dir_export

        if(self.dir_export not in self.dir_files):
            os.mkdir(self.dir_export)


    def create_script_bat(self) -> dict[str, str, str, str]:
        script :str = f'@echo off \nnetsh wlan export profile key=clear folder={self.save_path}\{self.dir_export} > {self.save_path}\{self.dir_export}\_remove.txt'

        if(self.file_name in self.dir_files and self.dir_export in self.dir_files):
            return True

        try:
            with open (self.file_name, 'w', encoding='utf-8') as file:
                file.write(script)

            return True

        except Exception as e:
            m: str = f'Erro durante {ExportWIFI.create_script_bat.__name__}, erro: {e})'
            Logs.log_to_file(m)

        return False


    def executeExportBat(self) -> bool:
        
        if (self.create_script_bat() and self.file_name != None):
            try:
                os.system(self.file_name)

                if '_remove.txt' in os.listdir(self.dir_export ):
                    os.remove(f'{self.dir_export}\_remove.txt')

                return True

            except Exception as e:
                m: str = f'Erro durante {ExportWIFI.executeExportBat.__name__}, erro: {e})'
                Logs.log_to_file(m)

        return False
    

    def create_qrcode_export_wifi(self, wifi_list: list) -> None:
        for i in wifi_list :
            with open(f'{self.dir_export}/{i}', 'r' ) as f:
                xml = minidom.parse(f)
                ssid = xml.getElementsByTagName('name')
                security_type = xml.getElementsByTagName('authentication')
                password = xml.getElementsByTagName('keyMaterial')

                _data: object = Dados.Wifi()
                _data.ssid = str(ssid[0].firstChild.data),
                _data.key = password[0].firstChild.data,
                _data.type_s = security_type[0].firstChild.data.replace('PSK', ''),
                _data.fileName = _data.ssid
                _data.update_composedPath()
                _data.update_url()

                try:
                    QR_Code.url(_data, False)
                except Exception as e:
                    m: str = f'Erro durante {ExportWIFI.create_qrcode_export_wifi.__name__}, erro: {e})'
                    Logs.log_to_file(m)

        print(f'Arquivos salvo em: ./{self.dir_export}')


    def export_wifi(self, user_input :bool = True) -> None:
        
        self.executeExportBat()
        wifi_files : list = os.listdir(self.dir_export) if os.path.exists(self.dir_export) else []

        if len(wifi_files) <= 0: 
            print('Nenhuma rede Wifi encontrada.')
            return

        if user_input :
            _wifi_files = [str(i).replace('Wi-Fi-', '').replace('.xml','') for i in wifi_files ]
            print('Redes encontradas: ' + fn.Listar(_wifi_files, sep = '\n\t'))
            if(Validar.SimNao(message="Deseja gerar QRCode das redes encontradas: [S/N]: ", loop=True)):
                self.create_qrcode_export_wifi(wifi_files)
            

class Testes():

    @Decorator.tFunction
    def tcreate_script_bat():
        ExportWIFI().create_script_bat()

    @Decorator.tFunction
    def texecuteExportBat():
        if (not ExportWIFI().executeExportBat()): raise

    @Decorator.tFunction
    def tcreate_qrcode_export_wifi():
        ExportWIFI().create_qrcode_export_wifi(os.listdir('ssid-key'))

    @Decorator.tFunction
    def texport_wifi():
        ExportWIFI().export_wifi(user_input=False)
        ExportWIFI().export_wifi(user_input=True)

    def run():
        
        fn.LimparConsole()
        Testes.tcreate_script_bat()
        Testes.texecuteExportBat()
        Testes.tcreate_qrcode_export_wifi()
        Testes.texport_wifi()


if __name__ == '__main__':
    if('image') not in os.listdir(): os.mkdir('image')

    Testes.run()
    