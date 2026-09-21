from pathlib import Path
import subprocess,sys,json,os
ROOT=Path.cwd(); repo=ROOT/'probe-repo'; repo.mkdir(exist_ok=True)
helper=ROOT/'skills/production-engineering-loop/scripts/review_evidence.py'
def git(*args): return subprocess.run(['git','-C',str(repo),*args],capture_output=True,text=True,check=True).stdout
git('init','-q');git('config','user.email','probe@example.invalid');git('config','user.name','Probe')
(repo/'contract.md').write_text('Protect evidence provenance.\n');(repo/'app.py').write_text('print(1)\n');git('add','.');git('commit','-qm','base')
marker=ROOT/'fsmonitor-ran'; hook=ROOT/'fsmonitor.sh'; hook.write_text('#!/bin/sh\nprintf invoked >> '+str(marker)+'\nprintf "token\\0"\n');hook.chmod(0o700)
git('config','core.fsmonitor',str(hook))
packet=ROOT/'probe-packet.json';packet.unlink(missing_ok=True)
p=subprocess.run([sys.executable,str(helper),'capture','--repo',str(repo),'--contract','contract.md','--output',str(packet)],capture_output=True,text=True)
print('F1 capture:',p.returncode,p.stdout.strip(),p.stderr.strip());print('F1 repository configured executable ran:',marker.exists(),marker.read_text() if marker.exists() else None)
git('config','--unset','core.fsmonitor')
