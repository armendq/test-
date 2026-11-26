"""Prepare a self-contained episode folder without changing the source tree.

Usage: python engine/prepare.py whereitgoes 7 /tmp/wig07
"""
from pathlib import Path
import argparse
import shutil


def prepare(series, episode, destination):
    root = Path(__file__).resolve().parents[1]
    target = Path(destination).resolve()
    target.mkdir(parents=True, exist_ok=True)
    files = {root / 'engine' / name: name for name in ('lib.py', 'make.py', 'edit.py')}
    files.update({root / series / f'ep{episode:02}' / name: name for name in ('scenes.py', 'audio.py')})
    if series == 'whereitgoes':
        files[root / series / 'ep02/scenes.py'] = 'base2.py'
        files[root / series / 'kit/kit.py'] = 'kit.py'
    else:
        files[root / series / 'base.py'] = 'base.py'
        files[root / series / 'ep02/scenes.py'] = 'ep2.py'
        files[root / series / 'ep05/scenes.py'] = 'ep5.py'
        files.update({p: p.name for p in (root / series / 'kit').glob('*.py')})
    for source, name in files.items():
        shutil.copy2(source, target / name)
    print(target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('series', choices=('whereitgoes', 'nightbus'))
    parser.add_argument('episode', type=int)
    parser.add_argument('destination')
    args = parser.parse_args()
    prepare(args.series, args.episode, args.destination)
