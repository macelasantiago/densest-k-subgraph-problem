"""
Para CADA instancia, o programa faz 6 passos:
  1) le a instancia
  2) roda a heuristica do Danilo
  3) roda o MIP exato 
  4) roda o MIP relaxado, sem e com reforco (limites superiores)
  5) confere se os resultados fazem sentido
  6) calcula quao boa foi a heuristica e imprime a linha da tabela
No final, salva tudo em comparacao.csv.
"""
import csv
import time
from dks_solucao import ler_instancia, heuristica, contar_arestas
from dks_mip import resolver_mip

INSTANCIAS = ["EX", "P1", "P2", "M1", "M2", "G1", "G2"]


def remover_arestas_repetidas(arestas):
    """Deixa cada aresta so uma vez, com o menor numero primeiro (3-6 e 6-3 sao a mesma)."""
    unicas = set()
    for u, v in arestas:
        unicas.add((min(u, v), max(u, v)))
    return sorted(unicas)


print(f"{'inst':<4} {'k':>3} | {'Heur':>5} {'t_heur(s)':>10} | {'MIP':>4} {'t_mip(s)':>9} {'provado':>8} | "
      f"{'Relax':>6} {'Rel+Ref':>8} | {'%otimo':>7}")

resultados = []

for nome in INSTANCIAS:

    # PASSO 1: ler a instancia
    n, k, arestas = ler_instancia("instancias/" + nome + ".txt")
    arestas = remover_arestas_repetidas(arestas)

    # PASSO 2: heuristica do Danilo (e quanto tempo ela levou)
    inicio = time.perf_counter()
    grupo_heuristica = heuristica(n, arestas, k)
    tempo_heuristica = time.perf_counter() - inicio
    valor_heuristica = contar_arestas(arestas, grupo_heuristica)

    # PASSO 3: MIP exato = o gabarito
    mip = resolver_mip(n, arestas, k)
    valor_otimo = round(mip["valor"])

    # PASSO 4: MIP relaxado = limites superiores ("ninguem passa disso")
    relaxado = resolver_mip(n, arestas, k, relaxado=True)
    relaxado_reforco = resolver_mip(n, arestas, k, relaxado=True, reforco=True)
    limite = relaxado["valor"]
    limite_reforco = relaxado_reforco["valor"]

    # PASSO 5: conferencias (se alguma falhar, o programa para com erro)
    #   a) o grupo do MIP realmente tem as arestas que o solver disse
    assert contar_arestas(arestas, mip["grupo"]) == valor_otimo
    #   b) a heuristica nunca pode passar do otimo
    assert valor_heuristica <= valor_otimo
    #   c) o relaxado nunca pode ficar abaixo do otimo (e um limite superior)
    assert valor_otimo <= limite + 0.000001

    # PASSO 6: qualidade da heuristica e linha da tabela
    percentual = 100 * valor_heuristica / valor_otimo
    print(f"{nome:<4} {k:>3} | {valor_heuristica:>5} {tempo_heuristica:>10.6f} | {valor_otimo:>4} "
          f"{mip['tempo']:>9.2f} {'sim' if mip['provado'] else 'nao':>8} | {limite:>6.2f} "
          f"{limite_reforco:>8.2f} | {percentual:>6.1f}%")

    resultados.append([nome, n, k, valor_heuristica, round(tempo_heuristica, 6), valor_otimo,
                       round(mip["tempo"], 3), mip["provado"], round(limite, 3),
                       round(limite_reforco, 3), round(percentual, 1)])

arquivo = open("comparacao.csv", "w", newline="", encoding="utf-8")
escritor = csv.writer(arquivo)
escritor.writerow(["instancia", "n", "k", "heuristica", "tempo_heuristica_s", "mip_otimo",
                   "tempo_mip_s", "otimo_provado", "limite_relaxado", "limite_relaxado_reforco",
                   "pct_do_otimo"])
escritor.writerows(resultados)
arquivo.close()
print("\nSalvo em comparacao.csv")