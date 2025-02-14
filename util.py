import os
from PIL import Image
# from dados import Messages

class Validar:

    def SimNao(message :str ='Digite [S/N]: ', loop :bool = False) -> bool:
        '''
        :params:
            :message: Usa a default caso não seja passado.

            :loop: True/False, ativar loop de validacao

            :acepted_values: ['s', '1', 'y', 'n', '0']
            
            :retrun:  bool
        '''
        _char = input(message).strip()[0].lower()

        _acepted_values:list = ['s', '1', 'y', 'n', '0']
        
        if(_char in _acepted_values):
            return _char in _acepted_values[0:3] 

        if (loop) :
            while True:
                print(f'Valor invalido: "{_char}"')
                _char = input(message).strip()[0].lower()
                if(_char in _acepted_values):
                    return _char in _acepted_values[0:3]

    def NumeroInteiro(char:str =''.replace(',', "."), message :str ='Digite o numero: ',  loop :bool = False) -> dict[bool, str]:
        '''
        :params
        :loop:True/False, ativar loop de validacao
        '''
        data :dict = {
            'Validation' : False,
            'char' : char
        }

        if (not char):
            char = input(message).replace(',', ".")
        
        try :
            if not char : char =''
            char = int(char) 
            data['char'] = char 
            data['Validation'] = True

        except Exception as e:
           pass

        if (loop and not data['Validation']) :
            print(f'Valor invalido: "{char}"')

            while not data['Validation']:
                try :
                    char = input(message).replace(',', ".")
                    if not char : char =''
                    char = int(char) 
                    data['char'] =  char 
                    data['Validation']  =  True
                    print(data['Validation'])

                except ValueError as e:
                    print(f'Valor invalido, nao e um valor valido: "{char}"')
                except Exception as e:
                    print(e)
                    print(f'Valor invalido: "{char}"')
                print(data)

        return data

    class Teste:
        def Message(usedfunction, status :bool = True) -> None:
            passed :str = 'PASS'
            faild :str = 'FAILD'

            print(f'TEST "{usedfunction.__name__}": {passed if status else faild}')


class functions:

    def LimparConsole() -> None: os.system('cls')


    def cria_diretorio(dir_name: str) -> None:
        os.mkdir(dir_name)


    def Listar(lista :list, sep = '\n') -> str:
        message :str = ''

        for i in lista:
            message += sep + i

        return message


    def RenomearArquivoFinal(fileName :str,fileExtension :str, message :str ='Digite o nome do arquivo com extensao: ') -> dict[str, str]:
        originalName :str = fileName + fileExtension

        name = input(message)
        
        if not name: name = fileName + fileExtension

        print(f'Arquivo renomeado para: {name}')
        
        fileExtension = name[name.find('.')::]
        fileName = name.replace(fileExtension, '')

        while True :
            if (Validar.SimNao(message= 'O nome digitado está correto [S/N]: ', loop=True).get('Validation')):
                break
            
            name = input(message)
            if not name: name = fileName + fileExtension
            
            fileExtension = name[name.find('.')::]
            fileName = name.replace(fileExtension, '')
            print(f'Arquivo renomeado para: {name}')

        data :dict={
            'file': fileName + fileExtension, 
            'fileName' : fileName, 
            'fileExtension' :fileExtension
        }
        print(f'Arquivo renomeado de "{originalName}" para "{fileName + fileExtension}".')
        return data

        
    def ReplaceURL(url: str, replace_to :str ='', show_replacede_values = False) -> str | list[str]:
        """
            Retorna somente a url sem ['www.','.com', ';br' ...]
            ex : https://youtube.com -> youtube 
        """

        replacede_values :list[str, str] =  ['.com', '.co', '.br', 'http://', 'https:', 'www.']
        def _get()-> list[str, str]: return replacede_values

        if (show_replacede_values):
            return _get()
        
        url = url.lower()
        for i in replacede_values:
            url = url.replace(i, replace_to)

        url = url.replace('.', '_').replace(' ', '_')

        return url
    
    
    def ShowImage(path :str )-> None:
        img = Image.open(path)
        img.show()


    def ListarDisponiveis()-> None:
        dir

class Decorator:
    
    def exibeNomeFuncao(func):
        def warpper():
            print(f'Funcao: <{func.__name__}>')
        return warpper   


    def tFunction(func):
        def warpper():
            try:
                func()
                print(f'Funcao: <{func.__name__}>: passed')
            except Exception as e:
                print(f'Funcao: <{func.__name__}>: faild')

        return warpper
        
class Logs:
    def log_to_file(message:str ,filename: str = 'logExecution.txt') -> None: 
        with open('logExecution.txt', 'a+') as file:
            file.write(message)

class Teste :

    @Decorator.tFunction
    def tFuntionsistar():
        functions.Listar([''])

    @Decorator.tFunction
    def tfunctionsReplaceURL():
        functions.ReplaceURL('www.google.com')

    def run():
        functions.LimparConsole()
        Teste.tFuntionsistar()
        Teste.tfunctionsReplaceURL()


if __name__ == '__main__':
    # Teste.run()
    functions.LimparConsole()
    Validar.SimNao(loop=True)