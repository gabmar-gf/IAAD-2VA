CREATE DATABASE IF NOT EXISTS FilmesDB;
USE FilmesDB;

CREATE TABLE Canal (
    num_canal INT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

INSERT INTO Canal (num_canal, nome) VALUES
(111, 'AXN'),
(222, 'HBO'),
(333, 'Cinemax'),
(444, 'TNT');

CREATE TABLE Filme (
    num_filme INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ano INT NOT NULL,
    duracao INT
);

INSERT INTO Filme (num_filme, nome, ano, duracao) VALUES
(90001, 'Avatar', 2022, 162),
(90002, 'Titanic', 1997, 194),
(90003, 'Star Wars', 2019, NULL),
(90004, 'Vingadores Ultimato', 2019, 180),
(90005, 'Lilo & Stitch', 2025, 108);

CREATE TABLE Exibicao (
    num_filme INT,
    num_canal INT,
    data_exibicao DATE,
    hora_exibicao TIME,
    PRIMARY KEY (num_filme, num_canal, data_exibicao, hora_exibicao),
    FOREIGN KEY (num_filme) REFERENCES Filme(num_filme),
    FOREIGN KEY (num_canal) REFERENCES Canal(num_canal)
);

INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) VALUES
(90001, 222, '2025-06-27', '14:00:00'),
(90003, 111, '2025-06-27', '19:45:00'),
(90002, 333, '2025-06-28', '09:30:00'),
(90004, 333, '2025-06-28', '20:30:00'),
(90005, 222, '2025-08-03', '16:20:00'),
(90005, 333, '2025-08-03', '16:20:00');

CREATE TABLE Elenco (
    num_filme INT NOT NULL,
    nome_ator VARCHAR(100) NOT NULL,
    protagonista BOOLEAN NOT NULL,
    PRIMARY KEY (num_filme, nome_ator),
    FOREIGN KEY (num_filme) REFERENCES Filme(num_filme)
);

INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES
(90002, 'Leonardo DiCaprio', 1),
(90002, 'Kate Winslet', 1),
(90002, 'Frances Fisher', 0),
(90002, 'Billy Zane', 0),
(90001, 'Sam Worthington', 1),
(90001, 'Zoe Saldana', 1),
(90003, 'Mark Hamill', 1),
(90003, 'Harrison Ford', 0);
