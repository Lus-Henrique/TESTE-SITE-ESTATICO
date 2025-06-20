from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
import datetime

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")
EXCEL_FILE1 = os.path.join(BASE_DIR, "Puxar Dados da Loggi", "Base.Rua.Juntos", "Base_Rua_Juntos.xlsx")
EXCEL_FILE2 = os.path.join(BASE_DIR, "Puxar Dados da Loggi", "BD_Loggi", "BDR.geral.loggi.xlsx")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

STATUS_PERMITIDOS = ["Em base", "Retirado", "Ausente", "Endereço errado", "Recusado"]

@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    prazo: str = Query(None),
    base2: str = Query(None, alias="base2")
):
    # --- Primeira tabela ---
    df1 = pd.read_excel(EXCEL_FILE1)
    df1 = df1.where(pd.notnull(df1), None)
    df1.columns = [col.strip() for col in df1.columns]
    df1 = df1[df1["Status"].isin(STATUS_PERMITIDOS)]
    df1["Prazo_str"] = pd.to_datetime(df1["Prazo"], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
    prazos_disponiveis = sorted(df1["Prazo_str"].dropna().unique())

    # Remove ".Rua" do final dos nomes das bases
    bases_raw = sorted(df1["base"].dropna().unique())
    bases = [base.replace(".Rua", "") for base in bases_raw]

    # Filtro de data único para as duas tabelas
    if prazo:
        df1 = df1[df1["Prazo_str"] == prazo]

    tabela = {}
    for base in bases:
        linha = {}
        for status in STATUS_PERMITIDOS:
            count = df1[(df1["base"].str.replace(".Rua", "") == base) & (df1["Status"] == status)]["ID do pacote"].count()
            linha[status] = count
        tabela[base] = linha
    total_geral = {}
    for status in STATUS_PERMITIDOS:
        total_geral[status] = sum(tabela[base][status] for base in bases)
    total_geral_geral = sum(sum(tabela[base][status] for status in STATUS_PERMITIDOS) for base in bases)
    bases_ordenadas = sorted(
        bases,
        key=lambda base: tabela[base]["Retirado"],
        reverse=True
    )

    # --- Segunda tabela ---
    df2 = pd.read_excel(EXCEL_FILE2)
    df2 = df2.where(pd.notnull(df2), None)
    df2.columns = [col.strip() for col in df2.columns]
    df2["Prazo_str"] = pd.to_datetime(df2["Prazo"], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
    prazos2_disponiveis = sorted(df2["Prazo_str"].dropna().unique())

    # Remove ".Rua" do final dos nomes das bases2
    bases2_raw = sorted(df2["base"].dropna().unique())
    bases2 = [base.replace(".Rua", "") for base in bases2_raw]

    # Filtro de data único para as duas tabelas
    if prazo:
        df2 = df2[df2["Prazo_str"] == prazo]
    if base2:
        df2 = df2[df2["base"].str.replace(".Rua", "") == base2]

    entregadores = sorted(df2["Entregador"].dropna().unique())
    status_titulos = ["Retirado", "Ocorrencia"]
    tabela2 = {}
    for entregador in entregadores:
        linha = {}
        linha["Retirado"] = df2[(df2["Entregador"] == entregador) & (df2["Status do pacote"] == "Retirado")]["Id do pacote"].count()
        linha["Ocorrencia"] = df2[(df2["Entregador"] == entregador) & (df2["Status do pacote"] != "Retirado")]["Id do pacote"].count()
        tabela2[entregador] = linha

    # Ordena entregadores pelo total (maior para menor)
    entregadores_ordenados = sorted(
        entregadores,
        key=lambda e: tabela2[e]["Retirado"] + tabela2[e]["Ocorrencia"],
        reverse=True
    )

    total_geral2 = {titulo: sum(tabela2[entregador][titulo] for entregador in entregadores) for titulo in status_titulos}
    total_geral_geral2 = sum(total_geral2.values())

    # Data/hora da última atualização do arquivo principal
    ultima_atualizacao = datetime.datetime.fromtimestamp(os.path.getmtime(EXCEL_FILE1)).strftime('%d/%m/%Y %H:%M:%S')

    return templates.TemplateResponse("index.html", {
        "request": request,
        # Primeira tabela
        "tabela": tabela,
        "bases": bases_ordenadas,
        "status_permitidos": STATUS_PERMITIDOS,
        "prazos": prazos_disponiveis,
        "prazo_selecionado": prazo,
        "total_geral": total_geral,
        "total_geral_geral": total_geral_geral,
        # Segunda tabela
        "tabela2": tabela2,
        "entregadores": entregadores_ordenados,
        "status_titulos": status_titulos,
        "prazos2": prazos2_disponiveis,
        "bases2": bases2,
        "base2_selecionada": base2,
        "total_geral2": total_geral2,
        "total_geral_geral2": total_geral_geral2,
        # Atualização
        "ultima_atualizacao": ultima_atualizacao
    })