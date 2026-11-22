#!/bin/sh
# Rode UMA vez, na raiz do repositório, depois de copiar estes arquivos por cima dele.
# Move os arquivos antigos para as pastas novas e remove os PDFs duplicados da raiz.
set -e
mkdir -p circuitos/original simulador scripts
[ -f "Projeto alpha .circ" ] && git mv "Projeto alpha .circ" circuitos/original/projeto_alpha.circ
[ -f "Simulador.py" ] && git mv "Simulador.py" simulador/simulador_antigo.py
[ -f "Alocação.py" ] && git mv "Alocação.py" scripts/alocacao.py
for f in MiniCPU4B_seletor_com_computador.pdf MiniCPU4_computador_portas_logicas.pdf; do
  [ -f "$f" ] && git rm -q "$f"
done
git add -A
echo "Pronto. Confira com: git status"
