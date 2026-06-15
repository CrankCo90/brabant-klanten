#!/usr/bin/env bash
[ -f /root/outreach-data/autopilot.json ] || exit 0
/usr/bin/python3 - <<'PY'
import json,datetime,subprocess,sys
ap=json.load(open("/root/outreach-data/autopilot.json"))
if not ap.get("on"): sys.exit(0)
now=datetime.datetime.now(); hm=now.strftime("%H:%M")
if not (ap.get("start","09:00")<=hm<=ap.get("stop","17:00")): sys.exit(0)
if ap.get("dagen","ma-vr")=="ma-vr" and now.weekday()>=5: sys.exit(0)
subprocess.run(["bash","-lc","cd /root/klanten && git pull -q; OUTREACH_DATA=/root/outreach-data OUTREACH_ALL=1 OUTREACH_BATCH=1 OUTREACH_CAP=%s /usr/bin/python3 _workflow/outreach/send-outreach.py >> /root/outreach-data/send.log 2>&1"%str(ap.get("cap",50))])
PY
