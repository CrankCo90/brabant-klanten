#!/usr/bin/env python3
"""Brabant Digital control-server — draait op de VPS (alleen 127.0.0.1), achter Caddy /api + token.
Voert ALLEEN vooraf bepaalde acties uit. De vrije Claude-opdracht draait via Claude Code (acceptEdits + guard-hook)."""
import json, os, subprocess, csv, datetime, hashlib, re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
ROOT="/root/klanten"; DATA="/root/outreach-data"
TOKEN=open(os.path.join(DATA,".control-token")).read().strip()
PWHASH_EXPECTED="64696df0eff1c7ed0db5371356e155b4279d2a260223f8a774798b9ac0654abe"
SENTLOG=os.path.join(DATA,"sent-log.csv"); AUTO=os.path.join(DATA,".autopilot_on")
REPLIES=os.path.join(DATA,"replies.json")
APJSON=os.path.join(DATA,"autopilot.json")
def _ap():
    import json as _j
    return _j.load(open(APJSON)) if os.path.exists(APJSON) else {}

def run(cmd, extra_env=None, timeout=900):
    e=dict(os.environ); e["PATH"]="/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    if extra_env: e.update(extra_env)
    try:
        p=subprocess.run(["bash","-lc",cmd],capture_output=True,text=True,env=e,cwd=ROOT,timeout=timeout)
        return p.returncode,(p.stdout+p.stderr)
    except subprocess.TimeoutExpired:
        return 1,"(time-out)"

def sent_info():
    rows=[]
    if os.path.exists(SENTLOG):
        with open(SENTLOG,newline="",encoding="utf-8") as f:
            for r in csv.DictReader(f): rows.append(r)
    today=datetime.date.today().isoformat()
    pr=[]
    pf=os.path.join(ROOT,"_workflow/outreach/prospects.json")
    if os.path.exists(pf):
        for x in json.load(open(pf)):
            pr.append({"bedrijf":x.get("bedrijf"),"email":x.get("email",""),"status":x.get("status"),"demo_url":x.get("demo_url","")})
    return {"prospects":pr,
            "sent":[{"email":r["email"],"datum":r["datum"],"bedrijf":r.get("bedrijf","")} for r in rows],
            "total":len(rows),"today":sum(1 for r in rows if r["datum"].startswith(today)),
            "autopilot":bool(_ap().get("on")),"settings":_ap(),
            "replies":json.load(open(REPLIES)) if os.path.exists(REPLIES) else {}}

def _norm_phone(p):
    d=re.sub(r"\D","",str(p or ""))
    if d.startswith("0031"): d=d[4:]
    elif d.startswith("31"): d=d[2:]
    elif d.startswith("0"): d=d[1:]
    return d[-9:]

def _git_push():
    run("git add -A && git -c user.email=vps@brabantdigital.nl -c user.name=BD-VPS commit -q -m 'afwijzing -> afgewezen + demo offline'")
    tkf=os.path.join(DATA,".git-token")
    if os.path.exists(tkf):
        tk=open(tkf).read().strip()
        run("git push -q https://%s@github.com/CrankCo90/brabant-klanten.git HEAD:main"%tk)

def _process_reject(bedrijf, reason="", channel="bericht"):
    cf=os.path.join(ROOT,"dashboard/clients.json"); C=json.load(open(cf)); target=None
    for c in C:
        if c.get("bedrijf")==bedrijf: target=c; break
    if not target: return False,"Bedrijf niet gevonden: %s"%bedrijf
    if target.get("status")!="afgewezen":
        target["status"]="afgewezen"; json.dump(C,open(cf,"w"),ensure_ascii=False,indent=1)
    nd=os.path.join(ROOT,"_workflow/niet-deployen.txt"); nd_set=set()
    if os.path.exists(nd):
        for l in open(nd).read().splitlines():
            l=l.strip()
            if l and not l.startswith("#"): nd_set.add(l)
    m=re.search(r"https://([^.]+)\.demo", target.get("demo_url") or "")
    if m: nd_set.add(m.group(1))
    header=("# Klanten die NOOIT gepubliceerd mogen worden (1 map-slug per regel).\n"
            "# vps-autodeploy.sh slaat deze over en haalt een eventueel al-live exemplaar offline.\n"
            "# Regel weghalen = klant mag weer gedeployed worden. Regels met # worden genegeerd.\n")
    open(nd,"w").write(header+"\n".join(sorted(nd_set))+"\n")
    rp=os.path.join(DATA,"replies.json"); R=json.load(open(rp)) if os.path.exists(rp) else {}
    R[bedrijf]={"status":"nee","datum":datetime.date.today().isoformat(),"laatste":(reason or ("Afwijzing via "+channel))[:160]}
    json.dump(R,open(rp,"w"),ensure_ascii=False,indent=1)
    _git_push()
    return True,"%s op 'afgewezen' gezet en demo offline gehaald."%bedrijf

def _classify(text):
    low=(text or "").lower()
    if re.search(r"\b(nee|geen interesse|afmeld|uitschrijf|niet ge.nteresseerd|stop|geen behoefte|niet nodig|graag niet|liever niet|haal me weg)\b",low): return "nee"
    if re.search(r"\b(ja|graag|interesse|akkoord|doen|bestellen|afspraak|leuk|mooi|top)\b",low): return "ja"
    return "reactie"

class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def _auth(self): return self.headers.get("Authorization","")==("Bearer "+TOKEN)
    def _s(self,code,obj):
        b=json.dumps(obj).encode(); self.send_response(code)
        for k,v in [("Content-Type","application/json"),("Content-Length",str(len(b))),
                    ("Access-Control-Allow-Origin","*"),("Access-Control-Allow-Headers","authorization,content-type"),
                    ("Access-Control-Allow-Methods","GET,POST,OPTIONS")]: self.send_header(k,v)
        self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self): self._s(204,{})
    def do_GET(self):
        if not self._auth(): return self._s(401,{"error":"unauthorized"})
        if self.path=="/api/status": return self._s(200,sent_info())
        self._s(404,{"error":"not found"})
    def do_POST(self):
        n=int(self.headers.get("Content-Length") or 0)
        try: body=json.loads(self.rfile.read(n) or b"{}")
        except: body={}
        if self.path=="/api/login":
            pw=body.get("pw") or ""
            if hashlib.sha256(pw.encode()).hexdigest()==PWHASH_EXPECTED: return self._s(200,{"token":TOKEN})
            return self._s(401,{"error":"unauthorized"})
        if not self._auth(): return self._s(401,{"error":"unauthorized"})
        if self.path=="/api/send-outreach":
            cap=int(body.get("cap",20)); sel=body.get("prospects") or body.get("only") or []
            env={"OUTREACH_DATA":DATA,"OUTREACH_CAP":str(cap)}
            if sel: env["OUTREACH_ONLY"]="|".join(sel)
            _intro=(body.get("intro") or "").strip()
            if _intro: env["OUTREACH_INTRO"]=_intro
            rc,out=run("git pull -q; python3 _workflow/outreach/send-outreach.py",env)
            return self._s(200,{"ok":rc==0,"log":out})
        if self.path=="/api/deploy":
            rc,out=run("bash _workflow/vps-autodeploy.sh"); return self._s(200,{"ok":rc==0,"log":out})
        if self.path=="/api/claude":
            pr=(body.get("prompt") or "")[:2000]
            if not pr: return self._s(400,{"error":"lege opdracht"})
            rc,out=run("git pull -q; claude -p %s --permission-mode acceptEdits"%json.dumps(pr),timeout=1200)
            return self._s(200,{"ok":rc==0,"log":out})
        if self.path=="/api/new-client":
            rc,out=run("python3 _workflow/new-client.py %s"%json.dumps(json.dumps(body)),{"OUTREACH_DATA":DATA},timeout=900)
            return self._s(200,{"ok":rc==0,"log":out})
        if self.path=="/api/test-mail":
            to=(body.get("to") or "").strip(); pros=(body.get("prospect") or "").strip()
            if not (to and pros): return self._s(400,{"error":"prospect en to vereist"})
            rc,out=run("python3 _workflow/outreach/send-one.py %s %s"%(json.dumps(pros),json.dumps(to)),{"OUTREACH_DATA":DATA})
            return self._s(200,{"ok":rc==0,"log":out})
        if self.path=="/api/autopilot":
            ap=_ap(); ap["on"]=bool(body.get("on")); json.dump(ap,open(APJSON,"w"))
            return self._s(200,{"autopilot":ap["on"]})
        if self.path=="/api/autopilot-settings":
            ap=_ap()
            for k in ("on","cap","start","stop","dagen","interval"):
                if body.get(k) is not None: ap[k]=body.get(k)
            json.dump(ap,open(APJSON,"w"))
            return self._s(200,{"ok":True,"log":"Autopilot-instellingen opgeslagen.","settings":ap})
        if self.path=="/api/set-status":
            b=(body.get("bedrijf") or "").strip(); st=(body.get("status") or "").strip()
            if not (b and st): return self._s(400,{"error":"bedrijf+status vereist"})
            cf=os.path.join(ROOT,"dashboard/clients.json"); C=json.load(open(cf))
            for c in C:
                if c.get("bedrijf")==b: c["status"]=st
            json.dump(C,open(cf,"w"),ensure_ascii=False,indent=1)
            run("git add -A && git -c user.email=vps@brabantdigital.nl -c user.name=BD-VPS commit -q -m 'status: %s'"%b)
            if os.path.exists("/root/outreach-data/.git-token"):
                tk=open("/root/outreach-data/.git-token").read().strip()
                run("git push -q https://%s@github.com/CrankCo90/brabant-klanten.git HEAD:main"%tk)
            return self._s(200,{"ok":True,"log":"Status van %s op '%s' gezet."%(b,st)})
        if self.path=="/api/reject":
            bedrijf=(body.get("bedrijf") or "").strip()
            if not bedrijf: return self._s(400,{"error":"bedrijf vereist"})
            ok,msg=_process_reject(bedrijf,(body.get("reason") or ""),(body.get("channel") or "handmatig"))
            return self._s(200 if ok else 404,{"ok":ok,"log":msg})
        if self.path=="/api/incoming":
            text=(body.get("text") or "").strip(); sender=(body.get("sender") or "").strip()
            channel=(body.get("channel") or "bericht").strip()
            if not text: return self._s(400,{"error":"lege tekst"})
            cls=_classify(text)
            C=json.load(open(os.path.join(ROOT,"dashboard/clients.json"))); bedrijf=None
            if sender:
                sn=_norm_phone(sender)
                for c in C:
                    if sn and _norm_phone(c.get("telefoon"))==sn: bedrijf=c.get("bedrijf"); break
            if not bedrijf:
                return self._s(200,{"ok":False,"cls":cls,"matched":False,"log":"Geen klant bij nummer %s. Tekst herkend als '%s'."%(sender or "(leeg)",cls)})
            if cls=="nee":
                ok,msg=_process_reject(bedrijf,text[:160],channel)
                return self._s(200,{"ok":ok,"cls":cls,"matched":True,"bedrijf":bedrijf,"log":msg})
            rp=os.path.join(DATA,"replies.json"); R=json.load(open(rp)) if os.path.exists(rp) else {}
            R[bedrijf]={"status":cls,"datum":datetime.date.today().isoformat(),"laatste":text[:160]}
            json.dump(R,open(rp,"w"),ensure_ascii=False,indent=1)
            return self._s(200,{"ok":True,"cls":cls,"matched":True,"bedrijf":bedrijf,"log":"%s: reactie '%s' gelogd (geen afwijzing)."%(bedrijf,cls)})
        if self.path=="/api/campaign":
            dg=(body.get("doelgroep") or "all"); tpl=(body.get("sjabloon") or "uitnodiging"); intro=(body.get("intro") or ""); test=bool(body.get("test"))
            tmap={"uitnodiging":"_workflow/outreach/template-nl.txt","herinnering":"_workflow/outreach/template-herinnering.txt","kort":"_workflow/outreach/template-kort.txt"}
            tplp=os.path.join(ROOT,tmap.get(tpl,tmap["uitnodiging"]))
            only=""
            if dg.startswith("niche:") or dg.startswith("regio:"):
                key,val=dg.split(":",1); names=[]
                cl=json.load(open(os.path.join(ROOT,"dashboard/clients.json")))
                for c in cl:
                    if key=="niche" and c.get("niche")==val: names.append(c["bedrijf"])
                    if key=="regio" and (c.get("regio")==val or (c.get("plaats","").split("\u00b7")[0].strip()==val)): names.append(c["bedrijf"])
                only="|".join(names)
            env={"OUTREACH_DATA":DATA,"OUTREACH_TEMPLATE":tplp,"OUTREACH_INTRO":intro}
            if only: env["OUTREACH_ONLY"]=only
            if test:
                P=json.load(open(os.path.join(ROOT,"_workflow/outreach/prospects.json")))
                cand=[x for x in P if x.get("status")=="klaar" and (not only or x.get("bedrijf") in only.split("|"))]
                if not cand: return self._s(200,{"ok":False,"log":"Geen klaar-prospect met e-mail in deze doelgroep om te testen."})
                rc,out=run("python3 _workflow/outreach/send-one.py %s %s"%(json.dumps(cand[0]["bedrijf"]),json.dumps("aanbod@brabantdigital.nl")),env)
                return self._s(200,{"ok":rc==0,"log":out})
            env["OUTREACH_CAP"]=str(int(body.get("cap",20)))
            rc,out=run("git pull -q; python3 _workflow/outreach/send-outreach.py",env)
            return self._s(200,{"ok":rc==0,"log":out})
        if self.path=="/api/add-prospects":
            pros=body.get("prospects") or []
            json.dump(pros,open("/tmp/ingest_in.json","w"))
            rc,out=run("git pull -q; python3 _workflow/ingest-prospects.py /tmp/ingest_in.json")
            run("git add -A && git -c user.email=vps@brabantdigital.nl -c user.name=BD-VPS commit -q -m 'n8n ingest prospects'")
            if os.path.exists("/root/outreach-data/.git-token"):
                tk=open("/root/outreach-data/.git-token").read().strip()
                run("git push -q https://%s@github.com/CrankCo90/brabant-klanten.git HEAD:main"%tk)
            return self._s(200,{"ok":rc==0,"log":out[-1500:]})
        self._s(404,{"error":"not found"})

if __name__=="__main__":
    ThreadingHTTPServer(("127.0.0.1",8787),H).serve_forever()
