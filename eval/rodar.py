#!/usr/bin/env python3
"""Roda o seu EVAL PESSOAL num modelo novo.

Dois modos, nenhum usa API paga nem chave:

1. PACOTE (padrão): junta todas as tarefas + contexto num arquivo para você colar
   (ou passar) no Claude Code, no Codex ou no chat que você já assina.
       python3 eval/rodar.py
       python3 eval/rodar.py --modelo "claude-novo"     # só para nomear a pasta

2. OLLAMA LOCAL: roda cada tarefa num modelo do Ollama na sua máquina.
       python3 eval/rodar.py --ollama qwen2.5:7b

Saída em eval/saida/<data>-<modelo>/:
  pacote.md        tudo para colar (modo pacote)
  NN-nome.md       resposta de cada tarefa (modo ollama; no modo pacote, cole aqui a resposta)
  notas.csv        planilha para você dar a nota de cada tarefa (0, 0,5 ou 1) lendo o criterio.md
Depois:  python3 eval/placar.py registrar eval/saida/<pasta>/notas.csv
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
TAREFAS = RAIZ / "tarefas"
SAIDA = RAIZ / "saida"
HOSTS_LOCAIS = {"localhost", "127.0.0.1", "::1"}
MAX_CONTEXTO = 200_000  # caracteres por arquivo de contexto


def listar_tarefas(pasta: Path = TAREFAS) -> list[Path]:
    return sorted(p for p in pasta.iterdir()
                  if p.is_dir() and re.match(r"^\d{2}-", p.name) and (p / "tarefa.md").exists())


def montar_prompt(tarefa: Path) -> str:
    partes = [f"# {tarefa.name}", "", (tarefa / "tarefa.md").read_text(encoding="utf-8").strip()]
    ctx = tarefa / "contexto"
    if ctx.is_dir():
        for arq in sorted(ctx.rglob("*")):
            if arq.is_file():
                try:
                    txt = arq.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    partes += ["", f"## Arquivo {arq.relative_to(tarefa)} (binário — anexe à mão)"]
                    continue
                partes += ["", f"## Arquivo {arq.relative_to(tarefa)}", "```", txt[:MAX_CONTEXTO].rstrip(), "```"]
    return "\n".join(partes) + "\n"


def slug(texto: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", texto).strip("-") or "modelo"


def pasta_saida(modelo: str, data: str, base: Path = SAIDA) -> Path:
    p = base / f"{data}-{slug(modelo)}"
    p.mkdir(parents=True, exist_ok=True)
    return p


def gravar_notas(pasta: Path, tarefas: list[Path], modelo: str, data: str) -> Path:
    arq = pasta / "notas.csv"
    if not arq.exists():
        with arq.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["data", "modelo", "tarefa", "nota"])
            for t in tarefas:
                w.writerow([data, modelo, t.name, ""])
    return arq


def modo_pacote(tarefas: list[Path], pasta: Path) -> Path:
    blocos = [
        "# Meu eval pessoal",
        "",
        "Faça cada tarefa abaixo como se fosse o meu trabalho de verdade.",
        "Responda cada uma numa seção própria que começa com `=== NN-nome ===`.",
        "",
    ]
    for t in tarefas:
        blocos += ["---", "", montar_prompt(t)]
    arq = pasta / "pacote.md"
    arq.write_text("\n".join(blocos), encoding="utf-8")
    return arq


def checar_host(host: str, permitir_remoto: bool) -> str:
    u = urllib.parse.urlparse(host)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError(f"host inválido: {host}")
    if u.hostname not in HOSTS_LOCAIS and not permitir_remoto:
        raise ValueError(f"{u.hostname} não é local. Este script só fala com Ollama na sua máquina "
                         "(use --permitir-remoto se for um Ollama SEU em outra máquina da rede).")
    return host.rstrip("/")


def ollama_gerar(host: str, modelo: str, prompt: str, timeout: int = 600) -> str:
    dados = json.dumps({"model": modelo, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(f"{host}/api/generate", data=dados,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())["response"]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Roda o eval pessoal (pacote para colar ou Ollama local).")
    p.add_argument("--ollama", metavar="MODELO", help="roda no Ollama local com este modelo")
    p.add_argument("--host", default="http://localhost:11434", help="endereço do Ollama (padrão local)")
    p.add_argument("--permitir-remoto", action="store_true", help="aceita Ollama seu em outra máquina")
    p.add_argument("--modelo", default="", help="nome do modelo para o placar (modo pacote)")
    p.add_argument("--data", default=dt.date.today().isoformat())
    p.add_argument("--tarefas", type=Path, default=TAREFAS)
    p.add_argument("--saida", type=Path, default=SAIDA)
    p.add_argument("--so", help="rodar só estas tarefas (ex.: 01,03)")
    a = p.parse_args(argv)

    tarefas = listar_tarefas(a.tarefas)
    if a.so:
        quero = {x.strip().zfill(2) for x in a.so.split(",")}
        tarefas = [t for t in tarefas if t.name[:2] in quero]
    if not tarefas:
        print("Nenhuma tarefa em", a.tarefas, file=sys.stderr)
        return 2

    modelo = a.ollama or a.modelo or "modelo-novo"
    pasta = pasta_saida(modelo, a.data, a.saida)

    if not a.ollama:
        arq = modo_pacote(tarefas, pasta)
        notas = gravar_notas(pasta, tarefas, modelo, a.data)
        print(f"Pacote com {len(tarefas)} tarefas: {arq}")
        print("Cole o pacote no Claude Code / Codex / chat que você assina, ou rode na pasta:")
        print(f"  claude  →  'Leia {arq} e faça as tarefas'   |   codex  →  o mesmo pedido")
        print(f"Salve cada resposta em {pasta}/NN-nome.md, compare com o criterio.md e dê a nota em:")
        print(f"  {notas}")
        return 0

    try:
        host = checar_host(a.host, a.permitir_remoto)
    except ValueError as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    for t in tarefas:
        print(f"[{t.name}] rodando em {a.ollama}...", flush=True)
        try:
            resp = ollama_gerar(host, a.ollama, montar_prompt(t))
        except Exception as e:  # rede, modelo ausente
            print(f"  falhou: {e}  (o Ollama está rodando? `ollama pull {a.ollama}`)", file=sys.stderr)
            return 1
        (pasta / f"{t.name}.md").write_text(resp, encoding="utf-8")
    notas = gravar_notas(pasta, tarefas, modelo, a.data)
    print(f"Respostas em {pasta}. Leia cada uma com o criterio.md da tarefa e preencha {notas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
