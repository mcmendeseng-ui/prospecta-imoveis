"""Collect authorized JSON feeds; never scrape portals or infer missing data."""
import json, os, pathlib, datetime, urllib.request, urllib.parse
ROOT = pathlib.Path(__file__).resolve().parents[1]
FILE = ROOT / 'data/listings.json'
def run():
    urls = json.loads(os.environ.get('PROPERTY_FEEDS', '[]'))
    if not isinstance(urls,list): raise ValueError('PROPERTY_FEEDS deve ser uma lista JSON de URLs')
    if not urls:
        print('Sem fontes configuradas; nenhum monitoramento realizado.')
        return
    old = json.loads(FILE.read_text()) if FILE.exists() else {'listings':[], 'events':[]}
    index = {(str(p['id']),p.get('source','')):p for p in old['listings']}
    events = old.get('events', [])
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # Fail atomically: partial source errors do not publish a misleading refresh.
    for url in urls:
        if urllib.parse.urlparse(url).scheme != 'https': raise ValueError('A fonte precisa usar HTTPS')
        req = urllib.request.Request(url, headers={'User-Agent':'Prospecta/1.0'})
        with urllib.request.urlopen(req, timeout=45) as response:
            if urllib.parse.urlparse(response.url).scheme != 'https': raise ValueError('Redirecionamento inseguro')
            raw = response.read(10_000_001)
            if len(raw)>10_000_000: raise ValueError('Fonte excedeu limite de 10 MB')
            payload = json.loads(raw)
        listings = payload.get('listings') if isinstance(payload,dict) else payload
        if not isinstance(listings,list): raise ValueError('Fonte precisa conter uma lista de imóveis')
        for p in listings:
            if not isinstance(p,dict) or any(not p.get(k) for k in ['id','title','city','source']):
                raise ValueError('Imóvel sem id, title, city ou source')
            if p.get('type') not in ['Compra','Locação']: raise ValueError('type inválido')
            # Public dataset: this workflow is for public listing data only.
            allowed = ['id','title','city','state','district','type','area','price','referenceM2','comparables','fleet','income','health','environment','works','equipment','projects','releaseDays','buildDays','monthlyRevenue','contributionMargin','otherMonthlyCosts','contractMonths','status','source','sourceDate','url','healthEvidence','marketEvidence','isDemo']
            p={k:v for k,v in p.items() if k in allowed}
            key=(str(p['id']),p['source']); previous=index.get(key)
            if previous is None:
                events.append({'id':f"{p['source']}:{p['id']}:{now}",'kind':'new','title':p['title'],'at':now,'message':'Novo imóvel recebido','listingId':str(p['id'])})
            elif previous.get('price')!=p.get('price'):
                events.append({'id':f"{p['source']}:{p['id']}:{now}",'kind':'price_change','title':p['title'],'at':now,'message':f"Preço alterado de {previous.get('price')} para {p.get('price')}",'listingId':str(p['id'])})
            index[key]=p
    result={'updatedAt':now,'status':'connected','listings':list(index.values()),'events':events[-500:]}
    FILE.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f"{len(index)} imóveis; {len(events)} eventos. Arquivo atualizado.")
if __name__=='__main__':run()
