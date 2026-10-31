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

for theme in ('dark', 'light'):
    dark = theme == 'dark'
    bg, panel, ink, muted, trace, cyan = (
        ('#081521', '#0d2132', '#edfaff', '#9ab9cd', '#244a60', '#4de0ed') if dark else
        ('#edf6fb', '#e1eff7', '#12344a', '#41657a', '#aecbdc', '#087c94')
    )
    routes = [
        'M822 125H768Q750 125 750 107V96H690', 'M822 193H696',
        'M822 261H770Q748 261 748 283V310H690',
        'M1140 125H1170Q1188 125 1188 107V96H1224', 'M1140 193H1224',
        'M1140 261H1170Q1188 261 1188 283V310H1224',
    ]
    hero = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 420" fill="none" role="img" aria-labelledby="title desc">
<title id="title">Coolen — software meets the physical world</title>
<desc id="desc">Embedded systems, robotics and edge AI. The Coloop mark sits inside a processor connected by cyan signal traces.</desc>
<defs><clipPath id="frame"><rect width="1280" height="420" rx="18"/></clipPath></defs>
<style>.signal{{stroke-dasharray:18 330;animation:signal 8s linear infinite}}@keyframes signal{{to{{stroke-dashoffset:-348}}}}@media(prefers-reduced-motion:reduce){{.signal{{animation:none}}}}</style>
<g clip-path="url(#frame)"><path fill="{bg}" d="M0 0h1280v420H0z"/>
{mono('coolenz@workbench:~',56,58,18,muted)}
{lettering('Coolen',56,200,100,ink)}
{lettering('Embedded systems + robotics.',61,251,24,muted)}
{lettering('Edge AI, closer to the device.',61,289,24,muted)}
<path d="M56 356H1224" stroke="{trace}"/>
{mono('github.com/Coolenz',61,391,16,muted)}
<rect x="840" y="78" width="280" height="264" rx="22" fill="{panel}" stroke="{trace}" stroke-width="2"/>
<rect x="857" y="95" width="246" height="230" rx="14" stroke="{cyan}" stroke-opacity=".35"/>
'''
    for y in (125, 159, 193, 227, 261, 295):
        hero += f'<path d="M822 {y}H840M1120 {y}H1140" stroke="{muted}" stroke-width="4" stroke-linecap="round"/>'
    for x in (884, 932, 980, 1028, 1076):
        hero += f'<path d="M{x} 60V78M{x} 342V356" stroke="{muted}" stroke-width="4" stroke-linecap="round"/>'
    for route in routes:
        hero += f'<path d="{route}" stroke="{trace}" stroke-width="2"/><path class="signal" d="{route}" stroke="{cyan}" stroke-width="2"/>'
    for x,y in ((690,96),(696,193),(690,310),(1224,96),(1224,193),(1224,310)):
        hero += f'<circle cx="{x}" cy="{y}" r="4" fill="{cyan}"/>'
    hero += f'<g transform="translate(885 115) scale(1.48)">{mark.replace("#FFFFFF",ink)}</g>'
    hero += mono('Coloop / in development',840,391,15,muted) + '</g></svg>'
    (ROOT / f'assets/hero-{theme}.svg').write_text(hero, encoding='utf-8')

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
    (ROOT / f'assets/loop-{theme}.svg').write_text(loop, encoding='utf-8')

print('Built theme-aware processor hero and Coloop architecture SVGs.')
