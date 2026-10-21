from dks_solucao import ler_instancia, heuristica, contar_arestas
from dks_mip import resolver_mip

n, k, arestas = ler_instancia("instancias/EX.txt")
print("INSTANCIA EX")
print("  vertices (0 a 7):", n, "| k =", k)
print("  arestas:", arestas)

print("\n1) HEURISTICA DO DANILO (rapida, sem garantia)")
grupo_h = heuristica(n, arestas, k, explicar=True)
print("  grupo:", sorted(grupo_h), "-> arestas dentro:", contar_arestas(arestas, grupo_h))

print("\n2) MIP EXATO (o gabarito)")
mip = resolver_mip(n, arestas, k)
print("  grupo:", sorted(mip["grupo"]), "-> arestas dentro:", round(mip["valor"]))
print("  x (1 = vertice no grupo):", [round(valor) for valor in mip["x"]])
print("  otimo provado pelo solver:", mip["provado"])

print("\n3) MIP RELAXADO (limite superior)")
rel = resolver_mip(n, arestas, k, relaxado=True)
print("  limite:", round(rel["valor"], 2), "(o otimo real e", round(mip["valor"]), ")")
print("  x (agora pode ter fracoes):", [round(valor, 2) for valor in rel["x"]])

print("\n4) CONCLUSAO")
print("  heuristica =", contar_arestas(arestas, grupo_h), "| otimo =", round(mip["valor"]),
      "| limite relaxado =", round(rel["valor"], 2))