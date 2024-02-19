# LogTools
Esse repositorio armazena ferramentas uteis para extrair informações especificas salvas nos logs.

# FiltraPedidosEpadoca

Este script em Python foi projetado para extrair pedidos de logs de uma aplicação ePadoca e salvá-los individualmente como arquivos JSON. Os pedidos são filtrados com base em padrões específicos encontrados nos logs.

## Requisitos

- Python 3.12 ou superior

## Instruções de Uso

1. **Clone o Repositório:**
    ```bash
    git clone https://github.com/seu-usuario/FiltraPedidosEpadoca.git
    ```

2. **Navegue até o Diretório do Projeto:**
    ```bash
    cd FiltraPedidosEpadoca
    ```

3. **Instale as Dependências (caso necessário):**
    ```bash
    pip install -r requirements.txt
    ```

4. **Execute o Script:**
    ```bash
    python FiltraPedidosEpadoca.py
    ```

5. **Insira o Nome do Arquivo de Log:**
    - O script solicitará o nome do arquivo de log. Certifique-se de que os rastros de logs estejam localizados em 'C:/integradorDeliveryDev/ePadoca/logsOriginais'. Insira o nome do arquivo com a extensão quando solicitado.

6. **Processamento dos Logs:**
    - O script processará os logs, extrairá os pedidos e salvará cada pedido individualmente como um arquivo JSON no diretório 'C:/integradorDeliveryDev/ePadoca/logsFinais'.

**Observação:** Certifique-se de que o Python 3.12 ou superior está instalado em sua máquina antes de executar o script. Você pode baixar o Python em [python.org](https://www.python.org/downloads/).

---

**Importante:** Personalize este README com informações adicionais sobre o funcionamento específico do seu script, detalhes sobre os dados esperados nos logs ou quaisquer outros detalhes relevantes para os usuários do seu script.
