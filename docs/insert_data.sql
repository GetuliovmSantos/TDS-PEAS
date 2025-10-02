-- -----------------------------------------------------
-- Script de Inserção de Dados - SAEP DB
-- Autor: Getulio Vagner
-- Projeto: TDS-PEAS - Sistema de Controle de Estoque
-- Data: 01/10/2025
-- -----------------------------------------------------

USE `saep_db`;

-- -----------------------------------------------------
-- Inserções na tabela Usuario
-- -----------------------------------------------------
INSERT INTO `Usuario` (`nome`, `usuario`, `senha`) VALUES
('João Silva Santos', 'joao.silva', '123456'),
('Maria Oliveira Costa', 'maria.oliveira', '123456'),
('Carlos Eduardo Lima', 'carlos.eduardo', '123456'),
('Ana Paula Ferreira', 'ana.paula', '123456'),
('Roberto Machado', 'roberto.machado', '123456');

-- -----------------------------------------------------
-- Inserções na tabela Produto
-- -----------------------------------------------------
INSERT INTO `Produto` (`codigo`, `codigo_alternativo`, `nome`, `descricao`, `categoria`, `unidade_medida`, `preco`, `estoque_minimo`, `estoque_atual`, `aplicacao_veicular`) VALUES
('MT001', 'ALT001', 'Óleo Motor 5W30 Sintético', 'Óleo lubrificante sintético para motores modernos', 'Lubrificantes', 'L', 45.90, 10, 25, 'Honda Civic, Toyota Corolla, Nissan Sentra'),
('FR002', 'ALT002', 'Pastilha de Freio Dianteira', 'Pastilha de freio cerâmica de alta performance', 'Freios', 'UN', 89.50, 5, 15, 'VW Golf, Audi A3, Ford Focus'),
('FT003', 'ALT003', 'Filtro de Ar Esportivo', 'Filtro de ar de alto fluxo lavável', 'Filtros', 'UN', 125.00, 3, 8, 'Honda Civic Type R, Toyota GR Yaris'),
('PH004', 'ALT004', 'Farol LED Principal', 'Farol de LED com luz de circulação diurna', 'Iluminação', 'UN', 350.00, 2, 6, 'VW Jetta, Honda Accord, Toyota Camry'),
('SU005', 'ALT005', 'Amortecedor Traseiro', 'Amortecedor a gás pressurizado', 'Suspensão', 'UN', 180.75, 4, 12, 'Chevrolet Onix, Hyundai HB20, Ford Ka'),
('MT006', 'ALT006', 'Fluido de Freio DOT 4', 'Fluido sintético para sistemas de freio ABS', 'Fluidos', 'L', 28.90, 8, 20, 'Universal - Todos os veículos'),
('EL007', 'ALT007', 'Bateria 60Ah', 'Bateria automotiva livre de manutenção', 'Elétrica', 'UN', 295.00, 3, 9, 'Fiat Uno, Chevrolet Celta, Ford Fiesta');

-- -----------------------------------------------------
-- Inserções na tabela Movimentacao
-- -----------------------------------------------------
INSERT INTO `Movimentacao` (`idUsuario`, `idProduto`, `tipo_movimentacao`, `quantidade`, `data_movimentacao`) VALUES
-- Entradas de estoque
(1, 1, 'ENTRADA', 50, '2025-09-15'),
(2, 2, 'ENTRADA', 30, '2025-09-16'),
(3, 3, 'ENTRADA', 20, '2025-09-17'),
(1, 4, 'ENTRADA', 15, '2025-09-18'),
(4, 5, 'ENTRADA', 25, '2025-09-19'),
(5, 6, 'ENTRADA', 40, '2025-09-20'),
(2, 7, 'ENTRADA', 18, '2025-09-21'),

-- Saídas de estoque (vendas)
(3, 1, 'SAIDA', 25, '2025-09-22'),
(4, 2, 'SAIDA', 15, '2025-09-23'),
(5, 3, 'SAIDA', 12, '2025-09-24'),
(1, 4, 'SAIDA', 9, '2025-09-25'),
(2, 5, 'SAIDA', 13, '2025-09-26'),
(3, 6, 'SAIDA', 20, '2025-09-27'),
(4, 7, 'SAIDA', 9, '2025-09-28'),

-- Movimentações adicionais para histórico
(5, 1, 'ENTRADA', 15, '2025-09-29'),
(1, 3, 'ENTRADA', 10, '2025-09-30'),
(2, 5, 'SAIDA', 5, '2025-10-01');

-- -----------------------------------------------------
-- Consultas de verificação
-- -----------------------------------------------------

-- Verificar usuários criados
SELECT 'USUÁRIOS CRIADOS:' as Info;
SELECT idUsuario, nome, usuario FROM Usuario;

-- Verificar produtos criados
SELECT 'PRODUTOS CRIADOS:' as Info;
SELECT idProduto, codigo, nome, categoria, preco, estoque_atual FROM Produto;

-- Verificar movimentações criadas
SELECT 'MOVIMENTAÇÕES CRIADAS:' as Info;
SELECT 
    m.id_movimentacao,
    u.nome as usuario,
    p.nome as produto,
    m.tipo_movimentacao,
    m.quantidade,
    m.data_movimentacao
FROM Movimentacao m
JOIN Usuario u ON m.idUsuario = u.idUsuario
JOIN Produto p ON m.idProduto = p.idProduto
ORDER BY m.data_movimentacao DESC;

-- Verificar estoque atual calculado
SELECT 'RELATÓRIO DE ESTOQUE:' as Info;
SELECT 
    p.codigo,
    p.nome,
    p.estoque_atual,
    COALESCE(entradas.total_entrada, 0) as total_entradas,
    COALESCE(saidas.total_saida, 0) as total_saidas,
    (COALESCE(entradas.total_entrada, 0) - COALESCE(saidas.total_saida, 0)) as estoque_calculado
FROM Produto p
LEFT JOIN (
    SELECT idProduto, SUM(quantidade) as total_entrada
    FROM Movimentacao 
    WHERE tipo_movimentacao = 'ENTRADA'
    GROUP BY idProduto
) entradas ON p.idProduto = entradas.idProduto
LEFT JOIN (
    SELECT idProduto, SUM(quantidade) as total_saida
    FROM Movimentacao 
    WHERE tipo_movimentacao = 'SAIDA'
    GROUP BY idProduto
) saidas ON p.idProduto = saidas.idProduto;