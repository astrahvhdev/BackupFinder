import os
import requests
import time
import sys
from colorama import init, Fore
from termcolor import colored
from threading import Thread
from itertools import cycle

# Instalar dependências automaticamente
try:
    import colorama
    import termcolor
except ImportError:
    print("Instalando dependências necessárias...")
    os.system(f"{sys.executable} -m pip install colorama termcolor requests")
    import colorama
    import termcolor

# Inicializar colorama para compatibilidade com cores no terminal
init()

# Animação de carregamento
def animacao_carregamento(mensagem="Processando..."):
    animacao = cycle(["|", "/", "-", "\\"])
    while not parar_loader:
        print(f"\r{mensagem} {next(animacao)}", end="")
        time.sleep(0.1)
    print("\r" + " " * len(mensagem) + "\r", end="")  # Limpa a linha

# Arte ASCII para apresentação
def exibir_logo():
    logo = r'''
    __       .          .___      .      
    [__) _. _.;_/. .._   [__ *._  _| _ ._.
    [__)(_](_.| \(_|[_)  |   |[ )(_](/,[  
                    |                     
    '''
    print(logo)
    print(colored("BackupFinder - Desenvolvido por @astrahvhdev (Telegram)", "cyan"))

exibir_logo()

# Carregar extensões de arquivo de um arquivo externo
def carregar_extensoes(arquivo='extensoes.txt'):
    try:
        with open(arquivo, 'r') as f:
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    except FileNotFoundError:
        print(colored(f"{arquivo} não encontrado. Continuando sem extensões.", "red"))
        return []

# Carregar domínios de um arquivo
def carregar_dominios(arquivo):
    try:
        with open(arquivo, 'r') as f:
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    except FileNotFoundError:
        print(colored(f"{arquivo} não encontrado. Encerrando.", "red"))
        exit()

# Buscar URLs no The Wayback Machine API
def buscar_urls(alvo, extensoes):
    print(f"\nBuscando URLs no Wayback Machine para {alvo}...")
    url_wayback = f'https://web.archive.org/cdx/search/cdx?url=*.{alvo}/*&output=txt&fl=original&collapse=urlkey'
    
    global parar_loader
    parar_loader = False
    thread_loader = Thread(target=animacao_carregamento, args=("Buscando URLs...",))
    thread_loader.start()

    try:
        resposta = requests.get(url_wayback)
        resposta.raise_for_status()
        lista_urls = resposta.text.splitlines()
        print(colored(f"\nForam encontradas {len(lista_urls)} URLs no arquivo.", "green"))
    except Exception as e:
        print(colored(f"\nErro ao buscar URLs: {e}", "red"))
        return []
    finally:
        parar_loader = True
        thread_loader.join()

    print("\nFiltrando URLs pelas extensões especificadas...")
    stats_extensoes = {ext: [] for ext in extensoes}
    
    for url in lista_urls:
        for ext in extensoes:
            if url.lower().endswith(ext.lower()):
                stats_extensoes[ext].append(url)

    for ext, urls in stats_extensoes.items():
        if urls:
            print(f"Extensão {ext} encontrada: {len(urls)} URLs")
    
    return stats_extensoes

# Verificar se há um backup disponível no Wayback Machine
def verificar_snapshot(url):
    url_wayback = f'https://archive.org/wayback/available?url={url}'
    try:
        resposta = requests.get(url_wayback)
        resposta.raise_for_status()
        dados = resposta.json()
        if "archived_snapshots" in dados and "closest" in dados["archived_snapshots"]:
            url_snapshot = dados["archived_snapshots"]["closest"].get("url")
            if url_snapshot:
                print(f"[+] Backup encontrado: {colored(url_snapshot, 'green')}")
        else:
            print(f"[-] Nenhum backup encontrado para {url}.")
    except Exception as e:
        print(f"[?] Erro ao verificar backup para {url}: {e}")

# Salvar URLs filtradas
def salvar_urls(alvo, stats_extensoes, sufixo="_urls_filtradas.txt"):
    pasta = f"conteudo/{alvo}"
    os.makedirs(pasta, exist_ok=True)
    todas_urls = []
    for ext, urls in stats_extensoes.items():
        if urls:
            caminho_arquivo = os.path.join(pasta, f"{alvo}_{ext.strip('.')}" + sufixo)
            with open(caminho_arquivo, 'w') as arquivo:
                arquivo.write("\n".join(urls))
            todas_urls.extend(urls)
            print(f"URLs filtradas para {ext} salvas em: {colored(caminho_arquivo, 'green')}")
    return todas_urls

# Processar um domínio específico
def processar_dominio(alvo, extensoes):
    stats_extensoes = buscar_urls(alvo, extensoes)
    todas_urls = salvar_urls(alvo, stats_extensoes)
    for url in todas_urls:
        verificar_snapshot(url)

# Execução principal do script
if __name__ == "__main__":
    print(colored('    Criado por @astrahvhdev (Telegram)\n', 'green'))

    modo = input("Escolha o modo (1: Domínio único, 2: Múltiplos domínios): ").strip()
    if modo == "1":
        alvo = input("\nInforme o domínio alvo (exemplo.com): ").strip()
        if not alvo:
            print(colored("Domínio alvo é obrigatório. Encerrando.", "red"))
            exit()
        dominios = [alvo]
    elif modo == "2":
        arquivo_dominios = input("\nInforme o caminho do arquivo com os domínios: ").strip()
        dominios = carregar_dominios(arquivo_dominios)
        print(f"Foram carregados {len(dominios)} domínios do arquivo {colored(arquivo_dominios, 'green')}.")
    else:
        print(colored("Escolha inválida. Encerrando.", "red"))
        exit()

    extensoes = carregar_extensoes()
    for alvo in dominios:
        print(colored(f"\nProcessando domínio: {alvo}", "blue"))
        processar_dominio(alvo, extensoes)

    print(colored("\nProcesso concluído para todos os domínios.", "green"))
