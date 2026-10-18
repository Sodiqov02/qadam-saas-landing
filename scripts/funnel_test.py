"""Only synthetic contacts, temporary databases and a mocked Telegram transport."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server
import tempfile
import threading
import json
import urllib.request
import urllib.error
import sqlite3
import uuid
import os
from unittest.mock import patch

def main():
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'leads.sqlite3';app=server.make_server(0,path)
        threading.Thread(target=app.serve_forever,daemon=True).start()
        base=f'http://127.0.0.1:{app.server_port}'
        def request(route,data=None,headers=None):
            req=urllib.request.Request(base+route,data=json.dumps(data).encode() if data is not None else None,headers=headers or {})
            try:
                with urllib.request.urlopen(req) as res:return res.status,res.read()
            except urllib.error.HTTPError as res:return res.code,res.read()
        try:
            status,body=request('/api/session');assert status==200
            token=json.loads(body)['csrf'];headers={'Origin':base,'X-CSRF-Token':token,'Content-Type':'application/json'}
            lead={'venue':'Synthetic Test Cafe','contact':'@test_cafe','locale':'ru','consent':True,'website':'','request_id':str(uuid.uuid4())}
            assert request('/api/leads',lead)[0]==403
            assert request('/api/leads',lead,{**headers,'Origin':'https://evil.invalid'})[0]==403
            assert request('/api/leads',{**lead,'contact':'bad'},headers)[0]==400
            assert request('/api/leads',{**lead,'consent':False},headers)[0]==400
            assert request('/api/leads',{**lead,'website':'spam'},headers)[0]==400
            assert request('/api/leads',{**lead,'venue':'x'*5000},headers)[0]==413
            assert request('/api/leads',lead,headers)[0]==201
            assert request('/api/leads',lead,headers)[0]==200
            assert request('/api/leads',{**lead,'venue':'Changed'},headers)[0]==409
            for _ in range(4): assert request('/api/leads',{**lead,'request_id':str(uuid.uuid4())},headers)[0]==201
            assert request('/api/leads',{**lead,'request_id':str(uuid.uuid4())},headers)[0]==429
            for route in ['/server.py','/.git/config','/docs/implementation.md','/assets/../server.py','/api/leads','/scripts/build.py']:
                assert request(route)[0]==404,route
            with server.connect(path) as db: assert db.execute('SELECT COUNT(*) FROM leads').fetchone()[0]==5
            class Response:
                status=200
                def __enter__(self):return self
                def __exit__(self,*args):pass
                def read(self,*args):return b'{"ok":true,"result":{"message_id":123}}'
            class Transport:
                def open(self,req,timeout):
                    assert req.full_url.startswith('https://api.telegram.org/bot')
                    assert json.loads(req.data)['chat_id']=='123'
                    return Response()
            class BadResponse(Response):
                def read(self,*args):return b'{"ok":false}'
            class BadTransport:
                def open(self,*args,**kwargs):return BadResponse()
            with patch.dict(os.environ,{'QADAMUP_BOT_TOKEN':'123:synthetic_test_token','QADAMUP_ADMIN_CHAT_ID':'123'}):
                assert server.notify(path,BadTransport())==1
                with server.connect(path) as db: assert db.execute('SELECT COUNT(*) FROM leads WHERE notified=1').fetchone()[0]==0
                assert server.notify(path,Transport())==0
            with server.connect(path) as db: assert db.execute('SELECT COUNT(*) FROM leads WHERE notified=1').fetchone()[0]==5
            with patch('server.sqlite3.connect',side_effect=sqlite3.OperationalError('synthetic failure')):
                assert request('/api/leads',{**lead,'request_id':str(uuid.uuid4())},headers)[0]==503
        finally: app.shutdown();app.server_close()
    print('FUNNEL_SERVER_OK')
if __name__=='__main__':main()
