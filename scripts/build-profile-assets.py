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

for theme in ['dark', 'light']:
    dark = theme == 'dark'
    bg, fg, muted, line = ('#202124','#f8f8f6','#b7b9bd','#45464a') if dark else ('#f8f8f6','#202124','#55585e','#d4d5d8')
    hero = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 420" fill="none" role="img" aria-labelledby="title desc">
<title id="title">Coolen</title><desc id="desc">Embedded systems, robotics and edge AI. Coloop's paired arcs with a slow orbital animation.</desc>
<defs>
 <linearGradient id="silver" x1="20" y1="25" x2="105" y2="100" gradientUnits="userSpaceOnUse">
  <stop stop-color="#ffffff"/><stop offset=".28" stop-color="#c4c7cc"/><stop offset=".48" stop-color="#ffffff"/><stop offset=".63" stop-color="#71757c"/><stop offset=".83" stop-color="#e0e2e5"/><stop offset="1" stop-color="#969ba2"/>
 </linearGradient>
 <clipPath id="frame"><rect width="1280" height="420" rx="18"/></clipPath>
</defs>
<style>
 .orbit {{ transform-origin:960px 210px; animation:orbit 36s linear infinite; }}
 @keyframes orbit {{ to {{ transform:rotate(360deg); }} }}
 @media (prefers-reduced-motion:reduce) {{ .orbit {{ animation:none; }} }}
</style>
<g clip-path="url(#frame)">
 <path fill="{bg}" d="M0 0h1280v420H0z"/>
 <path stroke="{line}" d="M56 350H1224"/>
 {lettering('Coolen',56,208,108,fg)}
 {lettering('Software meets',61,254,24,muted)}
 {lettering('the physical world.',61,288,24,muted)}
 {lettering('EMBEDDED / ROBOTICS / EDGE AI',61,386,13,muted)}
 <g stroke="{line}">
  <ellipse cx="960" cy="210" rx="247" ry="105" transform="rotate(-28 960 210)"/>
  <ellipse cx="960" cy="210" rx="208" ry="160" transform="rotate(24 960 210)"/>
  <path d="M690 210h22m496 0h22M960 24v18m0 336v18"/>
 </g>
 <g class="orbit">
  <circle cx="960" cy="210" r="182" stroke="{line}" stroke-dasharray="2 12"/>
  <path d="M960 28a182 182 0 0 1 157.6 91" stroke="{muted}" stroke-width="1.5"/>
  <circle cx="1117.6" cy="119" r="4" fill="{fg}"/>
  <circle cx="802.4" cy="301" r="3" fill="{muted}"/>
 </g>
 <g transform="translate(800 50) scale(2.5)">
  <g transform="rotate(-35 64 64)" fill="url(#silver)" fill-rule="evenodd">
   <path transform="translate(1.8 0)" d="{arc}"/>
   <path transform="translate(126.2 0) scale(-1 1)" d="{arc}"/>
  </g>
 </g>
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

print('Built restored orbital hero and Coloop architecture SVGs.')
