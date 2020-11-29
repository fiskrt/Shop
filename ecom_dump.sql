-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: Ecom1
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Admin`
--

DROP TABLE IF EXISTS `Admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Admin` (
  `idAdmin` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idAdmin`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Admin`
--

LOCK TABLES `Admin` WRITE;
/*!40000 ALTER TABLE `Admin` DISABLE KEYS */;
INSERT INTO `Admin` VALUES (1,'admino','pass');
/*!40000 ALTER TABLE `Admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Basket_Entry`
--

DROP TABLE IF EXISTS `Basket_Entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Basket_Entry` (
  `idBasket_Entry` int NOT NULL AUTO_INCREMENT,
  `quantity` int DEFAULT NULL,
  `idProduct` int NOT NULL,
  `idUser` int NOT NULL,
  PRIMARY KEY (`idBasket_Entry`,`idProduct`,`idUser`),
  KEY `fk_Basket_entry_Product1_idx` (`idProduct`),
  KEY `fk_Basket_entry_User1_idx` (`idUser`),
  CONSTRAINT `fk_Basket_entry_Product1` FOREIGN KEY (`idProduct`) REFERENCES `Product` (`idProduct`),
  CONSTRAINT `fk_Basket_entry_User1` FOREIGN KEY (`idUser`) REFERENCES `User` (`idUser`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Basket_Entry`
--

LOCK TABLES `Basket_Entry` WRITE;
/*!40000 ALTER TABLE `Basket_Entry` DISABLE KEYS */;
/*!40000 ALTER TABLE `Basket_Entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order_History`
--

DROP TABLE IF EXISTS `Order_History`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Order_History` (
  `idOrder` int NOT NULL AUTO_INCREMENT,
  `idSold_Product` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`idOrder`),
  KEY `fk_Order_History_Sold_Product1_idx` (`idSold_Product`),
  CONSTRAINT `fk_Order_History_Sold_Product1` FOREIGN KEY (`idSold_Product`) REFERENCES `Sold_Product` (`idSold_Product`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order_History`
--

LOCK TABLES `Order_History` WRITE;
/*!40000 ALTER TABLE `Order_History` DISABLE KEYS */;
INSERT INTO `Order_History` VALUES (2,2,5),(3,2,5),(4,1,25);
/*!40000 ALTER TABLE `Order_History` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product` (
  `idProduct` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `description` mediumtext,
  `Brand` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idProduct`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product`
--

LOCK TABLES `Product` WRITE;
/*!40000 ALTER TABLE `Product` DISABLE KEYS */;
/*!40000 ALTER TABLE `Product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sold_Product`
--

DROP TABLE IF EXISTS `Sold_Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sold_Product` (
  `idSold_Product` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`idSold_Product`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sold_Product`
--

LOCK TABLES `Sold_Product` WRITE;
/*!40000 ALTER TABLE `Sold_Product` DISABLE KEYS */;
INSERT INTO `Sold_Product` VALUES (1,'pizza',5.00),(2,'kebab',10.20),(3,'kebab',10.20);
/*!40000 ALTER TABLE `Sold_Product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `idUser` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idUser`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'filip','pass'),(2,'max','pass'),(3,'wille','pass'),(4,'filip','pass'),(5,'maxskogh','bobpass');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_has_Order`
--

DROP TABLE IF EXISTS `User_has_Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User_has_Order` (
  `idUser` int NOT NULL,
  `idOrder` int NOT NULL,
  `order_date` date DEFAULT NULL,
  PRIMARY KEY (`idUser`,`idOrder`),
  UNIQUE KEY `idOrder_UNIQUE` (`idOrder`),
  KEY `fk_User_has_Order_History_Order_History1_idx` (`idOrder`),
  KEY `fk_User_has_Order_History_User1_idx` (`idUser`),
  CONSTRAINT `fk_User_has_Order_History_Order_History1` FOREIGN KEY (`idOrder`) REFERENCES `Order_History` (`idOrder`),
  CONSTRAINT `fk_User_has_Order_History_User1` FOREIGN KEY (`idUser`) REFERENCES `User` (`idUser`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_has_Order`
--

LOCK TABLES `User_has_Order` WRITE;
/*!40000 ALTER TABLE `User_has_Order` DISABLE KEYS */;
INSERT INTO `User_has_Order` VALUES (1,2,'2019-12-19'),(1,3,'2020-01-01'),(2,4,'2020-01-01');
/*!40000 ALTER TABLE `User_has_Order` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-27 13:46:40
