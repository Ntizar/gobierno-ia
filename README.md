# Gobierno IA — Prototipo

Simulación multiagente del gobierno de España orientada a un objetivo: **simplificar la legislación española** (más corta, limpia y usable, sin perder eficacia).

## Estructura

```
constitution/          Constitución y reglas del juego
ministerios/
  hacienda/
    competencias.md    Qué puede tocar este ministerio
    leyes/             Bloques normativos (markdown, versionado con git)
    propuestas/        Propuestas diarias de cada ministro (YYYY-MM-DD.md)
  sanidad/             idem
  transicion-ecologica/ idem
presidencia/
  protocolo.md         Cómo preside el Consejo y redacta el informe
  informes/            Informe diario del presidente (YYYY-MM-DD.md)
consejo/
  actas/               Actas del Consejo de Ministros (YYYY-MM-DD.md)
```

## Reglas anti-invención

1. Toda propuesta debe citar **fichero y artículo exacto** del bloque que modifica. Sin referencia → propuesta rechazada en Consejo.
2. Los ministros solo leen/escriben en su carpeta. Nadie toca leyes ajenas.
3. Los cambios se aplican como diff de git, nunca reescribiendo de la nada.
4. El informe del presidente tiene máximo 2 páginas.

## Ciclo diario

- **Mañana**: cada ministro lee noticias de su área y revisa su bloque → deja propuestas en `ministerios/<nombre>/propuestas/`.
- **22:00 — Consejo de Ministros**: 3 rondas (exposición → réplica → decisión presidencial). Salen acuerdos concretos y diffs.
- **08:00 siguiente día — Informe presidencial** en Telegram: lo importante, qué se simplificó, qué está atascado, enlaces.

---
Hecho con ❤️ por David Antizar
