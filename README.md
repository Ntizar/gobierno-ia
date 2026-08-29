# Gobierno IA 🇪🇸

**Simulación multiagente de un gobierno de España creado con IA, cuyo objetivo es un Estado al máximo de simple: legislación eficaz, corta y clara, y el dinero donde hay problemas medidos.**

> ⚠️ Proyecto de experimentación. Los "ministros" son agentes de IA con personalidad inspirada en los ministros reales (Arcadi España, Mónica García, Sara Aagesen) pero **no** son ellos ni representan al Gobierno de España. Los textos legales son reales (BOE); las propuestas, ficticias.

## Cómo funciona

Cada día, automáticamente:

1. **10:00 — Pase de lista**: cada ministro lee las noticias de su área, revisa su ley insignia real del BOE y propone simplificaciones **frase por frase** con justificación, más una **reasignación presupuestaria** (dónde está el dinero, qué problema medido hay, a dónde debería ir).
2. **22:00 — Consejo de Ministros**: 3 rondas (exposición → réplica cruzada → decisión presidencial). Salen acuerdos: APROBADO / APLAZADO / RECHADO.
3. **23:30 — Auditoría del Estado**: un auditor independiente valida o rechaza cada acuerdo y los KPIs de los ministros, y señala los 3 mayores riesgos no atendidos.
4. **08:00 — Informe presidencial**: máximo 2 páginas con lo importante, lo simplificado, los KPIs de cada ministro (quién acierta y quién falla) y los riesgos del Estado.

## El equipo

| Agente | Perfil | Cartera |
|---|---|---|
| 🏛️ Presidente | Mastermind (orquestador) | Coordina, arbitra, informa |
| 💼 Ministro de Hacienda | `ministro-hacienda` — Arcadi España (IA) | Ley 58/2003 General Tributaria |
| 🏥 Ministra de Sanidad | `ministro-sanidad` — Mónica García (IA) | Ley 14/1986 General de Sanidad |
| 🌱 Ministra de Transición Ecológica | `ministro-ecologia` — Sara Aagesen (IA) | Ley 7/2021 de Cambio Climático |
| 🔍 Auditor del Estado | `auditor` | Fiscaliza todo, no propone nada |

## Las leyes que mejoran

Texto consolidado real descargado de la [API de Legislación Consolidada del BOE](https://www.boe.es/datosabiertos/):

- [`ministerios/hacienda/leyes/BOE-A-2003-23186.md`](ministerios/hacienda/leyes/BOE-A-2003-23186.md) — Ley 58/2003, General Tributaria
- [`ministerios/sanidad/leyes/BOE-A-1986-10499.md`](ministerios/sanidad/leyes/BOE-A-1986-10499.md) — Ley 14/1986, General de Sanidad
- [`ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md`](ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md) — Ley 7/2021, de Cambio Climático y Transición Ecológica

Regla de oro: **toda propuesta debe citar el bloque exacto de la ley real en el repo**. Sin cita verificable → rechazada. Los cambios se aplican como diffs de git, auditables por cualquiera.

## KPIs

Cada ministro gestiona su cuadro de mando evolutivo en `ministerios/<nombre>/kpis.md` (histórico diario + lecciones). El Auditor los audita. Ejemplo: [`ministerios/hacienda/kpis.md`](ministerios/hacienda/kpis.md).

## Estructura

```
constitution/    Reglas del juego (constitución, protocolos)
ministerios/     Leyes BOE reales, propuestas diarias y KPIs por ministerio
consejo/actas/   Acta diaria del Consejo de Ministros
auditoria/       Veredictos del Auditor del Estado
presidencia/     Informes presidenciales diarios
docs/            Boletín público (GitHub Pages)
```

## Ver el boletín diario

👉 **https://ntizar.github.io/gobierno-ia/**

---
Hecho con ❤️ por David Antizar · Mastermind es el ejecutor, David el autor
