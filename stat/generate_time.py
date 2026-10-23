#!/usr/bin/env python3
"""Minutes-per-attempt chart from "Competitive programming.xlsx" (first sheet).

Usage:  python generate_time.py CF_div2 C        ->  times_for_CF_div2_C.png

Columns used: A contest name (filled on the first row of a group), B date, C type (CF_div2, CF_div3,
AtCoder_Beg, ...), D problem letter, F rating (EMPTY = unsolved, minutes are time spent so far),
G hours, H minutes, I seconds.  Nothing else is read; nothing is fetched from the internet.
"""
import sys, os, datetime, math
from openpyxl import load_workbook

HANDLE = 'prituladima'
GATE_MIN = 45            # pass = solved in GATE_MIN minutes or less
WINDOW, NEED = 12, 9     # promote when NEED of the last WINDOW problems passed

def load_rows(path, typ, letter):
    ws = load_workbook(path, data_only=True).worksheets[0]
    rows, contest = [], ''
    for r in ws.iter_rows(values_only=True):
        if r[0]:
            contest = str(r[0])
        if r[2] != typ or not str(r[3] or '').startswith(letter):
            continue
        if not isinstance(r[1], datetime.datetime):
            continue
        minutes = (r[6] or 0) * 60 + (r[7] or 0) + (r[8] or 0) / 60
        if minutes <= 0:
            continue
        rating = r[5]
        rows.append(dict(date=r[1].strftime('%Y-%m-%d'), contest=contest, problem=str(r[3]),
                         rating=int(rating) if rating else None, solved=rating is not None,
                         minutes=minutes))
    return rows

def short(contest):
    c = (contest.replace('Educational Codeforces Round ', 'Edu ')
                .replace('Codeforces Round ', 'R')
                .replace('AtCoder Beginner Contest ', 'ABC '))
    c = c.split(' (')[0]
    return c if len(c) <= 14 else c[:13] + '…'

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def build_svg(rows, typ, letter):
    W, H = 1200, 660
    PX0, PX1, PY0, PY1 = 70, 1160, 96, 520
    YMAX = max(150, int(math.ceil(max(x['minutes'] for x in rows) / 30.0) * 30))
    n = len(rows)
    slot = (PX1 - PX0) / n
    X = lambda i: PX0 + (i + 0.5) * slot
    Y = lambda m: PY1 - m / YMAX * (PY1 - PY0)
    SANS = 'font-family="Liberation Sans, Arial, sans-serif"'
    last = rows[-WINDOW:]
    passed = sum(1 for x in last if x['solved'] and x['minutes'] <= GATE_MIN)
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
         f'<rect width="{W}" height="{H}" fill="#fcfcfb"/>',
         f'<text x="70" y="36" {SANS} font-size="18" font-weight="bold" fill="#0b0b0b">{esc(typ)} {esc(letter)}: minutes per attempt</text>',
         f'<text x="70" y="56" {SANS} font-size="12" fill="#52514e">{HANDLE} · {n} attempts, {rows[0]["date"]} to {rows[-1]["date"]} · rating as logged · empty rating = unsolved so far</text>',
         f'<text x="{PX1}" y="80" {SANS} font-size="12" font-weight="bold" fill="#52514e" text-anchor="end">Gate: {passed} of last {len(last)} passed (unaided, {GATE_MIN} min or less), promote at {NEED} of {WINDOW}</text>',
         f'<circle cx="{PX0 + 6}" cy="76" r="5" fill="#2a78d6"/>',
         f'<text x="{PX0 + 16}" y="80" {SANS} font-size="12" fill="#52514e">solved, minutes to accept</text>',
         f'<rect x="{PX0 + 226}" y="70" width="11" height="11" fill="#fcfcfb" stroke="#eb6834" stroke-width="2.5"/>',
         f'<text x="{PX0 + 243}" y="80" {SANS} font-size="12" fill="#52514e">unsolved so far, minutes spent</text>']
    for v in range(0, YMAX + 1, 30):
        y = Y(v)
        col = '#c3c2b7' if v == 0 else '#e1e0d9'
        s.append(f'<line x1="{PX0}" x2="{PX1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="1"/>')
        s.append(f'<text x="{PX0 - 8}" y="{y + 4:.1f}" {SANS} font-size="11" fill="#52514e" text-anchor="end">{v}</text>')
    yg = Y(GATE_MIN)
    s.append(f'<line x1="{PX0}" x2="{PX1}" y1="{yg:.1f}" y2="{yg:.1f}" stroke="#52514e" stroke-width="1.5" stroke-dasharray="6 5"/>')
    s.append(f'<text x="{PX1}" y="{yg - 6:.1f}" {SANS} font-size="11" fill="#52514e" text-anchor="end">{GATE_MIN}-minute gate</text>')
    pts = ' '.join(f'{X(i):.1f},{Y(x["minutes"]):.1f}' for i, x in enumerate(rows))
    s.append(f'<polyline points="{pts}" fill="none" stroke="#2a78d6" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, x in enumerate(rows):
        cx, cy, m = X(i), Y(x['minutes']), round(x['minutes'])
        if x['solved']:
            s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" fill="#2a78d6" stroke="#fcfcfb" stroke-width="2"/>')
            ly = cy + 20 if x['minutes'] < GATE_MIN else cy - 13
            s.append(f'<text x="{cx:.1f}" y="{ly:.1f}" {SANS} font-size="13" font-weight="bold" fill="#0b0b0b" text-anchor="middle">{m}</text>')
        else:
            s.append(f'<rect x="{cx - 6:.1f}" y="{cy - 6:.1f}" width="12" height="12" fill="#fcfcfb" stroke="#eb6834" stroke-width="2.5"/>')
            s.append(f'<text x="{cx:.1f}" y="{cy - 13:.1f}" {SANS} font-size="13" font-weight="bold" fill="#0b0b0b" text-anchor="middle">{m}+</text>')
        s.append(f'<text x="{cx:.1f}" y="{PY1 + 26}" {SANS} font-size="13" font-weight="bold" fill="#0b0b0b" text-anchor="middle">{i + 1}</text>')
        s.append(f'<text x="{cx:.1f}" y="{PY1 + 42}" {SANS} font-size="11" fill="#898781" text-anchor="middle">{esc(short(x["contest"]))} {esc(x["problem"])}</text>')
        s.append(f'<text x="{cx:.1f}" y="{PY1 + 56}" {SANS} font-size="11" fill="#898781" text-anchor="middle">{x["rating"] if x["rating"] else "—"}</text>')
    i = 0
    while i < n:
        j = i
        while j + 1 < n and rows[j + 1]['date'] == rows[i]['date']:
            j += 1
        x0, x1, yb = X(i) - slot / 2 + 8, X(j) + slot / 2 - 8, PY1 + 72
        s.append(f'<polyline points="{x0:.1f},{yb} {x0:.1f},{yb + 6} {x1:.1f},{yb + 6} {x1:.1f},{yb}" fill="none" stroke="#c3c2b7" stroke-width="1"/>')
        s.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{yb + 22}" {SANS} font-size="11" fill="#52514e" text-anchor="middle">{rows[i]["date"]}</text>')
        i = j + 1
    s.append('</svg>')
    return '\n'.join(s)

def main():
    if len(sys.argv) != 3:
        sys.exit('usage: python generate_time.py <type> <letter>   e.g.  python generate_time.py CF_div2 C')
    typ, letter = sys.argv[1], sys.argv[2]
    here = os.path.dirname(os.path.abspath(__file__))
    xlsx = os.path.join(here, 'Competitive programming.xlsx')
    rows = load_rows(xlsx, typ, letter)
    if not rows:
        sys.exit(f'no rows of type {typ} with problem {letter} in {xlsx}')
    svg = build_svg(rows, typ, letter)
    base = os.path.join(here, f'times_for_{typ}_{letter}')
    try:
        import cairosvg
    except ImportError:
        with open(base + '.svg', 'w', encoding='utf-8') as f:
            f.write(svg)
        sys.exit(f'cairosvg not installed (conda env cf-stat): wrote {base}.svg only')
    cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to=base + '.png', output_width=2400)
    print(f'{len(rows)} attempts -> {base}.png')

if __name__ == '__main__':
    main()
