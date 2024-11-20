
class Messages:
    ''' Classe de Mensagens gerais da Dados'''

    def mInicioExecucao() -> str: return 'Iniciando Execucao..'
    def mFimExecucao() -> str: return 'Encerrando Execucao..'
    def mErroGenerico() -> str: return 'Erro...'

    def mEntradaUrl() -> str: return 'Digite a url: ' 
    def mEntradaFileName() -> str: return 'Digite o nome do arquivo com extensao: '

    def mEchangeFileName(_fileName: str, _fileExtension : str) -> str: return f'Deseja renomear o arquivo final ({_fileName}.{_fileExtension}) [S/N]: '

    def mEntradaSSID() -> str: return 'Digite o nome da rede (SSID): '
    def mEntradakey() -> str: return 'Digite o senha da rede (Key/Password): '
    def mEntradaListatype_s() -> str: return 'Tipos de seguraca disponiveis: '
    def mEntradaHidden() -> str: return 'Rede oculta? [S/N] (default N) : '
    def mEntradatype_s() -> str: return 'Digite o tipo de seguranca: '

    
