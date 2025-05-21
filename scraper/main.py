import logging, os, re, json, markdown, time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from weasyprint import HTML

from scraper.utils.retry import retry_on_failure

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', '/tmp/exports'))

def create_dirs():
    date_dir = datetime.now().strftime('%Y-%m-%d')
    base = OUTPUT_DIR / date_dir
    for plat in ['chatgpt', 'claude']:
        for fmt in ['json', 'markdown', 'pdf']:
            (base / plat / fmt).mkdir(parents=True, exist_ok=True)
    return base

@retry_on_failure()
def dummy_extract(name):
    # Placeholder extractor
    return [{
        'title': f'Sample {name} conversation',
        'messages': [
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'content': 'Hi there!'}
        ]
    }]

def md_to_pdf(md_txt, out_path):
    html = markdown.markdown(md_txt, extensions=['extra'])
    HTML(string=f'<html><body>{html}</body></html>').write_pdf(out_path)

def save(conv, base, plat):
    title = re.sub(r'[^\w\-]', '_', conv['title'])[:50]
    ts = datetime.now().strftime('%H%M%S')
    fn = f'{title}_{ts}'
    json_path = base/plat/'json'/f'{fn}.json'
    md_path   = base/plat/'markdown'/f'{fn}.md'
    pdf_path  = base/plat/'pdf'/f'{fn}.pdf'
    json_path.write_text(json.dumps(conv, indent=2))
    md_body = f"# {conv['title']}\n\n" + "\n\n".join(
        f"## {m['role'].capitalize()}\n\n{m['content']}" for m in conv['messages'])
    md_path.write_text(md_body)
    md_to_pdf(md_body, pdf_path)

def run_once():
    base = create_dirs()
    for plat in ['chatgpt', 'claude']:
        for conv in dummy_extract(plat):
            save(conv, base, plat)
    log.info('Completed one-shot export')

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--once', action='store_true')
    args = p.parse_args()
    if args.once:
        run_once()
    else:
        run_once()
