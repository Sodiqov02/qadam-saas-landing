"""Current browser contract, replacing historical numeric-input/disabled-demo assumptions.
See docs/release-test-mapping.md. All retained checks execute, without hash exemptions.
"""
from pathlib import Path
import runpy
import sys
import tempfile
import threading
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server

def main():
    runpy.run_path(str(Path(__file__).with_name('funnel-browser.py')),run_name='__main__')
    from overdrive_accessibility import main as accessibility
    with tempfile.TemporaryDirectory() as tmp:
        app=server.make_server(0,Path(tmp)/'leads.sqlite3')
        threading.Thread(target=app.serve_forever,daemon=True).start()
        try:accessibility(f'http://127.0.0.1:{app.server_port}/')
        finally:app.shutdown();app.server_close()
    print('LANDING_BROWSER_OK')
if __name__=='__main__':main()
