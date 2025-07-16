-- 1. CRIAÇÃO E USO DO BANCO DE DADOS
-- -----------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS Programacoes_Filmes;
USE Programacoes_Filmes;

DROP TABLE IF EXISTS Exibicao;
DROP TABLE IF EXISTS Elenco;
DROP TABLE IF EXISTS Filme;
DROP TABLE IF EXISTS Canal;

-- 2. CRIAÇÃO DAS TABELAS PRINCIPAIS
-- -----------------------------------------------------------------------

CREATE TABLE Canal (
    num_canal INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE Filme (
    num_filme INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    ano INT,
    duracao INT
);

CREATE TABLE Elenco (
    num_filme INT,
    nome_ator VARCHAR(255) NOT NULL,
    protagonista BOOLEAN,
    PRIMARY KEY (num_filme, nome_ator),
    FOREIGN KEY (num_filme) REFERENCES Filme(num_filme) ON DELETE CASCADE
);

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


INSERT INTO Canal (nome) VALUES
('AXN'), ('HBO'), ('Cinemax'), ('TNT');

SET @axn_id = 1; 
SET @hbo_id = 2;
SET @cinemax_id = 3;
SET @tnt_id = 4;

INSERT INTO Filme (nome, ano, duracao) VALUES
('Avatar', 2022, 162),
('Titanic', 1997, 194),
('Star Wars', 2019, NULL),
('Vingadores Ultimato', 2019, 180),
('Lilo & Stitch', 2025, 108);

SET @avatar_id = 1; 
SET @titanic_id = 2;
SET @star_wars_id = 3;
SET @vingadores_id = 4;
SET @lilo_stitch_id = 5;

INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES
(@avatar_id, 'Sam Worthington', 1),
(@avatar_id, 'Zoe Saldaña', 1),
(@avatar_id, 'Sigourney Weaver', 0),
(@titanic_id, 'Leonardo DiCaprio', 1),
(@titanic_id, 'Kate Winslet', 1),
(@titanic_id, 'Billy Zane', 0),
(@titanic_id, 'Frances Fisher', 0),
(@star_wars_id, 'Daisy Ridley', 1),
(@star_wars_id, 'Adam Driver', 1),
(@star_wars_id, 'John Boyega', 0),
(@star_wars_id, 'Oscar Isaac', 0),
(@vingadores_id, 'Robert Downey Jr.', 1),
(@vingadores_id, 'Chris Evans', 1),
(@vingadores_id, 'Chris Hemsworth', 1),
(@vingadores_id, 'Scarlett Johansson', 0),
(@lilo_stitch_id, 'Daveigh Chase', 1),
(@lilo_stitch_id, 'Chris Sanders', 1),
(@lilo_stitch_id, 'Tia Carrere', 0);

INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) VALUES
(@avatar_id, @hbo_id, '2025-06-27', '14:00:00'),
(@star_wars_id, @axn_id, '2025-06-27', '19:45:00'),
(@titanic_id, @cinemax_id, '2025-06-28', '09:30:00'),
(@titanic_id, @cinemax_id, '2025-06-28', '20:30:00'),
(@lilo_stitch_id, @hbo_id, '2025-08-03', '16:20:00'),
(@lilo_stitch_id, @cinemax_id, '2025-08-03', '16:20:00');


-- 4. CRIAÇÃO DO TRIGGER (REGRA DE NEGÓCIO)
-- -----------------------------------------------------------------------

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
