# 🔬 Rayyan & Scopus Smart Screener

[![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Framework-Playwright-green.svg)](https://playwright.dev/python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma ferramenta de automação robótica (RPA) desenvolvida em Python e Playwright para otimizar e acelerar a etapa de **triagem (screening)** de artigos científicos dentro da plataforma Rayyan, com enriquecimento de dados em tempo real direto do Scopus.

O sistema analisa os artigos dinamicamente e toma decisões de **Include** ou **Exclude** baseando-se estritamente em critérios mecânicos de palavras-chave, gerando um relatório completo de auditoria em `.csv`.

---

## 📑 Índice

- [Funcionalidades](#-funcionalidades)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Fluxo de Funcionamento](#-fluxo-de-funcionamento)
- [Critérios de Inclusão](#-critérios-de-inclusão)
- [Pré-requisitos e Instalação](#-pré-requisitos-e-instalação)
- [Como Usar](#-como-usar)
- [Estrutura do Relatório (CSV)](#-estrutura-do-relatório-csv)

---

## 🚀 Funcionalidades

- **Triagem 100% Automática:** Executa os cliques de inclusão ou exclusão diretamente na interface do Rayyan.
- **Navegação Dinâmica (Anti-Crash):** Utiliza técnicas avançadas de simulação de teclado (`ArrowDown`) para contornar o _Virtual Scrolling_ do Rayyan, permitindo processar mais de 1000 artigos continuamente sem perda de performance.
- **Integração Híbrida com Scopus:** Identifica o link institucional do Scopus dentro do Rayyan, extrai os metadados profundos (Abstract completo, termos MeSH e EMTREE) e fecha a aba de forma limpa.
- **Sistema de Salvamento Incremental (Autosave):** Grava os resultados linha por linha. Se a automação for interrompida, ela continuará exatamente de onde parou, sem duplicar ou perder dados.
- **Transparência Científica:** Gera justificativas detalhadas no log e no arquivo de saída explicando quais termos foram encontrados em cada artigo.

---

## 🏗️ Arquitetura do Projeto

O sistema foi desenhado seguindo boas práticas de engenharia de software, dividindo as responsabilidades em módulos isolados:

- `config.py`: Centraliza as variáveis globais, URLs e dicionários de palavras-chave por categoria biológica/médica.
- `classifier.py`: Contém o motor lógico e as regras de correspondência textual do sistema.
- `scraper.py`: Abstrai toda a complexidade do Playwright para raspagem e interação com os portais Rayyan e Scopus.
- `main.py`: O orquestrador central que gerencia o loop principal, o histórico do CSV e a interface do terminal.

---

## 🔄 Fluxo de Funcionamento

[ Iniciar Script ]
↓
[ Carregar resultado.csv (Evita Retrabalho) ]
↓
[ Abrir Rayyan & Aguardar Login Manual ]
↓
┌───> [ Mapear Artigo Atual na Tela ]
│ ↓
│ [ Extrair Texto do Rayyan + Capturar Link Scopus ]
│ ↓
│ [ Abrir Scopus -> Puxar Texto Inteiro (MeSH/Emtree) -> Fechar Aba ]
│ ↓
│ [ Classificar Texto (Busca Literal de Palavras-Chave) ]
│ ↓
│ [ Executar Clique Automático no Rayyan (Include/Exclude) ]
│ ↓
│ [ Gravar Linha com Justificativa no resultado.csv ]
│ ↓
│ [ Pressionar 'ArrowDown' para Mudar de Artigo ]
└───── Existe próximo artigo? (Alvo: 1059)

---

## 🎯 Critérios de Inclusão

O artigo recebe a sugestão de **INCLUDE** se contiver **pelo menos um** dos termos mapeados abaixo:

| Categoria                    | Termos Monitorados                                                                                                                                       |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Animais**                  | `animal experiment`, `animal model`, `animal`, `mouse`, `mice`, `rat`, `rats`, `guinea pig`, `rabbit`                                                    |
| **Antioxidantes**            | `antioxidant`, `antioxidants`, `vitamin c`, `vitamin e`, `curcumin`, `quercetin`, `resveratrol`, `n-acetylcysteine`, `acetylcysteine`, `rosmarinic acid` |
| **Estresse Oxidativo**       | `oxidative stress`, `reactive oxygen species`, `ros`, `free radicals`, `lipid peroxidation`, `redox balance`                                             |
| **Marcadores Inflamatórios** | `tnf-alpha`, `tnf`, `il-1`, `il-6`, `il-10`, `nf-kb`, `cytokine`, `inflammation`, `inflammatory marker`                                                  |
| **Cóclea**                   | `cochlea`, `cochlear`, `hair cell`, `auditory hair cell`, `hearing loss`, `ototoxicity`                                                                  |
| **Grupo Controle**           | `control group`, `controlled study`, `wild type`, `vehicle group`, `placebo`                                                                             |

---

## 📦 Pré-requisitos e Instalação

### 1. Clonar o repositório ou criar a pasta do projeto

Certifique-se de ter todos os 4 arquivos python (`config.py`, `classifier.py`, `scraper.py`, `main.py`) no mesmo diretório.

### 2. Instalar as dependências do Python (3.12 ou superior)

```bash
pip install playwright pandas
3. Instalar os binários do navegador Chrome para o PlaywrightBashplaywright install chrome
🎮 Como UsarExecute o script principal pelo terminal:Bashpython main.py
A janela do navegador Chrome se abrirá de forma automatizada.Faça o login manualmente na sua conta do Rayyan e entre na revisão desejada (Tela de Screening).Clique em cima do primeiro artigo da lista lateral esquerda (para que ele fique selecionado/azul).Volte ao terminal e pressione ENTER.Atenção (Primeiro acesso ao Scopus): Quando o primeiro artigo que contém o link do Scopus for aberto em uma nova aba, o terminal fará uma pausa. Faça o seu login institucional (CAPES/Universidade) no Scopus para liberar o acesso aos resumos cheios. Volte ao terminal e aperte ENTER definitivo.O robô assumirá o controle total, alternando os artigos, clicando nas decisões e salvando o progresso.📊 Estrutura do Relatório (CSV)O arquivo resultado.csv gerado de forma incremental utiliza a codificação utf-8-sig (perfeitamente compatível com o Microsoft Excel) e possui o seguinte formato:TítuloDecisãoConfiançaMotivoURL ScopusFoxO3a plays a key role...INCLUDE100% Automático (Palavras-Chave)Termos encontrados em: Animais, Cóclea.https://www.scopus.com/...Effects of noise exposure...EXCLUDE100% Automático (Palavras-Chave)Nenhum termo correspondente encontrado no Scopus/Rayyan.
```
