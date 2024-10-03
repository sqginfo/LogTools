import re
import json
import os
import sys
from datetime import datetime

def verificar_se_arquivo_existe(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo {caminho_arquivo} não encontrado. Verifique o caminho e tente novamente.")
        return False
    return True

def criar_pasta_se_nao_existe(caminho_pasta):
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
        print(f"Pasta {caminho_pasta} criada.")

def extrair_json_do_log(log):
    # Procurar por padrões JSON nos logs
    matches = re.findall(r'Posição :Retorno Busca Pedido Completo: (.*?)(?=\n-{50,})', log, re.DOTALL)
    return matches

def salvar_jsons_na_pasta(logs_folder, jsons):
    # Excluir arquivos existentes no logs_folder
    for arquivo_existente in os.listdir(logs_folder):
        caminho_arquivo = os.path.join(logs_folder, arquivo_existente)
        if os.path.isfile(caminho_arquivo):
            os.remove(caminho_arquivo)

    # Lista para armazenar números de pedidos já salvos
    numeros_salvos = []

    # Salvar cada JSON individualmente
    for idx, json_data in enumerate(jsons, 1):
        # Carregar o JSON
        try:
            json_obj = json.loads(json_data)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            continue

        # Iterar sobre cada pedido no JSON
        for i, pedido in enumerate(json_obj):
            # Use o número do pedido como nome do arquivo
            numero_pedido = pedido['numero'].replace("#", "")

            # Verificar se o número do pedido já foi salvo
            if numero_pedido not in numeros_salvos:
                numeros_salvos.append(numero_pedido)

                # Criar nome do arquivo
                filename = os.path.join(logs_folder, f"{numero_pedido}_{idx}_{i}.json")

                # Salvar o JSON do pedido no arquivo
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(pedido, file, indent=2, ensure_ascii=False)
                    print(f"JSON do pedido {numero_pedido} salvo em: {filename}")
            else:
                print(f"Número do pedido {numero_pedido} já salvo. Ignorando duplicata.")

if __name__ == "__main__":
    # Subpastas
    pastas = [r'C:\integradorDeliveryDev\ePadoca\logsOriginais', r'C:\integradorDeliveryDev\ePadoca\logsFinais']

    # Verifique se as pastas foram criadas e exiba a mensagem correspondente
    if all(os.path.exists(endereco_pasta) for endereco_pasta in pastas):
        print("Certifique-se que os rastros de logs estao localizados em 'C:/integradorDeliveryDev/ePadoca/logsOriginais' antes de executar o script.")
    else: # cria as pastas
        for endereco_pasta in pastas:
            criar_pasta_se_nao_existe(endereco_pasta)
        print("Coloque os rastros de log dentro da pasta 'C:/integradorDeliveryDev/ePadoca/logsOriginais' e reinicie o script.")
        sys.exit()

    # Solicitar o nome do arquivo de log
    nome_arquivo_log = input("Digite o nome do arquivo com os rastro de log (com a extensão do arquivo): ")

    if nome_arquivo_log == "":
        print("Nome do arquivo não pode ser vazio.")
        sys.exit()

    # Usar os caminhos fornecidos
    caminho_log_original = r'C:\integradorDeliveryDev\ePadoca\logsOriginais'
    caminho_salvar_log = r'C:\integradorDeliveryDev\ePadoca\logsFinais'

    # Ler o arquivo de log original
    caminho_log_original_completo = os.path.join(caminho_log_original, nome_arquivo_log)

    # Verificar se o arquivo existe
    if not verificar_se_arquivo_existe(caminho_log_original_completo):
        sys.exit()

    with open(caminho_log_original_completo, 'r', encoding='utf-8') as file:
        log_content = file.read()

    # Extrair os JSONs dos logs
    jsons = extrair_json_do_log(log_content)

    # Salvar os JSONs na pasta desejada
    salvar_jsons_na_pasta(caminho_salvar_log, jsons)
