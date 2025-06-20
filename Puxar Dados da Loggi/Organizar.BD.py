import pandas as pd
import os
import re
import time

pasta = r"D:\Projeto inicial\Puxar Dados da Loggi\BD_Loggi"

bases = []
ruas = []
arquivos_para_apagar = []

def tratar_data(valor):
    """Converte para datetime para o Excel reconhecer como data."""
    if pd.isnull(valor):
        return pd.NaT
    valor = str(valor).strip()
    try:
        data = pd.to_datetime(valor, dayfirst=True, errors='coerce')
        return data
    except Exception:
        return pd.NaT

def aguardar_arquivo_pronto(caminho, tentativas=10, intervalo=1):
    """Aguarda até que o arquivo pare de crescer (download finalizado)."""
    tamanho_anterior = -1
    for _ in range(tentativas):
        if not os.path.exists(caminho):
            time.sleep(intervalo)
            continue
        tamanho_atual = os.path.getsize(caminho)
        if tamanho_atual == tamanho_anterior and tamanho_atual > 1024:
            return True
        tamanho_anterior = tamanho_atual
        time.sleep(intervalo)
    return False

for arquivo in os.listdir(pasta):
    if arquivo.endswith(".csv"):
        caminho_csv = os.path.join(pasta, arquivo)
        # Aguarda o arquivo estar pronto
        if not aguardar_arquivo_pronto(caminho_csv):
            print(f"Arquivo {arquivo} não está pronto para leitura. Pulando.")
            continue
        sigla = arquivo.replace(".csv", "")
        try:
            df = pd.read_csv(caminho_csv, sep=None, engine='python')
            # Garante que existam 7 colunas antes de adicionar a coluna base
            while df.shape[1] < 7:
                df[f'col_{df.shape[1]+1}'] = ""
            # Trata a coluna de data pelo nome, não pelo índice
            for nome_col_data in ["Prazo", "Data", "Data de entrega"]:
                if nome_col_data in df.columns:
                    df[nome_col_data] = df[nome_col_data].apply(tratar_data)
            # Formata a coluna 5 (índice 4) para todos os arquivos (mantido por compatibilidade)
            if df.shape[1] > 4:
                df.iloc[:, 4] = df.iloc[:, 4].apply(tratar_data)
            # Adiciona a coluna base ao final, preenchida com a sigla
            df["base"] = sigla
            # Garante que a coluna base seja a última
            cols = list(df.columns)
            if cols[-1] != "base":
                cols = [c for c in cols if c != "base"] + ["base"]
                df = df[cols]
            # Salva o CSV sobrescrevendo o original, com separador vírgula
            df.to_csv(caminho_csv, sep=",", index=False, encoding="utf-8")
            print(f"Arquivo CSV tratado e salvo: {arquivo}")

            # Adiciona o DataFrame à lista correspondente
            if arquivo.endswith(".Base.csv"):
                bases.append(df)
                arquivos_para_apagar.append(caminho_csv)
            elif arquivo.endswith(".Rua.csv"):
                ruas.append(df)
                arquivos_para_apagar.append(caminho_csv)

        except Exception as e:
            print(f"Erro ao converter {arquivo}: {e}")

time.sleep(5)  # Aguarda um segundo para evitar problemas de concorrência

# Junta e salva os arquivos finais
if bases:
    arquivo_bases = os.path.join(pasta, "BDB.geral.loggi.xlsx")
    df_bases_concat = pd.concat(bases, ignore_index=True)
    # Zera a hora da coluna 'Prazo'
    if 'Prazo' in df_bases_concat.columns:
        df_bases_concat['Prazo'] = pd.to_datetime(df_bases_concat['Prazo'], dayfirst=True, errors='coerce').dt.normalize()
    df_bases_concat.to_excel(arquivo_bases, index=False)
    print(f"Arquivo criado: {arquivo_bases}")

if ruas:
    arquivo_ruas = os.path.join(pasta, "BDR.geral.loggi.xlsx")
    df_ruas_concat = pd.concat(ruas, ignore_index=True)
    # Zera a hora da coluna 'Prazo'
    if 'Prazo' in df_ruas_concat.columns:
        df_ruas_concat['Prazo'] = pd.to_datetime(df_ruas_concat['Prazo'], dayfirst=True, errors='coerce').dt.normalize()
    df_ruas_concat.to_excel(arquivo_ruas, index=False)
    print(f"Arquivo criado: {arquivo_ruas}")

# Apaga os arquivos CSV usados
for caminho in arquivos_para_apagar:
    try:
        os.remove(caminho)
        print(f"Arquivo removido: {caminho}")
    except Exception as e:
        print(f"Erro ao remover {caminho}: {e}")

# Junta bases e ruas em uma planilha final
pasta_saida = r"D:\Projeto inicial\Puxar Dados da Loggi\Base.Rua.Juntos"
os.makedirs(pasta_saida, exist_ok=True)
arquivo_base = os.path.join(pasta, "BDB.geral.loggi.xlsx")
arquivo_rua = os.path.join(pasta, "BDR.geral.loggi.xlsx")
arquivo_saida = os.path.join(pasta_saida, "Base_Rua_Juntos.xlsx")

df_base = pd.read_excel(arquivo_base)
df_rua = pd.read_excel(arquivo_rua)

# Renomeia colunas para padronizar antes de juntar
colunas_renomear = {
    "Status do pacote": "Status",
    "id do pacote": "ID do pacote",
    "Id do pacote": "ID do pacote"
}
df_base.rename(columns=colunas_renomear, inplace=True)
df_rua.rename(columns=colunas_renomear, inplace=True)

# Altere os status conforme necessário
status_map = {
    "Sem tentativa": "Em base",
    "Aguardando reenvio": "Em base",
    "Aguardando tratativa":"Tratativa",
    "Arquivo integrado":"nulo",
    "Conferido":"nulo",
    "No centro de re-estoque":"nulo",
    "Pacote não encontrado":"nulo",
    "Pacote não retirado":"nulo",
    "Retornado para o cliente":"nulo",
    "Destinatário ausente": "Ausente",
    "Recusado pelo destinatário": "Recusado"
    # Adicione outros mapeamentos conforme necessário
}

if "Status" in df_base.columns:
    df_base["Status"] = df_base["Status"].replace(status_map)
if "Status" in df_rua.columns:
    df_rua["Status"] = df_rua["Status"].replace(status_map)

# Mantém apenas as colunas desejadas (ajuste para o nome correto da coluna de data)
colunas_desejadas = ["Prazo", "base", "Status", "ID do pacote"]
df_base = df_base[[col for col in colunas_desejadas if col in df_base.columns]]
df_rua = df_rua[[col for col in colunas_desejadas if col in df_rua.columns]]

# Zera a hora da coluna 'Prazo' em ambos
if 'Prazo' in df_base.columns:
    df_base['Prazo'] = pd.to_datetime(df_base['Prazo'], dayfirst=True, errors='coerce').dt.normalize()
if 'Prazo' in df_rua.columns:
    df_rua['Prazo'] = pd.to_datetime(df_rua['Prazo'], dayfirst=True, errors='coerce').dt.normalize()

# Junta os dois DataFrames
df_junto = pd.concat([df_base, df_rua], ignore_index=True)

# Remove '.Rua' e '.Base' do final dos valores da coluna 'base'
if 'base' in df_junto.columns:
    df_junto['base'] = df_junto['base'].str.replace(r'\.Rua$|\.Base$', '', regex=True)

# Zera a hora da coluna 'Prazo' no DataFrame final também (por segurança)
if 'Prazo' in df_junto.columns:
    df_junto['Prazo'] = pd.to_datetime(df_junto['Prazo'], dayfirst=True, errors='coerce').dt.normalize()

# Salva o resultado na nova pasta
df_junto.to_excel(arquivo_saida, index=False)
print(f"Arquivo criado: {arquivo_saida}")

print("Processamento concluído.")