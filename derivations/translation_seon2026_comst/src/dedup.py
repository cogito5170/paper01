import re,sys
parts=[f"part_{c}.tex" for c in "ABCDE"]
skip={"inference","reasoning"}
pat=re.compile(r'\(([A-Za-z][A-Za-z0-9\-]*(?:, [A-Za-z][A-Za-z0-9\- /]+)?|[a-z][A-Za-z\- ]+)\)')
seen=set(); apply=len(sys.argv)>1
for f in parts:
    s=open(f).read(); out=[]; last=0; n=0
    for m in pat.finditer(s):
        c=m.group(1); 
        if ', ' in c: ab,full=c.split(', ',1); keys=[ab.lower(),full.lower()]
        elif c[0].isupper() and (c.isupper() or re.fullmatch(r'[A-Z][A-Za-z0-9\-]*',c) and sum(ch.isupper() for ch in c)>=2): ab,full=c,None; keys=[c.lower()]
        else: ab,full=None,c; keys=[c.lower()]
        if any(k in skip for k in keys) or re.fullmatch(r'[ivx]+|[a-z]',c): continue
        # skip in math or citation-ish
        line=s[s.rfind('\n',0,m.start())+1:s.find('\n',m.end())]
        if line.lstrip().startswith('%'): continue
        dup=any(k in seen for k in keys)
        seen.update(keys)
        if not dup or f=='part_A.tex': continue
        if ab and full: rep=f"({ab})"
        elif ab: continue   # abbreviation-only repeat: keep
        else: rep=""
        print(f"{f}: {m.group(0)!r} -> {rep!r}   …{s[max(0,m.start()-15):m.start()]!r}")
        out.append(s[last:m.start()]+rep); last=m.end(); n+=1
    out.append(s[last:])
    if apply: open(f,'w').write(''.join(out))
