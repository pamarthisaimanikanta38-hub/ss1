from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).parent
STATIC = ROOT / "static"
UPLOAD_DIR = STATIC / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="A Little Universe for Sindhu")
app.mount("/static", StaticFiles(directory=STATIC), name="static")

NOTES = [
    ("A little reminder 🌷", "Sindhu, never forget how special you are. Your kindness, your smile, and the little things that make you you can brighten an ordinary day. I hope life gives you countless reasons to smile."),
    ("For the difficult days 🌙", "If today feels heavy, take a breath and remember that one difficult day does not define your whole story. You have made it through so much already. Be gentle with yourself, take things one step at a time, and keep believing in the good that is still ahead."),
    ("A wish for your future ✨", "I hope your dreams grow bigger than your fears. I hope you find people who respect your heart, opportunities that help you shine, and moments that remind you how beautiful life can be. May your future be full of peace, courage, laughter, and success."),
    ("Thank you for being you 💗", "Some people make life feel a little warmer simply by being themselves. Thank you for the memories, the laughs, and the little moments that become special without even trying. This page is a small reminder that you are appreciated."),
    ("Open when you need a smile 💌", "Surprise! Here is your reminder to relax your shoulders, drink some water, take a little break, and give yourself credit for how far you have come. Sending you a pocket-sized bundle of sunshine and a thousand imaginary hearts.")
]

def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))

def get_gallery():
    allowed = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    cards = []
    for p in sorted(UPLOAD_DIR.iterdir()):
        if p.is_file() and p.suffix.lower() in allowed:
            cards.append(
                f'<figure class="memory"><img src="/static/uploads/{esc(p.name)}" alt="A memory">'
                f'<figcaption>{esc(p.stem.replace("_", " "))}</figcaption></figure>'
            )
    if not cards:
        cards = [
            '<div class="empty-memory"><span>🌸</span><b>Your first memory goes here</b><small>Upload a photo below to begin your gallery.</small></div>',
            '<div class="empty-memory"><span>🌙</span><b>Little moments</b><small>Even ordinary days can become memories.</small></div>',
            '<div class="empty-memory"><span>✨</span><b>More memories to come</b><small>Your favourite pictures belong here.</small></div>',
        ]
    return "".join(cards)

def page():
    note_cards = "".join(
        f'<article class="note-card"><div class="note-icon">{icon}</div><h3>{esc(title)}</h3>'
        f'<p>{esc(body)}</p><button class="small-btn open-note" data-title="{esc(title)}" data-body="{esc(body)}">Read this note ↗</button></article>'
        for icon, (title, body) in zip(["🌷", "🌙", "✨", "💗", "💌"], NOTES)
    )
    html = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#21102f">
<title>A Little Universe for Sindhu 💗</title>
<style>
:root{--pink:#ff82b7;--light:#ffe3f0;--ink:#2b1235;--glass:rgba(255,255,255,.085)}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;color:#fff7fc;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;background:#160c27;overflow-x:hidden}
button,input{font:inherit}
a{color:inherit;text-decoration:none}
#sky,.float-layer{position:fixed;inset:0;pointer-events:none;overflow:hidden}
#sky{z-index:0;background:radial-gradient(ellipse at 10% 15%,#7d2868 0,transparent 38%),radial-gradient(ellipse at 88% 65%,#38358b 0,transparent 37%),radial-gradient(ellipse at 50% 110%,#9c285c 0,transparent 43%),linear-gradient(145deg,#100b23,#311334 55%,#100b23)}
.float-layer{z-index:3}
.wrap{position:relative;z-index:1;width:min(1120px,92%);margin:auto}
header{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px 0;flex-wrap:wrap}
.brand{font-weight:800;letter-spacing:.02em}.brand span{color:#ff9ec9}
nav{display:flex;gap:17px;flex-wrap:wrap;font-size:.9rem;color:#f7d9e9}
nav a:hover{color:#ffadd0}
.pill{padding:8px 13px;border:1px solid #ffffff2e;border-radius:999px;background:#ffffff0c;font-size:.82rem}
.hero{text-align:center;padding:58px 0 54px}
.kicker{font-size:.75rem;text-transform:uppercase;letter-spacing:.28em;color:#ffc2dc;font-weight:800}
h1{font-size:clamp(3rem,9vw,6.6rem);line-height:.98;margin:19px 0;background:linear-gradient(100deg,#fff,#ffb1d2 45%,#fff0f7);background-clip:text;-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 0 28px #ff6aa52b)}
.lead{max-width:680px;margin:0 auto;color:#f5dce9;line-height:1.8;font-size:1.08rem}
.heart-stage{height:250px;display:grid;place-items:center;position:relative;margin:10px auto 10px}
.heart{font-size:clamp(112px,20vw,174px);line-height:1;cursor:pointer;user-select:none;filter:drop-shadow(0 0 25px #ff4f9c);animation:pulse 1.4s ease-in-out infinite;z-index:1}
@keyframes pulse{0%,100%{transform:scale(1)}12%{transform:scale(1.13)}23%{transform:scale(1)}38%{transform:scale(1.08)}52%{transform:scale(1)}}
.ring{position:absolute;width:220px;height:220px;border:1px solid #ffc0de61;border-radius:50%;animation:rotate 18s linear infinite}
.ring:before,.ring:after{content:"✦";position:absolute;color:#ffe6f2;font-size:18px}.ring:before{top:10px;left:35px}.ring:after{right:12px;bottom:25px}
@keyframes rotate{to{transform:rotate(360deg)}}
.buttons{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:20px}
.btn{border:1px solid #ffffff3d;border-radius:999px;padding:13px 20px;background:#ffffff12;color:white;cursor:pointer;font-weight:750;transition:.2s}
.btn.primary{background:linear-gradient(100deg,#ffacd0,#fff0f7);color:#4a1538;border:0}
.btn:hover,.small-btn:hover{transform:translateY(-3px);box-shadow:0 12px 28px #ff66a32b}
.section{padding:28px 0 42px;scroll-margin-top:25px}
.section-heading{text-align:center;margin:0 auto 25px}
.section-heading .eyebrow{font-size:.73rem;letter-spacing:.2em;text-transform:uppercase;color:#ffb5d3;font-weight:800}
h2{font-size:clamp(1.7rem,4vw,2.5rem);margin:8px 0 10px}
.section-heading p{color:#e7c9dc;line-height:1.7;margin:0 auto;max-width:650px}
.glass{border:1px solid #ffffff25;background:linear-gradient(135deg,#ffffff14,#ffffff07);backdrop-filter:blur(14px);border-radius:25px;box-shadow:0 20px 60px #0703112b}
.letter{max-width:850px;margin:auto;padding:clamp(22px,5vw,42px);text-align:center}
.letter p{color:#f8e5ef;line-height:1.95;font-size:1.04rem;white-space:pre-line}
.signature{color:#ffb1d2;font-weight:800}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:15px}
.note-card{padding:23px;border:1px solid #ffffff20;background:#ffffff0b;border-radius:22px;display:flex;flex-direction:column;align-items:flex-start;min-height:260px}
.note-icon{font-size:1.7rem}.note-card h3{margin:12px 0 8px}.note-card p{color:#ead4e1;line-height:1.7;margin:0 0 18px;flex:1}
.small-btn{border:1px solid #ffffff3a;border-radius:999px;background:#ffffff0d;color:#ffe5f1;padding:9px 13px;cursor:pointer;font-weight:700;transition:.2s}
.gallery-shell{padding:20px}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:14px}
.memory,.empty-memory{margin:0;min-height:225px;border-radius:18px;overflow:hidden;position:relative;background:#ffffff0a;border:1px solid #ffffff24}
.memory img{width:100%;height:225px;object-fit:cover;display:block;transition:transform .5s}
.memory:hover img{transform:scale(1.06)}
.memory figcaption{position:absolute;bottom:0;left:0;right:0;padding:24px 12px 12px;background:linear-gradient(transparent,#120818d9);font-size:.85rem}
.empty-memory{display:flex;align-items:center;justify-content:center;flex-direction:column;text-align:center;gap:8px;padding:20px;color:#fbe4ef}
.empty-memory span{font-size:2rem}.empty-memory small{color:#d8b6cb;line-height:1.5}
.upload-box{margin-top:18px;padding:20px;border:1px dashed #ffffff55;border-radius:18px;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
.upload-box p{margin:0;color:#e8cbdd;font-size:.9rem;line-height:1.6}
input[type=file]{max-width:100%;color:#fbe6f1}
.wish-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
.wish{padding:20px 15px;text-align:center;border-radius:18px;background:#ffffff0b;border:1px solid #ffffff20}
.wish div{font-size:1.8rem}.wish b{display:block;margin:8px 0}.wish small{color:#e4c9d9;line-height:1.5}
footer{text-align:center;color:#cba9c1;padding:45px 0 28px;font-size:.85rem}
.modal{position:fixed;inset:0;background:#080511c9;z-index:10;display:none;align-items:center;justify-content:center;padding:20px}
.modal.show{display:flex}
.modal-box{width:min(600px,100%);padding:30px;text-align:center;position:relative;animation:pop .25s ease-out}
@keyframes pop{from{transform:scale(.88);opacity:0}to{transform:scale(1);opacity:1}}
.modal-box p{white-space:pre-line;line-height:1.9;color:#f5dce9}
.close{position:absolute;top:12px;right:14px;border:0;background:transparent;color:white;font-size:1.5rem;cursor:pointer}
.toast{position:fixed;bottom:24px;left:50%;transform:translate(-50%,25px);opacity:0;z-index:11;background:#fff0f7;color:#4b1538;padding:12px 18px;border-radius:999px;font-weight:800;transition:.25s;pointer-events:none;text-align:center;width:max-content;max-width:90%}
.toast.show{opacity:1;transform:translate(-50%,0)}
@media(max-width:600px){header{justify-content:center}nav{justify-content:center}.hero{padding-top:35px}.heart-stage{height:205px}.ring{width:185px;height:185px}.upload-box{align-items:flex-start}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important}}
</style>
</head>
<body>
<div id="sky"></div><div class="float-layer" id="floaties"></div>
<div class="wrap">
<header><div class="brand">S ✦ S <span>♡</span></div><nav><a href="#letter">The letter</a><a href="#notes">Little notes</a><a href="#memories">Memories</a><a href="#wishes">Wishes</a></nav><div class="pill">A page from Sai 💌</div></header>
<main>
<section class="hero">
<div class="kicker">A little universe made just for you</div>
<h1>Hey, Sindhu.</h1>
<p class="lead">For the smiles, the memories, the kind moments, and all the wonderful things still waiting for you. This tiny corner of the internet is just for you. 💗</p>
<div class="heart-stage"><div class="ring"></div><div class="heart" id="heart" title="Tap the heart">💖</div></div>
<div class="buttons"><button class="btn primary" id="surprise">Open a little surprise ✨</button><button class="btn" id="heartBurst">Send a shower of hearts 💞</button><a class="btn" href="#letter">Read your letter ↓</a></div>
</section>
<section class="section" id="letter">
<div class="section-heading"><div class="eyebrow">From the heart</div><h2>A little letter for Sindhu 💌</h2><p>Some words are small, but the feeling behind them can be big.</p></div>
<div class="glass letter"><p>Sindhu, I hope this page makes you smile, even if just for a moment.

You deserve days that feel peaceful, friends who cheer for you, dreams that excite you, and little surprises that remind you how appreciated you are.

When life gets busy, remember to pause and notice how far you have come. You do not need to have everything figured out today. Keep learning, keep laughing, and keep being the wonderful person you are.

May your future be filled with beautiful opportunities, genuine happiness, and memories you will always want to keep.</p><div class="signature">With warmth and good wishes — Sai ♡</div><div class="buttons"><button class="btn primary" id="copyNote">Copy this letter 📋</button><button class="btn" id="letterSurprise">Add some sparkle ✨</button></div></div>
</section>
<section class="section" id="notes">
<div class="section-heading"><div class="eyebrow">Open whenever you need it</div><h2>Little notes, just for you 🌷</h2><p>Choose a card. There is a different message waiting inside each one.</p></div>
<div class="grid">__NOTE_CARDS__</div>
</section>
<section class="section" id="memories">
<div class="section-heading"><div class="eyebrow">Keep the good moments close</div><h2>Our memory corner 📸</h2><p>Add photos when you are ready and turn this page into a little scrapbook.</p></div>
<div class="glass gallery-shell"><div class="gallery">__GALLERY__</div>
<form class="upload-box" action="/upload" method="post" enctype="multipart/form-data"><div><b>Bring your memories to life</b><p>Choose JPG, PNG, WEBP or GIF photos.<br>Use meaningful filenames for simple captions.</p></div><div><input type="file" name="photos" accept="image/jpeg,image/png,image/webp,image/gif" multiple required><button class="btn primary" type="submit">Add photos 📷</button></div></form>
</div>
</section>
<section class="section" id="wishes">
<div class="section-heading"><div class="eyebrow">A few wishes for your journey</div><h2>May life bring you… ✨</h2></div>
<div class="wish-grid"><div class="wish"><div>🌻</div><b>Happiness</b><small>Little reasons to smile, every day.</small></div><div class="wish"><div>🌙</div><b>Peace</b><small>Rest for your heart and mind.</small></div><div class="wish"><div>🚀</div><b>Big dreams</b><small>Courage to try and grow.</small></div><div class="wish"><div>🫶</div><b>Good people</b><small>Kindness, respect, and support.</small></div><div class="wish"><div>🌈</div><b>Hope</b><small>Light, even after hard days.</small></div></div>
<div class="buttons"><button class="btn primary" id="dailyWish">Give me one more wish 🌠</button></div>
</section>
</main>
<footer>Made with 💗 by Sai, for Sindhu.<br><span style="display:inline-block;margin-top:8px">A little reminder: you matter, and your story is still unfolding.</span></footer>
</div>
<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle"><div class="glass modal-box"><button class="close" id="closeModal" aria-label="Close">×</button><div style="font-size:2.5rem" id="modalEmoji">💖</div><h2 id="modalTitle">A surprise for you</h2><p id="modalText"></p><button class="btn primary" id="modalOk">Keep this smile 💗</button></div></div>
<div class="toast" id="toast">Sending a little happiness your way 💗</div>
<script>
const sky=document.getElementById('sky'), floaties=document.getElementById('floaties');
for(let i=0;i<100;i++){const s=document.createElement('i');s.style.cssText=`position:absolute;left:${Math.random()*100}%;top:${Math.random()*100}%;width:${Math.random()*3+1}px;height:${Math.random()*3+1}px;border-radius:50%;background:white;opacity:${Math.random()*.65+.15};box-shadow:0 0 8px #fff;animation:twinkle ${2+Math.random()*4}s ${Math.random()*3}s infinite alternate`;sky.appendChild(s)}
const style=document.createElement('style');style.textContent='@keyframes twinkle{to{opacity:.12;transform:scale(.55)}}';document.head.appendChild(style);
function floatOne(){const e=document.createElement('span');e.textContent=['💗','💕','💖','✨','🌸','🦋'][Math.floor(Math.random()*6)];e.style.cssText=`position:absolute;left:${Math.random()*100}%;bottom:-50px;font-size:${18+Math.random()*25}px;opacity:0;filter:drop-shadow(0 0 8px #ff75b7);animation:floatUp ${5+Math.random()*6}s linear forwards`;floaties.appendChild(e);setTimeout(()=>e.remove(),11500)}
const fs=document.createElement('style');fs.textContent='@keyframes floatUp{0%{transform:translateY(0) rotate(0);opacity:0}12%{opacity:.85}100%{transform:translateY(-115vh) rotate(40deg);opacity:0}}';document.head.appendChild(fs);
setInterval(floatOne,550);for(let i=0;i<14;i++)setTimeout(floatOne,i*180);
const modal=document.getElementById('modal'),toast=document.getElementById('toast');
function showToast(t='Sending a little happiness your way 💗'){toast.textContent=t;toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2400)}
function openModal(title,text,emoji='💖'){document.getElementById('modalTitle').textContent=title;document.getElementById('modalText').textContent=text;document.getElementById('modalEmoji').textContent=emoji;modal.classList.add('show')}
function burst(n=30){for(let i=0;i<n;i++)setTimeout(floatOne,i*35);showToast('A little happiness is on its way 💗')}
document.getElementById('surprise').onclick=()=>openModal('A tiny surprise for Sindhu 💝','You are allowed to take up space, to dream big, to rest, to start again, and to be proud of yourself. I hope this little surprise reminds you that good things are still ahead. Keep shining in your own way.','🎁');
document.getElementById('heartBurst').onclick=()=>burst(45);
document.getElementById('heart').onclick=()=>burst(18);
document.getElementById('letterSurprise').onclick=()=>burst(35);
document.getElementById('closeModal').onclick=()=>modal.classList.remove('show');
document.getElementById('modalOk').onclick=()=>{modal.classList.remove('show');burst(18)};
modal.addEventListener('click',e=>{if(e.target===modal)modal.classList.remove('show')});
document.addEventListener('keydown',e=>{if(e.key==='Escape')modal.classList.remove('show')});
document.querySelectorAll('.open-note').forEach(b=>b.addEventListener('click',()=>openModal(b.dataset.title,b.dataset.body,'💌')));
document.getElementById('dailyWish').onclick=()=>{const wishes=['May you find courage for the things you want to try. 🌻','May you have a peaceful mind and a heart that feels understood. 🌙','May your effort lead you toward opportunities you are proud of. 🚀','May you always remember to be kind to yourself. 🫶','May a small, unexpected moment make you smile today. 🌈'];openModal('A wish for you 🌠',wishes[Math.floor(Math.random()*wishes.length)],'✨')};
document.getElementById('copyNote').onclick=async()=>{const t=document.querySelector('.letter p').innerText;try{await navigator.clipboard.writeText(t);showToast('Letter copied to clipboard 📋')}catch(e){openModal('Your letter 💌',t,'📋')}};
</script>
</body></html>"""
    return html.replace("__NOTE_CARDS__", note_cards).replace("__GALLERY__", get_gallery())

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(page())

@app.post("/upload")
async def upload(photos: list[UploadFile] = File(...)):
    allowed = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    for photo in photos:
        suffix = Path(photo.filename or "").suffix.lower()
        if suffix not in allowed:
            await photo.close()
            continue
        # Randomized names prevent path traversal and filename collisions.
        target = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
        with target.open("wb") as out:
            shutil.copyfileobj(photo.file, out)
        await photo.close()
    return RedirectResponse("/", status_code=303)
