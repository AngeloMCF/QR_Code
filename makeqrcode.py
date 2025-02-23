import qrcode
from PIL import Image
from PIL import ImageDraw

from config import save_path
from util import functions as fn, Validar, Logs, Decorator
from dados import Dados, DefaultArquivo

class QR_Code:

    def Show(data : DefaultArquivo) -> None:
        try:
            fn.ShowImage(data.composedPath)
        except Exception as e:
            m: str = f'Erro durante a execução de {QR_Code.Show.__name__}'
            Logs.log_to_file(m)


    def url( data: DefaultArquivo, show_info: bool = True) -> object:

        data.status = False
        data.update_composedPath()

        try:
            img = qrcode.make(data.url)
            img.save(data.composedPath)
            data.status = True
            if show_info:
                print(f'URL Gerada: {data.url}')
                print(f'Arquivo salvo em: {data.composedPath}')

        except Exception as e:
            m: str = f'Erro durante a execução de {QR_Code.url.__name__}'
            Logs.log_to_file(m)
        
        return data
    
    
    def inserText(data: DefaultArquivo, text:str) -> None:
        try:
            img = Image.open(data.composedPath)
            _img = ImageDraw.Draw(img)
            width:float = img.width*0.14
            height:float = img.height*0.91 

            _img.text((width,height), text)
            img.save(data.composedPath)

        except Exception as e:
            m: str = f'Erro durante a execução de {QR_Code.inserText.__name__}'
            Logs.log_to_file(m)


    def Generate(data: DefaultArquivo, show_info: bool = True, text:str=''):
        img = QR_Code.url( data, show_info)
        QR_Code.inserText(data, text if len(text)> 0 else data.text)
        return img


class Teste:
    
    @Decorator.tFunction
    def tQR_CodeUrl():
        data = Dados.Url()
        data.url = 'teste.com'
        t = QR_Code
        t1 = t.Generate(data, False)

        if (not t1.status): raise

        data.fileName = 'teste'
        t2 = t.Generate(data, False)
        if (not t2.status): raise

    @Decorator.tFunction
    def tQR_CodeShow():
        data = Dados.Url()
        data.url = 'teste1.com'
        data.fileName = 'teste1'
        QR_Code.Generate(data, False)
        QR_Code.Show(data)

    @Decorator.tFunction
    def tQr_Codewifi():
        data = Dados.Wifi()
        data.ssid = 'nomeRede'
        data.key = 'senha'
        data.fileName = 'QRODE-' + data.ssid
        data.type_s =  data.TiposSeguranca().getValorTiposSeguranca().get('1') 
        data.update_url()
        QR_Code.Generate(data, False)

    
    def run():
        fn.LimparConsole()
        Teste.tQR_CodeUrl()
        Teste.tQR_CodeShow()
        Teste.tQr_Codewifi()

if __name__ == '__main__':

    Teste.run()
   