"""Single source of the stylesheet, the navigation and the Jekyll layout (figure-pages-site house style)."""
import pathlib
import shutil

from objectcore_utils import ASSETS, DOCS, write_text

DOC_NAV = [("Overview", "/", "index.html"), ("Profile", "/profile.html", "profile.html"),
           ("Crosswalk", "/crosswalk.html", "crosswalk.html"), ("Findings", "/findings.html", "findings.html")]


def vis_nav(m):
    items = [("Overview", "/visuals/index.html", "visuals/index.html"), ("Pipeline", "/visuals/pipeline.html", "visuals/pipeline.html"),
             ("Profile model", "/visuals/model.html", "visuals/model.html"), ("Crosswalk", "/visuals/crosswalk.html", "visuals/crosswalk.html"),
             ("Tests", "/visuals/tests.html", "visuals/tests.html")]
    return items


def ex_nav(m):
    items = []
    for ex in m["examples"]:
        n = "example-" + ex["file"].replace(".ttl", "")
        items.append((ex["file"].replace(".ttl", ""), "/visuals/%s.html" % n, "visuals/%s.html" % n))
    return items


CSS = """
@font-face{font-family:"Fira Sans";font-weight:400;src:url(fonts/FiraSans-Regular.ttf) format("truetype");font-display:swap}
@font-face{font-family:"Fira Sans";font-weight:500;src:url(fonts/FiraSans-Medium.ttf) format("truetype");font-display:swap}
:root{--bg:#f6f6f3;--card:#fff;--ink:#1f1f1d;--muted:#55544f;--rim:#d8d6ce;--accent:#9a3412}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.5 "Fira Sans",system-ui,sans-serif}
main{max-width:1040px;margin:0 auto;padding:16px 16px 48px}
h1{font-size:28px;font-weight:500;margin:24px 0 8px}
h2{font-size:22px;font-weight:500;margin:28px 0 8px}
a{color:var(--accent)}
nav{max-width:1008px;margin:16px auto 0;background:var(--card);border:1px solid var(--rim);border-radius:10px;overflow:hidden}
nav .row{display:flex;flex-wrap:wrap;gap:4px 18px;align-items:center;padding:10px 16px 10px 20px;border-left:5px solid var(--accent);font-size:15px}
nav .row+.row{border-top:1px solid var(--rim)}
nav .row.doc{border-left-color:var(--ink)}
nav .lab{font-size:11.5px;font-weight:500;letter-spacing:.07em;text-transform:uppercase;color:#fff;background:var(--accent);border-radius:5px;padding:3px 10px;flex:0 0 auto}
nav .row.doc .lab{background:var(--ink)}
nav a{text-decoration:none;color:var(--muted)}
nav a:hover{color:var(--ink)}
nav a.active{color:var(--accent);font-weight:500}
@media(max-width:1040px){nav{margin-left:16px;margin-right:16px}}
section,article.prose{background:var(--card);border:1px solid var(--rim);border-radius:10px;padding:16px;margin-bottom:24px}
section img{max-width:100%;height:auto;display:block}
.row2{display:flex;gap:12px;align-items:baseline;margin-top:10px}
.n{color:var(--accent);font-weight:500}
.cap{font-size:20px;font-weight:500;flex:1}
.credit{font-size:14px;color:var(--muted);margin:4px 0 8px}
button{font:inherit;font-size:14px;border:1px solid var(--rim);background:#fff;border-radius:6px;padding:2px 10px;cursor:pointer}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid section{margin:0}
@media(max-width:700px){.grid{grid-template-columns:1fr}}
table{border-collapse:collapse;width:100%;font-size:15px;display:block;overflow-x:auto}
th,td{border-bottom:1px solid var(--rim);padding:6px 8px;text-align:left;vertical-align:top}
blockquote{background:#fff7e0;border-left:4px solid #fbbf24;margin:12px 0;padding:8px 14px}
code{font-size:.92em;background:#f1f0ea;padding:0 4px;border-radius:4px}
"""


def nav_liquid(m):
    def row(label, items, cls=""):
        links = "".join('<a href="{{ \'%s\' | relative_url }}"{%% if page.url == \'%s\' %%} class="active"{%% endif %%}>%s</a>' % (u, u, l) for l, u, _ in items)
        return '<div class="row%s"><span class="lab">%s</span>%s</div>' % (cls, label, links)
    return "<nav>" + row("Documentation", DOC_NAV, " doc") + row("Visuals", vis_nav(m)) + row("Examples", ex_nav(m)) + "</nav>"


def nav_static(m, active):
    def row(label, items, cls=""):
        links = ""
        for l, _, f in items:
            href = ("../" + f) if True else f
            acls = ' class="active"' if f == active else ""
            links += '<a href="%s"%s>%s</a>' % (href, acls, l)
        return '<div class="row%s"><span class="lab">%s</span>%s</div>' % (cls, label, links)
    return "<nav>" + row("Documentation", DOC_NAV, " doc") + row("Visuals", vis_nav(m)) + row("Examples", ex_nav(m)) + "</nav>"


def write_assets(m):
    a = DOCS / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    for f in ("FiraSans-Regular.ttf", "FiraSans-Medium.ttf"):
        shutil.copyfile(ASSETS / "fonts" / f, a / "fonts" / f)
    shutil.copyfile(ASSETS / "fonts" / "OFL.txt", a / "fonts" / "OFL.txt")
    write_text(a / "site.css", CSS.strip())
    (DOCS / "_layouts").mkdir(parents=True, exist_ok=True)
    write_text(DOCS / "_layouts" / "default.html",
               '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
               '<title>{{ page.title }} · ObjectCore-AP</title><link rel="stylesheet" href="{{ \'/assets/site.css\' | relative_url }}"></head><body>'
               + nav_liquid(m) + '<main><article class="prose">{{ content }}</article></main></body></html>')
    write_text(DOCS / "_config.yml", "title: ObjectCore-AP\nurl: https://crossy-graph.github.io\nbaseurl: /objectcore-ap\nmarkdown: kramdown\n"
               "exclude: [visuals/img/README]\n")
