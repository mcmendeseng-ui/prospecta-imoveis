"""Municipal catalogue, official income and registered fleet; no private data."""
import json, io, re, unicodedata, datetime, urllib.request
from pathlib import Path
import openpyxl
ROOT=Path(__file__).resolve().parents[1]
CITIES='https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome'
INCOME='https://servicodados.ibge.gov.br/api/v3/agregados/10295/periodos/2022/variaveis/13431?localidades=N6[all]&classificacao=2[6794]|86[95251]|58[95253]'
FLEET_PAGE='https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-Senatran/frota-de-veiculos-2026'
def key(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.upper()) if not unicodedata.combining(c)).strip()
def get(url):
    with urllib.request.urlopen(url,timeout=45) as r:return r.read(20_000_000)
def build(cities,income,fleet_bytes,fleet_url):
    incomes={int(s['localidade']['id']):float(s['serie']['2022']) for s in income[0]['resultados'][0]['series'] if re.fullmatch(r'\d+(\.\d+)?',s['serie']['2022'])}
    ws=openpyxl.load_workbook(io.BytesIO(fleet_bytes),read_only=True,data_only=True).active
    rows=list(ws.values);header=next(r for r in rows if r[0]=='UF' and r[1]=='MUNICIPIO')
    fleet={}
    for r in rows:
        if not isinstance(r[2],(float,int)) or not r[0] or not r[1]:continue
        types={str(header[i]):int(r[i] or 0) for i in range(3,len(header))}
        fleet[(r[0],key(r[1]))]={'fleetTotal':int(r[2]),'fleet':sum(types.get(k,0) for k in ['AUTOMOVEL','CAMINHONETE','CAMIONETA','UTILITARIO'])}
    period=str(rows[0][0]).split(' - ')[-1]
    out=[]
    for c in cities:
        uf=c['regiao-imediata']['regiao-intermediaria']['UF']['sigla']
        out.append({'id':c['id'],'city':c['nome'],'state':uf,'income':incomes.get(c['id']),**fleet.get((uf,key(c['nome'])),{})})
    result={'updatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'incomePeriod':'2022','fleetPeriod':period,'incomeSource':INCOME,'fleetSource':fleet_url,'cities':out}
    (ROOT/'data/municipalities.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
    return result
def run():
    page=get(FLEET_PAGE).decode()
    url=re.search(r'href="([^"]*/Frota_por_municipio_e_tipo_[^"]+\.xlsx)"',page).group(1)
    return build(json.loads(get(CITIES)),json.loads(get(INCOME)),get(url),url)
if __name__=='__main__':run()
