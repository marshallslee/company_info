````mysql
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema company_info
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema company_info
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `company_info` DEFAULT CHARACTER SET utf8 ;
USE `company_info` ;

-- -----------------------------------------------------
-- Table `company_info`.`company_group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `company_info`.`company_group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `company_info`.`language`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `company_info`.`language` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `code_UNIQUE` (`code` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `company_info`.`company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `company_info`.`company` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `company_group_id` INT NOT NULL,
  `language_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_company_company_group1_idx` (`company_group_id` ASC),
  INDEX `fk_company_language1_idx` (`language_id` ASC),
  CONSTRAINT `fk_company_company_group1`
    FOREIGN KEY (`company_group_id`)
    REFERENCES `company_info`.`company_group` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_company_language1`
    FOREIGN KEY (`language_id`)
    REFERENCES `company_info`.`language` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `company_info`.`tag_group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `company_info`.`tag_group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `tag_code_UNIQUE` (`name` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `company_info`.`tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `company_info`.`tag` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `language_id` INT NOT NULL,
  `tag_group_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tag_language_idx` (`language_id` ASC),
  INDEX `fk_tag_tag_group1_idx` (`tag_group_id` ASC),
  CONSTRAINT `fk_tag_language`
    FOREIGN KEY (`language_id`)
    REFERENCES `company_info`.`language` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tag_tag_group1`
    FOREIGN KEY (`tag_group_id`)
    REFERENCES `company_info`.`tag_group` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `company_info`.`company_tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `company_info`.`company_tag` (
  `company_group_id` INT NOT NULL,
  `tag_group_id` INT NOT NULL,
  INDEX `fk_company_tag_tag_group1_idx` (`tag_group_id` ASC),
  INDEX `fk_company_tag_company_group1_idx` (`company_group_id` ASC),
  PRIMARY KEY (`company_group_id`, `tag_group_id`),
  CONSTRAINT `fk_company_tag_company_group1`
    FOREIGN KEY (`company_group_id`)
    REFERENCES `company_info`.`company_group` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_company_tag_tag_group1`
    FOREIGN KEY (`tag_group_id`)
    REFERENCES `company_info`.`tag_group` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


````
