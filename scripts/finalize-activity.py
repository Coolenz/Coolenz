"""Add accessible descriptions and reduced-motion handling to generated SVGs."""
from pathlib import Path
import re
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

for relative in (
    'profile-3d-contrib/activity-dark.svg',
    'profile-3d-contrib/activity-light.svg',
    'assets/contribution-trace-dark.svg',
    'assets/contribution-trace-light.svg',
):
    path = ROOT / relative
    content = path.read_text(encoding='utf-8')
    trace = 'trace' in path.name
    title = "Coolenz's public contribution trace" if trace else "Coolenz's public contribution skyline"
    description = (
        'An animated path through the GitHub contribution calendar. Updated daily by GitHub Actions.'
        if trace else
        'A three-dimensional view of the GitHub contribution calendar, public language mix and activity. Updated daily by GitHub Actions.'
    )
    accessible = f'<title>{escape(title)}</title><desc>{escape(description)}</desc>'
    reduced_motion = '<style>@media(prefers-reduced-motion:reduce){svg *{animation:none!important;transition:none!important}}</style>'
    content = content.replace(accessible, '').replace(reduced_motion, '')
    if not trace:
        colors = {'#f34b7d': '#4de0ed', '#3572A5': '#4b8dbd', '#444444': '#345267'} if 'dark' in path.name else {'#f34b7d': '#087c94', '#3572A5': '#4b8dbd', '#444444': '#a5c4d3'}
        for original, replacement in colors.items():
            content = content.replace(original, replacement)
    content = re.sub(r'(<svg\b[^>]*>)', lambda match: match[1] + accessible + reduced_motion, content, count=1)
    path.write_text(content, encoding='utf-8', newline=chr(10))
    print(f'Finalized {relative}')
