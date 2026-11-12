from playwright.sync_api import sync_playwright
import pathlib,sys
root=pathlib.Path(__file__).resolve().parent.parent / "site"
JS=open('audit.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=b.new_context(viewport={'width':1440,'height':900})
    def h(route):
        path=route.request.url.split('://x',1)[1].split('?')[0].split('#')[0]; f=root/path.lstrip('/')
        if f.is_dir(): f=f/'index.html'
        ct={'html':'text/html','css':'text/css','js':'text/javascript','webp':'image/webp','svg':'image/svg+xml','png':'image/png'}.get(f.suffix[1:],'application/octet-stream')
        route.fulfill(status=200,body=f.read_bytes(),content_type=ct) if f.exists() else route.fulfill(status=404,body='')
    ctx.route('http://x/**',h)
    for u in ['/nexora/','/nexora/brief/','/nexora/forge/','/nexora/manage/','/nexora/how-it-works/','/nexora/deliverables/','/nexora/contact/']:
        pg=ctx.new_page(); pg.goto('http://x'+u,wait_until='networkidle'); pg.wait_for_timeout(1000)
        res=pg.evaluate(JS); print('=====',u)
        for r in res: print(f"  {r['sel']:16} Δ{r['diff']:4}  | "+' | '.join(r['items']))
        pg.close()
    b.close()
