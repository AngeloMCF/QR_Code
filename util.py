import os

class Validar:

    def SimNao(char:str ='',  message :str ='Digite [S/N]: ', loop :bool = False) -> dict[bool, str]:
        '''
        :params
        :loop:True/False, ativar loop de validacao
        '''
        data :dict = {
            'Validation' : False,
            'char' : char
        }

        if (not char):
            char = input(message)
        
        data['char'] = char.strip()[0].lower() if char else ''
        # data['Validation']  =  True if(data['char'] in['s', 'n', 'y']) else False
        # data['Validation']  =  True if(data['char'] in['s', 'n', 'y']) else False
        if(data['char'] in['s', 'n', 'y']):
            if(data['char'] in['s','y']):
                data['Validation']  =  True 
            else: data['Validation']  =  False 
            
            return data

        if (loop and not data['Validation']) :
            while not data['Validation']:
                print(f'Valor invalido: "{char}"')
                char = input(message)
                data['char'] = char.strip()[0].lower() if char else ''
                if(data['char'] in['s', 'n', 'y']):
                    if(data['char'] in['s','y']):
                        data['Validation']  =  True 
                    else: data['Validation']  =  False 
                    
                    break

        return data

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
        
        # def TesteSimNao():
        #     Validar.Teste.Message(usedfunction=Validar.SimNao) if(Validar.SimNao('s')['Validation']and Validar.SimNao('n')['Validation']) else Validar.Teste.Message(usedfunction=Validar.SimNao, status=False)

        # def TesteNumeroInteiro():
        #     Validar.Teste.Message(Validar.SimNao) if(
        #         Validar.NumeroInteiro(1)['Validation']
        #         and Validar.NumeroInteiro(2)['Validation'] 
        #         and Validar.NumeroInteiro(-1)['Validation']
        #         and not Validar.NumeroInteiro('-1.001')['Validation']
        #     ) else Validar.Teste.Message(usedfunction= Validar.SimNao, status=False) 

class functions:

    def LimparConsole() -> None: os.system('cls')

    def Listar(lista :list) -> str:
        message :str = ''

        for i in lista:
            message += '\n' + i

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

if __name__ == '__main__':
    functions.LimparConsole()
    fn  = functions

    # print(fn.ReplaceURL('youube.com', show_replacede_values=True))
    a = fn.ReplaceURL('youube.com')
    print(a)
    # file = functions.RenomearArquivoFinal(fileName= 'teste',fileExtension ='.png')
    # print(file)
    # Validar.Teste.Message(usedfunction=Validar.SimNao)
    # Validar.Teste.TesteSimNao()
    # Validar.Teste.TesteNumeroInteiro()
    # print(Validar.SimNao(loop = True))
    # Validar.NumeroInteiro(loop = True)
    print('End...')
