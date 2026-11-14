# sobreviver-ia

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![sobreviver-ia](guia/assets/banner-es.jpg)](https://inematds.github.io/sobreviver-ia/guia/es/)

## Qué es

sobreviver-ia es un conjunto de herramientas simples, que corren en tu computadora, para atravesar los próximos dos años de IA con menos sobresaltos. Sirve para cualquier persona o familia: calcula la comida, el agua y el dinero de un kit de 14 días, instala una IA y la Wikipedia offline, muestra qué cuentas todavía dependen del SMS y mide, con tareas de tu propio trabajo, cuánto hace ya la IA por ti. Solo necesita Python 3 (y, si quieres la IA offline, espacio en disco). Nada usa clave de API.

## 📖 Guía de uso

Guía completa (landing + paso a paso, con datos y gráficos): **https://inematds.github.io/sobreviver-ia/guia/es/**

🎬 Video: https://www.youtube.com/shorts/bgVHDEm1yGI

## Tres horizontes de riesgo

| Horizonte | Riesgo | Herramienta |
|---|---|---|
| Corto plazo | seguridad física y digital | `kit/`, `offline/`, `seguranca/` |
| Mediano plazo (2 años) | trabajo e ingresos | `eval/`, `plano/` semanas 1–8 |
| Largo plazo | creencias e identidad | `plano/` semanas 9–13 |

Por qué ahora (hechos de 2026):
- **19%** — el empleo de personas de 22 a 25 años en las funciones más expuestas a la IA está cerca de un 19% por debajo de donde estaría si siguiera a las funciones menos expuestas. Es una brecha acumulada (13% → 15% → 19% en las versiones del estudio), vía contratación. Stanford Digital Economy Lab, "Canaries in the Coal Mine", ago/2026.
- **350+** — supermercados en Francia tuvieron sus refrigeradores calentados hasta ~50 °C por un ataque a controladores conectados a internet con contraseñas débiles (11/10/2026, Reuters; otras fuentes hablan de 500–700).
- **Jul/2026** — modelos de IA en prueba de seguridad escaparon del sandbox e invadieron parte de Hugging Face.

## Herramientas

| Archivo | Qué hace |
|---|---|
| `kit/calcula_kit.py` | personas × días → calorías (2.000 kcal/persona/día), agua (1,5–2 L/persona/día), bidones, dinero de 1 mes, lista de no perecederos; texto o checklist en markdown |
| `kit/checklist-casa.md` (en portugués) | comida, agua, dinero, primeros auxilios, extintor, linterna, radio, power bank, personas |
| `offline/instala-offline.sh` | Ollama + modelo pequeño + Kiwix + Wikipedia (pt/en/es; mini/nopic/maxi). **Dry-run por defecto** |
| `seguranca/checklist-mfa.md` (en portugués) | salir del SMS: orden de prioridad y paso a paso por cuenta |
| `seguranca/auditoria_contas.py` | CSV o modo interactivo de tus cuentas → informe de lo que conviene migrar primero |
| `eval/` | tu eval personal: `tarefas/NN-nome/{tarefa.md,contexto/,criterio.md}` + 3 ejemplos |
| `eval/rodar.py` | genera el paquete para pegar en Claude Code/Codex/el chat al que estás suscrito, o corre en Ollama local (`--ollama`). Nunca llama a una API paga |
| `eval/placar.py` | registra la nota por modelo y fecha y dibuja la evolución (SVG; PNG si hay matplotlib) |
| `plano/plano-90-dias.md` (en portugués) | ownership, distribución, mundo físico, identidad, creencias, personas — con ejercicios |

Las herramientas muestran la salida en portugués.

## Empezar

```bash
git clone https://github.com/inematds/sobreviver-ia && cd sobreviver-ia

python3 kit/calcula_kit.py --pessoas 2 --dias 14 --gasto-mensal 4500
bash offline/instala-offline.sh --modelo llama3.2:3b --wiki pt --tipo nopic     # dry-run
python3 seguranca/auditoria_contas.py --modelo contas.csv
python3 eval/rodar.py --modelo meu-modelo        # o: --ollama qwen2.5:7b
python3 eval/placar.py grafico
python3 -m pytest -q                              # pruebas
```

Windows: consulta la sección "Instala la IA y la Wikipedia offline" en la [guía](https://inematds.github.io/sobreviver-ia/guia/es/#guia).

## Licencia

MIT — consulta [LICENSE](LICENSE). Versión 1.0.0. Parte del ecosistema [INEMA.CLUB](https://inema.club).
