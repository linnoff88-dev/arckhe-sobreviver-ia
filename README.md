# sobreviver-ia

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

[![sobreviver-ia](guia/assets/banner.jpg)](https://inematds.github.io/sobreviver-ia/guia/)

## O que Ã©

O sobreviver-ia Ã© um conjunto de ferramentas simples, que rodam no seu computador, para atravessar os prÃ³ximos dois anos de IA com menos susto. Ele serve para qualquer pessoa ou famÃ­lia: calcula a comida, a Ã¡gua e o dinheiro de um kit de 14 dias, instala uma IA e a Wikipedia offline, mostra quais contas ainda dependem de SMS e mede, com tarefas do seu prÃ³prio trabalho, quanto a IA jÃ¡ faz por vocÃª. Precisa sÃ³ de Python 3 (e, se quiser a IA offline, de espaÃ§o em disco). Nada usa chave de API.

## ðŸ“– Guia de uso

Guia completo (landing + passo a passo, com dados e grÃ¡ficos): **https://inematds.github.io/sobreviver-ia/guia/**

ðŸŽ¬ VÃ­deo: https://www.youtube.com/shorts/bgVHDEm1yGI

## TrÃªs horizontes de risco

| Horizonte | Risco | Ferramenta |
|---|---|---|
| Curto prazo | seguranÃ§a fÃ­sica e digital | `kit/`, `offline/`, `seguranca/` |
| MÃ©dio prazo (2 anos) | trabalho e renda | `eval/`, `plano/` semanas 1â€“8 |
| Longo prazo | crenÃ§as e identidade | `plano/` semanas 9â€“13 |

Por que agora (fatos de 2026):
- **19%** â€” o emprego de 22 a 25 anos nas funÃ§Ãµes mais expostas Ã  IA estÃ¡ cerca de 19% abaixo de onde estaria se acompanhasse as funÃ§Ãµes menos expostas. Ã‰ um gap acumulado (13% â†’ 15% â†’ 19% nas versÃµes do estudo), via contrataÃ§Ã£o. Stanford Digital Economy Lab, "Canaries in the Coal Mine", ago/2026.
- **350+** â€” supermercados na FranÃ§a tiveram as geladeiras aquecidas atÃ© ~50 Â°C por ataque a controladores ligados Ã  internet com senha fraca (11/10/2026, Reuters; outras fontes falam em 500â€“700).
- **Jul/2026** â€” modelos de IA em teste de seguranÃ§a escaparam do sandbox e invadiram parte da Hugging Face.

## Ferramentas

| Arquivo | O que faz |
|---|---|
| `kit/calcula_kit.py` | pessoas Ã— dias â†’ calorias (2.000 kcal/pessoa/dia), Ã¡gua (1,5â€“2 L/pessoa/dia), galÃµes, dinheiro de 1 mÃªs, lista de nÃ£o perecÃ­veis; texto ou checklist markdown |
| `kit/checklist-casa.md` | comida, Ã¡gua, dinheiro, primeiros socorros, extintor, lanterna, rÃ¡dio, power bank, pessoas |
| `offline/instala-offline.sh` | Ollama + modelo pequeno + Kiwix + Wikipedia (pt/en/es; mini/nopic/maxi). **Dry-run por padrÃ£o** |
| `seguranca/checklist-mfa.md` | sair do SMS: ordem de prioridade e passo a passo por conta |
| `seguranca/auditoria_contas.py` | CSV ou modo interativo das suas contas â†’ relatÃ³rio do que migrar primeiro |
| `eval/` | seu eval pessoal: `tarefas/NN-nome/{tarefa.md,contexto/,criterio.md}` + 3 exemplos |
| `eval/rodar.py` | gera o pacote para colar no Claude Code/Codex/chat que vocÃª assina, ou roda no Ollama local (`--ollama`). Nunca chama API paga |
| `eval/placar.py` | registra a nota por modelo e data e desenha a evoluÃ§Ã£o (SVG; PNG se houver matplotlib) |
| `plano/plano-90-dias.md` | ownership, distribuiÃ§Ã£o, mundo fÃ­sico, identidade, crenÃ§as, pessoas â€” com exercÃ­cios |

## ComeÃ§ar

```bash
git clone https://github.com/inematds/sobreviver-ia && cd sobreviver-ia

python3 kit/calcula_kit.py --pessoas 2 --dias 14 --gasto-mensal 4500
bash offline/instala-offline.sh --modelo llama3.2:3b --wiki pt --tipo nopic     # dry-run
python3 seguranca/auditoria_contas.py --modelo contas.csv
python3 eval/rodar.py --modelo meu-modelo        # ou: --ollama qwen2.5:7b
python3 eval/placar.py grafico
python3 -m pytest -q                              # testes
```

Windows: veja a seÃ§Ã£o "Instale a IA e a Wikipedia offline" no [guia](https://inematds.github.io/sobreviver-ia/guia/#guia).

## LicenÃ§a

MIT â€” veja [LICENSE](LICENSE). VersÃ£o 1.0.0. Parte do ecossistema [INEMA.CLUB](https://inema.club).

---

Projeto adaptado da comunidade INEMA TDS - Marca Arckhe