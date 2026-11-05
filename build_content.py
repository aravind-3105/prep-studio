"""Build portable lesson data from the original revision Markdown, without dependencies."""
from pathlib import Path
import html, json, re, shutil
root = Path(__file__).resolve().parent

def inline(s):
    parts = re.split(r'(`[^`]+`)', s)
    out = ''
    for p in parts:
        if p.startswith('`'):
            out += '<code>' + html.escape(p[1:-1]) + '</code>'
        else:
            p = html.escape(p)
            p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p)
            p = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', p)
            out += p
    return out

def render(md):
    lines = md.splitlines(); out = []; i = 0
    while i < len(lines):
        s = lines[i]
        if not s.strip(): i += 1; continue
        if s.startswith('```'):
            code=[]; i+=1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i+=1
            out.append('<div class="code-label">PYTHON</div><pre><code>'+html.escape('\n'.join(code))+'</code></pre>'); i+=1
        elif s.startswith('|'):
            rows=[]
            while i < len(lines) and lines[i].startswith('|'):
                row=lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'[\s:\-]+', c) for c in row): rows.append(row)
                i+=1
            out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+inline(c.strip())+'</th>' for c in rows[0])+'</tr></thead><tbody>')
            for row in rows[1:]: out.append('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in row)+'</tr>')
            out.append('</tbody></table></div>')
        elif s.startswith('- '):
            out.append('<ul>')
            while i < len(lines) and lines[i].startswith('- '):
                out.append('<li>'+inline(lines[i][2:])+'</li>'); i+=1
            out.append('</ul>')
        elif s.startswith('#'):
            out.append('<h3>'+inline(s.lstrip('# '))+'</h3>'); i+=1
        else:
            p=[s]; i+=1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(('-', '#', '|', '```')):
                p.append(lines[i]); i+=1
            cls=' class="callout"' if re.match(r'\*\*(Trap|Critical trap|Critical traps|Cost)', s) else ''
            out.append('<p'+cls+'>'+inline(' '.join(p))+'</p>')
    return '\n'.join(out)

def lessons_from(path, prefix, minutes, track):
    sections=re.split(r'^## ', path.read_text(), flags=re.M)[1:]
    out=[]
    for idx, sec in enumerate(sections):
        title, body=sec.split('\n',1)
        title=re.sub(r'^\d+\. ', '',title)
        out.append({
            'id': f'{prefix}{idx+1}' if prefix else str(idx+1),
            'title': title,
            'html': render(body),
            'text': body,
            'minutes': minutes[idx],
            'track': track,
            'num': idx+1,
        })
    return out

lessons = lessons_from(root/'content/python-notes.md', '', [8,8,10,6,12,10,14,12,10,5,7,6,3], 'python')
lessons += lessons_from(root/'content/interview-notes.md', 'i', [10,8,12,8,8,12,12,8,5,3], 'interview')
(root/'dist/content.js').write_text('const LESSONS = '+json.dumps(lessons)+';\nconst SCHEDULE = '+json.dumps(render((root/'content/schedule.md').read_text()))+';\n')
shutil.copy(root/'content/python-notes.md',root/'dist/python-notes.md')
shutil.copy(root/'content/interview-notes.md',root/'dist/interview-notes.md')
shutil.copy(root/'content/schedule.md',root/'dist/schedule.md')
print(f'Built {len(lessons)} lesson sections.')
