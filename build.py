"""Rebuild lesson data and the single-file offline edition."""
from pathlib import Path
import runpy
root = Path(__file__).resolve().parent
runpy.run_path(str(root / 'build_content.py'))
dist = root / 'dist'
page = (dist / 'index.html').read_text()
page = page.replace('<link rel="stylesheet" href="style.css">', '<style>' + (dist / 'style.css').read_text() + '</style>')
page = page.replace('<script defer src="content.js"></script><script defer src="app.js"></script>', '')
scripts = ''.join('<script>' + (dist / name).read_text().replace('</script', '<\\/script') + '</script>' for name in ['content.js', 'app.js'])
(dist / 'Prep Studio.html').write_text(page.replace('</body>', scripts + '</body>'))
print('Built the single-file offline edition.')
