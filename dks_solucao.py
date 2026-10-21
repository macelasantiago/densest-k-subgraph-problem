"""
A ideia (gulosa):
  1) comecar pelo vertice com MAIS ligacoes (maior grau)
  2) repetir: entre os vertices de fora do grupo, escolher o que tem
     MAIS ligacoes com os vertices que ja estao no grupo
  3) parar quando o grupo tiver k vertices
"""

def ler_instancia(caminho):
    """Le o arquivo .txt da instancia e devolve (n, k, arestas)."""
    n = None
    k = None
    arestas = []

    arquivo = open(caminho, encoding="utf-8")
    for linha in arquivo:
        linha = linha.strip()

        if linha == "":
            continue                                   # ignora linha vazia

        if linha.startswith("#"):
            # cabecalho, por exemplo:  # nome=EX n=8 m=9 k=4
            for pedaco in linha[1:].split():
                if pedaco.startswith("n="):
                    n = int(pedaco[2:])
                if pedaco.startswith("k="):
                    k = int(pedaco[2:])
        else:
            # linha de aresta, por exemplo:  3 6
            u, v = linha.split()
            arestas.append((int(u), int(v)))
    arquivo.close()

    return n, k, arestas


def montar_vizinhos(n, arestas):
    """Para cada vertice, guarda o conjunto de vertices ligados a ele."""
    vizinhos = {}
    for v in range(n):
        vizinhos[v] = set()

    for u, v in arestas:
        vizinhos[u].add(v)
        vizinhos[v].add(u)

    return vizinhos


def escolher_primeiro_vertice(n, vizinhos):
    """Devolve o vertice com mais vizinhos (maior grau). Empate: o primeiro."""
    melhor_vertice = None
    maior_grau = -1
    for v in range(n):
        grau = len(vizinhos[v])
        if grau > maior_grau:                          # '>' estrito: no empate fica o primeiro
            maior_grau = grau
            melhor_vertice = v
    return melhor_vertice


def escolher_proximo_vertice(n, vizinhos, grupo):
    """
    Devolve o vertice de fora do grupo com mais ligacoes com o grupo.
    Tambem devolve o placar (quantas ligacoes cada candidato tem), para podermos explicar.
    """
    placar = {}
    melhor_vertice = None
    maior_numero = -1

    for v in range(n):
        if v in grupo:
            continue                                   # so olha quem esta fora do grupo
        ligacoes_com_grupo = len(vizinhos[v] & grupo)  # vizinhos de v que ja estao no grupo
        placar[v] = ligacoes_com_grupo
        if ligacoes_com_grupo > maior_numero:          # '>' estrito: no empate fica o primeiro
            maior_numero = ligacoes_com_grupo
            melhor_vertice = v

    return melhor_vertice, placar


def heuristica(n, arestas, k, explicar=False):
    """Devolve o grupo de k vertices escolhido pela heuristica (um conjunto)."""
    vizinhos = montar_vizinhos(n, arestas)

    # passo 1: primeiro vertice
    primeiro = escolher_primeiro_vertice(n, vizinhos)
    grupo = {primeiro}
    if explicar:
        print(f"  Passo 1: entra o vertice {primeiro} (maior grau: {len(vizinhos[primeiro])} ligacoes)")

    # passos seguintes: um vertice por vez ate chegar em k
    passo = 2
    while len(grupo) < k:
        escolhido, placar = escolher_proximo_vertice(n, vizinhos, grupo)
        grupo.add(escolhido)
        if explicar:
            candidatos = {v: c for v, c in placar.items() if c > 0}
            print(f"  Passo {passo}: ligacoes com o grupo anterior {candidatos} -> entra o vertice {escolhido}")
        passo = passo + 1

    return grupo

def contar_arestas(arestas, grupo):
    """Conta as arestas que tem os DOIS extremos dentro do grupo."""
    total = 0
    for u, v in arestas:
        if u in grupo and v in grupo:
            total = total + 1
    return total

if __name__ == "__main__":
    n, k, arestas = ler_instancia("instancias/EX.txt")
    print("Instancia EX: n =", n, "| k =", k, "| arestas =", len(arestas))
    grupo = heuristica(n, arestas, k, explicar=True)
    print("Grupo final:", sorted(grupo))
    print("Arestas dentro do grupo:", contar_arestas(arestas, grupo))