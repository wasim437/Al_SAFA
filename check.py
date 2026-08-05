import fitz, glob, os, re, pathlib, collections
files = sorted(glob.glob('UPLOAD_THESE_12_FILES/*.pdf'))
issues=[]; repo=0; mail=0; ext=0; sizes=collections.Counter()
for f in files:
    n = int(os.path.basename(f)[:2]); d = fitz.open(f)
    txt_all = []
    for i, pg in enumerate(d):
        sizes[f'{round(pg.rect.width/2.83459)}x{round(pg.rect.height/2.83459)}mm'] += 1
        t = pg.get_text() or ''; txt_all.append(t)
        for m in set(re.findall(r'UPLOAD SLOT (\d\d) OF 12', t)):
            if int(m) != n: issues.append(f'slot label: {os.path.basename(f)} p{i+1} says {m}')
        for l in pg.get_links():
            u = l.get('uri','')
            if not u: continue
            if u.startswith('mailto:'): mail += 1
            elif '/blob/main/' in u:
                repo += 1
                rel = u.split('/blob/main/',1)[1]
                if not pathlib.Path(rel).exists(): issues.append(f'dead link: {os.path.basename(f)} p{i+1} -> {rel}')
            elif u.startswith('http'): ext += 1
            else: issues.append(f'bad URI: {os.path.basename(f)} p{i+1} -> {u!r}')
    joined = ' '.join(txt_all)
    for need in ('VISIT THE LIVE PROJECT PORTAL','VERIFY THIS DOCUMENT', 'WHAT WE DID, AND HOW TO CHECK IT','EVIDENCE THE PIPELINE RAN'):
        if need not in joined: issues.append(f'{os.path.basename(f)} missing: {need}')
    if not d.get_toc(): issues.append(f'{os.path.basename(f)} has no bookmarks')
    if (d.metadata or {}).get('title') is None: issues.append(f'{os.path.basename(f)} no title')
    mb = os.path.getsize(f)/1e6
    if mb > 95: issues.append(f'{os.path.basename(f)} {mb:.0f} MB over the 100 MB form limit')
    d.close()
print(f'12 PDFs - {repo} repository links - {mail} mailto - {ext} external')
print('page sizes:', dict(sizes))
print(f'\n{len(issues)} issue(s)')
for i in issues[:20]: print(' X', i)
