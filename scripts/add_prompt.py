#!/usr/bin/env python3
import argparse, pathlib, subprocess, sys
root = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='Save a manually copied prompt into prompts/<slug>.txt')
parser.add_argument('slug', help='post slug, e.g. synex')
parser.add_argument('--from-clipboard', action='store_true', help='read prompt from macOS clipboard')
parser.add_argument('--text', help='prompt text')
args = parser.parse_args()
if args.from_clipboard:
    text = subprocess.check_output(['pbpaste'], text=True)
elif args.text:
    text = args.text
else:
    text = sys.stdin.read()
if not text.strip():
    raise SystemExit('No prompt text provided')
path = root / 'prompts' / f'{args.slug}.txt'
path.write_text(text.strip() + '\n', encoding='utf-8')
print(path)
subprocess.check_call([sys.executable, str(root / 'scripts' / 'build_prompts_json.py')])
