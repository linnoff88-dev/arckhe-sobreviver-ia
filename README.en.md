# sobreviver-ia

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![sobreviver-ia](guia/assets/banner-en.jpg)](https://inematds.github.io/sobreviver-ia/guia/en/)

## What it is

sobreviver-ia is a set of simple tools that run on your own computer, to get through the next two years of AI with fewer surprises. It is for any person or family: it works out the food, water and cash for a 14-day kit, installs an AI and Wikipedia offline, shows which of your accounts still depend on SMS and measures, with tasks from your own work, how much AI already does for you. All you need is Python 3 (and, if you want the offline AI, disk space). Nothing uses an API key.

The tools print their output in Portuguese.

## 📖 User guide

Full guide (landing + step by step, with data and charts): **https://inematds.github.io/sobreviver-ia/guia/en/**

🎬 Video: https://www.youtube.com/shorts/bgVHDEm1yGI

## Three risk horizons

| Horizon | Risk | Tool |
|---|---|---|
| Short term | physical and digital security | `kit/`, `offline/`, `seguranca/` |
| Medium term (2 years) | work and income | `eval/`, `plano/` weeks 1–8 |
| Long term | beliefs and identity | `plano/` weeks 9–13 |

Why now (2026 facts):
- **19%** — employment of 22- to 25-year-olds in the roles most exposed to AI is about 19% below where it would be if it had tracked the less exposed roles. It is a cumulative gap (13% → 15% → 19% across versions of the study), driven by hiring. Stanford Digital Economy Lab, "Canaries in the Coal Mine", Aug 2026.
- **350+** — supermarkets in France had their fridges heated up to ~50 °C by an attack on internet-connected controllers with weak passwords (Oct 11, 2026, Reuters; other sources say 500–700).
- **Jul 2026** — AI models under safety testing escaped the sandbox and broke into part of Hugging Face.

## Tools

| File | What it does |
|---|---|
| `kit/calcula_kit.py` | people × days → calories (2,000 kcal/person/day), water (1.5–2 L/person/day), jugs, 1 month of cash, list of non-perishables; text or markdown checklist |
| `kit/checklist-casa.md` | food, water, cash, first aid, fire extinguisher, flashlight, radio, power bank, people (in Portuguese) |
| `offline/instala-offline.sh` | Ollama + small model + Kiwix + Wikipedia (pt/en/es; mini/nopic/maxi). **Dry-run by default** |
| `seguranca/checklist-mfa.md` | getting off SMS: priority order and step by step per account (in Portuguese) |
| `seguranca/auditoria_contas.py` | CSV or interactive mode for your accounts → report of what to migrate first |
| `eval/` | your personal eval: `tarefas/NN-nome/{tarefa.md,contexto/,criterio.md}` + 3 examples (in Portuguese) |
| `eval/rodar.py` | generates the package to paste into the Claude Code/Codex/chat you subscribe to, or runs on local Ollama (`--ollama`). Never calls a paid API |
| `eval/placar.py` | records the score per model and date and draws the trend (SVG; PNG if matplotlib is installed) |
| `plano/plano-90-dias.md` | ownership, distribution, physical world, identity, beliefs, people — with exercises (in Portuguese) |

## Get started

```bash
git clone https://github.com/inematds/sobreviver-ia && cd sobreviver-ia

python3 kit/calcula_kit.py --pessoas 2 --dias 14 --gasto-mensal 4500
bash offline/instala-offline.sh --modelo llama3.2:3b --wiki pt --tipo nopic     # dry-run
python3 seguranca/auditoria_contas.py --modelo contas.csv
python3 eval/rodar.py --modelo meu-modelo        # or: --ollama qwen2.5:7b
python3 eval/placar.py grafico
python3 -m pytest -q                              # tests
```

Windows: see the "Install the AI and Wikipedia offline" section in the [guide](https://inematds.github.io/sobreviver-ia/guia/en/#guia).

## License

MIT — see [LICENSE](LICENSE). Version 1.0.0. Part of the [INEMA.CLUB](https://inema.club) ecosystem.
