# Bag of Words (BoW) - Processo de Vetorização

## 1. Tokenização:

O primeiro passo é dividir o texto em unidades menores chamadas "tokens". Em BoW, os tokens geralmente são palavras, mas podem ser n-gramas ou até mesmo caracteres, dependendo da granularidade desejada.

**Exemplo:**

Texto: "A análise de sentimentos é uma parte interessante do processamento de linguagem natural."

Tokens: ["A", "análise", "de", "sentimentos", "é", "uma", "parte", "interessante", "do", "processamento", "de", "linguagem", "natural"]


## 2. Construção do Vocabulário:

Em seguida, cria-se um vocabulário único a partir de todos os tokens encontrados no corpus (conjunto de documentos). Cada palavra única no vocabulário recebe um índice único.

**Exemplo:**

Vocabulário: {"A": 0, "análise": 1, "de": 2, "sentimentos": 3, "é": 4, "uma": 5, "parte": 6, "interessante": 7, "do": 8, "processamento": 9, "linguagem": 10, "natural":11}

## 3. Contagem de Ocorrências:

Para cada documento, conta-se quantas vezes cada palavra do vocabulário aparece no documento. Essa contagem é armazenada em um vetor

**Exemplo:**

Vetor do Documento: [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]

Este vetor representa a contagem de ocorrências de cada palavra no documento em relação ao vocabulário.

## 4. Vetorização Final:

O conjunto de vetores resultante, um para cada documento, forma a representação final do BoW para o corpus.

**Exemplo (Dois Documentos):**

Documento 1: [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Documento 2: [0, 2, 1, 0, 2, 1, 0, 1, 0, 2, 1, 1]

Cada posição no vetor representa a contagem de ocorrências de uma palavra específica no documento.

## Considerações Finais:

- BoW perde a ordem das palavras e considera apenas a presença ou ausência delas.
- Pode resultar em vetores esparsos, especialmente em grandes vocabulários.
- Pode ser usado como entrada para algoritmos de aprendizado.