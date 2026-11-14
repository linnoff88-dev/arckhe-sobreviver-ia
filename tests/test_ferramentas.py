"""Testes das ferramentas locais. Rodar: python3 -m pytest -q"""
import csv
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
for sub in ("kit", "seguranca", "eval"):
    sys.path.insert(0, str(RAIZ / sub))

import auditoria_contas as aud  # noqa: E402
import calcula_kit as ck  # noqa: E402
import placar  # noqa: E402
import rodar  # noqa: E402


# ---------- kit ----------
def test_kit_duas_pessoas_14_dias():
    kit = ck.calcular(2, 14, gasto_mensal=4500)
    assert kit.kcal_total == 56_000          # 2 × 14 × 2000
    assert kit.agua_min_total == 42.0        # 2 × 14 × 1,5
    assert kit.agua_max_total == 56.0        # 2 × 14 × 2
    assert kit.galoes_5l == 12
    assert kit.dinheiro == 4500


def test_kit_lista_cobre_as_calorias():
    for p, d in [(1, 3), (2, 14), (5, 30)]:
        kit = ck.calcular(p, d)
        assert ck.kcal_da_lista(kit) >= kit.kcal_total
        assert all(q >= 1 for _, q, _ in kit.itens)


def test_kit_fracoes_somam_um():
    assert abs(sum(f for *_, f in ck.CESTA) - 1.0) < 1e-9


def test_kit_higiene_e_meses():
    kit = ck.calcular(1, 10, higiene_l=1, gasto_mensal=3000, meses_dinheiro=0.5)
    assert kit.agua_max_total == 30.0
    assert kit.dinheiro == 1500


@pytest.mark.parametrize("args", [(0, 14), (2, 0)])
def test_kit_rejeita_invalido(args):
    with pytest.raises(ValueError):
        ck.calcular(*args)


def test_kit_markdown_e_cli(capsys):
    assert ck.main(["--pessoas", "3", "--dias", "14", "--markdown"]) == 0
    out = capsys.readouterr().out
    assert "84.000 kcal" in out and "- [ ]" in out
    assert ck.main(["--pessoas", "0"]) == 2


# ---------- auditoria ----------
def _csv(tmp_path, linhas):
    p = tmp_path / "contas.csv"
    aud.gravar(p, linhas)
    return p


def test_auditoria_prioriza_email_sms(tmp_path):
    p = _csv(tmp_path, [
        ("Loja", "compras", "email", "sim"),
        ("E-mail", "email", "sms", "nao"),
        ("Banco", "banco", "app", "sim"),
    ])
    res = aud.analisar(aud.ler(p))
    assert res["total"] == 3 and res["fortes"] == 1 and res["sms"] == 1
    assert res["pendentes"][0]["conta"] == "E-mail"
    assert [x["conta"] for x in res["pendentes"]] == ["E-mail", "Loja"]


def test_auditoria_tudo_ok(tmp_path):
    p = _csv(tmp_path, [("Banco", "banco", "chave", "sim")])
    texto = aud.relatorio(aud.analisar(aud.ler(p)))
    assert "Tudo em dia" in texto


def test_auditoria_metodo_invalido(tmp_path):
    p = _csv(tmp_path, [("X", "outro", "pombo", "nao")])
    with pytest.raises(ValueError):
        aud.ler(p)


def test_auditoria_modelo_nao_sobrescreve(tmp_path):
    p = tmp_path / "c.csv"
    assert aud.main([str(p), "--modelo"]) == 0
    assert aud.main([str(p), "--modelo"]) == 2
    saida = tmp_path / "rel.md"
    assert aud.main([str(p), "--saida", str(saida)]) == 0
    assert "O que falta" in saida.read_text(encoding="utf-8")


def test_auditoria_interativo(tmp_path):
    respostas = iter(["Banco", "banco", "sms", "nao", ""])
    p = tmp_path / "i.csv"
    aud.interativo(p, entrada=lambda _: next(respostas))
    assert aud.ler(p)[0]["metodo"] == "sms"


# ---------- placar ----------
def test_placar_add_e_ler(tmp_path):
    arq = tmp_path / "placar.csv"
    placar.adicionar("m1", 1, 10, "2026-07-01", arq)
    placar.adicionar("m2", 5.5, 10, "2026-10-01", arq)
    linhas = placar.ler(arq)
    assert [l["pct"] for l in linhas] == [10.0, 55.0]
    assert "55.0%" in placar.tabela(linhas)


def test_placar_valida(tmp_path):
    with pytest.raises(ValueError):
        placar.adicionar("m", 11, 10, "2026-10-01", tmp_path / "p.csv")
    with pytest.raises(ValueError):
        placar.adicionar("m", 1, 0, "2026-10-01", tmp_path / "p.csv")


def test_placar_registrar_notas(tmp_path):
    notas = tmp_path / "notas.csv"
    with notas.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["data", "modelo", "tarefa", "nota"])
        w.writerows([["2026-10-19", "qwen", "01-a", "1"], ["2026-10-19", "qwen", "02-b", "0,5"],
                     ["2026-10-19", "qwen", "03-c", "0"]])
    l = placar.registrar_notas(notas, tmp_path / "p.csv")
    assert l["feitas"] == 1.5 and l["pct"] == 50.0


def test_placar_notas_vazias(tmp_path):
    notas = tmp_path / "notas.csv"
    notas.write_text("data,modelo,tarefa,nota\n2026-10-19,x,01-a,\n")
    with pytest.raises(ValueError):
        placar.registrar_notas(notas, tmp_path / "p.csv")


def test_placar_svg(tmp_path):
    arq = tmp_path / "p.csv"
    assert "sem dados" in placar.svg([])
    placar.adicionar("m1", 1, 10, "2026-07-01", arq)
    placar.adicionar("m2", 5, 10, "2026-10-01", arq)
    s = placar.svg(placar.ler(arq))
    assert s.startswith("<svg") and s.count("<circle") == 2 and "50%" in s


# ---------- eval/rodar ----------
def test_rodar_pacote(tmp_path):
    assert rodar.main(["--saida", str(tmp_path), "--modelo", "teste", "--data", "2026-10-19"]) == 0
    pasta = tmp_path / "2026-10-19-teste"
    pacote = (pasta / "pacote.md").read_text(encoding="utf-8")
    for t in ("01-resumir-reuniao", "02-planilha-gastos", "03-email-cliente"):
        assert f"# {t}" in pacote
    assert "SUPERMERCADO BOM PRECO" in pacote
    assert len(list(csv.DictReader((pasta / "notas.csv").open()))) == 3


def test_rodar_recusa_host_remoto():
    with pytest.raises(ValueError):
        rodar.checar_host("https://api.exemplo.com", False)
    assert rodar.checar_host("http://localhost:11434/", False) == "http://localhost:11434"


def test_gabarito_gastos_bate_com_extrato():
    extrato = RAIZ / "eval/tarefas/02-planilha-gastos/contexto/extrato.csv"
    total = sum(float(r["valor"]) for r in csv.DictReader(extrato.open()))
    assert round(total, 2) == 2205.00


# ---------- offline ----------
def test_offline_dry_run_padrao():
    r = subprocess.run(["bash", str(RAIZ / "offline/instala-offline.sh"), "--wiki", "pt,en", "--tipo", "mini"],
                       capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, r.stderr
    assert "DRY-RUN" in r.stdout and "wikipedia_pt_all_mini" in r.stdout
    assert "~15.5 GB" in r.stdout  # 2,0 (llama3.2:3b) + 2,5 (pt mini) + 11 (en mini)


def test_offline_tipo_invalido():
    r = subprocess.run(["bash", str(RAIZ / "offline/instala-offline.sh"), "--tipo", "gigante"],
                       capture_output=True, text=True, timeout=30)
    assert r.returncode == 2
