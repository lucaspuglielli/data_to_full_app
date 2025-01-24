# Plataforma de Análise de Dados Agropecuários

### Requisitos

Antes de configurar o ambiente, certifique-se de que as ferramentas abaixo estão instaladas:

1. **Python 3.8+**  
   - [Download Python](https://www.python.org/downloads/)  
   - **Nota para usuários Windows**: Durante a instalação, habilite a opção de adicionar Python ao PATH nas variáveis de ambiente na tela inicial do instalador.

2. **Docker**  
   - [Download Docker](https://docs.docker.com/get-started/get-docker/)  
   - Certifique-se de que o Docker esteja em execução antes de subir os serviços.

---

### Configuração do Ambiente

#### 1. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```plaintext
POSTGRES_USER=docker
POSTGRES_PASSWORD=docker
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=datamaster
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
FERNET_KEY=chave_de_fernet
SIGN_UP_PASSWORD=senha_de_convite
```

- **`POSTGRES_USER`**: Nome de usuário do PostgreSQL.  
- **`POSTGRES_PASSWORD`**: Senha do PostgreSQL.  
- **`POSTGRES_HOST`**: Host do PostgreSQL.  
- **`POSTGRES_PORT`**: Port do PostgreSQL.  
- **`POSTGRES_DB`**: Nome do banco de dados PostgreSQL.  
- **`REDIS_HOST`**: Host do Redis.  
- **`REDIS_PORT`**: Port do Redis.  
- **`REDIS_DB`**: Nome do banco de dados Redis.  
- **`FERNET_KEY`**: Chave para criptografia de senhas (use uma chave gerada pela biblioteca `cryptography`).  
- **`SIGN_UP_PASSWORD`**: Senha de convite para registro de novos usuários.  

---

#### 2. Executar Script de Inicialização

Execute o script `run.bat` para configurar o ambiente automaticamente. Ele realiza as seguintes etapas:

1. Criação de um ambiente virtual Python (`.venv`).
2. Ativação do ambiente virtual e instalação das dependências definidas em `requirements.txt`.
3. Inicialização dos serviços Docker (PostgreSQL e Redis).
4. Abertura do Jupyter Notebook com o arquivo `main.ipynb`.
5. Finalização dos serviços Docker ao encerrar o processo.

---

#### 3. Inicialização Manual

Se o script `run.bat` não puder ser executado, siga estas etapas manualmente:

##### Criar o Ambiente Virtual

```bash
python -m venv .venv
```

##### Ativar o Ambiente Virtual

Windows:
```bash
.venv\Scripts\activate
```

Mac OS/Linux:
```bash
source .venv/bin/activate
```

##### Instalar Dependências

```bash
pip install -r requirements.txt
```

##### Subir os Serviços Docker

**Nota:** Certifique-se de que o Docker esteja em execução antes de executar este comando.

```bash
docker-compose up -d
```

##### Abrir o Jupyter Notebook

Para acessar a interface padrão:
```bash
jupyter notebook "main.ipynb"
```

Para acessar a interface completa (JupyterLab):
```bash
jupyter-lab "main.ipynb"
```

##### Finalizar os Serviços Docker (Quando Encerrar a Aplicação)

```bash
docker-compose down
```

##### Desativar o Ambiente Virtual (Quando Encerrar a Aplicação)

```bash
deactivate
```

## I. Objetivo do Case

O objetivo deste case é desenvolver uma solução completa para manipulação, análise e armazenamento de dados relacionados ao setor agropecuário e rural. A solução deve ser modular, escalável e reprodutível, utilizando tecnologias modernas como Python, Docker e bancos de dados relacionais. Além disso, a aplicação deve permitir autenticação segura, integração com APIs externas e demonstração de funcionalidades interativas através de Jupyter Notebook.

---

## II. Arquitetura de Solução e Arquitetura Técnica

### Arquitetura de Solução

A solução é composta por três camadas principais, cada uma projetada para cumprir uma função específica:

1. **Camada de Apresentação**:
   - **Jupyter Notebook**: Interface principal para interação com os dados e demonstração das funcionalidades implementadas.
   - Exemplos práticos para ilustrar o uso do script auxiliar `helper.py`.

2. **Camada de Aplicação**:
   - **`helper.py`**: Script Python que contém a lógica de negócios, incluindo:
   - Autenticação de usuários com senhas criptografadas.
   - Manipulação de dados agropecuários utilizando APIs externas.
   - Integração com o banco de dados PostgreSQL para persistência de dados.

3. **Camada de Dados**:
   - **PostgreSQL**: Banco de dados relacional utilizado para armazenar dados processados e informações de usuários.
   - **Redis**: Configurado como sistema de cache para gerenciamento de sessão de usuário.

---

### Arquitetura Técnica

A arquitetura técnica define como os componentes da solução interagem para entregar as funcionalidades esperadas.

#### Componentes Principais:

- **Docker Compose**:
  - Gerencia os serviços de infraestrutura, como PostgreSQL e Redis, garantindo a portabilidade do ambiente.
- **Python**:
  - Linguagem utilizada para o desenvolvimento do script `helper.py`, que centraliza a lógica de negócios.
- **Jupyter Notebook**:
  - Ferramenta interativa para demonstrar o uso da aplicação e explorar os dados processados.
- **APIs Externas**:
  - Dados obtidos através de bibliotecas como `ipeadatapy`.

#### Fluxo de Execução:

1. O ambiente é inicializado utilizando o script `run.bat`, que realiza:
   - Configuração do ambiente virtual Python.
   - Instalação de dependências.
   - Inicialização dos serviços Docker.
   - Abertura do Jupyter Notebook para interação.
2. Usuário autentica e acessa os dados armazenados no banco PostgreSQL ou obtém novos dados via APIs externas.
3. Dados processados são demonstrados no Jupyter Notebook com exemplos práticos de uso.

#### Tecnologias Utilizadas:

- **Python 3.8+**: Lógica de aplicação e manipulação de dados.
- **Docker**: Infraestrutura escalável para banco de dados e cache.
- **PostgreSQL**: Banco de dados relacional para persistência.
- **Redis**: Gerenciamento de sessão do usuário.
- **Bibliotecas Python**: `pandas`, `sqlalchemy`, `cryptography`, `ipeadatapy`, entre outras.

---

## III. Explicação sobre o Case Desenvolvido

Este projeto fornece um ambiente integrado para trabalhar com dados agropecuários e rurais.  

### Funcionalidades Implementadas:

1. **Autenticação Segura**:
   - Sistema de login e registro utilizando PostgreSQL, senhas criptografadas com a biblioteca `cryptography` e gerenciamento de sessão utilizando Redis.
   - Suporte para múltiplos usuários e verificação de credenciais.

2. **Manipulação de Dados**:
   - Integração com APIs para obter dados atualizados.
   - Estruturação de dados em tabelas relacionais e manipulação com `pandas`.

3. **Interface Interativa**:
   - O `main.ipynb` fornece exemplos detalhados para explorar e visualizar os dados.
   - Explicação passo a passo para cada funcionalidade, incluindo acesso ao banco de dados e consultas personalizadas.

4. **Infraestrutura Automatizada**:
   - Uso de `Docker Compose` para configurar e gerenciar serviços como PostgreSQL e Redis.
   - Script `run.bat` para automação do setup do ambiente.

---

## IV. Melhorias e Considerações Finais

### Melhorias:

1. **Otimização de Performance**:
   - Implementar uso efetivo do Redis como cache para consultas frequentes, reduzindo o tempo de resposta.
   - Paralelizar operações de consulta e processamento de dados para melhorar a eficiência.

2. **Interface Amigável**:
   - Expandir o `main.ipynb` com mais exemplos interativos e visualizações gráficas usando bibliotecas como `matplotlib` ou `seaborn`.

3. **Documentação e Testes**:
   - Adicionar mais testes unitários para as demais funções no script `helper.py`.
   - Melhorar a documentação detalhando as APIs utilizadas e o formato dos dados esperados.

4. **Expansão de Funcionalidades**:
   - Implementar suporte para múltiplas fontes de dados.
   - Adicionar um painel interativo usando frameworks como `Dash` ou `Streamlit`.
   - Adicionar funções para requisitar e salvar todas as tabelas disponíveis nos catalogos e de homologação dos dados de todas as tabelas geradas.

5. **Aumento de Segurança**:
   - Definir requisitos minimos de segurança para criação de senha.

### Considerações Finais:

Este projeto demonstra como criar uma solução modular e reprodutível para manipulação de dados complexos. Sua arquitetura escalável permite fácil adaptação para diferentes casos de uso. Com melhorias incrementais, ele pode se tornar uma ferramenta ainda mais poderosa para análises.
