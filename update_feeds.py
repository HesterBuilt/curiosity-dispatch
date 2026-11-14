import json, datetime, urllib.parse, urllib.request, xml.etree.ElementTree as ET, email.utils, re, html, pathlib
ROOT=pathlib.Path(__file__).parent
QUERIES={
'Close to Home':'Gainesville Hall County Oakwood Flowery Branch Braselton Dahlonega Georgia local news',
'Local & Peculiar':'Gainesville Hall County North Georgia quirky unusual wildlife discoveries folklore local news',
'The Future Is Weird':'robotics artificial intelligence inventions emerging technology discoveries',
'The Human Mind':'neuroscience psychology memory consciousness research discoveries',
'Medical Frontiers':'medical research clinical breakthroughs genetics new treatment study',
'Science & the Unexplained':'archaeology astronomy ocean science unusual discovery',
'Dark & Fascinating':'forensic science cold case historical mystery investigation',
'Hidden History':'historic discovery forgotten history southern United States',
'Wild World':'wildlife botany animal behavior rare species discovery',
'Beautifully Bizarre':'oddities unusual collections eccentric discovery',
'Forgotten & Found':'rediscovered lost artifacts historic sites treasure archaeology',
'Wait, That’s Real?':'strange scientific discovery bizarre animals nature',
'The Rabbit Hole':'longread history science mystery investigation',
'Good News, For Once':'wildlife rescue conservation breakthrough positive news',
'Forgotten Georgia':'Georgia historic ruins mills ghost towns preservation',
'The Long Way Home':'Georgia scenic byway mountain roads historic highway',
'Beautifully Haunted':'Georgia historic cemetery haunted history folklore',
'The Detour Files':'Georgia roadside attraction historic museum antiques garden'
}
def run():
  allitems=[]; seen=set(); now=datetime.datetime.now(datetime.timezone.utc)
  for category,q in QUERIES.items():
    url='https://news.google.com/rss/search?q='+urllib.parse.quote(q+' when:14d')+'&hl=en-US&gl=US&ceid=US:en'
    try:
      req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 CuriosityDispatch/1.0'})
      with urllib.request.urlopen(req,timeout=18) as r: xml=r.read()
      root=ET.fromstring(xml)
      for item in root.findall('./channel/item')[:10]:
        title=html.unescape((item.findtext('title') or '').strip()); link=(item.findtext('link') or '').strip()
        key=re.sub(r'\W+','',title.lower())[:100]
        if not title or not link or key in seen: continue
        try: dt=email.utils.parsedate_to_datetime(item.findtext('pubDate')).astimezone(datetime.timezone.utc)
        except Exception: dt=now
        if (now-dt).days>30:continue
        seen.add(key)
        entry={'title':title,'url':link,'category':category,'source':item.findtext('source') or 'Publisher','date':dt.isoformat()}
        # Use publisher-supplied RSS images only when present; never invent a story photo.
        media_ns='{http://search.yahoo.com/mrss/}'
        image=None
        for node in (item.find(media_ns+'thumbnail'),item.find(media_ns+'content'),item.find('enclosure')):
          if node is not None:
            candidate=node.get('url','').strip()
            media_type=node.get('type','')
            if candidate.startswith('https://') and (node.tag!='enclosure' or media_type.startswith('image/')):
              image=candidate
              break
        if image:
          entry['image']=image
        allitems.append(entry)
    except Exception as e: print('Skipped',category,repr(e))
  allitems.sort(key=lambda x:x['date'],reverse=True)
  (ROOT/'news.json').write_text(json.dumps({'updated':now.isoformat(),'stories':allitems},ensure_ascii=False,indent=2),encoding='utf-8')
  print('Saved',len(allitems),'articles')
if __name__=='__main__':run()
