# from config import save_path
from util import functions as fn, Decorator
from mensagens import Messages

class DefaultArquivo:
    
    def __init__(self, url:str, fileName: str , fileExtension: str, savepath: str ):
        '''Por algum motivo as strings estao como tuplas olhar depois
            Utilizando tratar_dados_tupla() para solução temporária
        '''
        
        self.url= url
        self.fileName= fileName
        self.fileExtension= fileExtension
        self.savepath= savepath
        self.composedPath = str(savepath + fileName +'.' + fileExtension)

    def tratar_dados_tupla(self) -> None:

        if (type(self.fileName) == tuple):
            self.fileName = self.fileName[0]

        if (type(self.fileExtension) == tuple):
            self.fileExtension = self.fileExtension[0]

    def update_composedPath(self) -> None:
        self.tratar_dados_tupla()
        self.composedPath = str(self.savepath + self.fileName + '.' + self.fileExtension)

class Dados:

    def changeFileName(_fileName: str, _fileExtension: str, userInput = True) -> tuple[str, str]:
        '''Troca o nome do arquivo de destino

        return fileName, fileExtension
        '''
        
        if userInput: _fileName = input(Messages.mEntradaFileName()) 

        _fileExtension = _fileName[_fileName.find('.')::]
        _fileName = _fileName.replace(_fileExtension, '')

        return _fileName, _fileExtension
        

    class Url(DefaultArquivo):
        def __init__(self, url: str = '', fileName: str = 'QRCode-', fileExtension: str = 'png', savepath: str = './image/'):
            super().__init__( url, fileName, fileExtension, savepath )
            self.update_composedPath()

        def EntradaDados(self, userInput = True) :
            
            if userInput:
                self.url = input(Messages.mEntradaUrl())
                self.fileName = fn.ReplaceURL(self.url)
                self.changeFileName :str = input( Messages.mEchangeFileName(self.fileName,self.fileExtension)) if userInput else 'n'

                if (self.changeFileName[0].lower() == 's'):
                    self.fileName, self.fileExtension = Dados.changeFileName(userInput =userInput)
            
            self.update_composedPath()

            return self

    
    class Wifi(DefaultArquivo):

        def __init__(self,
            ssid :str = ''
            ,key :str = ''
            ,type_s :str = 'WPA'
            ,hidden :str = 'false'
            ,url: str = '', fileName: str = 'QRCode_WI-FI-', fileExtension: str = 'png', savepath: str = './image/'):
            super().__init__( url, fileName, fileExtension, savepath )
            self.ssid = ssid
            self.key = key
            self.type_s = type_s
            self.hidden = hidden

            self.update_composedPath()

        class TiposSeguranca(object):
            
            def getTiposSeguranca(self) -> list [str, str]:
                _listaTiposSeguranca :list= [
                    '    [1] (WPA) Wi-Fi Protected Access (Padrao)',
                    '    [2] (WEP) Wired Equivalent Privacy',
                    '    [3] (WPA 2) Wi-Fi Protected Access 2',
                    '    [4] (WPA 3) Wi-Fi Protected Access 3',
                ]

                return _listaTiposSeguranca
             
            def getValorTiposSeguranca(self) -> dict [str, str]:
                _d :dict = {}
                
                for i in self.getTiposSeguranca():
                    i  = str(i).strip().replace(" ", '')
                    _d [i[1]] = i[i.index('(') +1: i.index(')')]
            
                return _d

            def formataMeensagemTipoSeguranca(self) -> str:
                return f'{Messages.mEntradaListatype_s()} {fn.Listar(self.getTiposSeguranca())} \n{Messages.mEntradatype_s()}'
            
            def getTipoSegurancaValoresAceitos(self) -> list[str, str]:
                return [str(i).strip()[1] for i in self.getTiposSeguranca()]


        def EntradaDados(self, userInput = True) :

            if userInput:            
                self.ssid = input(Messages.mEntradaSSID())
                self.key = input(Messages.mEntradakey())
                # self.hidden = input(Messages.mEntradaHidden())
                _TiposSeguranca:object = self.TiposSeguranca() 
                i_type_s = input(_TiposSeguranca.formataMeensagemTipoSeguranca())

                self.fileName += self.ssid

                _changeFileName :str = input( Messages.mEchangeFileName(self.fileName,self.fileExtension))

                if (_changeFileName[0].lower() == 's'):
                    self.fileName, self.fileExtension = Dados.changeFileName(userInput = userInput)

                _listaTipoSegurancaValoresAceitos: list =  _TiposSeguranca.getTipoSegurancaValoresAceitos() 
                _d_ValorTiposSeguranca: dict = _TiposSeguranca.getValorTiposSeguranca() 

                try:
                    self.type_s = _d_ValorTiposSeguranca.get(i_type_s) if(i_type_s in _listaTipoSegurancaValoresAceitos) else _d_ValorTiposSeguranca.get('1')
                except:
                    self.type_s = _d_ValorTiposSeguranca.get('1')

            self.url = f'WIFI:S:{self.ssid};T:{self.type_s};P:{self.key};H:{self.hidden.lower()};'
            self.update_composedPath()

            return self


class Testes:
    '''Testes da Dados'''

    class tDadosURL:

        @Decorator.tFunction
        def tUrl():
            _data1 = Dados.Url()

        @Decorator.tFunction
        def tchangeFileName():
            _f = Dados.Url
            _old = _f()
            _new = _f()
            _new.fileName, _new.fileExtension = Dados.changeFileName('NomeArquivoNome.jpg', 'png', False)
            if _old.fileName == _new.fileName: raise 

        @Decorator.tFunction
        def tEntradaDadosURL():
            _data = Dados.Url()
            _data.url = 'teste.com'
            _data.fileName = 'Qr_code-teste'
            _data.EntradaDados(userInput=False)

        def run():
            '''Executa todos os teste da classe'''
            Testes.tDadosURL.tUrl()
            Testes.tDadosURL.tchangeFileName()
            Testes.tDadosURL.tEntradaDadosURL()

    class tDadosWifi:

        @Decorator.tFunction
        def tWifi():
            _data1 = Dados.Wifi()

        @Decorator.tFunction
        def tEntradaDados():
            data = Dados.Wifi()
            data.ssid = 'nomeRedeTEste'
            data.key = 'senhateste'
            data.type_s = 'WPA'
            data.fileName += data.ssid
            data.update_composedPath()
            recebido = data.EntradaDados(userInput=False)
            print('Teste Nao finalizado')
            # a = recebido
            # recebido = data.EntradaDados()
            
        def run():
            '''Executa todos os teste da classe'''
            Testes.tDadosWifi.tWifi()
            Testes.tDadosWifi.tEntradaDados()


    def run():
        Testes.tDadosURL.run()
        Testes.tDadosWifi.run()

if __name__ == '__main__':
    fn.LimparConsole()

    Testes.run()