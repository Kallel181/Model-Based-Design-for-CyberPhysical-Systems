# Model-Based Design para Sistemas Ciberfísicos — AuroraArm

Projeto desenvolvido na disciplina de **Model-Based Design for Cyber-Physical Systems**, com foco na aplicação de técnicas de Engenharia Baseada em Modelos (Model-Based Design — MBD) ao desenvolvimento, modelagem, simulação e verificação de um braço robótico colaborativo denominado **AuroraArm**.

O projeto utiliza o AuroraArm como estudo de caso para demonstrar como práticas de engenharia baseada em modelos podem apoiar o desenvolvimento de sistemas ciberfísicos (Cyber-Physical Systems — CPS), especialmente em aplicações nas quais desempenho de controle, restrições operacionais e segurança funcional são requisitos fundamentais.

O principal objetivo é estabelecer um fluxo de engenharia reproduzível no qual requisitos do sistema sejam traduzidos em modelos matemáticos, arquiteturas de controle, simulações e procedimentos automatizados de verificação.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Motivação do Projeto](#motivação-do-projeto)
- [Objetivos](#objetivos)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Abordagem de Model-Based Design](#abordagem-de-model-based-design)
- [Modelagem do Sistema](#modelagem-do-sistema)
- [Arquitetura de Controle](#arquitetura-de-controle)
- [Requisitos do Sistema](#requisitos-do-sistema)
- [Requisitos de Segurança](#requisitos-de-segurança)
- [Implementação](#implementação)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Simulação e Avaliação](#simulação-e-avaliação)
- [Verificação e Testes](#verificação-e-testes)
- [Resultados Experimentais](#resultados-experimentais)
- [Rastreabilidade e Evidências](#rastreabilidade-e-evidências)
- [Limitações e Trabalhos Futuros](#limitações-e-trabalhos-futuros)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Configuração](#instalação-e-configuração)
- [Execução dos Testes](#execução-dos-testes)
- [Escopo do Projeto](#escopo-do-projeto)
- [Contribuições](#contribuições)
- [Licença](#licença)
- [Autor](#autor)

---

## Visão Geral

O AuroraArm é um projeto de engenharia baseada em modelos que envolve o desenvolvimento e a avaliação de uma arquitetura de controle para um braço robótico colaborativo.

Sistemas ciberfísicos combinam processos computacionais com componentes físicos, criando sistemas nos quais decisões de software influenciam diretamente o comportamento de equipamentos e processos do mundo real.

Consequentemente, o desenvolvimento desses sistemas exige mais do que a implementação de funcionalidades de software. Também é necessário considerar a dinâmica física, a estabilidade do controle, as restrições temporais, os limites operacionais e as propriedades de segurança.

Este projeto aborda esses desafios por meio de uma abordagem baseada em modelos.

O sistema é representado por modelos matemáticos de sua planta física e de seus componentes de controle. Esses modelos são utilizados para simular o comportamento do braço robótico, avaliar o desempenho da arquitetura de controle e verificar requisitos de engenharia previamente definidos.

As principais atividades desenvolvidas incluem:

- Definição de requisitos funcionais e de segurança.
- Modelagem matemática do sistema robótico.
- Desenvolvimento de uma arquitetura de controle em cascata.
- Implementação de controladores em tempo discreto.
- Simulação do sistema em malha fechada.
- Avaliação quantitativa do desempenho do controle.
- Implementação de testes automatizados.
- Documentação dos requisitos e das evidências de verificação.

O projeto enfatiza a reprodutibilidade e a rastreabilidade, permitindo relacionar os requisitos de engenharia à implementação correspondente e aos procedimentos utilizados para sua verificação.

## Motivação do Projeto

O projeto é motivado pelos desafios associados à operação segura de sistemas robóticos colaborativos.

Um protótipo anterior apresentou uma situação de quase acidente, evidenciando um problema importante de engenharia: a ausência de evidências suficientemente reproduzíveis que demonstrassem que o sistema operava dentro das restrições de segurança e dos limites operacionais estabelecidos.

Esse aspecto é particularmente importante na robótica colaborativa, uma vez que o equipamento pode operar em ambientes nos quais operadores humanos estão fisicamente presentes.

Um controlador que apresenta funcionamento adequado em condições normais não é necessariamente suficiente para demonstrar que o sistema completo se comporta de maneira segura em diferentes condições de operação.

Diante disso, o projeto adota uma abordagem sistemática na qual:

1. Os requisitos são definidos explicitamente.
2. O comportamento do sistema é representado por modelos matemáticos.
3. Os controladores são projetados e avaliados com base nesses modelos.
4. As simulações fornecem evidências reproduzíveis do comportamento esperado.
5. Testes automatizados verificam propriedades específicas da implementação.
6. Os resultados e requisitos não atendidos são documentados.

O objetivo não é apenas produzir um controlador funcional, mas estabelecer um processo de engenharia que torne o comportamento do sistema mensurável, verificável e rastreável.

## Objetivos

### Objetivo Geral

Desenvolver e avaliar uma arquitetura de controle baseada em modelos para um braço robótico colaborativo, estabelecendo um fluxo de trabalho reproduzível para modelagem do sistema, simulação, avaliação de desempenho e verificação de requisitos de engenharia.

### Objetivos Específicos

- Desenvolver uma representação matemática da dinâmica física relevante do braço robótico.
- Implementar uma arquitetura de controle em tempo discreto.
- Projetar um sistema de controle em cascata para posição e corrente.
- Definir restrições operacionais de corrente, tensão e movimento.
- Estabelecer requisitos mensuráveis de desempenho do controle.
- Simular o sistema em malha fechada sob condições operacionais definidas.
- Avaliar erro de rastreamento, sobressinal, tempo de acomodação e restrições elétricas.
- Implementar testes automatizados para o comportamento dos controladores.
- Estabelecer rastreabilidade entre requisitos, implementação e evidências de verificação.
- Identificar limitações e melhorias necessárias antes de uma eventual implantação física.

---

## Arquitetura do Sistema

O AuroraArm é modelado como um sistema ciberfísico composto por subsistemas computacionais e físicos.

A arquitetura pode ser dividida nos seguintes componentes conceituais:

| Componente | Responsabilidade |
|---|---|
| Entrada de referência | Define a posição desejada do braço robótico. |
| Controlador de posição | Calcula a corrente de referência necessária para alcançar a posição desejada. |
| Controlador de corrente | Calcula o comando de tensão necessário para atingir a corrente solicitada. |
| Atuador e motor | Convertem a entrada elétrica em movimento mecânico. |
| Planta mecânica | Representa a dinâmica física do braço robótico. |
| Sistema de realimentação | Fornece informações sobre o estado atual do sistema. |
| Camada de avaliação | Mede o desempenho do controle e verifica os requisitos. |

### Arquitetura de Controle em Cascata

O sistema utiliza dois laços de controle interconectados:

**Laço externo — Controle de posição**

O controlador de posição recebe a posição desejada e a compara com a posição medida.

Sua saída é uma referência de corrente, limitada aos valores operacionais permitidos pelo sistema.

**Laço interno — Controle de corrente**

O controlador de corrente recebe a referência de corrente e a compara com a corrente medida no motor.

Sua saída é um comando de tensão, limitado de acordo com as restrições elétricas.

A arquitetura resultante é:

```text
             Referência de Posição
                      |
                      v
               +-------------+
               | PID Posição |
               +-------------+
                      |
                      v
                Limite de Corrente
                    +/- 8 A
                      |
                      v
               +-------------+
               | PI Corrente |
               +-------------+
                      |
                      v
                 Limite de Tensão
                     +/- 48 V
                      |
                      v
               +-------------+
               | Motor/Planta|
               +-------------+
                      |
                      v
               Realimentação de
               Posição e Corrente
                      |
                      +-----------> Controlador de Posição
                      |
                      +-----------> Controlador de Corrente
```

Essa estrutura separa o problema de regulação da posição mecânica do problema de controle da corrente elétrica.

O laço interno é responsável por responder às demandas elétricas de controle, enquanto o laço externo determina a corrente necessária para alcançar o comportamento mecânico desejado.

---

## Abordagem de Model-Based Design

O projeto segue um processo de desenvolvimento baseado em modelos, no qual o sistema é progressivamente especificado, modelado, implementado, simulado e avaliado.

O fluxo de trabalho é organizado nas seguintes etapas.

### 1. Definição de Requisitos

Os requisitos de engenharia são estabelecidos antes da avaliação dos controladores.

Cada requisito recebe um identificador, um critério de aceitação mensurável e uma estratégia de verificação correspondente.

Isso permite determinar se o sistema implementado satisfaz o comportamento esperado.

### 2. Modelagem do Sistema

Os componentes físicos e computacionais relevantes são representados matematicamente.

A planta física é modelada para reproduzir a relação entre as entradas elétricas e as saídas mecânicas.

O controlador é representado como um sistema computacional em tempo discreto.

### 3. Projeto dos Controladores

A arquitetura de controle é implementada utilizando uma estrutura PID/PI em cascata.

Os parâmetros dos controladores são selecionados e ajustados com base nos resultados das simulações.

### 4. Simulação

Os modelos matemáticos são executados em um ambiente simulado.

A simulação permite observar variáveis internas e respostas do sistema, possibilitando a avaliação do desempenho sob condições controladas.

### 5. Verificação

Testes automatizados avaliam propriedades específicas da implementação.

Os resultados das simulações também são comparados com os critérios de aceitação definidos para cada requisito.

### 6. Evidências e Rastreabilidade

Os resultados de verificação são associados aos respectivos requisitos.

Requisitos que não são atendidos são mantidos como resultados de engenharia, em vez de serem omitidos da avaliação final.

---

## Modelagem do Sistema

O sistema físico é representado por modelos matemáticos que descrevem seu comportamento elétrico e mecânico.

O projeto utiliza uma representação em tempo discreto para os componentes de controle e simulação.

### Representação em Tempo Discreto

O sistema é discretizado utilizando o seguinte intervalo de amostragem:

| Parâmetro | Valor |
|---|---:|
| Tempo de amostragem | 0,002 s |
| Frequência de amostragem | 500 Hz |
| Redução da caixa de engrenagens | 100:1 |

O modelo em tempo discreto é representado na forma de espaço de estados:

\[
x[k+1] = A_d x[k] + B_d u[k]
\]

\[
y[k] = C_d x[k] + D_d u[k]
\]

Onde:

- \(x[k]\) representa o vetor de estados do sistema.
- \(u[k]\) representa a entrada de controle.
- \(y[k]\) representa a saída do sistema.
- \(A_d\) e \(B_d\) são as matrizes do sistema discretizado.
- \(C_d\) e \(D_d\) descrevem a relação entre estados e saídas.

O sistema discretizado possui os seguintes autovalores registrados:

\[
\lambda_1 = 0.27559655
\]

\[
\lambda_2 = 0.9557773
\]

Esses valores são relevantes para a análise da dinâmica do sistema em tempo discreto.

### Ponto de Operação Elétrico

O projeto também registra o seguinte ponto de operação:

| Parâmetro | Valor |
|---|---:|
| Corrente | 3,735294 A |
| Tensão | 41,238235 V |

Esses valores são utilizados como informações de referência para as condições elétricas de operação do sistema modelado.

---

## Arquitetura de Controle

### Controlador de Posição — PID

O laço externo utiliza um controlador PID.

Sua formulação em tempo contínuo é:

\[
u(t) =
K_p e(t)
+
K_i \int_0^t e(\tau)d\tau
+
K_d \frac{de(t)}{dt}
\]

Onde:

- \(e(t)\) representa o erro de rastreamento da posição.
- \(K_p\) é o ganho proporcional.
- \(K_i\) é o ganho integral.
- \(K_d\) é o ganho derivativo.

O controlador gera a referência de corrente utilizada pelo laço interno.

A referência de corrente é limitada a:

\[
-8 \leq I_{ref} \leq 8 \text{ A}
\]

A configuração de controlador avaliada inclui:

| Parâmetro | Valor |
|---|---:|
| \(K_p\) | 12 |
| \(K_i\) | 3 |
| \(K_d\) | 2 |

### Controlador de Corrente — PI

O laço interno utiliza um controlador PI.

Sua formulação é:

\[
u(t) =
K_p e(t)
+
K_i \int_0^t e(\tau)dt
\]

O controlador gera o comando de tensão aplicado ao modelo do motor.

A saída de tensão é limitada a:

\[
-48 \leq V_{cmd} \leq 48 \text{ V}
\]

A configuração inicial registrada inclui:

| Parâmetro | Valor |
|---|---:|
| \(K_p\) | 0,1508 |
| \(K_i\) | 100,531 |
| Ganho anti-windup | 50 |

O controlador incorpora um mecanismo de anti-windup para lidar com o acúmulo do termo integral quando o comando do atuador atinge seus limites de saturação.

---

## Requisitos do Sistema

Os requisitos são divididos entre desempenho do controle e segurança operacional.

### Requisitos de Controle

| ID | Requisito | Critério de Aceitação |
|---|---|---|
| CTRL-001 | Erro de posição em regime permanente | Erro final deve ser igual a zero. |
| CTRL-002 | Limitação de sobressinal | Sobressinal menor ou igual a 8%. |
| CTRL-003 | Tempo de acomodação | Tempo menor ou igual a 300 ms. |
| CTRL-004 | Limites elétricos de operação | Corrente e tensão devem permanecer dentro dos limites especificados. |

Esses requisitos estabelecem critérios mensuráveis para a avaliação do sistema de controle.

### Requisitos de Segurança

| ID | Requisito | Critério de Aceitação |
|---|---|---|
| SAFE-001 | Resposta à parada de emergência | Torque do motor deve atingir zero em até 100 ms. |
| SAFE-002 | Ausência de reinicialização automática | O sistema não deve reiniciar automaticamente após uma parada de segurança. |
| SAFE-003 | Reinicialização explícita | A operação deve exigir a remoção da condição de disparo e um comando explícito de reset. |
| SAFE-004 | Limitação de velocidade linear | A velocidade linear não deve exceder 250 mm/s. |

Os requisitos de segurança estabelecem as restrições operacionais pretendidas.

Sua verificação completa exige evidências adicionais além das simulações nominais de malha fechada.

---

## Implementação

A implementação é organizada em módulos separados, responsáveis pelo controle, modelagem da planta, simulação e verificação.

### Módulo de Controle

O módulo de controle contém as implementações dos controladores PID de posição, PI de corrente e da arquitetura de controle em cascata.

Suas responsabilidades incluem:

- Inicialização dos controladores.
- Configuração dos ganhos.
- Execução em tempo discreto.
- Cálculo dos erros.
- Saturação das saídas.
- Gerenciamento dos estados integrais.
- Comportamento anti-windup.
- Integração entre os laços de posição e corrente.

### Módulo da Planta

O módulo da planta representa o sistema físico e sua interação em malha fechada com os controladores.

Suas responsabilidades incluem:

- Modelagem da dinâmica da planta.
- Execução das atualizações em tempo discreto.
- Conexão das saídas dos controladores ao modelo físico.
- Atualização dos estados do sistema.
- Disponibilização das variáveis de realimentação.

### Métricas e Avaliação

Os componentes de avaliação calculam indicadores de desempenho, incluindo:

- Erro final de rastreamento.
- Sobressinal.
- Tempo de acomodação.
- Corrente máxima.
- Tensão máxima.

Essas métricas são utilizadas para comparar os resultados das simulações com os requisitos estabelecidos.

---

## Estrutura do Repositório

O repositório está organizado nos seguintes diretórios principais:

```text
Model-Based-Design-for-CyberPhysical-Systems/
│
├── config/
│   └── Arquivos de configuração
│
├── generated/
│   └── Artefatos gerados
│
├── other/
│   └── Materiais complementares
│
├── scripts/
│   └── Scripts de simulação e avaliação
│
├── src/
│   ├── controller/
│   │   ├── pid_position.py
│   │   ├── pi_current.py
│   │   ├── cascade.py
│   │   └── metrics.py
│   │
│   └── plant/
│       └── closed_loop.py
│
├── tests/
│   └── Testes automatizados de verificação
│
├── .gitattributes
└── .gitignore
```

### Responsabilidade dos Diretórios

| Diretório | Descrição |
|---|---|
| `config/` | Armazena informações de configuração utilizadas pelo projeto. |
| `generated/` | Contém artefatos gerados durante o desenvolvimento. |
| `other/` | Armazena materiais complementares. |
| `scripts/` | Contém scripts utilizados para executar simulações e avaliar o comportamento do sistema. |
| `src/` | Contém a implementação principal do sistema. |
| `tests/` | Contém testes automatizados dos componentes implementados. |

### Principais Arquivos-fonte

| Arquivo | Responsabilidade |
|---|---|
| `src/controller/pid_position.py` | Implementação do controlador PID de posição. |
| `src/controller/pi_current.py` | Implementação do controlador PI de corrente. |
| `src/controller/cascade.py` | Integração dos laços de controle em cascata. |
| `src/controller/metrics.py` | Cálculo das métricas de desempenho do controle. |
| `src/plant/closed_loop.py` | Simulação da planta em malha fechada. |
| `scripts/simulate_cascade.py` | Execução da simulação do controle em cascata. |
| `scripts/evaluate_controller.py` | Avaliação do desempenho dos controladores. |
| `tests/test_cascade.py` | Testes automatizados da implementação do controle em cascata. |

---

## Simulação e Avaliação

O ambiente de simulação permite avaliar a arquitetura de controle sem exigir interação imediata com o hardware físico do braço robótico.

A simulação é utilizada para investigar a relação entre os parâmetros dos controladores e o comportamento do sistema.

### Principais Métricas de Avaliação

**Erro em Regime Permanente**

Mede a diferença entre a posição desejada e a posição final do sistema.

\[
e_{ss} = |r-y(\infty)|
\]

**Sobressinal**

Mede quanto a resposta do sistema ultrapassa sua referência desejada.

\[
M_p =
\frac{y_{max}-y_{ref}}{|y_{ref}|}
\times 100\%
\]

**Tempo de Acomodação**

Mede o tempo necessário para que a resposta entre e permaneça dentro da faixa de tolerância especificada.

**Corrente Máxima**

Mede o maior valor absoluto de corrente observado durante a simulação.

**Tensão Máxima**

Mede o maior valor absoluto do comando de tensão observado durante a simulação.

Essas métricas fornecem evidências quantitativas para a avaliação do sistema de controle.

---

## Verificação e Testes

Os testes automatizados são uma parte importante do fluxo de desenvolvimento.

O projeto utiliza testes para avaliar o comportamento dos componentes individuais de controle e sua integração.

A estratégia de verificação inclui:

- Testes de comportamento dos controladores.
- Testes da arquitetura em cascata.
- Verificação dos limites de saturação das saídas.
- Verificações de consistência numérica.
- Avaliação de desempenho baseada em simulação.

### Verificação Software-in-the-Loop (SIL)

O projeto inclui um procedimento de verificação Software-in-the-Loop (SIL).

A avaliação SIL registrada apresenta os seguintes resultados:

| Parâmetro | Resultado |
|---|---:|
| Ciclos executados | 2.000 |
| Diferença máxima | 0 |
| Tolerância numérica | \(10^{-9}\) |
| Status da verificação | APROVADO |

Esse resultado indica concordância numérica entre os caminhos de execução de software comparados nas condições avaliadas.

Entretanto, esse resultado isoladamente não comprova a segurança física do sistema nem a equivalência com a implementação em hardware.

---

## Resultados Experimentais

A avaliação do controlador em cascata produziu os seguintes resultados registrados:

| Métrica | Resultado Medido | Requisito | Status |
|---|---:|---:|---|
| Erro final de posição | 0,0201 rad | 0 rad | NÃO ATENDIDO |
| Sobressinal | 5,73% | ≤ 8% | ATENDIDO |
| Tempo de acomodação | 8,292 s | ≤ 0,300 s | NÃO ATENDIDO |
| Corrente máxima | 7,327 A | Dentro de ±8 A | ATENDIDO |
| Tensão máxima | 30,429 V | Dentro de ±48 V | ATENDIDO |

### Análise dos Resultados

A avaliação demonstra que o controlador em cascata atende a alguns dos requisitos de desempenho definidos, mas ainda não satisfaz todos os critérios de aceitação.

**CTRL-001 — Erro em Regime Permanente**

O erro final de posição foi de 0,0201 rad.

Embora o erro seja relativamente pequeno, o requisito estabelece que o erro em regime permanente deve ser zero. Portanto, o requisito não é considerado atendido.

**CTRL-002 — Sobressinal**

O sobressinal medido foi de 5,73%, valor inferior ao limite máximo permitido de 8%.

O requisito foi atendido no cenário avaliado.

**CTRL-003 — Tempo de Acomodação**

O tempo de acomodação medido foi de 8,292 segundos, consideravelmente superior ao limite máximo estabelecido de 300 milissegundos.

Esse requisito não foi atendido.

São necessários novos ajustes dos controladores e uma análise adicional da dinâmica do sistema.

**CTRL-004 — Limites Elétricos de Operação**

A corrente máxima medida foi de 7,327 A, abaixo do limite configurado de 8 A.

A tensão máxima medida foi de 30,429 V, abaixo do limite de 48 V.

Ambas as restrições elétricas foram atendidas no cenário de simulação avaliado.

### Avaliação Isolada do Laço de Corrente

Uma avaliação adicional do controlador de corrente isolado produziu os seguintes resultados:

| Métrica | Resultado |
|---|---:|
| Erro final de corrente | 0 A |
| Sobressinal | 0% |
| Tempo de acomodação | 22 ms |
| Corrente máxima | 4 A |
| Tensão máxima | 3,2 V |
| Duração da simulação | 0,5 s |

Esse teste isolado demonstra que o controlador de corrente consegue alcançar a resposta especificada nas condições avaliadas.

Entretanto, os resultados do laço isolado não devem ser interpretados como prova de que o sistema completo em cascata atende aos mesmos requisitos de desempenho.

---

## Rastreabilidade e Evidências

A rastreabilidade é um dos fundamentos do projeto.

Cada requisito de engenharia deve estar associado a:

1. Um identificador único.
2. Uma descrição do comportamento esperado.
3. Um critério de aceitação mensurável.
4. O componente de implementação correspondente.
5. Um procedimento de verificação.
6. O resultado observado.
7. Um status final de conformidade.

Essa estrutura permite justificar decisões de engenharia por meio de evidências reproduzíveis.

O projeto diferencia:

- Requisitos atendidos pela implementação avaliada.
- Requisitos que ainda não foram atendidos.
- Propriedades verificadas por testes de software.
- Propriedades que ainda necessitam de validação adicional.

Em particular, a aprovação dos testes de software não demonstra automaticamente que um sistema robótico físico é seguro para operação colaborativa.

---

## Limitações e Trabalhos Futuros

A implementação atual fornece uma base para o desenvolvimento baseado em modelos e para a avaliação por meio de simulações.

Entretanto, ainda existem melhorias necessárias.

### Desempenho do Controle

- Reduzir o erro de posição em regime permanente.
- Melhorar o tempo de acomodação do controlador em cascata.
- Investigar a interação entre os laços de posição e corrente.
- Avaliar a robustez dos controladores sob diferentes condições de operação.
- Investigar os efeitos de perturbações e variações de parâmetros.

### Engenharia de Segurança

- Implementar e verificar o comportamento de parada de emergência.
- Validar o requisito de remoção de torque em até 100 ms.
- Implementar a prevenção de reinicialização automática.
- Implementar e verificar o procedimento de reset de segurança.
- Avaliar a velocidade linear máxima permitida.
- Estabelecer evidências para os requisitos de segurança independentemente do desempenho nominal do controlador.

### Validação dos Modelos

- Melhorar a correspondência entre o modelo matemático e o sistema físico.
- Validar os parâmetros do modelo por meio de medições em hardware.
- Investigar a influência do tempo de amostragem e da discretização numérica.
- Avaliar os efeitos de ruído dos sensores e limitações dos atuadores.

### Verificação e Reprodutibilidade

- Expandir a cobertura dos testes automatizados.
- Adicionar cenários operacionais adicionais.
- Melhorar a geração e organização das evidências de verificação.
- Fortalecer a rastreabilidade entre requisitos e testes.
- Expandir a verificação Software-in-the-Loop quando apropriado.

Essas melhorias representam etapas importantes para a construção de um processo mais completo de garantia de engenharia.

---

## Tecnologias Utilizadas

O projeto utiliza as seguintes tecnologias e ferramentas de desenvolvimento:

| Tecnologia | Finalidade |
|---|---|
| Python 3.11 | Linguagem principal de implementação. |
| NumPy | Computação numérica e operações matemáticas. |
| SciPy | Computação científica e modelagem de sistemas, quando aplicável. |
| pytest | Execução de testes automatizados. |
| Modelos de espaço de estados em tempo discreto | Representação matemática da dinâmica do sistema. |
| Controle PID / PI | Arquitetura de controle em malha fechada. |
| Software-in-the-Loop (SIL) | Verificação em nível de software. |
| Git | Controle de versão e colaboração. |

---

## Instalação e Configuração

### Pré-requisitos

O ambiente de desenvolvimento utilizado no projeto inclui:

- Python 3.11.9.
- Windows AMD64.
- Git.
- Gerenciador de pacotes Python (`pip`).

### Clonar o Repositório

```bash
git clone https://github.com/Kallel181/Model-Based-Design-for-CyberPhysical-Systems.git

cd Model-Based-Design-for-CyberPhysical-Systems
```

### Criar um Ambiente Virtual

Windows:

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### Instalar Dependências

Instale as dependências especificadas na configuração de dependências do projeto, caso disponível.

Por exemplo, se o repositório possuir um arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Caso não exista um arquivo de dependências, instale os pacotes necessários para a implementação e para a execução dos testes.

### Executar as Simulações

Os principais scripts de simulação e avaliação estão localizados no diretório `scripts/`.

```bash
python scripts/simulate_cascade.py
```

Para avaliar o desempenho dos controladores:

```bash
python scripts/evaluate_controller.py
```

Esses scripts são destinados à execução dos respectivos fluxos de simulação e avaliação.

---

## Execução dos Testes

O projeto utiliza `pytest` para a execução de testes automatizados.

Para executar toda a suíte de testes a partir da raiz do repositório:

```bash
python -m pytest -v
```

Para executar individualmente os testes do controlador em cascata:

```bash
python -m pytest tests/test_cascade.py -v
```

A suíte de testes tem como objetivo verificar o comportamento esperado dos componentes implementados e sua integração.

---

## Escopo do Projeto

É importante distinguir o escopo atual do projeto dos requisitos necessários para um sistema robótico colaborativo completo.

O trabalho atual concentra-se em:

- Modelagem matemática do sistema.
- Implementação de controladores em tempo discreto.
- Controle de posição e corrente em cascata.
- Avaliação de desempenho baseada em simulação.
- Verificação em nível de software.
- Rastreabilidade de requisitos.

O projeto não afirma que a implementação atual está pronta para implantação em um ambiente físico de robótica colaborativa.

Em particular, a existência de limites de controle simulados não substitui mecanismos de segurança validados independentemente.

Uma avaliação de segurança completa exigiria atividades adicionais de verificação, incluindo validação em hardware, análise de falhas, testes de parada de emergência e avaliação sob condições representativas de operação.

O objetivo deste projeto é estabelecer uma base de engenharia reproduzível que possa apoiar essas atividades futuras.

---

## Contribuições

Este repositório foi desenvolvido como parte de um projeto acadêmico.

Sugestões, melhorias e discussões técnicas são bem-vindas.

Ao propor alterações, recomenda-se:

- Preservar a arquitetura modular.
- Manter os requisitos do sistema explícitos.
- Incluir testes automatizados para novas funcionalidades.
- Documentar alterações nos parâmetros dos controladores.
- Manter a rastreabilidade entre requisitos e evidências de verificação.

---

## Licença

Nenhuma licença foi especificada para este repositório.

Enquanto uma licença não for adicionada, aplicam-se as restrições padrão de direitos autorais sobre o conteúdo do repositório.

---

## Autor

**Kallel Fiori**

GitHub: [@Kallel181](https://github.com/Kallel181)

Repositório: [Model-Based Design for Cyber-Physical Systems](https://github.com/Kallel181/Model-Based-Design-for-CyberPhysical-Systems)

Contexto acadêmico: Model-Based Design for Cyber-Physical Systems.
