"""
Variaveis:
   x[v] = 1 se o vertice v esta no grupo, 0 se nao esta
   y[i] = 1 se a aresta i esta DENTRO do grupo, 0 se nao esta

Modelo (linearizado):
   maximizar   y[0] + y[1] + ... (soma de todos os y)           <- arestas dentro do grupo
   sujeito a   soma de todos os x = k                           <- grupo com k vertices
               y[i] <= x[u]  e  y[i] <= x[v]  (aresta i = u-v)  <- aresta so conta se os 2 extremos estao dentro

Modelo relaxado: igual, mas x pode ser qualquer numero entre 0 e 1 (da um LIMITE SUPERIOR).
Reforco (opcional): cada vertice tem no maximo k-1 vizinhos dentro do grupo.
"""
import time
from mip import Model, xsum, maximize, BINARY, CONTINUOUS, OptimizationStatus

def resolver_mip(n, arestas, k, relaxado=False, reforco=False, tempo_limite=120):
    modelo = Model(sense="MAX", solver_name="CBC")
    modelo.verbose = 0

    # cria as variaveis x (uma por vertice)
    if relaxado:
        tipo_x = CONTINUOUS          # qualquer numero entre 0 e 1
    else:
        tipo_x = BINARY              # so 0 ou 1
    x = []
    for v in range(n):
        x.append(modelo.add_var(var_type=tipo_x, lb=0, ub=1))

    # cria as variaveis y (uma por aresta)
    y = []
    for i in range(len(arestas)):
        y.append(modelo.add_var(var_type=CONTINUOUS, lb=0, ub=1))

    # objetivo: maximizar a soma dos y (= arestas dentro do grupo)
    modelo.objective = maximize(xsum(y))

    # restricao: o grupo tem exatamente k vertices
    modelo += xsum(x) == k

    # linearizacao: a aresta i (entre u e v) so pode valer 1 se u E v estiverem no grupo
    for i in range(len(arestas)):
        u, v = arestas[i]
        modelo += y[i] <= x[u]
        modelo += y[i] <= x[v]

    # reforco (opcional): cada vertice tem no maximo k-1 vizinhos dentro do grupo
    if reforco:
        for v in range(n):
            arestas_de_v = []
            for i in range(len(arestas)):
                if v in arestas[i]:
                    arestas_de_v.append(y[i])
            modelo += xsum(arestas_de_v) <= (k - 1) * x[v]

    inicio = time.perf_counter()
    status = modelo.optimize(max_seconds=tempo_limite)
    tempo = time.perf_counter() - inicio

    valores_x = [x[v].x for v in range(n)]
    grupo = None
    if not relaxado:
        grupo = set()
        for v in range(n):
            if valores_x[v] >= 0.5:          # >= 0.5 porque o computador pode devolver 0.9999999
                grupo.add(v)

    return {
        "valor": modelo.objective_value,
        "x": valores_x,
        "grupo": grupo,
        "provado": status == OptimizationStatus.OPTIMAL,
        "tempo": tempo,
    }

if __name__ == "__main__":
    arestas = [(1, 2), (1, 6), (2, 3), (2, 4), (2, 5), (3, 5), (4, 7), (5, 8), (7, 8)]

    arestas = [(u - 1, v - 1) for u, v in arestas]
    r = resolver_mip(8, arestas, 4)
    print("Otimo:", round(r["valor"]), "| grupo (numeracao 0 a 7):", sorted(r["grupo"]), "| provado:", r["provado"])
    r2 = resolver_mip(8, arestas, 4, relaxado=True)
    print("Limite do relaxado:", round(r2["valor"], 2))