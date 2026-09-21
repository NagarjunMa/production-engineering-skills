from pathlib import Path
import subprocess,sys,json,hashlib
ROOT=Path.cwd(); fixture=ROOT/'round2'; fixture.mkdir(exist_ok=True); repo=fixture/'repo'; repo.mkdir(exist_ok=True)
helper=ROOT/'skills/production-engineering-loop/scripts/review_evidence.py'
def git(*args): return subprocess.run(['git','-C',str(repo),*args],capture_output=True,text=True,check=True).stdout
git('init','-q');git('config','user.email','probe@example.invalid');git('config','user.name','Probe')
(repo/'contract.md').write_text('Protect evidence provenance.\n');(repo/'app.py').write_text('print(1)\n');git('add','.');git('commit','-qm','base')
marker=fixture/'fsmonitor-ran'; hook=fixture/'fsmonitor.sh'; hook.write_text('#!/bin/sh\nprintf invoked >> '+str(marker)+'\nprintf "token\\0"\n');hook.chmod(0o700)
git('config','core.fsmonitor',str(hook))
packet=fixture/'packet.json';packet.unlink(missing_ok=True);marker.unlink(missing_ok=True)
args=[sys.executable,str(helper)]
def run(action,*extra):
 p=subprocess.run(args+[action,'--repo',str(repo)]+list(extra),capture_output=True,text=True)
 assert p.returncode==0,(action,p.returncode,p.stdout,p.stderr)
 assert not marker.exists(),action+' ran fsmonitor'
 print(action+': PASS; exit 0; configured hook never executed')
run('capture','--contract','contract.md','--output',str(packet))
run('check','--packet',str(packet))
p=json.loads(packet.read_text());report={'schema_version':1,'snapshot_id':p['snapshot_id'],'reviewer':{'identity':'probe','model':None,'implementer_model':None,'fresh_context':True,'kind':'fresh-context'},'verdict':'no_material_findings','coverage':['fsmonitor regression fixture'],'limitations':['Synthetic report tests parser path only'],'checks':[],'findings':[]}
reportpath=fixture/'report.json';reportpath.write_text(json.dumps(report))
run('validate','--packet',str(packet),'--report',str(reportpath))
