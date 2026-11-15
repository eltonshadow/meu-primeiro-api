#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

VENV_PY="$DIR/.venv/bin/python3"
VENV_UVICORN="$DIR/.venv/bin/uvicorn"
VENV_PYTEST="$DIR/.venv/bin/pytest"

case "$1" in
  test)
    echo "🧪 Executando suíte de testes com cobertura..."
    "$VENV_PYTEST"
    ;;
  start)
    echo "🚀 Iniciando servidor FastAPI..."
    "$VENV_UVICORN" app.main:app --host 0.0.0.0 --port 8000 --reload
    ;;
  *)
    echo "Uso: ./run.sh [start | test]"
    echo "  start : Inicia o servidor na porta 8000"
    echo "  test  : Roda todos os testes automatizados com pytest e coverage"
    exit 1
    ;;
esac
