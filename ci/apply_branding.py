#!/usr/bin/env python3
"""
apply_branding.py  <upstream_dir>  <branding_res_dir>  <version>

Aplica la marca "Pablito's TV" sobre un árbol de fuente de StreamFlix Reborn
recién clonado (de git.gay). Lo usa el workflow build-pablito.yml, que clona el
upstream al día en el runner de GitHub (que sí tiene internet) y luego llama a
este script con los assets de marca que viven en este repo (streamflix2).

Qué hace:
  - copia icono (launcher, round, foreground, banner) y splash a mismas rutas res
  - pone app_name = Pablito's TV en todos los idiomas
  - ajusta colores de fondo adaptativo
  - fija versionName/versionCode en app/build.gradle
  - (best-effort) repunta el in-app updater a iryp0108-lab/streamflix2
  - (best-effort) corrige la URL DoH de OpenDNS si está mal

Falla con mensaje claro si no encuentra strings.xml o build.gradle (señal de que
la estructura del upstream cambió y hay que ajustar el script).
"""
import sys, os, re, glob, shutil

if len(sys.argv) != 4:
    print(__doc__); sys.exit(2)
UP, BR, VERSION = sys.argv[1], sys.argv[2], sys.argv[3]
VERSION = VERSION.lstrip('v')
APP_NAME = "Pablito\\'s TV"

up_res = os.path.join(UP, 'app/src/main/res')
if not os.path.isdir(up_res):
    sys.exit('ERROR: no existe %s (estructura del upstream distinta)' % up_res)

# 1) assets de icono / splash (copiar misma ruta relativa)
assets = []
for dpi in ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi'):
    for n in ('ic_launcher.png', 'ic_launcher_round.png', 'ic_launcher_foreground.png'):
        assets.append('mipmap-%s/%s' % (dpi, n))
assets += ['mipmap-xhdpi/ic_banner.png', 'mipmap-xhdpi/ic_banner_foreground.png',
           'drawable/bg_splash_screen.xml', 'drawable-nodpi/splash_logo.png']
copied = 0
for rel in assets:
    src = os.path.join(BR, rel)
    if os.path.exists(src):
        dst = os.path.join(up_res, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst); copied += 1
print('assets copiados:', copied)

# 2) app_name en cada strings.xml
found = 0
for f in glob.glob(os.path.join(up_res, 'values*/strings.xml')):
    s = open(f, encoding='utf-8').read()
    if '<string name="app_name">' not in s:
        continue
    found += 1
    s2 = re.sub(r'(<string name="app_name">).*?(</string>)', r'\g<1>' + APP_NAME + r'\g<2>', s, count=1)
    if s2 != s:
        open(f, 'w', encoding='utf-8').write(s2)
if found == 0:
    sys.exit('ERROR: no se encontró app_name en ningún strings.xml')
print('app_name fijado en', found, 'archivo(s)')

# 3) colores de fondo adaptativo -> tono del degradado
colors = os.path.join(up_res, 'values/colors.xml')
if os.path.exists(colors):
    s = open(colors, encoding='utf-8').read()
    s = re.sub(r'(<color name="ic_launcher_background">)#[0-9A-Fa-f]{6,8}(</color>)', r'\g<1>#C435B1\g<2>', s)
    s = re.sub(r'(<color name="ic_banner_background">)#[0-9A-Fa-f]{6,8}(</color>)', r'\g<1>#C435B1\g<2>', s)
    open(colors, 'w', encoding='utf-8').write(s)
    print('colores de fondo ajustados')

# 4) version en app/build.gradle
bg = os.path.join(UP, 'app/build.gradle')
if not os.path.exists(bg):
    bg = os.path.join(UP, 'app/build.gradle.kts')
if not os.path.exists(bg):
    sys.exit('ERROR: no se encontró app/build.gradle(.kts)')
parts = re.findall(r'\d+', VERSION)[:3]
while len(parts) < 3:
    parts.append('0')
vcode = int(parts[0]) * 100000 + int(parts[1]) * 1000 + int(parts[2])
s = open(bg, encoding='utf-8').read()
s = re.sub(r'versionName\s+"[^"]*"', 'versionName "%s"' % VERSION, s, count=1)
s = re.sub(r'versionName\s*=\s*"[^"]*"', 'versionName = "%s"' % VERSION, s, count=1)
s = re.sub(r'versionCode\s+\d+', 'versionCode %d' % vcode, s, count=1)
s = re.sub(r'versionCode\s*=\s*\d+', 'versionCode = %d' % vcode, s, count=1)
open(bg, 'w', encoding='utf-8').write(s)
print('version fijada: name=%s code=%d' % (VERSION, vcode))

# 5) repuntar in-app updater (best-effort; el upstream pudo moverlo a git.gay)
upd = glob.glob(os.path.join(UP, 'app/src/main/java/**/InAppUpdater.kt'), recursive=True)
patched = False
for f in upd:
    s = open(f, encoding='utf-8').read(); o = s
    s = re.sub(r'(GITHUB_OWNER\s*=\s*)"[^"]*"', r'\1"iryp0108-lab"', s)
    s = re.sub(r'(GITHUB_REPO\s*=\s*)"[^"]*"', r'\1"streamflix2"', s)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); patched = True
print('updater repuntado a iryp0108-lab/streamflix2' if patched
      else 'AVISO: no se pudo repuntar el updater (el upstream cambió su updater); '
           'actualiza re-corriendo el Action')

# 6) fix DoH OpenDNS (best-effort)
doh = os.path.join(up_res, 'values/doh_resources.xml')
if os.path.exists(doh):
    s = open(doh, encoding='utf-8').read()
    s2 = s.replace('https://doh/opendns.com/dns-query', 'https://doh.opendns.com/dns-query')
    if s2 != s:
        open(doh, 'w', encoding='utf-8').write(s2); print('fix DoH OpenDNS aplicado')

print('OK: marca Pablito\'s TV aplicada sobre el upstream')
