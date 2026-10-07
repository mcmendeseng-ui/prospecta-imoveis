"""Public territorial APIs and public commercial listings. No corporate data."""
import json, gzip, re, datetime, urllib.request, urllib.parse, concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
CATALOG='https://www.alextongo.com/aluguel-estudante/comerciais'
INCOME='https://servicodados.ibge.gov.br/api/v3/agregados/10295/periodos/2022/variaveis/13431?localidades=N6[3205002]&classificacao=2[6794]|86[95251]|58[95253]'
CLIMATE='https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=T2M,PRECTOTCORR,WS10M&community=RE&longitude=-40.3&latitude=-20.12&format=JSON'

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Prospecta public listing monitor/1.0'})
    with urllib.request.urlopen(req,timeout=25) as r:
        b=r.read(10_000_001)
    if len(b)>10_000_000:raise ValueError('Resposta excedeu o limite')
    return gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b

def br_number(s):return float(s.replace('.','').replace(',','.'))

def parse_listing(url, content):
    soup=BeautifulSoup(content,'html.parser')
    h=soup.find('h1')
    if not h:return None
    title=h.get_text(' ',strip=True)
    # Only the current listing, before the recommendations section.
    text=soup.get_text(' ',strip=True).split('Imóveis Semelhantes')[0]
    ref=re.search(r'ref-(\d+)',url)
    area=re.search(r'([\d.,]+)\s*m[²2]\s*de área privativa',text,re.I)
    price=re.search(r'Aluguel Estudante:\s*R\$\s*([\d.,]+)',text,re.I)
    if not (ref and area and price):return None
    square=br_number(area.group(1));amount=br_number(price.group(1))
    if square<=0 or amount<=0:return None
    # Bound focus for the first monitored city; do not infer location from a generic title.
    if 'serra-' not in url:return None
    district_match=re.search(r'galpao-deposito-serra-(.+?)-aluguel',url)
    district=district_match.group(1).replace('-',' ').title() if district_match else 'A confirmar'
    image=soup.find('meta',attrs={'property':'og:image'})
    return {'id':ref.group(1),'title':title.split('(referência')[0].strip(),'city':'Serra','state':'ES','district':district,'type':'Locação','area':square,'price':amount,'url':url,'source':'Imobiliária Alex Tongo','sourceDate':datetime.date.today().isoformat(),'image':image.get('content') if image else None,'isDemo':False,'environment':'Não avaliado','status':'Anúncio localizado; disponibilidade a confirmar'}

def run():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    territory=json.loads((ROOT/'data/territory.json').read_text())
    statuses={}
    for name,url in [('income',INCOME),('climate',CLIMATE)]:
        try:
            payload=json.loads(get(url))
            if name=='income':territory['income']=float(payload[0]['resultados'][0]['series'][0]['serie']['2022'])
            else:territory['climate']=payload
            statuses[name]={'status':'ok','checkedAt':now,'url':url}
        except Exception as e:statuses[name]={'status':'failed','checkedAt':now,'error':str(e)}
    territory['sources']=statuses;territory['checkedAt']=now
    (ROOT/'data/territory.json').write_text(json.dumps(territory,ensure_ascii=False,indent=2)+'\n')
    file=ROOT/'data/listings.json';old=json.loads(file.read_text());index={(str(p['id']),p.get('source','')):p for p in old['listings']};events=old.get('events',[])
    try:
        catalog=BeautifulSoup(get(CATALOG),'html.parser')
        urls=sorted(set(urllib.parse.urljoin(CATALOG,a['href']) for a in catalog.find_all('a',href=True) if '/imovel/galpao-deposito-serra-' in a['href'] and '-aluguel-ref-' in a['href']))[:24]
        if not urls:raise ValueError('Catálogo não apresentou links reconhecidos; último conjunto mantido')
        # Small bounded batch, no evasive retries on blocks or rate limits.
        def fetch_listing(u):
            try:return parse_listing(u,get(u))
            except Exception as e:print('Imóvel não atualizado:',u,str(e));return None
        checked=0
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            for p in pool.map(fetch_listing,urls):
                if not p:continue
                checked+=1;key=(p['id'],p['source']);previous=index.get(key)
                if previous is None:events.append({'id':f"{p['source']}:{p['id']}:{now}",'title':p['title'],'kind':'new','message':'Novo anúncio público localizado','at':now})
                elif previous.get('price')!=p['price']:events.append({'id':f"{p['source']}:{p['id']}:{now}",'title':p['title'],'kind':'price_change','message':f"Preço alterado de {previous.get('price')} para {p['price']}",'at':now})
                if previous:p={**previous,**p}
                p['income']=territory.get('income');p['incomePeriod']='2022';p['marketEvidence']='IBGE Censo 2022, tabela 10295, renda per capita municipal. Preço e área são anunciados.'
                index[key]=p
        if not checked:raise ValueError('Formato dos anúncios não reconhecido; coleta não validada')
        old.update(updatedAt=now,status='public_connected',listings=list(index.values()),events=events[-500:],checkedListings=checked)
    except Exception as e:
        old.update(status='collection_failed',lastAttempt=now,collectionError=str(e))
        print('Coleta imobiliária falhou; anúncios anteriores preservados:',e)
    file.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
    print('Fontes territoriais:',statuses,'Imóveis:',len(old['listings']))
if __name__=='__main__':run()
