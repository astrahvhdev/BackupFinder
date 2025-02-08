# BackupFinder

## Descrição
O **BackupFinder** é uma ferramenta Python que busca arquivos arquivados na Wayback Machine. Ele permite filtrar arquivos por extensões específicas, verificar snapshots arquivados e salvar as URLs encontradas de maneira organizada. Ideal para recuperar backups de sites e arquivos que podem não estar mais acessíveis.

**Desenvolvido por @astrahvhdev (Telegram).**

## Funcionalidades
- Busca automática de URLs arquivadas na Wayback Machine.
- Filtragem de URLs por extensões específicas (ex.: `.zip`, `.pdf`).
- Verificação de snapshots arquivados.
- Salvamento de URLs filtradas em arquivos organizados.
- Possibilidade de trabalhar com domínios individuais ou múltiplos.

## Requisitos
- **Python 3.x**
- Bibliotecas necessárias:
  - `requests`
  - `colorama`
  - `termcolor`

Caso não tenha essas bibliotecas, o script irá instalá-las automaticamente.

## Como Usar
### 1. Executando o Script
1. Baixe o script `BackupFinder.py`.
2. Execute o script no terminal:
   ```bash
   python BackupFinder.py
   ```
3. Escolha entre:
   - **Domínio único**: Digite o nome do domínio (ex.: `example.com`).
   - **Múltiplos domínios**: Informe o caminho do arquivo contendo a lista de domínios.
4. Escolha entre usar extensões personalizadas ou carregar do arquivo `extensoes.txt`.
5. O script buscará as URLs arquivadas, filtrará por extensões e verificará backups disponíveis.

### 2. Exemplo de Entrada
```
Informe o domínio alvo (exemplo.com): example.com
Usar extensões personalizadas ou carregar do arquivo? (custom/load): load
```

### 3. Exemplo de Saída
```
Buscando URLs no Wayback Machine para example.com...
Foram encontradas 1200 URLs no arquivo.
Extensão .pdf encontrada: 45 URLs
Backup encontrado: https://web.archive.org/web/20220101000000/https://example.com/sample.pdf
```

## Estrutura dos Arquivos Gerados
Os resultados serão salvos dentro da pasta `conteudo/`, separando as URLs encontradas por extensão:
```
conteudo/
 ├── example.com/
 │   ├── example_com_pdf_urls_filtradas.txt
 │   ├── example_com_zip_urls_filtradas.txt
```

## Casos de Uso
- Encontrar backups de sites e arquivos deletados.
- Verificar versões antigas de documentos e recursos digitais.
- Monitoramento de arquivos que foram removidos de sites ativos.

## Licença
Este projeto é de uso livre e pode ser modificado conforme necessário.

