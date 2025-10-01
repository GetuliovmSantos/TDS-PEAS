-- -----------------------------------------------------
-- Schema saep_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `saep_db` ;

-- -----------------------------------------------------
-- Schema saep_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `saep_db` DEFAULT CHARACTER SET utf8 ;
USE `saep_db` ;

-- -----------------------------------------------------
-- Table `saep_db`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `saep_db`.`Usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `usuario` VARCHAR(50) NOT NULL,
  `senha` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`idUsuario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `saep_db`.`Produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `saep_db`.`Produto` (
  `idProduto` INT NOT NULL AUTO_INCREMENT,
  `codigo` VARCHAR(50) NOT NULL,
  `codigo_alternativo` VARCHAR(50) NULL,
  `nome` VARCHAR(150) NOT NULL,
  `descricao` TEXT NULL,
  `categoria` VARCHAR(50) NULL,
  `unidade_medida` VARCHAR(20) NULL,
  `preco` DECIMAL(10,2) NULL,
  `estoque_minimo` INT NULL,
  `estoque_atual` INT NULL,
  `aplicacao_veicular` VARCHAR(200) NULL,
  PRIMARY KEY (`idProduto`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `saep_db`.`Movimentacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `saep_db`.`Movimentacao` (
  `id_movimentacao` INT NOT NULL AUTO_INCREMENT,
  `idUsuario` INT NOT NULL,
  `idProduto` INT NOT NULL,
  `tipo_movimentacao` ENUM('ENTRADA', 'SAIDA') NOT NULL,
  `quantidade` INT NOT NULL,
  `data_movimentacao` DATE NOT NULL,
  PRIMARY KEY (`id_movimentacao`),
  CONSTRAINT `fk_Movimentacao_Usuario`
    FOREIGN KEY (`idUsuario`)
    REFERENCES `saep_db`.`Usuario` (`idUsuario`),
  CONSTRAINT `fk_Movimentacao_Produto1`
    FOREIGN KEY (`idProduto`)
    REFERENCES `saep_db`.`Produto` (`idProduto`))
ENGINE = InnoDB;