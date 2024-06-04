import subprocess

def test_main(args):
    try:
        # Executa o arquivo main.py com os argumentos fornecidos
        process = subprocess.Popen(['python', 'main.py'] + args, stderr=subprocess.PIPE)
        _, stderr = process.communicate()

        # Verifica se houve erros no stderr
        if stderr:
            print(f"Erro ao executar main.py com os argumentos {args}:")
            print(stderr.decode())
        # else:
        #     print(f"main.py executado com sucesso com os argumentos {args}")
    except Exception as e:
        print(f"Erro ao executar main.py com os argumentos {args}:")
        print(str(e))

# Teste com diferentes argumentos
test_main(['teste.lua'])


