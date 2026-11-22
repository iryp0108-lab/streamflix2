# Pablito's TV — compilar y publicar (método principal)

El APK se genera con el workflow **`.github/workflows/build-pablito.yml`**, que:
1. Clona la fuente **más reciente** de StreamFlix Reborn desde **git.gay**
   (`https://git.gay/streamflix-reborn2/streamflix.git`) — extractores y listas al día.
2. Le aplica la marca **Pablito's TV** (icono, splash, nombre, versión) con
   `ci/apply_branding.py` e intenta repuntar el updater a este repo.
3. Compila, firma con tu keystore y publica el APK como *release*.

> El proyecto se movió de GitHub a git.gay tras un DMCA. Por eso NO se compila el
> código congelado de este fork, sino el upstream vivo. Así los extractores (voe,
> etc.) se mantienen al día solos cada vez que corres el workflow.

## Secrets (una sola vez)

En **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Valor |
|--------|-------|
| `KEYSTORE` | contenido de `xptv-keystore.p12.base64` |
| `SIGNING_KEY_ALIAS` | `xptv` |
| `SIGNING_STORE_PASSWORD` | `xptv-sign` |
| `SIGNING_KEY_PASSWORD` | `xptv-sign` |
| `TMDB_API_KEY` | tu API key de TMDB (themoviedb.org → Settings → API → v3) — **obligatoria** |
| `RABBITSTREAM_SOURCE_API` | opcional |

## Compilar una versión

1. Ve a **Actions → "Pablito's TV (upstream al día)" → Run workflow**.
2. En *Versión* pon el tag (ej. `v1.7.252`, o la versión actual que veas en git.gay).
3. **Run workflow**. En ~5–10 min el release tendrá el/los APK (`PablitosTV-*.apk`).

Para actualizar más adelante: vuelve a correr el workflow (baja lo último del
upstream) con un tag mayor. Firma siempre con el mismo keystore para que las
actualizaciones se instalen encima.
