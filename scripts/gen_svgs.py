import random
import sys
from html import escape

OUT = sys.argv[1]
MONO = "'JetBrains Mono','Fira Code','SF Mono',Menlo,Consolas,monospace"
random.seed(7)

# ---------------------------------------------------------------- header
W, H, HZ = 1200, 400, 268  # width, height, horizon y
VX = W / 2

stars = "".join(
    f'<circle cx="{random.randint(0, W)}" cy="{random.randint(0, HZ - 20)}" r="{random.choice([0.6, 0.9, 1.3])}" '
    f'fill="#fff" class="tw" style="animation-delay:{random.uniform(0, 4):.2f}s"/>'
    for _ in range(90)
)

verticals = "".join(
    f'<line x1="{VX + k * 34}" y1="{HZ}" x2="{VX + k * 300}" y2="{H}"/>' for k in range(-16, 17)
)
horizontals = "".join(
    f'<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}">'
    f'<animate attributeName="y1" values="{HZ};{H}" dur="4s" begin="{-i * 0.5}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines="0.55 0 1 0.45"/>'
    f'<animate attributeName="y2" values="{HZ};{H}" dur="4s" begin="{-i * 0.5}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines="0.55 0 1 0.45"/>'
    f'<animate attributeName="stroke-opacity" values="0;1" dur="4s" begin="{-i * 0.5}s" repeatCount="indefinite"/>'
    f"</line>"
    for i in range(8)
)

# stripes cut out of the sun
stripes = "".join(
    f'<rect x="0" y="{HZ - 70 + i * 13}" width="{W}" height="{2 + i * 1.2}" fill="#000"/>' for i in range(6)
)

header = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#03000a"/><stop offset="0.55" stop-color="#0d0623"/><stop offset="1" stop-color="#2a0845"/>
  </linearGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#14002b"/><stop offset="1" stop-color="#03000a"/>
  </linearGradient>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffd166"/><stop offset="0.5" stop-color="#ff2bd6"/><stop offset="1" stop-color="#7c3aed"/>
  </linearGradient>
  <linearGradient id="nameg" x1="0" x2="1">
    <stop offset="0" stop-color="#00f0ff"/><stop offset="0.5" stop-color="#e0e7ff"/><stop offset="1" stop-color="#ff2bd6"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="soft"><feGaussianBlur stdDeviation="18"/></filter>
  <mask id="sunmask"><rect width="{W}" height="{H}" fill="#fff"/>{stripes}</mask>
  <clipPath id="above"><rect width="{W}" height="{HZ}"/></clipPath>
  <clipPath id="below"><rect y="{HZ}" width="{W}" height="{H - HZ}"/></clipPath>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity="0.25"/></pattern>
</defs>
<style>
  .tw {{ animation: tw 4s ease-in-out infinite; }}
  @keyframes tw {{ 0%,100% {{ opacity: .15 }} 50% {{ opacity: .9 }} }}
  .hud {{ font: 600 13px {MONO}; fill: #7dd3fc; letter-spacing: 2px; }}
  .dim {{ fill: #a78bfa; }}
  .name {{ font: 800 76px {MONO}; letter-spacing: 6px; }}
  .tag {{ font: 500 17px {MONO}; fill: #c4b5fd; letter-spacing: 5px; }}
  .g1 {{ animation: g1 5s steps(1) infinite; }}
  .g2 {{ animation: g2 5s steps(1) infinite; }}
  @keyframes g1 {{ 0%,88%,100% {{ transform: translate(0,0); opacity: 0 }} 89% {{ transform: translate(-6px,2px); opacity: .8 }} 92% {{ transform: translate(4px,-1px); opacity: .8 }} 95% {{ transform: translate(-2px,0); opacity: .6 }} }}
  @keyframes g2 {{ 0%,88%,100% {{ transform: translate(0,0); opacity: 0 }} 89% {{ transform: translate(6px,-2px); opacity: .8 }} 92% {{ transform: translate(-4px,1px); opacity: .8 }} 95% {{ transform: translate(2px,0); opacity: .6 }} }}
  .blink {{ animation: blink 1.2s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0 }} }}
  .sun {{ animation: rise 6s ease-in-out infinite alternate; }}
  @keyframes rise {{ from {{ transform: translateY(6px) }} to {{ transform: translateY(-6px) }} }}
</style>

<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars}

<g clip-path="url(#above)">
  <circle cx="{VX}" cy="{HZ - 10}" r="120" fill="#ff2bd6" opacity=".35" filter="url(#soft)"/>
  <g class="sun"><circle cx="{VX}" cy="{HZ - 10}" r="95" fill="url(#sun)" mask="url(#sunmask)"/></g>
</g>

<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floor)"/>
<g clip-path="url(#below)" stroke="#ff2bd6" stroke-width="1.4" fill="none" filter="url(#glow)">
  <g stroke-opacity=".55">{verticals}</g>
  {horizontals}
</g>
<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}" stroke="#00f0ff" stroke-width="2" filter="url(#glow)"/>

<g text-anchor="middle">
  <text x="{VX}" y="118" class="name g1" fill="#00f0ff">ALEXANDRE MENDES</text>
  <text x="{VX}" y="118" class="name g2" fill="#ff2bd6">ALEXANDRE MENDES</text>
  <text x="{VX}" y="118" class="name" fill="url(#nameg)" filter="url(#glow)">ALEXANDRE MENDES</text>
  <text x="{VX}" y="156" class="tag">BACKEND · DISTRIBUTED SYSTEMS · PLATFORM</text>
</g>

<g fill="none" stroke="#00f0ff" stroke-width="2" opacity=".8">
  <path d="M24 54 V24 H54"/><path d="M{W - 54} 24 H{W - 24} V54"/>
  <path d="M24 {H - 54} V{H - 24} H54"/><path d="M{W - 54} {H - 24} H{W - 24} V{H - 54}"/>
</g>
<text x="40" y="46" class="hud">SYS://AEMENDES <tspan class="dim">v2026.10</tspan></text>
<circle cx="318" cy="41" r="4" fill="#4ade80" class="blink"/><text x="330" y="46" class="hud" style="fill:#4ade80">ONLINE</text>
<text x="{W - 40}" y="46" class="hud" text-anchor="end">41.15°N  8.61°W <tspan class="dim">// PORTO.PT</tspan></text>
<text x="40" y="{H - 34}" class="hud dim">&gt; uplink established_</text>
<text x="{W - 40}" y="{H - 34}" class="hud dim" text-anchor="end">UPTIME ∞ · LATENCY 0ms</text>

<rect width="{W}" height="{H}" fill="url(#scan)"/>
</svg>
"""

# -------------------------------------------------------------- terminal
C = {"k": "#7dd3fc", "v": "#f0abfc", "s": "#fde68a", "c": "#64748b", "p": "#4ade80", "t": "#e2e8f0", "x": "#a78bfa"}

# each line: list of (color, text)
L = [
    [("p", "❯ "), ("t", "kubectl get engineer alexandre -o yaml")],
    [("k", "apiVersion"), ("t", ": "), ("v", "humans.aemendes.dev/v1")],
    [("k", "kind"), ("t", ": "), ("v", "SoftwareEngineer")],
    [("k", "metadata"), ("t", ":")],
    [("t", "  "), ("k", "name"), ("t", ": "), ("v", "alexandre-mendes")],
    [("t", "  "), ("k", "namespace"), ("t", ": "), ("v", "porto-pt")],
    [("t", "  "), ("k", "labels"), ("t", ": { "), ("k", "role"), ("t", ": "), ("v", "backend"), ("t", ", "), ("k", "domain"), ("t", ": "), ("v", "betting"), ("t", " }")],
    [("k", "spec"), ("t", ":")],
    [("t", "  "), ("k", "education"), ("t", ": "), ("s", '"MSc Artificial Intelligence @ ISEP"')],
    [("t", "  "), ("k", "thesis"), ("t", ":    "), ("s", '"Forecasting Bitcoin from Twitter sentiment"')],
    [("t", "  "), ("k", "stack"), ("t", ":")],
    [("t", "    "), ("k", "streaming"), ("t", ": ["), ("v", "java, spring-boot, flink, kafka, grpc, protobuf"), ("t", "]")],
    [("t", "    "), ("k", "platform"), ("t", ":  ["), ("v", "go, kubernetes, crossplane, argocd, ansible"), ("t", "]")],
    [("t", "    "), ("k", "web"), ("t", ":       ["), ("v", "typescript, next.js, react, bun, postgres"), ("t", "]")],
    [("t", "    "), ("k", "onchain"), ("t", ":   ["), ("v", "rust, solidity, hypersync, parquet"), ("t", "]")],
    [("t", "  "), ("k", "sideQuests"), ("t", ":")],
    [("t", "    - "), ("s", "native crossplane providers for my gitops homelab")],
    [("t", "    - "), ("s", "on-chain intelligence, wallet clustering & MEV")],
    [("t", "    - "), ("s", "teaching a model to hear what a metal detector hears")],
    [("k", "status"), ("t", ":")],
    [("t", "  "), ("k", "phase"), ("t", ": "), ("p", "Shipping"), ("c", "   # ☕ fuelled, 🚀 deploying")],
    [("t", "  "), ("k", "conditions"), ("t", ": [{ "), ("k", "type"), ("t", ": "), ("v", "OpenToCollaborate"), ("t", ", "), ("k", "status"), ("t", ": "), ("s", '"True"'), ("t", " }]")],
    [("p", "❯ "), ("t", "▍")],
]

TW, LH, TOP = 900, 23, 76
TH = TOP + len(L) * LH + 24
rows = []
for i, line in enumerate(L):
    spans = "".join(f'<tspan fill="{C[c]}">{escape(t)}</tspan>' for c, t in line)
    cls = "ln cur" if i == len(L) - 1 else "ln"
    rows.append(f'<text x="34" y="{TOP + i * LH}" class="{cls}" style="animation-delay:{0.3 + i * 0.11:.2f}s">{spans}</text>')

terminal = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">
<defs>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#00f0ff"/><stop offset="1" stop-color="#ff2bd6"/></linearGradient>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0820"/><stop offset="1" stop-color="#05030f"/></linearGradient>
</defs>
<style>
  .ln {{ font: 500 15px {MONO}; white-space: pre; animation: in .25s ease-out both; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateX(-8px) }} to {{ opacity: 1; transform: none }} }}
  .cur tspan:last-child {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0 }} }}
  .ttl {{ font: 600 13px {MONO}; fill: #94a3b8; letter-spacing: 1px; }}
</style>
<rect x="2" y="2" width="{TW - 4}" height="{TH - 4}" rx="14" fill="url(#bg)" stroke="url(#bd)" stroke-width="2"/>
<path d="M2 46 H{TW - 2}" stroke="#1e1b4b"/>
<circle cx="28" cy="24" r="6" fill="#ff5f57"/><circle cx="48" cy="24" r="6" fill="#febc2e"/><circle cx="68" cy="24" r="6" fill="#28c840"/>
<text x="{TW / 2}" y="29" text-anchor="middle" class="ttl">alexandre@porto — ~/whoami — zsh</text>
<g xml:space="preserve">{''.join(rows)}</g>
</svg>
"""

# ---------------------------------------------------------------- footer
FW, FH = 1200, 140
wave = " ".join(f"{x},{70 + (18 if x % 80 == 40 else -18 if x % 80 == 0 else 0)}" for x in range(0, FW + 1, 20))
footer = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{FW}" height="{FH}" viewBox="0 0 {FW} {FH}">
<defs>
  <linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="#00f0ff" stop-opacity="0"/><stop offset=".5" stop-color="#a855f7"/><stop offset="1" stop-color="#ff2bd6" stop-opacity="0"/></linearGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
  .w {{ stroke-dasharray: 60 1400; animation: run 3.5s linear infinite; }}
  @keyframes run {{ to {{ stroke-dashoffset: -1460 }} }}
  .t {{ font: 600 14px {MONO}; fill: #a78bfa; letter-spacing: 6px; }}
  .blink {{ animation: blink 1.2s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0 }} }}
</style>
<polyline points="{wave}" fill="none" stroke="url(#fl)" stroke-width="1.5" opacity=".35"/>
<polyline points="{wave}" fill="none" stroke="#00f0ff" stroke-width="2.5" class="w" filter="url(#glow)"/>
<text x="{FW / 2}" y="122" text-anchor="middle" class="t">[ END OF TRANSMISSION ]  SIGNAL STAYS OPEN<tspan class="blink">_</tspan></text>
</svg>
"""

for name, svg in [("header.svg", header), ("terminal.svg", terminal), ("footer.svg", footer)]:
    with open(f"{OUT}/{name}", "w") as f:
        f.write(svg)
