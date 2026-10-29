#!/usr/bin/env python3
# todo review this neiro-slop
"""Record how a file changes while you solve, as diffs inside one zip.

    python watch.py <file>              # e.g. python watch.py cf_2300_C.py ; Ctrl-C to stop; run again to resume

History lives in .history/<file name>.zip next to this script, one entry per change, named
<YYYY-MM-DDTHH-MM-SS>.diff (unified diff).  On start the whole file is written as a diff against an empty
file, unless the file can be restored exactly from the entries already in the zip; then nothing is
written.  After that an entry is appended every 10 seconds, always: the diff if the file changed, a
headers-only diff if it did not.  So the number of entries times 10 seconds is the time spent, across
all sessions, and the diffs show when the edits happened.  The file must exist when you start.
"""
import sys, os, re, time, difflib, datetime, zipfile, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
INTERVAL = 10

def stamp():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

def apply_unified(old, diff):
    """Apply a unified diff (list of lines) produced by this tool to `old` (list of lines)."""
    out, i, k = [], 0, 0
    while k < len(diff):
        m = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', diff[k])
        if not m:
            k += 1
            continue
        a = int(m.group(1)); b = int(m.group(2)) if m.group(2) is not None else 1
        start = a - 1 if b > 0 else a            # with ",0" the number is the line after which to insert
        out.extend(old[i:start]); i = start
        k += 1
        while k < len(diff) and not diff[k].startswith('@@'):
            t = diff[k]
            if t.startswith('+'): out.append(t[1:])
            elif t.startswith('-'): i += 1
            elif t.startswith(' '): out.append(old[i]); i += 1
            k += 1
    out.extend(old[i:])
    return out

def entries(zip_path):
    if not os.path.exists(zip_path):
        return []
    with zipfile.ZipFile(zip_path) as zf:
        return sorted(n for n in zf.namelist() if n.endswith('.diff'))

def rebuild(zip_path):
    lines = []
    with zipfile.ZipFile(zip_path) as zf:
        for name in entries(zip_path):
            diff = zf.read(name).decode('utf-8').splitlines()
            if diff and diff[0].startswith('--- ') and diff[0].endswith('@ empty'):
                lines = []                       # a whole-file diff restarts the state
            lines = apply_unified(lines, diff)
    return lines

def append_entry(zip_path, name, text):
    """Append one entry; the zip is updated through a temporary copy so an interrupted write cannot damage it."""
    tmp = zip_path + '.tmp'
    if os.path.exists(zip_path):
        shutil.copy(zip_path, tmp)
    with zipfile.ZipFile(tmp, 'a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(name, text)
    os.replace(tmp, zip_path)

def read_lines(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read().splitlines()

def main():
    if len(sys.argv) != 2:
        sys.exit('usage: python watch.py <file>')
    path = os.path.abspath(sys.argv[1])
    if not os.path.isfile(path):
        sys.exit(f'ERROR: no such file: {path}')
    name = os.path.basename(path)
    os.makedirs(os.path.join(ROOT, '.history'), exist_ok=True)
    zip_path = os.path.join(ROOT, '.history', name + '.zip')
    existing = entries(zip_path)
    restored = None
    if existing:
        try:
            restored = rebuild(zip_path)
        except Exception as e:
            print(f'could not rebuild from {zip_path} ({e})')
    print(f'watching {path}\n{len(existing)} diffs in {zip_path}, checking every {INTERVAL} s, Ctrl-C to stop', flush=True)
    written = 0
    last, last_stamp = [], 'empty'               # start from empty: the first record() writes the whole file ...
    if restored is not None and restored == read_lines(path):
        last, last_stamp = restored, existing[-1][:-5]    # ... unless the file is exactly what the zip restores
        print('  file matches the history, nothing written at start', flush=True)
    first_write_pending = not existing            # empty history: the first record() always writes, even for an empty file

    def record(tick):
        """Append an entry: the diff if the file changed; on a tick, a headers-only diff even if it did not."""
        nonlocal last, last_stamp, written, first_write_pending
        if not os.path.exists(path):
            return
        cur = read_lines(path)
        changed = cur != last
        if not changed and not tick and not first_write_pending:
            return
        first_write_pending = False
        now = stamp()
        diff = list(difflib.unified_diff(last, cur, fromfile=f'{name} @ {last_stamp}', tofile=f'{name} @ {now}', lineterm='', n=3))
        if not diff:                             # no change (a timer tick) or an empty file at the start: headers only
            diff = [f'--- {name} @ {last_stamp}', f'+++ {name} @ {now}']
        entry = now + '.diff'
        if entry in entries(zip_path):           # two entries inside one second: keep both
            entry = now + f'-{int(time.time() * 1000) % 1000:03d}.diff'
        append_entry(zip_path, entry, '\n'.join(diff) + '\n')
        last, last_stamp, written = cur, now, written + 1
        if changed:
            print(f'  {now}  {len(cur):>4} lines  {entry}', flush=True)
        elif written % 6 == 0:                   # a quiet heartbeat once a minute
            total = len(existing) + written
            print(f'  {now}  no change, {total} entries = {total * INTERVAL // 60} min total', flush=True)

    try:
        record(tick=False)                       # the start: whole file, or nothing if the zip restores it
        while True:
            time.sleep(INTERVAL)
            record(tick=True)
    except KeyboardInterrupt:
        record(tick=False)                       # do not lose the last edits
        total = len(existing) + written
        print(f'\nstopped, {written} entries this run, {total} in total = about {total * INTERVAL // 60} min {total * INTERVAL % 60} s on this file', flush=True)
        sys.exit(0)

if __name__ == '__main__':
    main()
