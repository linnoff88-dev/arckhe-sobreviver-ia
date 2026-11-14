#!/usr/bin/env bash
# instala-offline.sh — IA local (Ollama) + Wikipedia offline (Kiwix) para Linux e macOS.
#
# PADRÃO = --dry-run: só mostra o que faria e quanto vai ocupar. Nada é baixado.
# Para instalar de verdade, rode com --instalar.
#
# Uso:
#   bash offline/instala-offline.sh                         # dry-run com o padrão
#   bash offline/instala-offline.sh --modelo qwen2.5:7b --wiki pt --tipo nopic
#   bash offline/instala-offline.sh --wiki pt,en --tipo mini --destino ~/offline --instalar
#
# Opções:
#   --modelo NOME     modelo do Ollama (padrão llama3.2:3b). Ex.: qwen2.5:7b, qwen2.5:3b, gemma3:4b
#   --wiki LISTA      idiomas da Wikipedia separados por vírgula: pt, en, es (padrão pt)
#   --tipo TIPO       mini (só o começo dos artigos) | nopic (texto completo, sem fotos) | maxi (com fotos)
#   --destino DIR     pasta dos arquivos .zim (padrão ~/offline)
#   --sem-ollama      não instala Ollama nem modelo
#   --sem-wiki        não instala Kiwix nem Wikipedia
#   --instalar        executa de verdade (sem isso é sempre dry-run)
#   --porta N         porta do kiwix-serve no comando final (padrão 8088)
#
# Downloads: ollama.com (instalador e modelo) e download.kiwix.org (ZIM + kiwix-tools).
# Não usa nenhuma chave de API. Os tamanhos são aproximados (mudam a cada edição mensal).
set -euo pipefail

MODELO="llama3.2:3b"; WIKI="pt"; TIPO="nopic"; DESTINO="$HOME/offline"
OLLAMA=1; KIWIX=1; DRY=1; PORTA=8088

while [ $# -gt 0 ]; do
  case "$1" in
    --modelo) MODELO="$2"; shift 2;;
    --wiki) WIKI="$2"; shift 2;;
    --tipo) TIPO="$2"; shift 2;;
    --destino) DESTINO="$2"; shift 2;;
    --porta) PORTA="$2"; shift 2;;
    --sem-ollama) OLLAMA=0; shift;;
    --sem-wiki) KIWIX=0; shift;;
    --instalar) DRY=0; shift;;
    --dry-run) DRY=1; shift;;
    -h|--help) sed -n '2,24p' "$0"; exit 0;;
    *) echo "opção desconhecida: $1" >&2; exit 2;;
  esac
done

case "$TIPO" in mini|nopic|maxi) ;; *) echo "--tipo precisa ser mini, nopic ou maxi" >&2; exit 2;; esac

# Tamanho aproximado do modelo (GB)
tamanho_modelo() {
  case "$1" in
    llama3.2:1b) echo 1.3;; llama3.2:3b|llama3.2) echo 2.0;;
    qwen2.5:3b) echo 1.9;; qwen2.5:7b|qwen2.5) echo 4.7;;
    gemma3:4b) echo 3.3;; llama3.1:8b) echo 4.9;;
    *) echo "?";;
  esac
}

# Tamanho aproximado do ZIM wikipedia_<lang>_all_<tipo> (GB, edição 2026)
tamanho_zim() {
  case "$1_$2" in
    en_mini) echo 11;; en_nopic) echo 55;; en_maxi) echo 110;;
    pt_mini) echo 2.5;; pt_nopic) echo 9;; pt_maxi) echo 30;;
    es_mini) echo 4;; es_nopic) echo 17;; es_maxi) echo 45;;
    *) echo "?";;
  esac
}

SO="$(uname -s)"
fazer() {  # imprime sempre; executa só com --instalar
  echo "  \$ $*"
  if [ "$DRY" -eq 0 ]; then bash -c "$*"; fi
}

echo "== instala-offline ($([ $DRY -eq 1 ] && echo 'DRY-RUN: nada será baixado' || echo 'INSTALANDO')) =="
echo "Sistema: $SO   Destino dos ZIM: $DESTINO"
TOTAL=0
soma() { [ "$1" = "?" ] || TOTAL=$(awk -v a="$TOTAL" -v b="$1" 'BEGIN{print a+b}'); }

if [ "$OLLAMA" -eq 1 ]; then
  T=$(tamanho_modelo "$MODELO"); soma "$T"
  echo; echo "[1] Ollama + modelo $MODELO (~${T} GB)"
  if command -v ollama >/dev/null 2>&1; then
    echo "  ollama já instalado: $(command -v ollama)"
  elif [ "$SO" = "Darwin" ]; then
    fazer "brew install ollama || echo 'Sem Homebrew: baixe o app em https://ollama.com/download/mac'"
  else
    fazer "curl -fsSL https://ollama.com/install.sh | sh"
  fi
  fazer "ollama pull $MODELO"
  echo "  Teste depois:  ollama run $MODELO \"Como tratar água para beber sem fervura?\""
fi

if [ "$KIWIX" -eq 1 ]; then
  echo; echo "[2] Kiwix (leitor offline) + Wikipedia ($WIKI, $TIPO)"
  if command -v kiwix-serve >/dev/null 2>&1; then
    echo "  kiwix-serve já instalado: $(command -v kiwix-serve)"
  elif [ "$SO" = "Darwin" ]; then
    fazer "brew install kiwix-tools || echo 'Ou instale o app Kiwix: https://kiwix.org/en/applications/'"
  elif command -v apt-get >/dev/null 2>&1; then
    fazer "sudo apt-get install -y kiwix-tools"
  else
    echo "  Sem apt: baixe o binário em https://download.kiwix.org/release/kiwix-tools/"
  fi
  fazer "mkdir -p '$DESTINO'"
  IFS=',' read -ra LANGS <<< "$WIKI"
  ZIMS=()
  for L in "${LANGS[@]}"; do
    T=$(tamanho_zim "$L" "$TIPO"); soma "$T"
    BASE="https://download.kiwix.org/zim/wikipedia"
    PADRAO="wikipedia_${L}_all_${TIPO}_AAAA-MM.zim"
    echo "  Wikipedia $L/$TIPO: ~${T} GB  ($BASE/$PADRAO — a edição mais recente)"
    if [ "$DRY" -eq 0 ]; then
      ARQ=$(curl -fsSL "$BASE/" | grep -o "wikipedia_${L}_all_${TIPO}_[0-9-]*\.zim" | sort -u | tail -1)
      [ -n "$ARQ" ] || { echo "  não achei o arquivo de $L/$TIPO na listagem" >&2; continue; }
      fazer "curl -fL -C - -o '$DESTINO/$ARQ' '$BASE/$ARQ'"
      ZIMS+=("$DESTINO/$ARQ")
    else
      echo "  \$ curl -fL -C - -o '$DESTINO/$PADRAO' '$BASE/$PADRAO'"
      ZIMS+=("$DESTINO/$PADRAO")
    fi
  done
  echo "  Abrir no navegador depois:  kiwix-serve --port $PORTA ${ZIMS[*]}  →  http://localhost:$PORTA"
fi

echo
echo "Espaço total aproximado: ~${TOTAL} GB"
LIVRE=$(df -Pk "$HOME" | awk 'NR==2{printf "%.0f", $4/1024/1024}')
echo "Livre em $HOME: ~${LIVRE} GB"
if [ "$DRY" -eq 1 ]; then
  echo; echo "Isto foi um DRY-RUN. Para instalar de verdade, repita com --instalar."
fi
