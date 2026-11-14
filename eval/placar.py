#!/usr/bin/env python3
"""Placar do eval pessoal: guarda a nota de cada modelo por data e desenha a evolução.

    python3 eval/placar.py registrar eval/saida/<pasta>/notas.csv   # soma as notas da rodada
    python3 eval/placar.py add --modelo qwen2.5:7b --feitas 4 --total 12 [--data 2026-10-19]
    python3 eval/placar.py ver                                       # tabela no terminal
    python3 eval/placar.py grafico                                   # eval/placar.svg (+ .png se houver matplotlib)

O placar fica em eval/placar.csv (data,modelo,feitas,total,pct).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PLACAR = RAIZ / "placar.csv"
CAMPOS = ["data", "modelo", "feitas", "total", "pct"]


def ler(caminho: Path = PLACAR) -> list[dict]:
    if not caminho.exists():
        return []
    with caminho.open(newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    for l in linhas:
        l["feitas"] = float(l["feitas"])
        l["total"] = int(float(l["total"]))
        l["pct"] = float(l["pct"])
    return sorted(linhas, key=lambda l: (l["data"], l["modelo"]))


def adicionar(modelo: str, feitas: float, total: int, data: str | None = None,
              caminho: Path = PLACAR) -> dict:
    if total <= 0:
        raise ValueError("total precisa ser > 0")
    if not 0 <= feitas <= total:
        raise ValueError("feitas precisa ficar entre 0 e o total")
    data = data or dt.date.today().isoformat()
    dt.date.fromisoformat(data)  # valida
    linha = {"data": data, "modelo": modelo, "feitas": feitas, "total": total,
             "pct": round(100 * feitas / total, 1)}
    novo = not caminho.exists()
    with caminho.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        if novo:
            w.writeheader()
        w.writerow(linha)
    return linha


def registrar_notas(notas: Path, caminho: Path = PLACAR) -> dict:
    with notas.open(newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    if not linhas:
        raise ValueError("notas.csv vazio")
    vazias = [l["tarefa"] for l in linhas if not (l.get("nota") or "").strip()]
    if vazias:
        raise ValueError(f"faltam notas: {', '.join(vazias)}")
    soma = 0.0
    for l in linhas:
        n = float(l["nota"].replace(",", "."))
        if not 0 <= n <= 1:
            raise ValueError(f"nota fora de 0–1 na tarefa {l['tarefa']}")
        soma += n
    return adicionar(linhas[0]["modelo"], soma, len(linhas), linhas[0]["data"], caminho)


def tabela(linhas: list[dict]) -> str:
    if not linhas:
        return "Placar vazio. Rode o eval e registre as notas."
    out = [f"{'data':<11} {'modelo':<24} {'feitas':>7} {'%':>6}", "-" * 51]
    for l in linhas:
        out.append(f"{l['data']:<11} {l['modelo'][:24]:<24} {l['feitas']:>4g}/{l['total']:<2} {l['pct']:>5.1f}%")
    return "\n".join(out)


def svg(linhas: list[dict], largura: int = 720, altura: int = 360) -> str:
    """Gráfico de linha único (melhor % por data), sem dependências.

    Cores por variável CSS com valor padrão, para herdar o tema da página.
    """
    m = {"l": 52, "r": 24, "t": 36, "b": 48}
    w, h = largura - m["l"] - m["r"], altura - m["t"] - m["b"]
    melhor: dict[str, dict] = {}
    for l in linhas:
        if l["data"] not in melhor or l["pct"] > melhor[l["data"]]["pct"]:
            melhor[l["data"]] = l
    pts = [melhor[d] for d in sorted(melhor)]
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} {altura}" '
              f'role="img" aria-label="Evolução do eval pessoal: % de tarefas que a IA já faz">',
              '<rect width="100%" height="100%" fill="var(--card, #16161e)"/>',
              f'<text x="{m["l"]}" y="22" fill="var(--txt, #e9e9ee)" font-family="Inter, sans-serif" '
              'font-size="14" font-weight="600">% do meu eval que a IA já faz (melhor modelo da data)</text>']
    for v in (0, 25, 50, 75, 100):
        y = m["t"] + h - h * v / 100
        partes.append(f'<line x1="{m["l"]}" x2="{m["l"] + w}" y1="{y:.1f}" y2="{y:.1f}" '
                      'stroke="var(--line, #272730)" stroke-width="1"/>')
        partes.append(f'<text x="{m["l"] - 8}" y="{y + 4:.1f}" text-anchor="end" fill="var(--mut, #9a9aa6)" '
                      f'font-family="Inter, sans-serif" font-size="12">{v}%</text>')
    if not pts:
        partes.append(f'<text x="{m["l"] + w / 2}" y="{m["t"] + h / 2}" text-anchor="middle" '
                      'fill="var(--mut, #9a9aa6)" font-family="Inter, sans-serif" font-size="14">'
                      'sem dados ainda</text></svg>')
        return "\n".join(partes)
    n = len(pts)
    xy = []
    for i, p in enumerate(pts):
        x = m["l"] + (w / 2 if n == 1 else w * i / (n - 1))
        y = m["t"] + h - h * p["pct"] / 100
        xy.append((x, y, p))
    if n > 1:
        d = " ".join(f'{"M" if i == 0 else "L"}{x:.1f},{y:.1f}' for i, (x, y, _) in enumerate(xy))
        partes.append(f'<path d="{d}" fill="none" stroke="var(--amb, #FACC15)" stroke-width="2" '
                      'stroke-linejoin="round"/>')
    for i, (x, y, p) in enumerate(xy):
        partes.append(f'<g><title>{escape(p["data"])} · {escape(p["modelo"])} · {p["pct"]:g}%</title>'
                      f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="var(--amb, #FACC15)" '
                      'stroke="var(--card, #16161e)" stroke-width="2"/></g>')
        partes.append(f'<text x="{x:.1f}" y="{m["t"] + h + 20}" text-anchor="middle" fill="var(--mut, #9a9aa6)" '
                      f'font-family="Inter, sans-serif" font-size="12">{escape(p["data"][5:])}</text>')
        if i in (0, n - 1):  # rótulo direto só no primeiro e no último ponto
            partes.append(f'<text x="{x:.1f}" y="{y - 12:.1f}" text-anchor="middle" fill="var(--txt, #e9e9ee)" '
                          f'font-family="Inter, sans-serif" font-size="13" font-weight="600">{p["pct"]:g}%</text>')
    partes.append("</svg>")
    return "\n".join(partes)


def png(linhas: list[dict], destino: Path) -> bool:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    melhor: dict[str, float] = {}
    for l in linhas:
        melhor[l["data"]] = max(melhor.get(l["data"], 0), l["pct"])
    datas = sorted(melhor)
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=150)
    fig.patch.set_facecolor("#16161e")
    ax.set_facecolor("#16161e")
    ax.plot(datas, [melhor[d] for d in datas], color="#FACC15", lw=2, marker="o", ms=6)
    ax.set_ylim(0, 100)
    ax.set_ylabel("% do eval", color="#9a9aa6")
    ax.set_title("% do meu eval que a IA já faz", color="#e9e9ee", loc="left", fontsize=11)
    ax.tick_params(colors="#9a9aa6", labelsize=8)
    ax.grid(axis="y", color="#272730", lw=1)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(destino, facecolor=fig.get_facecolor())
    plt.close(fig)
    return True


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Placar do eval pessoal.")
    p.add_argument("--placar", type=Path, default=PLACAR)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("registrar", help="soma um notas.csv preenchido")
    r.add_argument("notas", type=Path)
    a = sub.add_parser("add", help="adiciona uma linha à mão")
    a.add_argument("--modelo", required=True)
    a.add_argument("--feitas", type=float, required=True)
    a.add_argument("--total", type=int, required=True)
    a.add_argument("--data")
    sub.add_parser("ver")
    g = sub.add_parser("grafico")
    g.add_argument("--saida", type=Path, default=RAIZ / "placar.svg")
    x = p.parse_args(argv)
    try:
        if x.cmd == "registrar":
            l = registrar_notas(x.notas, x.placar)
            print(f"Registrado: {l['data']} {l['modelo']} {l['feitas']:g}/{l['total']} = {l['pct']}%")
        elif x.cmd == "add":
            l = adicionar(x.modelo, x.feitas, x.total, x.data, x.placar)
            print(f"Registrado: {l['data']} {l['modelo']} {l['pct']}%")
        elif x.cmd == "ver":
            print(tabela(ler(x.placar)))
        elif x.cmd == "grafico":
            linhas = ler(x.placar)
            x.saida.write_text(svg(linhas), encoding="utf-8")
            print(f"Gráfico: {x.saida}")
            if linhas and png(linhas, x.saida.with_suffix(".png")):
                print(f"Gráfico: {x.saida.with_suffix('.png')}")
    except (ValueError, FileNotFoundError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
