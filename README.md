# ApexStock - Sistema de Inventário

![ApexStock em Execução](Imagem%20do%20Sistema%20em%20execução.png)

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

2. **Configure as credenciais do banco de dados:**
   
   Abra o arquivo `automacao_estoque.py` e localize as funções:
   - `criar_banco_se_nao_existe()` (linha ~18)
   - `conectar_mysql()` (linha ~69)
   
   Altere os seguintes parâmetros com as credenciais do seu servidor MySQL:
   ```python
   host='localhost',      # Mude para o IP/host do seu servidor
   user='root',           # Mude para seu usuário MySQL
   password='',           # Mude para sua senha MySQL
   database='empresa_db'  # Mantém o nome do banco
   ```
   
   **Exemplo:**
   ```python
   mysql.connector.connect(
       host='192.168.1.100',    # IP do servidor
       user='admin',             # Seu usuário
       password='sua_senha_aqui', # Sua senha
       database='empresa_db'
   )
   ```

3. Execute o banco de dados MySQL (XAMPP ou outro servidor local).

4. Inicie o sistema:
   ```bash
   python automacao_estoque.py
   ```

> **Nota**: O programa cria automaticamente o banco de dados `empresa_db` e as tabelas necessárias na primeira execução. Não é necessário rodar o script.sql manualmente.

---

## Sobre o arquivo `script.sql`

O arquivo `script.sql` é um **backup de segurança e documentação** dos comandos SQL que criam o banco de dados e as tabelas. Ele está incluído no projeto para:

1. **Backup manual**: Caso você queira criar o banco manualmente pelo MySQL Workbench ou terminal
2. **Documentação**: Deixa claro qual é a estrutura do banco de dados
3. **Portabilidade**: Se precisar restaurar o banco em outro servidor

**Você não precisa executá-lo** - o programa faz tudo automaticamente! 🚀

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
