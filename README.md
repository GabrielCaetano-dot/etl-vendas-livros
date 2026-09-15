# ETL - Vendas de Livrarias

Pipeline de Extração, Transformação e Carga (ETL) que processa dados de vendas de uma rede fictícia de livrarias, aplicando regras de negócio e carregando o resultado em um banco PostgreSQL.

Este projeto é baseado no exercício prático "Produção de Alimentos" do curso DSA - Fundamentos de Engenharia de Dados, adaptado para um cenário próprio (vendas de livros), com mais entidades e regras de negócio, e usando ferramentas diferentes (pandas + PostgreSQL, em vez de inserts manuais + SQLite).

## Sobre os dados

O arquivo de origem (`vendas_livrarias.csv`) contém registros de vendas com as colunas:

| Coluna | Descrição |
|---|---|
| `livro` | Título do livro vendido |
| `categoria` | Categoria do livro (Ficção, Não-Ficção, Tecnologia) |
| `filial` | Filial onde a venda ocorreu |
| `quantidade_vendida` | Quantidade de unidades vendidas |
| `preco_unitario` | Preço de venda por unidade (formato `R$ 00,00`) |
| `custo_unitario` | Custo por unidade (formato `R$ 00,00`) |
| `data_venda` | Data da venda (formato `DD/MM/AAAA`) |

## Regras de negócio implementadas

- **Tratamento de valores ausentes:** campos descritivos (`categoria`, `filial`) sem valor são preenchidos com `"Não Informado"`, preservando a venda na análise. Já campos essenciais ao cálculo (`preco_unitario`, `custo_unitario`, `quantidade_vendida`, `data_venda`) descartam a linha quando ausentes, já que não há como estimar esses valores sem distorcer o resultado financeiro.
- **Padronização numérica:** conversão dos valores monetários do formato brasileiro (`"R$ 49,90"`) para float.
- **Padronização de data:** conversão de `data_venda` de string (`DD/MM/AAAA`) para `datetime`.
- **Remoção de duplicatas:** vendas idênticas (mesmo livro, filial e data) são removidas, mantendo apenas o primeiro registro.
- **Enriquecimento:** cálculo de `receita_total` (quantidade × preço) e `margem_lucro` ((preço − custo) × quantidade), além de um alerta booleano `alerta_prejuizo` para vendas com margem negativa.
- **Filtro de carga:** apenas vendas com `quantidade_vendida > 5` são carregadas no banco de destino.

## Tecnologias utilizadas

- Python
- pandas
- SQLAlchemy
- PostgreSQL
- python-dotenv

## Estrutura do projeto

```
etl-vendas-livros/
├── vendas_livrarias.csv
├── pipeline.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

## Como executar

### Pré-requisitos

- Python 3.10+
- Um banco PostgreSQL disponível (local, ou um serviço gerenciado como Neon/Supabase)

### Passo a passo

1. Clone o repositório:
```bash
git clone https://github.com/GabrielCaetano-dot/etl-vendas-livros.git
cd etl-vendas-livros
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto (use `.env.example` como referência) com as credenciais do seu banco:
```
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco
```

5. Execute o pipeline:
```bash
python pipeline.py
```

## Schema da tabela de destino (`vendas`)

| Coluna | Tipo |
|---|---|
| livro | TEXT |
| categoria | TEXT |
| filial | TEXT |
| quantidade_vendida | INTEGER |
| preco_unitario | FLOAT |
| custo_unitario | FLOAT |
| data_venda | DATE |
| receita_total | FLOAT |
| margem_lucro | FLOAT |
| alerta_prejuizo | BOOLEAN |

## Autor

Gabriel Caetano
