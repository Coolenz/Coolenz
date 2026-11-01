"""Build repository-hosted artwork; the profile itself remains native Markdown."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parent.parent
font = instantiateVariableFont(TTFont(ROOT / 'assets/Sora-Variable.ttf'), {'wght': 550})
glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
units = font['head'].unitsPerEm
mark = re.search(r'<g\b.*?</g>', (ROOT / 'assets/coloop.svg').read_text(encoding='utf-8'), re.S).group()

def lettering(text, x, y, size, fill):
    cursor, paths = 0, []
    for char in text:
        name = cmap[ord(char)]
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        if pen.getCommands():
            paths.append(f'<path transform="translate({cursor} 0)" d="{pen.getCommands()}"/>')
        cursor += glyphs[name].width
    return f'<g fill="{fill}" transform="translate({x} {y}) scale({size/units} {-size/units})">' + ''.join(paths) + '</g>'

def mono(text, x, y, size, color):
    return f'<text x="{x}" y="{y}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="{size}" fill="{color}">{escape(text)}</text>'

arc = 'M51.588 24.138A41.75 41.75 0 0 0 51.588 103.862C54.8 104.9 56.65 102.5 56.65 99.2V28.8C56.65 25.5 54.8 23.1 51.588 24.138Z M47.9 36.056A32.25 32.25 0 0 0 47.9 91.944Q49.35 92.73 49.35 91.08V36.92Q49.35 35.27 47.9 36.056Z'


def orbital_tracks(fg, muted, line):
    """A small, script-free constellation, compatible with SVG-as-image rendering."""
    tracks = []
    # Normalized path lengths keep the star and its fading wake on the same orbit.
    for name, seconds, phase, reverse, width in (
        ('near', 26, .18, False, 2.4),
        ('far', 39, .64, True, 1.8),
        ('polar', 54, .84, False, 1.35),
    ):
        direction = 'reverse' if reverse else 'normal'
        def moving(dash, stroke, thickness, alpha, lag=0):
            delay = -seconds * phase + (-1 if reverse else 1) * seconds * lag / 1000
            return (f'<use href="#{name}" class="drift" stroke="{stroke}" stroke-width="{thickness}" '
                    f'stroke-opacity="{alpha}" stroke-linecap="round" stroke-dasharray="{dash}" '
                    f'style="--still:{(1 if reverse else -1) * (phase * 1000 - lag)};animation-duration:{seconds}s;animation-delay:{delay:.4f}s;animation-direction:{direction}"/>')
        body = f'<use href="#{name}" stroke="{line}" stroke-width=".8"/>'
        # Twelve short contiguous segments form a genuinely tapering, fading tail.
        for segment in range(12, 0, -1):
            alpha = round(.06 + .76 * (1 - segment / 13) ** 1.4, 3)
            body += moving('5 995', fg, round(width * (.35 + .65 * (1 - segment / 13)), 2), alpha, segment * 5)
        body += moving('0.01 999.99', fg, 11, .045)
        body += moving('0.01 999.99', fg, 6.5, .16)
        body += moving('0.01 999.99', fg, 4.3 if name == 'near' else 3.3, .95)
        if name == 'far':
            # A quieter companion on the same distant orbit.
            body += moving('0.01 999.99', muted, 2, .7, 480)
        tracks.append((name, body))
    background = ''.join(f'<g class="track-{name}">{body}</g>' for name, body in tracks)
    # The lower sweep crosses in front of the mark; upper sweeps pass behind it.
    foreground = f'<g clip-path="url(#front-pass)">{tracks[0][1]}</g>'
    stars = ''
    points = [(726,97,1),(780,51,.9),(851,35,1.2),(1026,43,.8),(1146,65,1),
              (1195,120,.8),(1210,269,1),(1155,314,1.2),(1084,327,.8),
              (791,320,1),(718,279,.9),(739,169,.65),(1115,106,.7),(1164,228,.65)]
    for i,(x,y,r) in enumerate(points):
        stars += (f'<circle class="twinkle" cx="{x}" cy="{y}" r="{r}" fill="{muted}" opacity=".4" '
                  f'style="animation-duration:{6+i%5}s;animation-delay:-{i*.73:.2f}s"/>')
    # Two restrained four-point stars give the field a deliberate constellation accent.
    for x,y,delay in [(781,96,1.3),(1167,291,4.6)]:
        stars += (f'<path class="twinkle" d="M{x-4} {y}Q{x} {y} {x} {y-4}Q{x} {y} {x+4} {y}'
                  f'Q{x} {y} {x} {y+4}Q{x} {y} {x-4} {y}Z" fill="{fg}" opacity=".5" '
                  f'style="animation-duration:7.6s;animation-delay:-{delay}s"/>')
    return stars + background, foreground

for theme in ['dark', 'light']:
    dark = theme == 'dark'
    bg, fg, muted, line = ('#202124','#f8f8f6','#b7b9bd','#45464a') if dark else ('#f8f8f6','#202124','#55585e','#d4d5d8')
    stars, front_stars = orbital_tracks(fg, muted, line)
    hero = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 420" fill="none" role="img" aria-labelledby="title desc">
<title id="title">Coolen</title><desc id="desc">Embedded systems, robotics and edge AI. Coloop's silver paired arcs surrounded by layered orbital star trails and a gently twinkling constellation.</desc>
<defs>
 <linearGradient id="silver" x1="20" y1="25" x2="105" y2="100" gradientUnits="userSpaceOnUse">
  <stop stop-color="#ffffff"/><stop offset=".28" stop-color="#c4c7cc"/><stop offset=".48" stop-color="#ffffff"/><stop offset=".63" stop-color="#71757c"/><stop offset=".83" stop-color="#e0e2e5"/><stop offset="1" stop-color="#969ba2"/>
 </linearGradient>
 <ellipse id="near" cx="960" cy="210" rx="247" ry="105" transform="rotate(-28 960 210)" pathLength="1000"/>
 <ellipse id="far" cx="960" cy="210" rx="208" ry="160" transform="rotate(24 960 210)" pathLength="1000"/>
 <circle id="polar" cx="960" cy="210" r="182" pathLength="1000"/>
 <linearGradient id="field-fade" x1="0" y1="18" x2="0" y2="344" gradientUnits="userSpaceOnUse">
  <stop stop-color="#ffffff" stop-opacity="0"/><stop offset=".1" stop-color="#ffffff"/>
  <stop offset=".88" stop-color="#ffffff"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
 </linearGradient>
 <mask id="field-mask" maskUnits="userSpaceOnUse" x="682" y="18" width="552" height="326"><path d="M682 18H1234V344H682Z" fill="url(#field-fade)"/></mask>
 <clipPath id="front-pass"><path d="M690 210H1230V344H690Z"/></clipPath>
 <clipPath id="star-field"><path d="M682 18H1234V344H682Z"/></clipPath>
 <clipPath id="frame"><rect width="1280" height="420" rx="18"/></clipPath>
</defs>
<style>
 .drift {{ animation:drift 26s linear infinite; }}
 .twinkle {{ animation:twinkle 7s ease-in-out infinite; }}
 .orbital-grid {{ transform-origin:960px 210px; animation:revolve 90s linear infinite; }}
 @keyframes drift {{ to {{ stroke-dashoffset:-1000; }} }}
 @keyframes revolve {{ to {{ transform:rotate(360deg); }} }}
 @keyframes twinkle {{ 0%,100% {{ opacity:.22; }} 50% {{ opacity:.78; }} }}
 @media (prefers-reduced-motion:reduce) {{ .drift,.twinkle,.orbital-grid {{ animation:none; }} .drift {{ stroke-dashoffset:var(--still); }} }}
</style>
<g clip-path="url(#frame)">
 <path fill="{bg}" d="M0 0h1280v420H0z"/>
 <path stroke="{line}" d="M56 350H1224"/>
 {lettering('Coolen',56,208,108,fg)}
 {lettering('Software meets',61,254,24,muted)}
 {lettering('the physical world.',61,288,24,muted)}
 {lettering('EMBEDDED / ROBOTICS / EDGE AI',61,386,13,muted)}
 <g clip-path="url(#star-field)" mask="url(#field-mask)">
  <circle class="orbital-grid" cx="960" cy="210" r="182" stroke="{line}" stroke-width=".8" stroke-dasharray="1 11" opacity=".7"/>
  {stars}
 </g>
 <g transform="translate(800 50) scale(2.5)">
  <g transform="rotate(-35 64 64)" fill="url(#silver)" fill-rule="evenodd">
   <path transform="translate(1.8 0)" d="{arc}"/>
   <path transform="translate(126.2 0) scale(-1 1)" d="{arc}"/>
  </g>
 </g>
 <g clip-path="url(#star-field)" mask="url(#field-mask)">{front_stars}</g>
 {lettering('COOLENZ / GITHUB',1032,386,13,muted)}
</g></svg>'''
    (ROOT / f'assets/hero-{theme}.svg').write_text(hero, encoding='utf-8', newline='\n')


for theme in ('dark', 'light'):
    dark = theme == 'dark'
    bg, panel, ink, muted, trace, cyan = (
        ('#081521', '#0d2132', '#edfaff', '#9ab9cd', '#244a60', '#4de0ed') if dark else
        ('#edf6fb', '#e1eff7', '#12344a', '#41657a', '#aecbdc', '#087c94')
    )
    loop = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 196" fill="none" role="img" aria-labelledby="title desc">
<title id="title">Coloop feedback loop</title><desc id="desc">Observe screen context, plan a task, act through a device, and verify the result. A concept in development.</desc>
<rect width="1280" height="196" rx="12" fill="{bg}"/>
{mono('Coloop / feedback loop',40,35,15,muted)}
{mono('concept in development',974,35,13,muted)}
'''
    for label, sub, x in [('Observe','screen context',72),('Plan','task plan',382),('Act','device action',692),('Verify','result check',1002)]:
        loop += f'<rect x="{x}" y="68" width="36" height="36" rx="8" stroke="{cyan}"/><circle cx="{x+18}" cy="86" r="4" fill="{cyan}"/>'
        loop += lettering(label,x+53,96,26,ink) + mono(sub,x+54,125,14,muted)
        if x < 1000:
            loop += f'<path d="M{x+204} 86h60m-7-6 7 6-7 6" stroke="{trace}" stroke-width="2"/>'
    loop += f'<path d="M1190 142v24H90v-24m-6 7 6-7 6 7" stroke="{trace}" stroke-width="2"/>'
    loop += mono('feedback',603,186,12,muted) + '</svg>'
    (ROOT / f'assets/loop-{theme}.svg').write_text(loop, encoding='utf-8', newline='\n')

print('Built layered orbital star trails and Coloop architecture SVGs.')
