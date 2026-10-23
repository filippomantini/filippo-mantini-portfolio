from pathlib import Path
import re
R=Path(__file__).resolve().parents[2]
for lang in ['', 'it/']:
 p=R/f'public/{lang}work/collapse/index.html'
 if not p.exists():continue
 s=p.read_text();prefix='/it' if lang else ''
 pattern=r'<details class="cp-archive-item cp-archive-details" data-category="events"><summary>(?:(?!</details>).)*?<strong class="cp-card-title">CHAOS AS DUALITY</strong>(?:(?!</details>).)*?</details>'
 match=re.search(pattern,s)
 if not match:continue
 body=match.group();body=re.sub(r'^<details.*?<summary>','',body);body=re.sub(r'</summary>.*$','',body);body=body.replace('>+</span>','>↗</span>')
 replacement=f'<a class="cp-archive-item" data-category="events" href="{prefix}/work/chaos-as-duality/" aria-label="Chaos as Duality">{body}</a>'
 p.write_text(s[:match.start()]+replacement+s[match.end():])
