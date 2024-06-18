# Otimizando a Busca pela Menor Energia 

<br>**Alunos**: Cauê Gomes Correia dos Santos, Izaque Junior Oliveira Silva e Karla Rovedo Pascoalini.</br>
<br>**Professor**: Daniel Roberto Cassar.</br>
<br>**Disciplina**: Redes Neurais e Algoritmos Genéticos</br>
___
## Objetivo
Este trabalho tem como objetivo desenvolver um algoritmo genético para otimizar a busca pela menor energia de uma molécula, dado um conjunto de átomos, através do método de Huckel.

## Arquivos neste Github:

- `arquivo_principal_notebook`: notebook contendo referências e explicações acerca do nosso raciocínio para desenvolver o nosso trabalho.
  
- `scripts.py`: arquivo contendo as funções que são utilizadas no notebook jupyter.

- `LICENSE`: arquivo que contém o tipo de licença deste repositório.

- `README.md`: arquivo que armazena as informações deste readme.

## Bibliotecas necessárias para rodar o notebook:

- **numpy**
  
- **random**

- **scripts**

## Introdução

O trabalho 'Hamiltonian for n-site molecules' desenvolvido pelo aluno Cauê Santos, turma 2023, com orientação do professor e pesquisador Felipe Crasto, foi um trabalho realizado com intuito de calcular a menor energia do hamiltoniano de cada conformação possível de uma molécula. Esse cálculo foi baseado num importante método físico chamado de Método de Huckel.

O Método de Huckel diz que pode-se calcular a energia, que é o autovalor do hamiltoniano, como uma aproximação que considera apenas elétrons p deslocalizados, que pode ser considerado uma versão mais sofisticada do modelo de elétrons livres. O MH (método de Huckel) considera apenas elétrons p se movendo numa rede de ligações-π (pi).

![Texto Alternativo](ligacaoPiOrbitalp.png)

Esse modelo considera uma rede de carbonos que possuem 2 ligações com hidrogênios, ou seja, em geral só é utilizada para hidrocarbonetos. De forma que os hidrogênios podem ser desconsiderados e os elétrons observados são os elétrons dos orbitais não ligantes p. Os elétrons-σ (sigma) são ignorados na aproximação, visto que as funções de ondas utilizadas para descrever os orbitais ligantes de cada parte são resultados de diferentes combinações de orbitais moleculares. Por isso, esse método só considera hidrocarbonetos conjugados e orbitais-π (Já que eles já determinam as propriedades gerais da molécula).

O método de Huckel se limita em muitos sentidos, à apenas hidrocarbonetos, orbitais-π, e também a sistemas planares.

![Texto](nivelEnergiaPi.png)

De acordo com esse método. Pode-se escrever o hamiltoniano de um hidrocarboneto qualquer dessa forma:

$$DA PRA POR UM HAMILTONIANO geral AQUI? \frac{1}{2}$$
    
De forma que sua diagonal principal representa a energia no sítio, ou seja, a energia do sítio que o elétron se encontra no átomo, e todos os outros elementos da matriz representam a energia de hopping, essa é a energia necessária para um elétron pular de um átomo para outro. Neste trabalho foi considerado a energia do sítio igual a 0 e a energia de hopping sendo um um valor binário, 0 ou 1.

Calcular os autovalores desse hamiltoniano é calcular os níveis energéticos dele, e portanto, descobrir quais níveis estão desocupados para os elétrons livres ocuparem. Note que a quantidade de elétrons livres, para esse caso, é de 1 para cada átomo. Ou seja, para o caso de uma rede de 6 átomos, há 6 elétrons livres. Onde cada dupla ocupa 1 nível, podendo haver elétrons desemparelhados, ou seja, isolados.

A questão com o trabalho desenvolvido é que ele calcula o nível de energia de todas as conformações possíveis de uma cadeia de N átomos e então retorna a menor. Para, por exemplo, uma cadeia de N=2, apenas 2 conformações são possíveis. Mas ao aumentar de 1 em 1, nota-se um padrão exponencial na quantidade total de conformações da cadeia. Para 5 átomos, são 1024 conformações. Para 7, 2 milhões.
A equação que calcula a quantidade de conformações totais é a seguinte

$DA PRA BOTAR UMA EQUAÇÃO AQUI?$

Por conta disso, o código é visivelmente não otimizado para uma quantidade maior do que 8 átomos. Dado esse problema, foi estipulado criar um algoritmo genético de minimização que retorna a melhor energia com apenas o número de átomos estipulado.

Porém, é sabido que este algoritmo não calcula a energia de todas as conformações possíveis, pois isto demandaria um poder computacional imenso. Ele calcula de algumas e, por meio da seleção por torneio, define os melhores candidatos para seguirem para a próxima geração e auxiliar na devolução de uma das possíveis melhores energias daquele hamiltoniano com N átomos. Ou seja, não necessariamente ele encontrará o mínimo global das conformações, mas procura encontrar o mais próximo disso.

Proposta de GA

Como funciona uma GA


## Desenvolvimento
Durante o tempo de produção do trabalho contamos com a ajuda do professor e pesquisador Dr. Felipe David Crasto de Lima [2], que nos auxiliou na compreensão do método do cálculo da energia total e eventuais dúvidas que surgiram durante o trabalho. 

## Conclusão
(destacar se alcançamos o objetivo principal do trabalho ou o que falta que tal)

## Referências Bibliográficas
<br>[1] Cassar, Daniel Roberto. GA 4.2 - Notebook Descobrindo a senha.</br>

<br>[2]Santos, C. e Lima, F. </br>
