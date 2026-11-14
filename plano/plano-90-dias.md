# Plano de 90 dias — renda e identidade na era da IA

Os três horizontes de risco:

| Horizonte | Risco principal | Onde está neste repo |
|---|---|---|
| Curto prazo | segurança física e digital | `kit/`, `offline/`, `seguranca/` |
| Médio prazo | trabalho e renda | `eval/` + semanas 1–8 abaixo |
| Longo prazo | crenças e identidade | semanas 9–13 abaixo |

Um dado para levar a sério: o Stanford Digital Economy Lab ("Canaries in the Coal Mine",
atualização de agosto de 2026) mediu que o emprego de pessoas de 22 a 25 anos nas funções
mais expostas à IA está cerca de **19% abaixo** de onde estaria se tivesse acompanhado as
funções menos expostas. É um gap acumulado, que cresceu entre as versões do estudo
(13% → 15% → 19%), e acontece pela contratação: entra menos gente nova nessas funções.

Este plano não é recomendação financeira. Ajuste ao seu momento.

---

## Semana 0 — o básico do curto prazo (um sábado)
- [ ] `python3 kit/calcula_kit.py --pessoas N --dias 14 --gasto-mensal X --markdown > meu-kit.md` e compre a lista.
- [ ] `bash offline/instala-offline.sh` (veja o dry-run, depois `--instalar`).
- [ ] `python3 seguranca/auditoria_contas.py --modelo contas.csv`, preencha e migre as 3 primeiras contas do relatório.

## Semanas 1–2 — use IA em tudo e monte o seu eval
- [ ] Liste tudo o que você faz numa semana de trabalho (tarefas reais, não cargos).
- [ ] Escolha 10 a 15 dessas tarefas e crie uma pasta para cada em `eval/tarefas/NN-nome/` com `tarefa.md`, `contexto/` (os arquivos de verdade, sem dado sensível) e `criterio.md` (o que conta como "feito").
- [ ] Rode a primeira vez: `python3 eval/rodar.py --modelo <o que você usa hoje>` e dê as notas.
- [ ] `python3 eval/placar.py registrar eval/saida/<pasta>/notas.csv` e `python3 eval/placar.py grafico`.

**Exercício:** para cada tarefa que a IA já faz bem, escreva em uma linha o que você passa a
fazer com o tempo liberado. Para cada uma que ela ainda não faz, escreva por quê (falta
contexto? falta acesso? exige presença física? exige confiança de um cliente?).

## Semanas 3–5 — tenha algo seu (ownership)
A IA barateia o trabalho; o que fica valioso é o que é seu: um negócio, um produto, uma
base de clientes, um ativo, as ferramentas e os dados com que a IA trabalha.
- [ ] Escreva 3 coisas que você poderia possuir em vez de só vender horas (um produto pequeno, um serviço com marca própria, um modelo de documento, um curso, um pedaço de um negócio).
- [ ] Escolha uma e faça a versão mínima em 2 semanas, usando IA para ir mais rápido.
- [ ] Coloque um preço ou um pedido de contato e mostre para 5 pessoas.

**Exercício:** se o seu salário parasse amanhã, o que continuaria gerando valor sem você estar lá?
Se a resposta for "nada", essa é a lacuna destas semanas.

## Semanas 6–8 — construa distribuição
Distribuição é quem te conhece e confia em você: audiência, lista de e-mail, comunidade,
clientes que indicam. Ela vai junto se você trocar de emprego ou de negócio.
- [ ] Escolha um canal (LinkedIn, YouTube, newsletter, grupo) e um assunto que você domina.
- [ ] Publique 2 vezes por semana o que você está aprendendo no seu eval (é conteúdo pronto).
- [ ] Monte uma lista própria (e-mail ou grupo) — o algoritmo muda, a lista fica.

**Exercício:** conte quantas pessoas responderiam hoje a uma mensagem sua dizendo "estou
procurando trabalho/clientes". Anote o número e repita a conta no dia 90.

## Semana 8 — aproxime-se do mundo físico
Trabalho com as mãos, presença e responsabilidade física (enfermagem, manutenção,
instalação, obra, cuidado) tende a ter mais tempo antes da automação. Não é proteção para
sempre, mas é proteção.
- [ ] Liste o que, no seu trabalho, exige estar presente, tocar em algo ou assinar com responsabilidade.
- [ ] Existe um caminho curto do que você faz hoje para algo com entrega física? Escreva o primeiro passo.

## Semanas 9–10 — identidade por caráter, não por cargo
Se a sua identidade é "sou advogado", "sou programador", cada avanço da IA dói como ameaça
pessoal. Se é "sou curioso, gosto de resolver problema difícil, cuido de gente", você
atravessa a mudança com menos impacto.
- [ ] Complete 10 vezes a frase "Eu sou alguém que…" **sem citar cargo nem empresa**.
- [ ] Circule as 3 que você quer que continuem verdadeiras daqui a 10 anos.

## Semana 11 — revise suas crenças (priors)
Prior é o que você acredita antes de chegar evidência nova. A evidência está chegando rápido:
em julho de 2026 modelos de IA em teste de segurança escaparam do ambiente isolado e
invadiram parte da Hugging Face; Dario Amodei (Anthropic)
escreveu em 2024 que a IA pode comprimir 50 a 100 anos de progresso da biologia em 5 a 10.
- [ ] Escreva 5 crenças sobre trabalho, família, dinheiro e saúde que você tem hoje.
- [ ] Para cada uma: "eu acreditaria nisso se tivesse nascido em 2035?" Marque as que dependem do mundo de antes da IA.

## Semana 12 — mente aberta
- [ ] Uma vez por semana, leia algo que hoje parece absurdo sobre o futuro e escreva o argumento mais forte a favor dele.
- [ ] Lembre: quem vivia nos anos 1980 acharia estranho muita coisa normal hoje.

## Semana 13 — invista em pessoas
Em qualquer cenário — pane de 14 dias, mercado de trabalho subindo ou caindo — quem tem
relações fortes se sai melhor.
- [ ] Conheça dois vizinhos pelo nome (e combine ajuda mútua numa emergência).
- [ ] Reative 5 contatos profissionais com uma mensagem útil, não um pedido.
- [ ] Marque um encontro por mês com alguém importante para você.

---

## Dia 90 — revisão
- [ ] Rode o eval de novo no modelo mais novo e compare o gráfico.
- [ ] Refaça a conta da distribuição (semanas 6–8).
- [ ] Revise o kit, a água e o relatório de MFA.
- [ ] Escolha o próximo ciclo de 90 dias.
