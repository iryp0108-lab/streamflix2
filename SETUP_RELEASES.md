# Releases y auto-actualización (iryp0108-lab/streamflix2)

El *in-app updater* ya quedó apuntando a **este** repo
(`InAppUpdater.kt`: `GITHUB_OWNER="iryp0108-lab"`, `GITHUB_REPO="streamflix2"`).
El workflow `.github/workflows/release.yml` compila, firma y publica el APK como
*release* al empujar un tag `vX.Y.Z`. La app, al abrir, ve el release nuevo aquí y
ofrece actualizar.

## 1. Secrets (una sola vez)

En **Settings → Secrets and variables → Actions → New repository secret** del repo
`streamflix2`, crea:

| Secret | Valor |
|--------|-------|
| `KEYSTORE` | el contenido de `xptv-keystore.p12.base64` (el que te entregué) |
| `SIGNING_KEY_ALIAS` | `xptv` |
| `SIGNING_STORE_PASSWORD` | `xptv-sign` |
| `SIGNING_KEY_PASSWORD` | `xptv-sign` |
| `TMDB_API_KEY` | tu API key de TMDB (gratis en themoviedb.org → Settings → API → v3) |
| `RABBITSTREAM_SOURCE_API` | opcional; déjalo vacío si no lo usas |

> **TMDB es necesario**: sin esa key la app no muestra el catálogo principal
> (películas/series vía TMDB). Es gratis y tarda 2 minutos sacarla.

> **Firma estable**: firma SIEMPRE con este mismo keystore. Si lo cambias, las
> actualizaciones dejarán de instalarse encima (Android exige misma firma).

## 2. Publicar una versión

1. Sube tus mejoras a `main`.
2. Sube el número de versión en `app/build.gradle` (`versionCode` y `versionName`,
   p.ej. `versionName "1.7.72"`).
3. Crea y empuja un tag con la **misma** versión y prefijo `v`:
   ```
   git tag v1.7.72
   git push origin v1.7.72
   ```
4. El Action compila 3 APKs (universal, solo-móvil, solo-TV), los firma con tu
   keystore y los publica en el release `v1.7.72`.
5. La app instalada (con `versionName` menor) detecta el release y ofrece actualizar.

## Notas

- Esta es la base **StreamFlix Reborn** (paquete `com.streamflixreborn.streamflix`),
  limpia y sin el control remoto de usuarios de markbn15. Es una app distinta del
  APK parcheado de "Xuper TV" que te pasé antes (otro paquete y otra firma): se
  instala aparte. El auto-update encadena entre versiones de ESTA app.
- Si quieres el nombre/icono "Xuper TV", se cambian como edición propia (recursos
  en `app/src/main/res`) y se re-compila igual.
- El build corre en GitHub Actions (tiene Android SDK y red); no necesitas compilar
  en tu PC.
