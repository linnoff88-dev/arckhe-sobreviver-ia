#!/usr/bin/env python3
"""Auditoria das suas contas: quem ainda está no SMS e o que falta migrar.

Uso:
    python3 seguranca/auditoria_contas.py --modelo contas.csv        # cria planilha modelo
    python3 seguranca/auditoria_contas.py --interativo contas.csv    # pergunta conta a conta
    python3 seguranca/auditoria_contas.py contas.csv                 # relatório no terminal
    python3 seguranca/auditoria_contas.py contas.csv --saida relatorio.md

CSV (cabeçalho obrigatório):  conta,categoria,metodo,codigos_recuperacao
  metodo: senha | sms | email | app | chave   (chave = passkey/chave física)
  codigos_recuperacao: sim | nao

O arquivo fica só no seu computador. Não guarde senhas nele, só o nome da conta.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

METODOS = {
    "senha": (0, "só senha", "fraca"),
    "sms": (1, "SMS", "fraca"),
    "email": (2, "e-mail", "média"),
    "app": (3, "app autenticador", "boa"),
    "chave": (4, "passkey/chave física", "ótima"),
}
# Peso da categoria na prioridade (maior = migrar antes)
PESO = {"email": 5, "banco": 5, "senhas": 5, "celular": 4, "mensagens": 3,
        "trabalho": 3, "social": 2, "compras": 2, "outro": 1}
CAMPOS = ["conta", "categoria", "metodo", "codigos_recuperacao"]

MODELO = [
    ("E-mail principal", "email", "sms", "nao"),
    ("Banco principal", "banco", "sms", "nao"),
    ("Gerenciador de senhas", "senhas", "app", "sim"),
    ("Conta Google/Apple do celular", "celular", "sms", "nao"),
    ("WhatsApp", "mensagens", "senha", "nao"),
    ("Instagram", "social", "sms", "nao"),
    ("Loja online", "compras", "email", "nao"),
]


def normaliza(linha: dict) -> dict:
    metodo = (linha.get("metodo") or "").strip().lower()
    if metodo not in METODOS:
        raise ValueError(f"método inválido '{metodo}' na conta '{linha.get('conta')}'"
                         f" (use {', '.join(METODOS)})")
    cat = (linha.get("categoria") or "outro").strip().lower()
    cod = (linha.get("codigos_recuperacao") or "nao").strip().lower() in ("sim", "s", "yes", "y", "1")
    return {"conta": (linha.get("conta") or "").strip(), "categoria": cat if cat in PESO else "outro",
            "metodo": metodo, "codigos": cod}


def ler(caminho: Path) -> list[dict]:
    with caminho.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        faltando = set(CAMPOS) - set(r.fieldnames or [])
        if faltando:
            raise ValueError(f"CSV sem colunas: {', '.join(sorted(faltando))}")
        return [normaliza(l) for l in r if (l.get("conta") or "").strip()]


def analisar(contas: list[dict]) -> dict:
    pendentes = []
    for c in contas:
        nivel = METODOS[c["metodo"]][0]
        acoes = []
        if nivel < 3:
            acoes.append(f"trocar {METODOS[c['metodo']][1]} por app autenticador ou passkey")
        if not c["codigos"]:
            acoes.append("salvar códigos de recuperação")
        if acoes:
            prioridade = PESO[c["categoria"]] * (4 - min(nivel, 3)) + (0 if c["codigos"] else 1)
            pendentes.append({**c, "acoes": acoes, "prioridade": prioridade})
    pendentes.sort(key=lambda x: (-x["prioridade"], x["conta"]))
    total = len(contas)
    fortes = sum(1 for c in contas if METODOS[c["metodo"]][0] >= 3)
    return {
        "total": total,
        "fortes": fortes,
        "sms": sum(1 for c in contas if c["metodo"] == "sms"),
        "sem_codigos": sum(1 for c in contas if not c["codigos"]),
        "pct_fortes": round(100 * fortes / total) if total else 0,
        "pendentes": pendentes,
    }


def relatorio(res: dict) -> str:
    md = ["# Auditoria de contas", "",
          f"- Contas: **{res['total']}**",
          f"- Com app autenticador ou passkey: **{res['fortes']}** ({res['pct_fortes']}%)",
          f"- Ainda no SMS: **{res['sms']}**",
          f"- Sem códigos de recuperação salvos: **{res['sem_codigos']}**", ""]
    if not res["pendentes"]:
        md.append("Tudo em dia. Revise de novo em 6 meses.")
        return "\n".join(md) + "\n"
    md += ["## O que falta (mais urgente primeiro)", "",
           "| # | Conta | Categoria | Hoje | Fazer |", "|---|---|---|---|---|"]
    for i, p in enumerate(res["pendentes"], 1):
        md.append(f"| {i} | {p['conta']} | {p['categoria']} | {METODOS[p['metodo']][1]} "
                  f"({METODOS[p['metodo']][2]}) | {'; '.join(p['acoes'])} |")
    md += ["", "Passo a passo de cada conta: `seguranca/checklist-mfa.md`."]
    return "\n".join(md) + "\n"


def gravar(caminho: Path, linhas: list[tuple]) -> None:
    with caminho.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CAMPOS)
        w.writerows(linhas)


def interativo(caminho: Path, entrada=input) -> None:
    linhas = []
    if caminho.exists():
        linhas = [(c["conta"], c["categoria"], c["metodo"], "sim" if c["codigos"] else "nao")
                  for c in ler(caminho)]
    print(f"Categorias: {', '.join(PESO)}   Métodos: {', '.join(METODOS)}")
    print("Enter vazio no nome da conta encerra.")
    while True:
        conta = entrada("Conta: ").strip()
        if not conta:
            break
        cat = entrada("  categoria [outro]: ").strip().lower() or "outro"
        met = ""
        while met not in METODOS:
            met = entrada("  método (senha/sms/email/app/chave): ").strip().lower()
        cod = entrada("  códigos de recuperação salvos? (sim/nao) [nao]: ").strip().lower() or "nao"
        linhas.append((conta, cat, met, "sim" if cod.startswith("s") else "nao"))
    gravar(caminho, linhas)
    print(f"Gravado: {caminho} ({len(linhas)} contas)")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Auditoria de MFA das suas contas.")
    p.add_argument("csv", type=Path)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--modelo", action="store_true", help="cria um CSV modelo no caminho dado")
    g.add_argument("--interativo", action="store_true", help="pergunta conta a conta e grava o CSV")
    p.add_argument("--saida", type=Path, help="grava o relatório markdown neste arquivo")
    a = p.parse_args(argv)
    if a.modelo:
        if a.csv.exists():
            print(f"erro: {a.csv} já existe (não sobrescrevo)", file=sys.stderr)
            return 2
        gravar(a.csv, MODELO)
        print(f"Modelo criado: {a.csv}. Edite e rode de novo sem --modelo.")
        return 0
    if a.interativo:
        interativo(a.csv)
    try:
        res = analisar(ler(a.csv))
    except (ValueError, FileNotFoundError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    texto = relatorio(res)
    if a.saida:
        a.saida.write_text(texto, encoding="utf-8")
        print(f"Relatório: {a.saida}")
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
