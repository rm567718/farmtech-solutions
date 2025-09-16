#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FarmTech Solutions - Aplicação de Agricultura Digital (Console)
Adaptado para Eusébio – CE
Culturas: Milho e Mandioca
"""

import math
import csv
from typing import List, Dict, Optional

# Culturas escolhidas
CULTURAS = ["Milho", "Mandioca"]

# Produtos e doses padrão
DEFAULT_APLICACOES = {
    "Milho": [
        {"produto": "Adubo NPK 20-10-20", "dose_mL_por_m": 60.0},
        {"produto": "Inseticida Lagarta-do-Cartucho", "dose_mL_por_m": 25.0},
    ],
    "Mandioca": [
        {"produto": "Fosfato Natural", "dose_mL_por_m": 45.0},
        {"produto": "Herbicida Pós-emergência", "dose_mL_por_m": 30.0},
    ],
}

# Vetor principal de operações
operacoes: List[Dict] = []

CSV_SAIDA = "dados_operacoes.csv"


# -------------------- Utilidades -------------------- #

def input_float(msg: str, minimo: Optional[float] = None) -> float:
    while True:
        try:
            v = float(input(msg).replace(",", "."))
            if minimo is not None and v < minimo:
                print(f"Valor deve ser >= {minimo}.")
                continue
            return v
        except ValueError:
            print("Entrada inválida. Digite número (use . ou , para decimais).")


def escolher_opcoes(msg: str, opcoes: List[str]) -> str:
    while True:
        print(msg)
        for i, op in enumerate(opcoes, start=1):
            print(f"  {i}) {op}")
        try:
            idx = int(input("Escolha: "))
            if 1 <= idx <= len(opcoes):
                return opcoes[idx - 1]
        except ValueError:
            pass
        print("Opção inválida.\n")


def pause():
    input("\nPressione Enter para continuar...")


# -------------------- Áreas -------------------- #

def area_milho_retangulo() -> float:
    print("\n[Milho] Área como retângulo (comprimento x largura)")
    comp = input_float("Comprimento do talhão (m): ", minimo=0.01)
    larg = input_float("Largura do talhão (m): ", minimo=0.01)
    return comp * larg  # m²


def area_mandioca_circulo() -> float:
    print("\n[Mandioca] Área como círculo (π * r²)")
    raio = input_float("Raio do talhão (m): ", minimo=0.01)
    return math.pi * (raio ** 2)  # m²


def calcular_area(cultura: str) -> float:
    if cultura == "Milho":
        return area_milho_retangulo()
    elif cultura == "Mandioca":
        return area_mandioca_circulo()
    else:
        raise ValueError("Cultura não suportada.")


# -------------------- Manejo de insumos -------------------- #

def calcular_manejo_insumos() -> Dict[str, float]:
    print("\n[Manejo de Insumos]")
    dose = input_float("Dose (mL por metro): ", minimo=0.0)
    n_ruas = input_float("Número de ruas/linhas na lavoura: ", minimo=0.0)
    comp_rua = input_float("Comprimento de cada rua (m): ", minimo=0.0)

    total_metros = n_ruas * comp_rua
    total_mL = dose * total_metros
    total_L = total_mL / 1000.0

    print(f"\nTotal de metros tratados: {total_metros:.2f} m")
    print(f"Total necessário: {total_L:.2f} L")
    return {
        "dose_mL_por_m": dose,
        "n_ruas": n_ruas,
        "comp_rua_m": comp_rua,
        "total_metros": total_metros,
        "total_L": total_L,
    }


# -------------------- CRUD -------------------- #

def entrada_dados():
    print("\n=== ENTRADA DE DADOS ===")
    cultura = escolher_opcoes("Escolha a cultura:", CULTURAS)
    area_m2 = calcular_area(cultura)

    print("\nProdutos sugeridos:")
    for i, p in enumerate(DEFAULT_APLICACOES[cultura], start=1):
        print(f"  {i}) {p['produto']} (dose sugerida: {p['dose_mL_por_m']} mL/m)")
    print("  0) Outro produto")

    try:
        idx = int(input("Selecione o produto (número): "))
    except ValueError:
        idx = -1

    if idx == 0:
        produto = input("Nome do produto: ").strip() or "Produto sem nome"
        dose_padrao = input_float("Dose sugerida (mL/m): ", minimo=0.0)
    elif 1 <= idx <= len(DEFAULT_APLICACOES[cultura]):
        escolhido = DEFAULT_APLICACOES[cultura][idx - 1]
        produto = escolhido["produto"]
        dose_padrao = float(escolhido["dose_mL_por_m"])
    else:
        print("Opção inválida, usando produto genérico.")
        produto = "Produto sem nome"
        dose_padrao = 0.0

    manejo = calcular_manejo_insumos()
    if dose_padrao and manejo["dose_mL_por_m"] == 0.0:
        manejo["dose_mL_por_m"] = dose_padrao

    registro = {
        "cultura": cultura,
        "area_m2": area_m2,
        "produto": produto,
        "dose_mL_por_m": manejo["dose_mL_por_m"],
        "n_ruas": manejo["n_ruas"],
        "comp_rua_m": manejo["comp_rua_m"],
        "total_metros": manejo["total_metros"],
        "total_L": manejo["total_L"],
    }
    operacoes.append(registro)
    print("\nRegistro adicionado com sucesso!")
    pause()


def saida_dados():
    print("\n=== SAÍDA DE DADOS ===")
    if not operacoes:
        print("Nenhuma operação cadastrada.")
    else:
        for i, op in enumerate(operacoes, start=1):
            print(f"\n[{i}] Cultura: {op['cultura']}")
            print(f"     Área: {op['area_m2']:.2f} m²")
            print(f"     Produto: {op['produto']}")
            print(f"     Dose: {op['dose_mL_por_m']:.2f} mL/m")
            print(f"     Ruas: {op['n_ruas']:.2f}  |  Comp/rua: {op['comp_rua_m']:.2f} m")
            print(f"     Total metros: {op['total_metros']:.2f} m")
            print(f"     Total necessário: {op['total_L']:.2f} L")
    pause()


def atualizar_dados():
    print("\n=== ATUALIZAÇÃO DE DADOS ===")
    if not operacoes:
        print("Nenhuma operação cadastrada.")
        pause()
        return
    saida_dados_sem_pause()
    try:
        idx = int(input("\nDigite o número do registro para atualizar: "))
        if not (1 <= idx <= len(operacoes)):
            raise ValueError
    except ValueError:
        print("Índice inválido.")
        pause()
        return

    op = operacoes[idx - 1]
    print("\nDeixe em branco para manter o valor atual.")

    novo_prod = input(f"Produto [{op['produto']}]: ").strip()
    if novo_prod:
        op["produto"] = novo_prod

    def upd_float(campo, rotulo):
        s = input(f"{rotulo} [{op[campo]}]: ").strip().replace(",", ".")
        if s:
            try:
                op[campo] = float(s)
            except ValueError:
                print(f"Valor inválido para {rotulo}. Mantido.")

    upd_float("dose_mL_por_m", "Dose (mL/m)")
    upd_float("n_ruas", "Número de ruas")
    upd_float("comp_rua_m", "Comprimento de cada rua (m)")

    op["total_metros"] = op["n_ruas"] * op["comp_rua_m"]
    op["total_L"] = (op["dose_mL_por_m"] * op["total_metros"]) / 1000.0

    print("\nRegistro atualizado!")
    pause()


def deletar_dados():
    print("\n=== DELEÇÃO DE DADOS ===")
    if not operacoes:
        print("Nenhuma operação cadastrada.")
        pause()
        return
    saida_dados_sem_pause()
    try:
        idx = int(input("\nDigite o número do registro para deletar: "))
        if not (1 <= idx <= len(operacoes)):
            raise ValueError
    except ValueError:
        print("Índice inválido.")
        pause()
        return

    removido = operacoes.pop(idx - 1)
    print(f"Registro da cultura {removido['cultura']} removido.")
    pause()


def saida_dados_sem_pause():
    if not operacoes:
        print("Nenhuma operação cadastrada.")
        return
    for i, op in enumerate(operacoes, start=1):
        print(f"[{i}] {op['cultura']} | Área {op['area_m2']:.2f} m² | "
              f"{op['produto']} | Dose {op['dose_mL_por_m']:.2f} mL/m | "
              f"Total {op['total_L']:.2f} L")


def exportar_csv():
    if not operacoes:
        print("\nNada para exportar.")
        pause()
        return
    campos = ["cultura", "area_m2", "produto", "dose_mL_por_m", "n_ruas", "comp_rua_m",
              "total_metros", "total_L"]
    with open(CSV_SAIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(operacoes)
    print(f"\nExportado para {CSV_SAIDA} (use no R).")
    pause()


# -------------------- Menu -------------------- #

def menu():
    while True:
        print("\n========== FARMTECH SOLUTIONS ==========")
        print("1) Entrada de dados")
        print("2) Saída de dados")
        print("3) Atualizar dados")
        print("4) Deletar dados")
        print("5) Exportar CSV (para R)")
        print("0) Sair")
        opc = input("Escolha: ").strip()
        if opc == "1":
            entrada_dados()
        elif opc == "2":
            saida_dados()
        elif opc == "3":
            atualizar_dados()
        elif opc == "4":
            deletar_dados()
        elif opc == "5":
            exportar_csv()
        elif opc == "0":
            print("Encerrando... até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
