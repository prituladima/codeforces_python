#!/usr/bin/env python3
"""Record how a file changes while you solve, as a folder of diffs.

    python watcher.py <file>              # e.g. python watcher.py cf_2300_C.py ; Ctrl-C to stop; run again to resume

On start the whole file is written as a diff against an empty file, unless the file can be restored
exactly from the diffs already in .history/<file name>/; then nothing is written.  After that, every
10 seconds the file is compared with the last recorded state and, if it changed, the unified diff is
written to .history/<file name>/<YYYY-MM-DDTHH-MM-SS>.diff next to this script.  Unchanged: no file.
"""
import sys, os, re, time, difflib, datetime

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

def rebuild(folder):
    lines = []
    for name in sorted(f for f in os.listdir(folder) if f.endswith('.diff')):
        with open(os.path.join(folder, name), encoding='utf-8') as f:
            diff = f.read().splitlines()
        if diff and diff[0].startswith('--- ') and diff[0].endswith('@ empty'):
            lines = []                           # a whole-file diff restarts the state
        lines = apply_unified(lines, diff)
    return lines

def read_lines(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read().splitlines()

def main():
    if len(sys.argv) != 2:
        sys.exit('usage: python watcher.py <file>')
    path = os.path.abspath(sys.argv[1])
    if not os.path.isfile(path):
        sys.exit(f'ERROR: no such file: {path}')
    name = os.path.basename(path)
    folder = os.path.join(ROOT, '.history', name)
    os.makedirs(folder, exist_ok=True)
    existing = sorted(f for f in os.listdir(folder) if f.endswith('.diff'))
    restored = None
    if existing:
        try:
            restored = rebuild(folder)
        except Exception as e:
            print(f'could not rebuild from {folder} ({e})')
    print(f'watching {path}\n{len(existing)} diffs in {folder}, checking every {INTERVAL} s, Ctrl-C to stop', flush=True)
    written = 0
    last, last_stamp = [], 'empty'               # start from empty: the first record() writes the whole file ...
    if restored is not None and os.path.exists(path) and restored == read_lines(path):
        last, last_stamp = restored, existing[-1][:-5]    # ... unless the file is exactly what the diffs restore
        print('  file matches the history, nothing written at start', flush=True)
    first_write_pending = not existing            # empty history: the first record() always writes, even for an empty file

    def record():
        nonlocal last, last_stamp, written, first_write_pending
        if not os.path.exists(path):
            return
        cur = read_lines(path)
        if cur == last and not first_write_pending:
            return
        first_write_pending = False
        now = stamp()
        diff = list(difflib.unified_diff(last, cur, fromfile=f'{name} @ {last_stamp}', tofile=f'{name} @ {now}', lineterm='', n=3))
        if not diff:                             # an empty file at the very start: headers only, so the start is on record
            diff = [f'--- {name} @ {last_stamp}', f'+++ {name} @ {now}']
        out = os.path.join(folder, now + '.diff')
        if os.path.exists(out):                  # two changes inside one second: keep both
            out = os.path.join(folder, now + f'-{int(time.time() * 1000) % 1000:03d}.diff')
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(diff) + '\n')
        last, last_stamp, written = cur, now, written + 1
        print(f'  {now}  {len(cur):>4} lines  {os.path.basename(out)}', flush=True)

    try:
        while True:
            record()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        record()                                 # do not lose the last edits
        print(f'\nstopped, {written} diff(s) written this run', flush=True)
        sys.exit(0)

if __name__ == '__main__':
    main()
