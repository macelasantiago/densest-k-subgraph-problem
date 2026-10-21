# Densest k-Subgraph

Implementação e comparação de métodos para o problema **Densest k-Subgraph**, utilizando uma heurística gulosa e modelos de Programação Linear Inteira Mista (MIP). O projeto analisa a qualidade das soluções, os limites superiores obtidos por relaxação linear e o tempo de execução em diferentes instâncias de grafos.

## Sobre o problema

Dado um grafo e um inteiro \(k\), o objetivo do **Densest k-Subgraph** é selecionar exatamente \(k\) vértices de modo a maximizar o número de arestas cujos dois extremos pertencem ao grupo selecionado.

O trabalho compara duas abordagens:

- **Heurística gulosa:** constrói uma solução de forma iterativa e busca obter bons resultados rapidamente, mas não garante o ótimo em todos os grafos.
- **Modelo MIP:** representa o problema matematicamente e utiliza um solver para encontrar uma solução ótima e, quando conclui a prova de otimalidade, certificar que não existe solução melhor para a instância.

## Minha contribuição

Minha participação concentrou-se na modelagem MIP e na análise dos resultados:

- **Modelo linearizado:** criação das variáveis de decisão e das restrições lineares que representam as arestas internas ao grupo.
- **Relaxação linear:** implementação de uma versão que permite valores contínuos entre 0 e 1 para as variáveis dos vértices, a fim de obter limites superiores para o ótimo inteiro.
- **Reforço do modelo:** inclusão de restrições adicionais e avaliação do efeito delas sobre os limites superiores.
- **Análise do solver:** estudo de como a otimização pode comprovar a otimalidade, incluindo o método Branch and Bound.
- **Validação e comparação:** análise dos valores da heurística e do MIP nas mesmas instâncias, considerando também os tempos de execução.
- **Visualização dos resultados:** preparação de um notebook Jupyter para organizar os dados e reproduzir os gráficos de comparação.

## Métodos

### 1. Heurística gulosa

A heurística começa pelo vértice de maior grau. Em seguida, adiciona ao grupo o vértice que possui mais vizinhos já selecionados, até completar os \(k\) vértices. Ao final, conta as arestas com os dois extremos dentro do grupo.

É uma abordagem simples e rápida, mas não oferece garantia geral de encontrar a solução ótima.

### 2. Modelo MIP linearizado

O modelo utiliza as seguintes variáveis:

- \(x_v\): indica se o vértice \(v\) foi selecionado.
- \(y_e\): representa a contribuição da aresta \(e\) para o número de arestas internas.

A função objetivo maximiza a soma das variáveis \(y_e\). As restrições exigem a seleção de exatamente \(k\) vértices e impedem que uma aresta seja contabilizada quando algum de seus extremos não está selecionado.

A linearização permite expressar o problema por meio de uma função objetivo e de restrições lineares, mantendo as variáveis de seleção dos vértices binárias no modelo exato.

### 3. Relaxação linear e reforço

Na versão relaxada, as variáveis \(x_v\) podem assumir valores contínuos entre 0 e 1, em vez de serem restritas a 0 ou 1. Como o problema é de maximização, essa relaxação fornece um **limite superior** para o ótimo inteiro.

Também é avaliada uma restrição de reforço que limita, para cada vértice, a soma das variáveis das arestas incidentes em função de \(k-1\) e de \(x_v\). Essa restrição preserva as soluções inteiras válidas e pode melhorar o limite do relaxado.

## Experimentos e resultados

Foram avaliadas sete instâncias: `EX`, `P1`, `P2`, `M1`, `M2`, `G1` e `G2`.

As comparações consideram:

- Valor da solução encontrada pela heurística.
- Valor ótimo obtido pelo MIP, quando a otimalidade foi comprovada.
- Limites superiores do relaxado, com e sem reforço.
- Tempo de execução dos métodos.

Nos experimentos realizados, a heurística encontrou o mesmo valor de objetivo que o MIP nas sete instâncias testadas. Esse resultado demonstra bom desempenho nesses casos, mas não significa que a heurística encontre o ótimo para qualquer grafo.

O reforço também reduziu o limite superior em algumas instâncias, como `P1` e `P2`, enquanto em outras não alterou o valor obtido. O efeito depende da estrutura de cada grafo.

> **Observação sobre a reprodutibilidade:** os gráficos do notebook preparado reproduzem os valores transcritos dos resultados da apresentação. Para realizar uma nova medição independente, é necessário executar novamente os códigos dos algoritmos e atualizar os dados utilizados nos gráficos.

## Gráficos

O notebook Jupyter contém três visualizações:

1. **Heurística × MIP:** compara o valor das soluções em cada instância.
2. **Relaxado × ótimo:** compara o ótimo inteiro com os limites superiores sem reforço e com reforço.
3. **Tempo de execução:** compara o tempo medido dos métodos; a escala logarítmica facilita visualizar valores de magnitudes diferentes.

## Tecnologias utilizadas

- **Python** — implementação dos algoritmos e dos experimentos.
- **Python-MIP** — formulação e resolução dos modelos MIP.
- **CBC** — solver utilizado para resolver os modelos.
- **Jupyter Notebook** — organização dos dados e geração dos gráficos.
- **pandas, Matplotlib e NumPy** — manipulação de dados e visualização.

## Objetivo acadêmico

O trabalho explora a aplicação de técnicas de otimização combinatória ao Densest k-Subgraph, comparando uma abordagem heurística com modelos exatos. Também permite estudar modelagem matemática, linearização, relaxação linear, limites superiores, comprovação de otimalidade e análise experimental de algoritmos.

**Contexto:** trabalho acadêmico desenvolvido em grupo. Minha contribuição concentrou-se nos modelos MIP, na relaxação linear, no reforço do modelo e na análise comparativa dos resultados.
