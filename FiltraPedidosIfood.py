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

def substituir_posicao(log):
    # Substitui 'Posição :{"id' por 'Posição :BuscaDetalhesPedidoRetorno {"id' em todo o log
    log_modificado = re.sub(r'Posição :\{"id', 'Posição :BuscaDetalhesPedidoRetorno {"id', log)
    return log_modificado

def extrair_json_do_log(log):
    # Procurar por padrões JSON nos logs
    matches = re.findall(r'Posição :BuscaDetalhesPedidoRetorno (.*?)(?=\n-{50,})', log, re.DOTALL)
    json_data = []
    for match in matches:
        # Tenta carregar o conteúdo como JSON
        try:
            parsed_json = json.loads(match.strip())
            json_data.append(parsed_json)
        except json.JSONDecodeError:
            # Ignora caso o conteúdo não seja JSON válido
            continue
    return matches

def exclui_arquivos_existente(logs_folder):
    # Excluir arquivos existentes no logs_folder
    for arquivo_existente in os.listdir(logs_folder):
        caminho_arquivo = os.path.join(logs_folder, arquivo_existente)
        if os.path.isfile(caminho_arquivo):
            os.remove(caminho_arquivo)

def salvar_jsons_na_pasta(logs_folder, jsons):
    # Excluir arquivos existentes no logs_folder
    exclui_arquivos_existente(logs_folder)

    # Lista para armazenar números de pedidos já salvos
    numeros_salvos = []

    # Salvar cada JSON individualmente
    for idx, pedido_json in enumerate(jsons, 1):
        # Carregar o JSON
        try:
            pedido_obj = json.loads(pedido_json)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            continue

        # Use o número do pedido como nome do arquivo
        numero_pedido = pedido_obj['displayId'].replace("#", "")
        # Verificar se o número do pedido já foi salvo
        if pedido_obj['displayId'] not in numeros_salvos:
            numeros_salvos.append(numero_pedido)
            # Criar nome do arquivo
            filename = os.path.join(logs_folder, f"{numero_pedido}_{idx}.json")
            # Salvar o JSON do pedido no arquivo
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(pedido_obj, file, indent=2, ensure_ascii=False)
                print(f"JSON do pedido {numero_pedido} salvo em: {filename}")
        else:
            print(f"Número do pedido {numero_pedido} já salvo. Ignorando duplicata.")

if __name__ == "__main__":
    # Subpastas
    pastas = [r'C:\integradorDeliveryDev\ePadoca\logsOriginais', r'C:\integradorDeliveryDev\ePadoca\logsFinais']

    # Verifique se as pastas foram criadas e exiba a mensagem correspondente
    if all(os.path.exists(endereco_pasta) for endereco_pasta in pastas):
        print("Certifique-se que os rastros de logs estao localizados em 'C:/integradorDeliveryDev/logsOriginais' antes de executar o script.")
    else: # cria as pastas
        for endereco_pasta in pastas:
            criar_pasta_se_nao_existe(endereco_pasta)
        print("Coloque os rastros de log dentro da pasta 'C:/integradorDeliveryDev/logsOriginais' e reinicie o script.")
        sys.exit()

    # Solicitar o nome do arquivo de log
    nome_arquivo_log = input("Digite o nome do arquivo com os rastro de log (com a extensão do arquivo): ")

    if nome_arquivo_log == "":
        print("Nome do arquivo não pode ser vazio.")
        sys.exit()

    # Usar os caminhos fornecidos
    caminho_log_original = r'C:\integradorDeliveryDev\logsOriginais'
    caminho_salvar_log = r'C:\integradorDeliveryDev\logsFinais'

    # Ler o arquivo de log original
    caminho_log_original_completo = os.path.join(caminho_log_original, nome_arquivo_log)

    # Verificar se o arquivo existe
    if not verificar_se_arquivo_existe(caminho_log_original_completo):
        sys.exit()

    with open(caminho_log_original_completo, 'r', encoding='utf-8') as file:
        log_content = file.read()

    # Substituir a posição
    log_content = substituir_posicao(log_content)

    # Extrair os JSONs dos logs
    jsons = extrair_json_do_log(log_content)

    # Salvar os JSONs na pasta desejada
    salvar_jsons_na_pasta(caminho_salvar_log, jsons)
