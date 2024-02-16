import re
import json
import os
from datetime import datetime

def extrair_json_do_log(log):
    # Procurar por padrões JSON nos logs
    matches = re.findall(r'Posição :BuscarPedidosNovosCompletos: (.*?)(?=\n-{50,})', log, re.DOTALL)
    return matches

def salvar_jsons_na_pasta(logs_folder, jsons, nome_arquivo):
    # Criar a pasta com o nome do arquivo
    pasta_arquivo = os.path.join(logs_folder, nome_arquivo)
    os.makedirs(pasta_arquivo, exist_ok=True)

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
                filename = os.path.join(pasta_arquivo, f"{numero_pedido}_{idx}_{i}.json")

                # Salvar o JSON do pedido no arquivo
                with open(filename, 'w') as file:
                    json.dump(pedido, file, indent=2)
                    print(f"JSON do pedido {numero_pedido} salvo em: {filename}")
            else:
                print(f"Número do pedido {numero_pedido} já salvo. Ignorando duplicata.")

if __name__ == "__main__":
    # Solicitar o nome do arquivo de log
    nome_arquivo_log = input("Digite o nome do arquivo de log (com extensão .log): ")

    # Usar os caminhos fornecidos
    caminho_log_original = r'C:\Users\Note-Dev04\Documents\SQG documentos\ePadoca\logsOriginais'
    caminho_salvar_log = r'C:\Users\Note-Dev04\Documents\SQG documentos\ePadoca\logsFinais'

    # Ler o arquivo de log original
    caminho_log_original_completo = os.path.join(caminho_log_original, nome_arquivo_log)

    with open(caminho_log_original_completo, 'r', encoding='utf-8') as file:
        log_content = file.read()

    # Extrair os JSONs dos logs
    jsons = extrair_json_do_log(log_content)

    # Salvar os JSONs na pasta desejada
    salvar_jsons_na_pasta(caminho_salvar_log, jsons, nome_arquivo_log)
