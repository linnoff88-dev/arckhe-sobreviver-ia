#!/usr/bin/env python3
"""Calcula o kit de emergência da casa: comida, água e dinheiro vivo.

Base do cálculo (ajustável por parâmetro):
- 2.000 kcal por pessoa por dia;
- 1,5 a 2 litros de água para beber por pessoa por dia (mais 1 L para higiene/cozinha, opcional);
- dinheiro vivo = 1 mês do seu gasto mensal (ou a fração que você escolher).

Uso:
    python3 kit/calcula_kit.py --pessoas 2 --dias 14 --gasto-mensal 4500
    python3 kit/calcula_kit.py --pessoas 4 --dias 14 --markdown > meu-kit.md

Tudo local, sem internet e sem chave de API.
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass, field

KCAL_DIA = 2000
AGUA_MIN_L = 1.5
AGUA_MAX_L = 2.0

# Alimentos não perecíveis: (nome, kcal por unidade, unidade, fração das calorias do kit)
# As frações somam 1,0. Valores calóricos aproximados de rótulo comum.
CESTA = [
    ("Arroz branco (pacote 1 kg)", 3600, "pacote 1 kg", 0.25),
    ("Macarrão seco (pacote 500 g)", 1750, "pacote 500 g", 0.15),
    ("Feijão/lentilha seca (pacote 1 kg)", 3300, "pacote 1 kg", 0.10),
    ("Pasta de amendoim (pote 500 g)", 2950, "pote 500 g", 0.12),
    ("Aveia em flocos (pacote 500 g)", 1900, "pacote 500 g", 0.08),
    ("Atum/sardinha em lata (lata 120 g)", 250, "lata", 0.08),
    ("Leite em pó (lata 400 g)", 2000, "lata 400 g", 0.08),
    ("Óleo de cozinha (garrafa 900 ml)", 7900, "garrafa 900 ml", 0.06),
    ("Biscoito/bolacha (pacote 400 g)", 1800, "pacote 400 g", 0.08),
]

OUTROS = [
    "Sal, açúcar e café/chá",
    "Abridor de latas manual",
    "Fogareiro + gás de reserva (ou forma de cozinhar sem a rede)",
    "Sacos de lixo e lenços umedecidos",
]


@dataclass
class Kit:
    pessoas: int
    dias: int
    kcal_dia: int = KCAL_DIA
    agua_min_l: float = AGUA_MIN_L
    agua_max_l: float = AGUA_MAX_L
    higiene_l: float = 0.0
    gasto_mensal: float | None = None
    meses_dinheiro: float = 1.0
    itens: list[tuple[str, int, str]] = field(default_factory=list)

    @property
    def kcal_total(self) -> int:
        return self.pessoas * self.dias * self.kcal_dia

    @property
    def agua_min_total(self) -> float:
        return round(self.pessoas * self.dias * (self.agua_min_l + self.higiene_l), 1)

    @property
    def agua_max_total(self) -> float:
        return round(self.pessoas * self.dias * (self.agua_max_l + self.higiene_l), 1)

    @property
    def galoes_5l(self) -> int:
        return math.ceil(self.agua_max_total / 5)

    @property
    def dinheiro(self) -> float | None:
        if self.gasto_mensal is None:
            return None
        return round(self.gasto_mensal * self.meses_dinheiro, 2)


def calcular(pessoas: int, dias: int, kcal_dia: int = KCAL_DIA,
             agua_min_l: float = AGUA_MIN_L, agua_max_l: float = AGUA_MAX_L,
             higiene_l: float = 0.0, gasto_mensal: float | None = None,
             meses_dinheiro: float = 1.0) -> Kit:
    if pessoas < 1 or dias < 1:
        raise ValueError("pessoas e dias precisam ser >= 1")
    if kcal_dia < 500:
        raise ValueError("kcal_dia muito baixo (mínimo 500)")
    if agua_min_l <= 0 or agua_max_l < agua_min_l:
        raise ValueError("água: use 0 < mínimo <= máximo")
    if gasto_mensal is not None and gasto_mensal < 0:
        raise ValueError("gasto mensal não pode ser negativo")
    kit = Kit(pessoas, dias, kcal_dia, agua_min_l, agua_max_l, higiene_l,
              gasto_mensal, meses_dinheiro)
    for nome, kcal_un, unidade, fracao in CESTA:
        qtd = math.ceil(kit.kcal_total * fracao / kcal_un)
        kit.itens.append((nome, qtd, unidade))
    return kit


def kcal_da_lista(kit: Kit) -> int:
    """Calorias que a lista sugerida realmente entrega (arredondada para cima)."""
    tabela = {nome: kcal for nome, kcal, _, _ in CESTA}
    return sum(tabela[nome] * qtd for nome, qtd, _ in kit.itens)


def fmt_num(n: float) -> str:
    s = f"{n:,.1f}" if isinstance(n, float) and not float(n).is_integer() else f"{int(n):,}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def texto(kit: Kit) -> str:
    linhas = [
        f"KIT DE EMERGÊNCIA — {kit.pessoas} pessoa(s) × {kit.dias} dia(s)",
        "=" * 52,
        f"Calorias:  {fmt_num(kit.kcal_total)} kcal  ({fmt_num(kit.kcal_dia)} kcal/pessoa/dia)",
        f"Água:      {fmt_num(kit.agua_min_total)} a {fmt_num(kit.agua_max_total)} litros"
        f"  (~{kit.galoes_5l} galões de 5 L)",
    ]
    if kit.dinheiro is not None:
        linhas.append(f"Dinheiro:  R$ {fmt_num(kit.dinheiro)} em espécie"
                      f" ({fmt_num(kit.meses_dinheiro)} mês(es) de gasto)")
    linhas += ["", "Lista sugerida (não perecíveis):"]
    for nome, qtd, unidade in kit.itens:
        linhas.append(f"  - {qtd:>3} × {nome}")
    linhas.append(f"  (a lista entrega ~{fmt_num(kcal_da_lista(kit))} kcal)")
    linhas += ["", "Não esqueça:"] + [f"  - {o}" for o in OUTROS]
    linhas += ["", "Troque a comida pela de uso diário antes de vencer (o mais velho sai primeiro)."]
    return "\n".join(linhas)


def markdown(kit: Kit) -> str:
    md = [
        f"# Meu kit — {kit.pessoas} pessoa(s) × {kit.dias} dias",
        "",
        "| Item | Meta |",
        "|---|---|",
        f"| Calorias | {fmt_num(kit.kcal_total)} kcal |",
        f"| Água | {fmt_num(kit.agua_min_total)}–{fmt_num(kit.agua_max_total)} L (~{kit.galoes_5l} galões de 5 L) |",
    ]
    if kit.dinheiro is not None:
        md.append(f"| Dinheiro vivo | R$ {fmt_num(kit.dinheiro)} |")
    md += ["", "## Comprar", ""]
    md += [f"- [ ] {qtd} × {nome}" for nome, qtd, _ in kit.itens]
    md += [f"- [ ] {o}" for o in OUTROS]
    md += ["", "## Água", "",
           f"- [ ] {kit.galoes_5l} galões de 5 L cheios, com data na tampa",
           "- [ ] Trocar a água a cada 6 meses",
           "", "## Dinheiro", "",
           "- [ ] Notas pequenas guardadas em local seguro (cofre ou envelope escondido)",
           "", "Checklist completo da casa: `kit/checklist-casa.md`."]
    return "\n".join(md) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Calcula comida, água e dinheiro do kit de emergência.")
    p.add_argument("--pessoas", type=int, default=2)
    p.add_argument("--dias", type=int, default=14)
    p.add_argument("--kcal-dia", type=int, default=KCAL_DIA)
    p.add_argument("--agua-min", type=float, default=AGUA_MIN_L, help="litros/pessoa/dia (mín)")
    p.add_argument("--agua-max", type=float, default=AGUA_MAX_L, help="litros/pessoa/dia (máx)")
    p.add_argument("--higiene", type=float, default=0.0, help="litros extra/pessoa/dia p/ higiene")
    p.add_argument("--gasto-mensal", type=float, default=None, help="gasto mensal da casa (R$)")
    p.add_argument("--meses", type=float, default=1.0, help="meses de dinheiro vivo")
    p.add_argument("--markdown", action="store_true", help="saída em checklist markdown")
    a = p.parse_args(argv)
    try:
        kit = calcular(a.pessoas, a.dias, a.kcal_dia, a.agua_min, a.agua_max,
                       a.higiene, a.gasto_mensal, a.meses)
    except ValueError as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    print(markdown(kit) if a.markdown else texto(kit))
    return 0


if __name__ == "__main__":
    sys.exit(main())
