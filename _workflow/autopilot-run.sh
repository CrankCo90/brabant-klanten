#!/usr/bin/env bash
[ -f /root/outreach-data/autopilot.json ] || exit 0
/usr/bin/python3 - <<'PY'
import json,datetime,subprocess,sys
ap=json.load(open("/root/outreach-data/autopilot.json"))
if not ap.get("on"): sys.exit(0)
now=datetime.datetime.now(); hm=now.strftime("%H:%M")
if not (ap.get("start","09:00")<=hm<=ap.get("stop","17:00")): sys.exit(0)
_dg=str(ap.get("dagen","Ma-Vr")).lower().replace("\u2013","-")
_wd=now.weekday()
if "alle" not in _dg:
    if "za" in _dg or "ma-za" in _dg:
        if _wd>=6: sys.exit(0)      # Ma-Za: zondag overslaan
    else:
        if _wd>=5: sys.exit(0)      # Ma-Vr: weekend overslaan
subprocess.run(["bash","-lc","cd /root/klanten && git pull -q; OUTREACH_DATA=/root/outreach-data OUTREACH_ALL=1 OUTREACH_BATCH=1 OUTREACH_CAP=%s /usr/bin/python3 _workflow/outreach/send-outreach.py >> /root/outreach-data/send.log 2>&1"%str(ap.get("cap",50))])
PY
