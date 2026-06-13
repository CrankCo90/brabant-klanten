#!/usr/bin/env python3
"""Brabant Digital control-server — draait op de VPS (alleen 127.0.0.1), achter Caddy /api + token.
Voert ALLEEN vooraf bepaalde acties uit. De vrije Claude-opdracht draait via Claude Code (acceptEdits + guard-hook)."""
import json, os, subprocess, csv, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
ROOT="/root/klanten"; DATA="/root/outreach-data"
TOKEN=open(os.path.join(DATA,".control-token")).read().strip()
SENTLOG=os.path.join(DATA,"sent-log.csv"); AUTO=os.path.join(DATA,".autopilot_on")
REPLIES=os.path.join(DATA,"replies.json")

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
            "autopilot":os.path.exists(AUTO),
            "replies":json.load(open(REPLIES)) if os.path.exists(REPLIES) else {}}

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
        if not self._auth(): return self._s(401,{"error":"unauthorized"})
        n=int(self.headers.get("Content-Length") or 0)
        try: body=json.loads(self.rfile.read(n) or b"{}")
        except: body={}
        if self.path=="/api/send-outreach":
            cap=int(body.get("cap",20)); sel=body.get("prospects") or []
            env={"OUTREACH_DATA":DATA,"OUTREACH_CAP":str(cap)}
            if sel: env["OUTREACH_ONLY"]="|".join(sel)
            rc,out=run("git pull -q; python3 _workflow/outreach/send-outreach.py",env)
            return self._s(200,{"ok":rc==0,"log":out})
        if self.path=="/api/deploy":
            rc,out=run("bash _workflow/vps-autodeploy.sh"); return self._s(200,{"ok":rc==0,"log":out})
        if self.path=="/api/claude":
            pr=(body.get("prompt") or "")[:2000]
            if not pr: return self._s(400,{"error":"lege opdracht"})
            rc,out=run("git pull -q; claude -p %s --permission-mode acceptEdits"%json.dumps(pr),timeout=1200)
            return self._s(200,{"ok":rc==0,"log":out})
        if self.path=="/api/autopilot":
            if body.get("on"): open(AUTO,"w").write("on")
            elif os.path.exists(AUTO): os.remove(AUTO)
            return self._s(200,{"autopilot":os.path.exists(AUTO)})
        self._s(404,{"error":"not found"})

if __name__=="__main__":
    ThreadingHTTPServer(("127.0.0.1",8787),H).serve_forever()
