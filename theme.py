import streamlit as st

FOODS = ["🍛", "🥘", "🌶️", "🥭", "🍚", "🥥", "🧅", "🍅", "🫓", "🍋", "🥕", "🫚"]

GRANDMA_SVG = """
<svg viewBox="0 0 200 210" xmlns="http://www.w3.org/2000/svg" class="gran-svg">
  <path d="M30 210 Q100 118 170 210Z" fill="#E63946"/>
  <path d="M30 210 Q100 118 170 210" fill="none" stroke="#FFC93C" stroke-width="6"/>
  <circle cx="100" cy="36" r="17" fill="#EDEDF2"/>
  <circle cx="100" cy="86" r="42" fill="#F2B98F"/>
  <path d="M58 84 Q56 40 100 42 Q144 40 142 84 Q126 58 100 58 Q74 58 58 84Z" fill="#EDEDF2"/>
  <circle cx="100" cy="68" r="3.5" fill="#E63946"/>
  <g class="blink"><circle cx="84" cy="90" r="3.2" fill="#3b2a20"/><circle cx="116" cy="90" r="3.2" fill="#3b2a20"/></g>
  <circle cx="84" cy="90" r="12" fill="rgba(255,255,255,.35)" stroke="#6b4a3a" stroke-width="3"/>
  <circle cx="116" cy="90" r="12" fill="rgba(255,255,255,.35)" stroke="#6b4a3a" stroke-width="3"/>
  <path d="M96 90 H104" stroke="#6b4a3a" stroke-width="3"/>
  <circle cx="72" cy="106" r="6" fill="#FF8FAB" opacity=".6"/><circle cx="128" cy="106" r="6" fill="#FF8FAB" opacity=".6"/>
  <path d="M86 108 Q100 124 114 108" fill="none" stroke="#9b3d3d" stroke-width="3.5" stroke-linecap="round"/>
  <g class="ladle"><line x1="150" y1="168" x2="182" y2="112" stroke="#8a5a3c" stroke-width="6" stroke-linecap="round"/>
    <circle cx="184" cy="106" r="13" fill="#C9CED6" stroke="#8a93a1" stroke-width="3"/></g>
</svg>
"""

def inject_theme():
    spans = ""
    for i, f in enumerate(FOODS * 2):
        left = (i * 41) % 96
        dur = 14 + (i * 3) % 11
        delay = -(i * 2.3)
        size = 28 + (i * 7) % 34
        spans += (f'<span style="left:{left}%;font-size:{size}px;'
                  f'animation-duration:{dur}s;animation-delay:{delay}s">{f}</span>')

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;800&family=Caveat:wght@600&family=Nunito:wght@500;700&display=swap');
html, body, [class*="css"] {{ font-family:'Nunito',sans-serif; }}
[data-testid="stAppViewContainer"] {{
  background: linear-gradient(120deg,#FFD166,#FF8FAB,#FFB347,#9BE7C4);
  background-size: 300% 300%; animation: sky 18s ease infinite;
}}
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ position:relative; z-index:1; padding-top:1.5rem; max-width:1150px; }}
@keyframes sky {{ 0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}} }}

/* floating 3D food */
.food {{ position:fixed; inset:0; overflow:hidden; pointer-events:none; z-index:0; }}
.food span {{ position:absolute; bottom:-80px; opacity:.85; animation: rise linear infinite; }}
@keyframes rise {{
  from {{ transform: translateY(0) rotateY(0deg) rotate(-14deg); }}
  to   {{ transform: translateY(-125vh) rotateY(720deg) rotate(14deg); }}
}}

/* hero */
.hero {{ display:flex; align-items:center; gap:28px; padding:18px 30px; margin-bottom:22px;
  background:#fffaf0; border:4px solid #2B2D6E; border-radius:40px; box-shadow:10px 10px 0 #2B2D6E; }}
.gran-svg {{ width:170px; flex:none; animation: bob 2.6s ease-in-out infinite; transform-origin:50% 100%; }}
.gran-svg .ladle {{ transform-origin:150px 168px; animation: stir 1.4s ease-in-out infinite; }}
.gran-svg .blink {{ transform-origin:100px 90px; animation: blink 4s infinite; }}
@keyframes bob {{ 0%,100%{{transform:translateY(0) rotate(-2deg)}} 50%{{transform:translateY(-8px) rotate(2deg)}} }}
@keyframes stir {{ 0%,100%{{transform:rotate(-14deg)}} 50%{{transform:rotate(14deg)}} }}
@keyframes blink {{ 0%,92%,100%{{transform:scaleY(1)}} 96%{{transform:scaleY(.1)}} }}
.hero h1 {{ font-family:'Baloo 2'; font-weight:800; font-size:3.2rem; margin:0; color:#2B2D6E; line-height:1; }}
.hero p {{ margin:.4rem 0 0; font-size:1.15rem; color:#5b3a2e; }}

/* four different page styles, one per stage */
.st-key-rec, .st-key-heard, .st-key-recipe, .st-key-watch {{
  padding:26px 28px; margin-bottom:22px; transition: transform .35s ease; }}
.st-key-rec {{ background:#FFE066; border:4px solid #2B2D6E; border-radius:30px;
  box-shadow:8px 8px 0 #2B2D6E; transform:perspective(900px) rotateY(5deg) rotate(-1deg); color:#2B2D6E; }}
.st-key-heard {{ background:#fff repeating-linear-gradient(transparent 0 31px,#cfe3ff 31px 33px);
  border-left:12px solid #FF5C8A; border-radius:10px; box-shadow:0 14px 30px rgba(0,0,0,.18);
  transform:perspective(900px) rotateX(3deg) rotate(1deg); font-family:'Caveat'; font-size:1.5rem; color:#1d3557; }}
.st-key-recipe {{ background:#fffdf7; border:3px dashed #E63946; border-radius:6px;
  box-shadow:0 0 0 8px #fffdf7, 0 18px 30px rgba(0,0,0,.2); transform:rotate(-1.2deg); color:#3a2a22; }}
.st-key-watch {{ background:#2B2D6E; border:12px solid #151745; border-radius:44px; color:#fff;
  box-shadow:0 0 0 4px #FFC93C, 0 0 50px rgba(255,201,60,.55); transform:perspective(900px) rotateY(-5deg); }}
.st-key-rec:hover, .st-key-heard:hover, .st-key-recipe:hover, .st-key-watch:hover {{ transform:none; }}
.st-key-watch p, .st-key-watch h3, .st-key-watch label {{ color:#fff !important; }}

/* chunky 3D button */
.stButton > button {{ background:#E63946; color:#fff; font-family:'Baloo 2'; font-weight:800; font-size:1.3rem;
  border:3px solid #2B2D6E; border-radius:999px; padding:.55rem 1.6rem; box-shadow:0 7px 0 #8f1c27;
  transition: transform .1s, box-shadow .1s; }}
.stButton > button:hover {{ background:#ff4d5a; color:#fff; border-color:#2B2D6E; }}
.stButton > button:active {{ transform:translateY(6px); box-shadow:0 1px 0 #8f1c27; }}

@media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important; }} }}
@media (max-width:700px) {{ .hero {{ flex-direction:column; text-align:center; }} .hero h1 {{ font-size:2.2rem; }} }}
</style>
<div class="food">{spans}</div>
""", unsafe_allow_html=True)

def header():
    st.markdown(f"""
<div class="hero">{GRANDMA_SVG}
  <div><h1>Recipe Whisperer</h1>
  <p>Tell Paati's recipe in your own words. We turn "a handful, till it smells right" into exact grams, then cook it up on screen.</p></div>
</div>""", unsafe_allow_html=True)