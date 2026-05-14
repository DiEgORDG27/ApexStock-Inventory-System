# ApexStock - Sistema de Inventário

O ApexStock é uma solução de gerenciamento de inventário desenvolvida para automatizar a importação de dados, a atualização de estoque e a visualização de produtos em um fluxo simples.

---

## Tecnologias

* Python 3.x
* Pandas
* Openpyxl
* MySQL Connector
* CustomTkinter
* Tkinter
* XAMPP / MySQL Server

---

## O que o sistema faz

- Importa dados de CSV e Excel
- Limpa duplicatas e padroniza datas
- Insere produtos no banco MySQL
- Mostra inventário em tabela com filtros
- Exibe alerta de baixo estoque
- Permite cadastro manual de produto e fornecedor
- Exporta relatórios em CSV e Excel
- Atualiza a interface automaticamente após add/editar/excluir dados
- Permite edição de quantidade em massa com senha de administrador
- Permite exclusão de produtos selecionados e fornecedores

---

## Como usar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute o banco de dados MySQL (XAMPP ou outro servidor local).
3. Rode o script de criação da tabela:
   ```bash
   mysql -u root < script.sql
   ```

4. Inicie o sistema:
   ```bash
   python automacao_estoque.py
   ```

---

## Abas do sistema

- Importar: escolhe CSV e Excel, processa e envia para o banco.
- Visualizar: filtra e mostra todos os produtos.
- Baixo Estoque: alerta itens com menos de 20 unidades.
- Fornecedores: lista fornecedores e permite abrir o cadastro com senha.

---

## Dicas

- Senha admin pra editar fornecedores: 12345 (senha de exemplo)
- Arquivos CSV/Excel precisam ter colunas: Produto, Quantidade, Valor, Data de Entrada, Data de Saída, Fornecedor
- Pra ícone personalizado, adiciona icone.ico na pasta e descomenta a linha no código

---

## Senha de acesso

- Senha para abrir o fornecedor: `12345`(senha de exemplo)

> Importante: em um projeto real use variáveis de ambiente. Para este portfólio, a senha é apenas um exemplo.

---

## Banco de dados

Tabela `inventario`:

- `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `Produto` (VARCHAR(255), NOT NULL)
- `Quantidade` (INT, NOT NULL)
- `Valor` (DECIMAL(10,2), NOT NULL)
- `DataEntrada` (DATE, NOT NULL)
- `DataSaida` (DATE)
- `Fornecedor` (VARCHAR(255), NOT NULL)

---

## Observações

- A interface usa tema escuro.
- A janela de importação/exportação abre centralizada.
- É possível adicionar produtos e fornecedores manualmente.
- O projeto está pronto para rodar localmente.

---

## 📝 Notas de Desenvolvimento

- Interface responsiva e moderna com ícones emoji.
- Código modular com funções separadas para cada operação.
- Suporte a grandes volumes de dados com tabelas otimizadas.

---
