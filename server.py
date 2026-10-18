"""Loopback landing preview + isolated lead store. Never imports the product backend."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from contextlib import contextmanager
import argparse
import hashlib
import hmac
import json
import mimetypes
import os
import re
import secrets
import sqlite3
import subprocess
import sys
import time
import urllib.request
import urllib.error
from urllib.parse import urlsplit, unquote

ROOT=Path(__file__).resolve().parent
PUBLIC={'/':'index.html','/index.html':'index.html','/uz.html':'uz.html','/en.html':'en.html',
        '/styles.css':'styles.css','/funnel.css':'funnel.css','/main.js':'main.js','/funnel.js':'funnel.js',
        '/favicon.ico':'favicon.ico','/robots.txt':'robots.txt','/sitemap.xml':'sitemap.xml','/site.webmanifest':'site.webmanifest',
        '/apple-touch-icon.png':'apple-touch-icon.png','/android-chrome-192x192.png':'android-chrome-192x192.png','/android-chrome-512x512.png':'android-chrome-512x512.png'}

@contextmanager
def connect(path, **options):
    db=sqlite3.connect(path, **options)
    try:
        with db:
            yield db
    finally:
        db.close()

def initialize(path):
    path=Path(path).resolve()
    if path.is_relative_to(ROOT):
        raise ValueError('Lead database must be outside the public checkout')
    path.parent.mkdir(parents=True,exist_ok=True)
    with connect(path) as db:
        db.executescript('''CREATE TABLE IF NOT EXISTS leads (
          id INTEGER PRIMARY KEY, request_id TEXT UNIQUE NOT NULL,
          venue TEXT NOT NULL, contact TEXT NOT NULL, locale TEXT NOT NULL,
          created REAL NOT NULL, notified INTEGER NOT NULL DEFAULT 0);
          CREATE TABLE IF NOT EXISTS attempts (client TEXT NOT NULL, created REAL NOT NULL);''')
    return path

def make_server(port=4173, database=None):
    db_path=initialize(database or Path(os.environ.get('LOCALAPPDATA',str(Path.home()))) / 'QadamUp' / 'landing-preview' / 'leads.sqlite3')
    secret=secrets.token_bytes(32)
    class Handler(BaseHTTPRequestHandler):
        server_version='QadamUpPreview'
        def log_message(self,*args): pass  # No request bodies, URLs or credentials in logs.
        def setup(self):
            super().setup(); self.connection.settimeout(10)
        def headers_common(self):
            self.send_header('X-QadamUp-Preview','b2b-funnel-v1')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Referrer-Policy','no-referrer')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; media-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'none'")
            self.send_header('Cache-Control','no-store')
        def respond(self,status,data):
            body=json.dumps(data).encode();self.send_response(status);self.headers_common()
            self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        def trusted(self):
            expected=f'127.0.0.1:{self.server.server_port}'
            return self.headers.get('Host')==expected
        def token(self):
            issued=str(int(time.time()));nonce=secrets.token_hex(12);payload=issued+'.'+nonce
            return payload+'.'+hmac.new(secret,payload.encode(),hashlib.sha256).hexdigest()
        def csrf_valid(self):
            try:
                token=self.headers.get('X-CSRF-Token','');issued,nonce,signature=token.split('.')
                age=time.time()-int(issued)
                return 0<=age<=3600 and hmac.compare_digest(signature,hmac.new(secret,(issued+'.'+nonce).encode(),hashlib.sha256).hexdigest())
            except (ValueError,TypeError): return False
        def do_GET(self):
            if not self.trusted(): return self.respond(403,{'error':'origin'})
            path=unquote(urlsplit(self.path).path)
            if path=='/api/session': return self.respond(200,{'csrf':self.token()})
            filename=PUBLIC.get(path)
            if not filename and path.startswith('/assets/'):
                filename=path.lstrip('/')
            if not filename: return self.respond(404,{'error':'not_found'})
            target=(ROOT/filename).resolve()
            if not target.is_relative_to(ROOT) or (path.startswith('/assets/') and (not target.is_relative_to((ROOT/'assets').resolve()) or target.suffix.lower() not in {'.webp','.png','.jpg','.jpeg','.ico','.mp4','.vtt'})):
                return self.respond(404,{'error':'not_found'})
            try: body=target.read_bytes()
            except OSError: return self.respond(404,{'error':'not_found'})
            content_type=mimetypes.guess_type(target)[0] or 'application/octet-stream'
            if target.suffix in {'.html','.css','.js'}: content_type+='; charset=utf-8'
            self.send_response(200);self.headers_common();self.send_header('Content-Type',content_type);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        def do_POST(self):
            if self.path!='/api/leads': return self.respond(404,{'error':'not_found'})
            origin=f'http://127.0.0.1:{self.server.server_port}'
            if not self.trusted() or self.headers.get('Origin')!=origin or not self.csrf_valid(): return self.respond(403,{'error':'origin_or_csrf'})
            if self.headers.get_content_type()!='application/json': return self.respond(415,{'error':'content_type'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=4096: return self.respond(413,{'error':'size'})
                data=json.loads(self.rfile.read(length))
                if not isinstance(data,dict): raise ValueError()
                venue=data.get('venue');contact=data.get('contact');locale=data.get('locale');request_id=data.get('request_id')
                if not isinstance(venue,str) or not isinstance(contact,str): raise ValueError()
                venue=venue.strip();contact=contact.strip()
                valid_contact=bool(re.fullmatch(r'@[A-Za-z][A-Za-z0-9_]{4,31}',contact)) or (bool(re.fullmatch(r'[+0-9\s()\-]+',contact)) and 7<=len(re.sub(r'\D','',contact))<=15)
                if not (2<=len(venue)<=100 and len(contact)<=64 and valid_contact and locale in ('ru','uz','en') and data.get('consent') is True and not data.get('website') and isinstance(request_id,str) and re.fullmatch(r'[0-9a-f-]{36}',request_id)):
                    raise ValueError()
                if any(ord(ch)<32 or ord(ch)==127 for ch in venue+contact): raise ValueError()
            except (ValueError,TypeError,UnicodeDecodeError): return self.respond(400,{'error':'validation'})
            try:
                with connect(db_path,timeout=5) as db:
                    db.execute('BEGIN IMMEDIATE')
                    # A repeated request is safe, including retry after a lost response.
                    previous=db.execute('SELECT venue,contact,locale,notified FROM leads WHERE request_id=?',(request_id,)).fetchone()
                    if previous:
                        if previous[:3]!=(venue,contact,locale): return self.respond(409,{'error':'request_conflict'})
                        return self.respond(200,{'saved':True,'notification':'delivered' if previous[3] else 'queued'})
                    now=time.time();client=hmac.new(secret,self.client_address[0].encode(),hashlib.sha256).hexdigest()
                    db.execute('DELETE FROM attempts WHERE created < ?',(now-3600,))
                    count=db.execute('SELECT COUNT(*) FROM attempts WHERE client=? AND created>?',(client,now-600)).fetchone()[0]
                    if count>=5: return self.respond(429,{'error':'rate_limit'})
                    db.execute('INSERT INTO attempts VALUES (?,?)',(client,now))
                    db.execute('INSERT INTO leads (request_id,venue,contact,locale,created) VALUES (?,?,?,?,?)',(request_id,venue,contact,locale,now))
                return self.respond(201,{'saved':True,'notification':'queued'})
            except sqlite3.Error: return self.respond(503,{'error':'unavailable'})
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    server.db_path=db_path
    return server

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def notify(database, opener=None):
    """Explicit outbox drain. Never called by preview or tests with real credentials."""
    token=os.environ.get('QADAMUP_BOT_TOKEN','');chat=os.environ.get('QADAMUP_ADMIN_CHAT_ID','')
    if not re.fullmatch(r'[0-9]+:[A-Za-z0-9_-]+',token) or not re.fullmatch(r'-?[0-9]+',chat):
        print('NOTIFICATION_NOT_CONFIGURED');return 1
    opener=opener or urllib.request.build_opener(NoRedirect())
    try:
        with connect(initialize(database),timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            for ident,venue,contact,locale in db.execute('SELECT id,venue,contact,locale FROM leads WHERE notified=0 ORDER BY id LIMIT 50').fetchall():
                body=json.dumps({'chat_id':chat,'text':f'QadamUp demo lead #{ident}\n{venue}\n{contact}\n{locale}'}).encode()
                req=urllib.request.Request('https://api.telegram.org/bot'+token+'/sendMessage',data=body,headers={'Content-Type':'application/json'},method='POST')
                with opener.open(req,timeout=10) as response:
                    result=json.loads(response.read(65536))
                    if response.status!=200 or result.get('ok') is not True or not isinstance(result.get('result'),dict) or not isinstance(result['result'].get('message_id'),int):
                        raise ValueError()
                db.execute('UPDATE leads SET notified=1 WHERE id=?',(ident,))
                db.commit();db.execute('BEGIN IMMEDIATE')
    except Exception:
        # Deliberately do not print exceptions: library errors may contain the bot URL/token.
        print('NOTIFICATION_PENDING_RETRY');return 1
    print('NOTIFICATION_OUTBOX_DRAINED');return 0

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=4173);parser.add_argument('--database');parser.add_argument('--notify',action='store_true');args=parser.parse_args()
    default=Path(os.environ.get('LOCALAPPDATA',str(Path.home()))) / 'QadamUp' / 'landing-preview' / 'leads.sqlite3'
    if args.notify: raise SystemExit(notify(args.database or default))
    # CLI preview always builds from this checkout, independent of shell cwd.
    subprocess.run([sys.executable,str(ROOT/'scripts'/'funnel.py'),'--target','local'],cwd=ROOT,check=True)
    server=make_server(args.port,args.database)
    print(f'Serving B2B funnel from: {ROOT}',flush=True)
    print(f'Local preview: http://127.0.0.1:{server.server_port}/',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
