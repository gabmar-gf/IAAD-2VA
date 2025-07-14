-- 1. CRIAÇÃO E USO DO BANCO DE DADOS
-- -----------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS Programacoes_Filmes;
USE Programacoes_Filmes;


-- 2. CRIAÇÃO DAS TABELAS PRINCIPAIS
-- -----------------------------------------------------------------------

-- Tabela Canal
CREATE TABLE Canal (
    num_canal INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Tabela Filme
CREATE TABLE Filme (
    num_filme INT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    ano INT,
    duracao INT
);

-- Tabela Elenco
CREATE TABLE Elenco (
    num_filme INT,
    nome_ator VARCHAR(255) NOT NULL,
    protagonista BOOLEAN,
    PRIMARY KEY (num_filme, nome_ator),
    FOREIGN KEY (num_filme) REFERENCES Filme(num_filme) ON DELETE CASCADE
);

-- Tabela Exibicao
CREATE TABLE Exibicao (
    num_filme INT,
    num_canal INT,
    data_exibicao DATE,
    hora_exibicao TIME,
    PRIMARY KEY (num_filme, num_canal, data_exibicao, hora_exibicao),
    FOREIGN KEY (num_filme) REFERENCES Filme(num_filme) ON DELETE CASCADE,
    FOREIGN KEY (num_canal) REFERENCES Canal(num_canal) ON DELETE CASCADE
);


-- 3. POPULAÇÃO DAS TABELAS (INSERÇÃO DE DADOS)
-- -----------------------------------------------------------------------

-- Populando a Tabela Canal
INSERT INTO Canal (num_canal, nome) VALUES
(111, 'AXN'),
(222, 'HBO'),
(333, 'Cinemax'),
(444, 'TNT');

-- Populando a Tabela Filme
INSERT INTO Filme (num_filme, nome, ano, duracao) VALUES
(90001, 'Avatar', 2022, 162),
(90002, 'Titanic', 1997, 194),
(90003, 'Star Wars', 2019, NULL),
(90004, 'Vingadores Ultimato', 2019, 180),
(90005, 'Lilo & Stitch', 2025, 108);

-- Populando a Tabela Elenco
INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES
(90001, 'Sam Worthington', 1),
(90001, 'Zoe Saldaña', 1),
(90001, 'Sigourney Weaver', 0),
(90002, 'Leonardo DiCaprio', 1),
(90002, 'Kate Winslet', 1),
(90002, 'Billy Zane', 0),
(90002, 'Frances Fisher', 0),
(90003, 'Daisy Ridley', 1),
(90003, 'Adam Driver', 1),
(90003, 'John Boyega', 0),
(90003, 'Oscar Isaac', 0),
(90004, 'Robert Downey Jr.', 1),
(90004, 'Chris Evans', 1),
(90004, 'Chris Hemsworth', 1),
(90004, 'Scarlett Johansson', 0),
(90005, 'Daveigh Chase', 1),
(90005, 'Chris Sanders', 1),
(90005, 'Tia Carrere', 0);

-- Populando a Tabela Exibicao
INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) VALUES
(90001, 222, '2025-06-27', '14:00:00'),
(90003, 111, '2025-06-27', '19:45:00'),
(90002, 333, '2025-06-28', '09:30:00'),
(90002, 333, '2025-06-28', '20:30:00'),
(90005, 222, '2025-08-03', '16:20:00'),
(90005, 333, '2025-08-03', '16:20:00');


-- 4. CRIAÇÃO DO TRIGGER (REGRA DE NEGÓCIO)
-- -----------------------------------------------------------------------

-- Trigger: Validação de intervalo de horário de exibição
DELIMITER $$
CREATE TRIGGER trg_valida_intervalo_exibicao
BEFORE INSERT ON Exibicao
FOR EACH ROW
BEGIN
    DECLARE conflitos INT DEFAULT 0;

    SELECT COUNT(*) INTO conflitos
    FROM Exibicao
    WHERE
        num_canal = NEW.num_canal
        AND data_exibicao = NEW.data_exibicao
        AND ABS(TIMESTAMPDIFF(MINUTE, hora_exibicao, NEW.hora_exibicao)) < 240;

    IF conflitos > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ERRO: Já existe uma exibição agendada para este canal com menos de 4 horas de intervalo neste dia.';
    END IF;
END$$
DELIMITER ;