# from config import save_path
from util import functions as fn, Decorator

class DefaultUrl:
    
    def __init__(self, url: str = '', fileName: str = 'QRCODE_', fileExtension: str = 'png', savepath: str = './image/'):
        '''Por algum motivo as strings estao como tuplas olhar depois'''

        self.url= url,
        self.fileName= fileName, 
        self.fileExtension= fileExtension, 
        self.savepath= savepath


class DefaultWifi:
    
    def __init__(self 
                ,ssid :str = ''
                ,key :str = ''
                ,type_s :str = ''
                ,hidden :str = 'False'
                ,fileName :str = 'QRCode_WI-FI-'
                ,fileExtension :str = 'png'
                ,savepath: str = './image/'):
        '''Por algum motivo as strings estao como tuplas olhar depois'''
        self.ssid = ssid
        self.key = key
        self.type_s = type_s
        self.hidden = hidden
        self.fileName = fileName
        self.fileExtension = fileExtension
        self.savepath= savepath

    def tiposSeguranca() -> list [str, str]:
        _listaTiposSeguranca :list= [
            '    [1] (WPA) Wi-Fi Protected Access (Padrao)',
            '    [2] (WEP) Wired Equivalent Privacy',
            '    [3] (WPA 2) Wi-Fi Protected Access 2',
            '    [4] (WPA 3) Wi-Fi Protected Access 3',
        ]

        return _listaTiposSeguranca
    
    def tipoSegurancaValoresAceitos() -> list[str, str]:
        return [str(i).strip()[1] for i in DefaultWifi.tiposSeguranca()]
    
    def ValorTiposSeguranca() -> dict [str, str]:
        _d :dict = {}
        
        for i in DefaultWifi.tiposSeguranca():
            i  = str(i).strip().replace(" ", '')
            _d [i[1]] = i[i.index('(') +1: i.index(')')]
    
        return _d


class Messages:
    ''' Classe de Mensagens gerais da Dados'''

    def mInicioExecucao() -> str: return 'Encerrando Execucao..'
    def mFimExecucao() -> str: return 'Encerrando Execucao..'
    def mErroGenerico() -> str: return 'Erro...'

    def mEntradaUrl() -> str: return 'Digite a url: ' 
    def mEntradaFileName() -> str: return 'Digite o nome do arquivo com extensao: '

    def mEchangeFileName(_fileName: str, _fileExtension : str) -> str: return f'Deseja renomear o arquivo final ({_fileName}.{_fileExtension}) [S/N]: '

    def mEntradaSSID() -> str: return 'Digite o nome da rede (SSID): '
    def mEntradakey() -> str: return 'Digite o senha da rede (Key/Password): '
    def mEntradaListatype_s() -> str: return 'Tipos de seguraca disponiveis: '
    def mEntradatype_s() -> str: return 'Digite o tipo de seguranca: '

    def formataMeensagemTipoSeguranca() -> str:
         return f'{Messages.mEntradaListatype_s()} {fn.Listar(Dados.Wifi.tiposSeguranca())} \n{Messages.mEntradatype_s()}'


class Dados:

    def changeFileName(_fileName: str, _fileExtension: str, userInput = True) -> tuple[str, str]:
        '''Troca o nome do arquivo de destino

        return fileName, fileExtension
        '''
        
        if userInput: _fileName = input(Messages.mEntradaFileName()) 

        _fileExtension = _fileName[_fileName.find('.')::]
        _fileName = _fileName.replace(_fileExtension, '')

        return _fileName, _fileExtension
        
    class Url(DefaultUrl):
        def __init__(self):
            super().__init__()

        def EntradaDados(self, userInput = True) :
            
            self.url = input(Messages.mEntradaUrl())
            self.fileName = fn.ReplaceURL(self.url)
            self.changeFileName :str = input( Messages.mEchangeFileName(self.fileName,self.fileExtension))

            if (self.changeFileName[0].lower() == 's'):
                self.fileName, self.fileExtension = Dados.changeFileName()

            return self

    class Wifi(DefaultWifi):
        def __init__(self):
            super().__init__()

        def getTiposSeguranca():
            return DefaultWifi.tiposSeguranca() 
        
        def getValorTiposSeguranca():
            return DefaultWifi.ValorTiposSeguranca() 
        
        def getTipoSegurancaValoresAceitos():
            return DefaultWifi.tipoSegurancaValoresAceitos()

        def EntradaDados(self, userInput = True) :
            
            self.ssid = input(Messages.mEntradaSSID())
            self.key = input(Messages.mEntradakey())
            i_type_s = input(Messages.formataMeensagemTipoSeguranca())

            _listaTipoSegurancaValoresAceitos: list =  Dados.Wifi.getTipoSegurancaValoresAceitos() 
            _d_ValorTiposSeguranca: dict = Dados.Wifi.getValorTiposSeguranca() 

            try:
                self.type_s = _d_ValorTiposSeguranca.get(i_type_s) if(i_type_s in _listaTipoSegurancaValoresAceitos) else _d_ValorTiposSeguranca.get('1')
            except:
                self.type_s = _d_ValorTiposSeguranca.get('1')

            _changeFileName :str = input( Messages.mEchangeFileName(self.fileName+self.ssid,self.fileExtension))

            if (_changeFileName[0].lower() == 's'):
                self.fileName, self.fileExtension = Dados.changeFileName()

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

        # @Decorator.tFunction
        def tEntradaDadosURL():
            _data = Dados.Url()
            _data.EntradaDados
            print('tEntradaDadosURL ta sem teste')

        def run():
            '''Executa todos os teste da classe'''
            Testes.tDadosURL.tUrl()
            Testes.tDadosURL.tchangeFileName()
            Testes.tDadosURL.tEntradaDadosURL()

    class tDadosWifi:

        @Decorator.tFunction
        def tWifi():
            _data1 = Dados.Wifi()

        def tEntradaDados():
            data = Dados.Wifi()
            recebido = data.EntradaDados()
            
        def run():
            '''Executa todos os teste da classe'''
            Testes.tDadosWifi.tWifi()
            Testes.tDadosWifi.tEntradaDados()


    def run():
        # Testes.tDadosURL.run()
        Testes.tDadosWifi.run()

if __name__ == '__main__':
    fn.LimparConsole()

    Testes.run()