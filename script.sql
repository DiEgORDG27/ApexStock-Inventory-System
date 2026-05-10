-- Criar um banco de dados chamado "empresa_db"
CREATE DATABASE IF NOT EXISTS empresa_db;
-- Usar o banco de dados criado
USE empresa_db;
-- Criar uma tabela chamada "inventario" com as colunas: id, Produto, Quantidade, Valor, DataEntrada, DataSaida, Fornecedor
CREATE TABLE IF NOT EXISTS inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Produto VARCHAR(255) NOT NULL,
    Quantidade INT NOT NULL,
    Valor DECIMAL(10, 2) NOT NULL,
    DataEntrada DATE NOT NULL,
    DataSaida DATE,
    Fornecedor VARCHAR(255) NOT NULL
);  