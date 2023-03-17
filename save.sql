-- MariaDB dump 10.19  Distrib 10.4.24-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: save
-- ------------------------------------------------------
-- Server version	10.4.24-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `conductores`
--

DROP TABLE IF EXISTS `conductores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conductores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `empresa` int(11) DEFAULT NULL,
  `activo` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conductores`
--

LOCK TABLES `conductores` WRITE;
/*!40000 ALTER TABLE `conductores` DISABLE KEYS */;
INSERT INTO `conductores` VALUES (1,'Alex Pocohuanca','ap@chama.pe',1,'Si'),(2,'Alonso Llap','al@chama.pe',1,'Si'),(3,'Juan Bouroncle','jb@movil.pe',2,'Si'),(4,'Franchescolli Anticona','fa@acvdo.pe',3,'Si'),(5,'Piero Zuloeta','pz@empresa.pe',4,'Si'),(6,'Pablo Cardenas','pabloc@chama.pe',1,'Si'),(7,'Lucas Donayre','lucasd@chama.pe',1,'Si'),(8,'Mario Hart','marioh@chama.pe',1,'Si'),(9,'Carlitos Castro','carlosc@movil.pe',2,'Si'),(10,'Astorga Chocolatada','tonho@chama.pe',1,'Si'),(11,'Christian Manrique','christian@movil.pe',2,'Si'),(12,'Carmine Corp','carmine@empresa.pe',4,'Si'),(13,'Martin Galvez','martin@empresa.pe',4,'Si'),(14,'Steven Quispe','steven@acvdo.pe',3,'Si');
/*!40000 ALTER TABLE `conductores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispositivos`
--

DROP TABLE IF EXISTS `dispositivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dispositivos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `empresa` int(11) DEFAULT NULL,
  `conductor` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispositivos`
--

LOCK TABLES `dispositivos` WRITE;
/*!40000 ALTER TABLE `dispositivos` DISABLE KEYS */;
INSERT INTO `dispositivos` VALUES (1,4,5),(2,2,3),(3,1,1),(4,1,2),(5,3,4),(6,2,9),(7,1,8),(8,2,11),(9,4,12),(10,4,13),(11,3,4),(12,3,14);
/*!40000 ALTER TABLE `dispositivos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empresas`
--

DROP TABLE IF EXISTS `empresas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empresas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `empresa` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresas`
--

LOCK TABLES `empresas` WRITE;
/*!40000 ALTER TABLE `empresas` DISABLE KEYS */;
INSERT INTO `empresas` VALUES (1,'Chama'),(2,'Movil'),(3,'Acvdo'),(4,'Empresa');
/*!40000 ALTER TABLE `empresas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incidentes`
--

DROP TABLE IF EXISTS `incidentes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `incidentes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ID_dispositivo` int(11) DEFAULT NULL,
  `tipo_incidente` varchar(50) NOT NULL,
  `max_vel` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incidentes`
--

LOCK TABLES `incidentes` WRITE;
/*!40000 ALTER TABLE `incidentes` DISABLE KEYS */;
INSERT INTO `incidentes` VALUES (1,1,'giro_brusco',56),(2,1,'frenado_brusco',56),(3,2,'exceso_vel',89),(4,3,'exceso_vel',89),(5,3,'exceso_vel',89),(6,4,'exceso_vel',89),(7,4,'exceso_vel',89),(8,4,'exceso_vel',109),(9,4,'giro_brusco',109),(10,4,'giro_brusco',209),(11,4,'giro_brusco',209),(12,4,'giro_brusco',209),(13,4,'giro_brusco',209),(14,4,'frenado_brusco',43),(15,3,'giro_brusco',109),(16,3,'giro_brusco',109),(17,3,'giro_brusco',109),(18,3,'giro_brusco',109),(19,3,'giro_brusco',109),(20,3,'giro_brusco',109),(21,3,'giro_brusco',109),(22,3,'giro_brusco',109),(23,3,'exceso_vel',89),(24,3,'exceso_vel',89),(25,4,'exceso_vel',89),(26,4,'exceso_vel',89),(27,4,'exceso_vel',89),(28,4,'exceso_vel',89),(29,6,'exceso_vel',19),(30,6,'exceso_vel',200),(31,6,'giro_brusco',200),(32,6,'giro_brusco',200),(33,7,'giro_brusco',200),(34,7,'giro_brusco',200),(35,7,'frenado_brusco',140),(36,7,'frenado_brusco',140),(37,7,'exceso_vel',140),(38,7,'acel_brusca',191),(39,8,'acel_brusca',191),(40,8,'exceso_vel',140),(41,8,'frenado_brusco',191),(42,8,'acel_brusca',191),(43,8,'acel_brusca',191),(44,8,'acel_brusca',191),(45,9,'acel_brusca',191),(46,9,'frenado_brusco',121),(47,9,'frenado_brusco',121),(48,9,'frenado_brusco',121),(49,9,'exceso_vel',221),(50,9,'exceso_vel',321),(51,9,'exceso_vel',129),(52,10,'exceso_vel',129),(53,10,'exceso_vel',228),(54,10,'exceso_vel',143),(55,10,'frenado_brusco',143),(56,10,'frenado_brusco',143),(57,10,'frenado_brusco',143),(58,11,'exceso_vel',228),(59,11,'exceso_vel',228),(60,11,'exceso_vel',228),(61,11,'exceso_vel',228),(62,11,'acel_brusca',228),(63,11,'acel_brusca',228),(64,11,'acel_brusca',218),(65,11,'acel_brusca',218),(66,12,'acel_brusca',218),(67,12,'acel_brusca',211),(68,12,'frenado_brusco',224),(69,12,'frenado_brusco',224),(70,12,'frenado_brusco',224),(71,12,'exceso_vel',214),(72,12,'exceso_vel',212),(73,12,'exceso_vel',122),(74,12,'giro_brusco',122),(75,12,'giro_brusco',122),(76,12,'giro_brusco',122),(77,14,'exceso_vel',212),(78,14,'exceso_vel',212),(79,14,'exceso_vel',212),(80,14,'exceso_vel',212),(81,12,'exceso_vel',212),(82,12,'exceso_vel',212),(83,12,'exceso_vel',212),(84,12,'exceso_vel',212);
/*!40000 ALTER TABLE `incidentes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `names` varchar(50) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `account` varchar(50) DEFAULT NULL,
  `company` int(11) DEFAULT NULL,
  `position` varchar(50) DEFAULT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `country` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'Carmen Gerrard','carmen@123.com','manager',3,'Programmer','carmen','$2b$12$13LFc/1TnhT2q6L97we0a.FlC8XkOqcy7hNwGEehbaIZohIQo9QgW','Palau'),(2,'Sample','sample@sample.com','manager',2,'Enginneering','sample','$2b$12$13LFc/1TnhT2q6L97we0a.NeLPVYPY1At7WK6gEUVXaz.9FSlJe72','Reunion'),(3,'chamo','chamo@chamos.com','manager',1,'Programmer','chamo','$2b$12$Xe7K91nSMKkDgRzwX4sKoO77MzY/hlmWeNuz1gSZg33FxOuBHgUDa','Saudi Arabia'),(4,'siracevedo','air@acevedo.com','manager',3,'Enginneering','siracevedo','$2b$12$uUYio.mJCbNYAWybCFAar.4AAGhSV69M/MCQdFkrb/HTYm51ouxAi','Northern Mariana Islands'),(5,'empresario','empresario@empresa.com','manager',4,'Programmer','empresario','$2b$12$tlaD41Su7lstQSz654YRFeTQOPPXAhXnJ6OzjK/.ugE7aLXr5xfoO','Norfolk Island'),(6,'Alexander Astorga','aastorga@gmail.com','admin',1,'Programmer','adminadmin','$2b$12$cZr9pVMIPv7kll9tS47kTOw5a6Gy8p8j4VbsztMPgjSoSnnmCA3u.','Niger');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-30  3:43:53
