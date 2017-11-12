-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: Sudarshan_Enterprises
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Brand`
--

DROP TABLE IF EXISTS `Brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Brand` (
  `BID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) DEFAULT NULL,
  `Phone` char(10) DEFAULT NULL,
  `Address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`BID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Brand`
--

LOCK TABLES `Brand` WRITE;
/*!40000 ALTER TABLE `Brand` DISABLE KEYS */;
INSERT INTO `Brand` VALUES (1,'Sardar Feed','7894561230','221B Baker Street'),(2,'Sudharma Feed','7194561230','21B Baker Street'),(3,'Medha feeds','7017360433','Rajpur road,Dehradun'),(4,'Pappu Feed','8465132330','Rajpur Road, Dehradun'),(5,'asdasdasd','7042654964','asdasdasdasdas'),(6,'asdasdaf','ahsdhasd','Nagpur');
/*!40000 ALTER TABLE `Brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Customer` (
  `CID` int(11) NOT NULL AUTO_INCREMENT,
  `Address` varchar(50) DEFAULT NULL,
  `User` int(11) DEFAULT NULL,
  PRIMARY KEY (`CID`),
  KEY `User` (`User`),
  CONSTRAINT `Customer_ibfk_1` FOREIGN KEY (`User`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (1,'Kholi 420, Saharanpur',2),(2,'Earth',3),(3,'Dehradun',13),(4,'A-6, Vivek Vihar, Shastri Nagar',14),(5,'sdasdasdasd',17),(6,'Room B306,Aryabhatta Hostel, IIT (BHU),BHU',22),(14,' Roshan Lal Gurbax Singh,',30),(15,'Saharanpur',31);
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CustomerOrder`
--

DROP TABLE IF EXISTS `CustomerOrder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CustomerOrder` (
  `OID` int(11) NOT NULL AUTO_INCREMENT,
  `CID` int(11) DEFAULT NULL,
  `Sum` int(11) DEFAULT NULL,
  `Paid` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Discount` float DEFAULT NULL,
  `Approved` char(1) DEFAULT 'N',
  PRIMARY KEY (`OID`),
  KEY `CID` (`CID`),
  CONSTRAINT `CustomerOrder_ibfk_1` FOREIGN KEY (`CID`) REFERENCES `Customer` (`CID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CustomerOrder`
--

LOCK TABLES `CustomerOrder` WRITE;
/*!40000 ALTER TABLE `CustomerOrder` DISABLE KEYS */;
INSERT INTO `CustomerOrder` VALUES (44,5,8856,8856,'2017-11-07','22:36:27',0,'Y'),(45,1,4677,4677,'2017-11-07','22:38:15',0,'Y'),(46,15,96879,96879,'2017-11-08','00:23:54',0,'Y'),(47,1,78219,78219,'2017-11-08','21:42:55',0,'Y'),(48,1,269230,269230,'2017-11-08','22:11:28',0,'Y'),(49,1,50885,50885,'2017-11-09','13:25:22',0,'Y'),(50,1,501024,501024,'2017-11-09','13:38:18',0,'Y'),(52,1,297143,297143,'2017-11-09','20:40:07',0,'Y'),(53,4,297143,116000,'2017-11-09','20:40:10',0,'Y'),(54,15,37142,37142,'2017-11-09','20:54:37',0,'Y'),(55,1,60400,25093,'2017-11-11','19:09:02',0,'Y'),(56,1,194775,0,'2017-11-12','02:29:12',0,'Y'),(57,3,101871,101500,'2017-11-12','02:47:19',0,'Y'),(68,1,6040,0,'2017-11-12','14:08:50',0,'N'),(69,1,509,499,'2017-11-12','15:31:41',10,'Y');
/*!40000 ALTER TABLE `CustomerOrder` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 trigger balanceCheck before insert on CustomerOrder for each row if new.Paid>new.Sum+new.Discount then set new.Paid=new.Sum+new.Discount; end if */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 trigger balanceUpdate before update on CustomerOrder for each row if new.Paid>new.Sum+new.Discount then set new.Paid=new.Sum+new.Discount; end if */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `CustomerPhones`
--

DROP TABLE IF EXISTS `CustomerPhones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CustomerPhones` (
  `CID` int(11) NOT NULL,
  `Phone` char(10) NOT NULL,
  PRIMARY KEY (`CID`,`Phone`),
  CONSTRAINT `CustomerPhones_ibfk_1` FOREIGN KEY (`CID`) REFERENCES `Customer` (`CID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CustomerPhones`
--

LOCK TABLES `CustomerPhones` WRITE;
/*!40000 ALTER TABLE `CustomerPhones` DISABLE KEYS */;
INSERT INTO `CustomerPhones` VALUES (1,'7894512320'),(1,'7894512360'),(2,'9784561530'),(14,'7894561233'),(15,'8654321790'),(15,'8745693210');
/*!40000 ALTER TABLE `CustomerPhones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feed`
--

DROP TABLE IF EXISTS `Feed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feed` (
  `FID` int(11) NOT NULL AUTO_INCREMENT,
  `S_GST` float DEFAULT NULL,
  `C_GST` float DEFAULT NULL,
  `Type` char(20) DEFAULT NULL,
  PRIMARY KEY (`FID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feed`
--

LOCK TABLES `Feed` WRITE;
/*!40000 ALTER TABLE `Feed` DISABLE KEYS */;
INSERT INTO `Feed` VALUES (1,5,5,'Type 1'),(2,5,5.2,'Type 2'),(3,0,0,'Choker');
/*!40000 ALTER TABLE `Feed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Godown`
--

DROP TABLE IF EXISTS `Godown`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Godown` (
  `GodownNum` int(11) NOT NULL AUTO_INCREMENT,
  `Capacity` int(11) DEFAULT NULL,
  `Address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`GodownNum`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Godown`
--

LOCK TABLES `Godown` WRITE;
/*!40000 ALTER TABLE `Godown` DISABLE KEYS */;
INSERT INTO `Godown` VALUES (1,10000,'Next to shop'),(2,20000,'Away from shop');
/*!40000 ALTER TABLE `Godown` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrderFill`
--

DROP TABLE IF EXISTS `OrderFill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OrderFill` (
  `OID` int(11) DEFAULT NULL,
  `PID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `GID` int(11) DEFAULT NULL,
  `Cost` float DEFAULT NULL,
  KEY `PID` (`PID`),
  KEY `OID` (`OID`),
  KEY `GID` (`GID`),
  CONSTRAINT `OrderFill_ibfk_1` FOREIGN KEY (`PID`) REFERENCES `Pricing` (`PID`) ON DELETE CASCADE,
  CONSTRAINT `OrderFill_ibfk_2` FOREIGN KEY (`OID`) REFERENCES `SupplyOrder` (`OID`) ON DELETE CASCADE,
  CONSTRAINT `OrderFill_ibfk_3` FOREIGN KEY (`GID`) REFERENCES `Godown` (`GodownNum`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrderFill`
--

LOCK TABLES `OrderFill` WRITE;
/*!40000 ALTER TABLE `OrderFill` DISABLE KEYS */;
INSERT INTO `OrderFill` VALUES (2,1,50,2,3000),(2,2,50,1,3000),(2,1,40,2,3000),(12,4,1000,2,3000),(14,1,600,2,5000),(15,8,500,2,4000),(16,1,200,2,7000),(17,1,100,2,3000),(17,2,100,2,3500),(18,1,150,2,3500),(18,2,100,2,3750),(19,2,1000,2,5000),(24,3,1000,2,4000),(24,8,1000,2,4000),(24,4,500,2,5000),(24,5,700,2,4000),(25,4,1500,2,6000),(26,2,1000,2,5000),(27,2,1000,2,5000),(28,5,2000,1,3000),(29,8,100,2,2500),(30,8,1000,2,2500),(31,8,1000,2,2500),(32,9,1000,1,3500),(33,9,100,2,4000),(34,1,1500,2,4000);
/*!40000 ALTER TABLE `OrderFill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrderRemove`
--

DROP TABLE IF EXISTS `OrderRemove`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OrderRemove` (
  `OID` int(11) DEFAULT NULL,
  `PID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `GID` int(11) DEFAULT NULL,
  `Rate` float DEFAULT '0',
  KEY `PID` (`PID`),
  KEY `OID` (`OID`),
  KEY `GID` (`GID`),
  CONSTRAINT `OrderRemove_ibfk_1` FOREIGN KEY (`PID`) REFERENCES `Pricing` (`PID`) ON DELETE CASCADE,
  CONSTRAINT `OrderRemove_ibfk_2` FOREIGN KEY (`OID`) REFERENCES `CustomerOrder` (`OID`) ON DELETE CASCADE,
  CONSTRAINT `OrderRemove_ibfk_3` FOREIGN KEY (`GID`) REFERENCES `Godown` (`GodownNum`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrderRemove`
--

LOCK TABLES `OrderRemove` WRITE;
/*!40000 ALTER TABLE `OrderRemove` DISABLE KEYS */;
INSERT INTO `OrderRemove` VALUES (44,2,10,1,5010),(44,8,10,1,3846),(45,1,10,2,4677.75),(46,1,100,2,4677.75),(46,2,100,1,5010.24),(47,4,100,2,3714.29),(47,5,100,2,4107.71),(48,8,700,1,3846.15),(49,1,100,2,4677.75),(49,5,10,2,4107.71),(50,2,1000,1,5010.24),(52,4,800,2,3714.29),(53,4,800,2,3714.29),(54,4,100,2,3714.29),(55,2,100,2,6040.06),(56,9,500,1,3895.5),(57,1,200,2,5093.55),(68,2,10,2,6040.06),(69,1,1,2,5093.55);
/*!40000 ALTER TABLE `OrderRemove` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pricing`
--

DROP TABLE IF EXISTS `Pricing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pricing` (
  `PID` int(11) NOT NULL AUTO_INCREMENT,
  `FID` int(11) DEFAULT NULL,
  `BID` int(11) DEFAULT NULL,
  `Price` int(11) DEFAULT NULL,
  PRIMARY KEY (`PID`),
  KEY `FID` (`FID`),
  KEY `BID` (`BID`),
  CONSTRAINT `Pricing_ibfk_1` FOREIGN KEY (`FID`) REFERENCES `Feed` (`FID`) ON DELETE CASCADE,
  CONSTRAINT `Pricing_ibfk_2` FOREIGN KEY (`BID`) REFERENCES `Brand` (`BID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pricing`
--

LOCK TABLES `Pricing` WRITE;
/*!40000 ALTER TABLE `Pricing` DISABLE KEYS */;
INSERT INTO `Pricing` VALUES (1,1,1,500),(2,2,1,600),(3,1,2,600),(4,2,2,800),(5,2,3,590),(8,1,3,3000),(9,3,4,3000);
/*!40000 ALTER TABLE `Pricing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Supplier`
--

DROP TABLE IF EXISTS `Supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Supplier` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) DEFAULT NULL,
  `Address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Supplier`
--

LOCK TABLES `Supplier` WRITE;
/*!40000 ALTER TABLE `Supplier` DISABLE KEYS */;
INSERT INTO `Supplier` VALUES (2,'Pappu Patola','Saharanpur'),(3,'Teesra Supplier','Chauthi Gali'),(9,'Chautha Supplier','A-6, Vivek Vihar'),(10,'Test data','asdasd');
/*!40000 ALTER TABLE `Supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SupplierPhones`
--

DROP TABLE IF EXISTS `SupplierPhones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SupplierPhones` (
  `SID` int(11) NOT NULL,
  `Phone` char(10) NOT NULL,
  PRIMARY KEY (`SID`,`Phone`),
  CONSTRAINT `SupplierPhones_ibfk_1` FOREIGN KEY (`SID`) REFERENCES `Supplier` (`UID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SupplierPhones`
--

LOCK TABLES `SupplierPhones` WRITE;
/*!40000 ALTER TABLE `SupplierPhones` DISABLE KEYS */;
INSERT INTO `SupplierPhones` VALUES (9,'8654321790'),(9,'9555555555'),(10,'9555555547');
/*!40000 ALTER TABLE `SupplierPhones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SupplyOrder`
--

DROP TABLE IF EXISTS `SupplyOrder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SupplyOrder` (
  `OID` int(11) NOT NULL AUTO_INCREMENT,
  `SID` int(11) DEFAULT NULL,
  `Sum` int(11) DEFAULT NULL,
  `Paid` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `DateExpected` date DEFAULT NULL,
  `Loading` int(11) DEFAULT NULL,
  `Transport` int(11) DEFAULT NULL,
  PRIMARY KEY (`OID`),
  KEY `SID` (`SID`),
  CONSTRAINT `SupplyOrder_ibfk_1` FOREIGN KEY (`SID`) REFERENCES `Supplier` (`UID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SupplyOrder`
--

LOCK TABLES `SupplyOrder` WRITE;
/*!40000 ALTER TABLE `SupplyOrder` DISABLE KEYS */;
INSERT INTO `SupplyOrder` VALUES (2,2,50000,50000,'2017-10-30','10:00:00','2017-11-15',20,200),(12,9,6000,6200,'2017-11-01','16:02:25','2017-11-20',10,200),(13,3,1620,1700,'2017-11-01','16:06:24','2017-11-14',10,100),(14,10,30000,30000,'2017-11-02','05:05:33','2017-11-08',10,200),(15,9,20000,20000,'2017-11-02','11:08:55','2017-11-13',20,200),(16,9,14000,14000,'2017-11-02','12:19:01','2017-11-02',10,200),(17,2,6500,6500,'2017-11-02','19:01:03','2017-11-14',10,200),(18,3,9000,8920,'2017-11-04','15:00:08','2017-11-14',50,500),(19,9,50000,49800,'2017-11-04','15:49:25','2017-11-14',20,200),(24,2,133000,133000,'2017-11-10','19:21:52','2017-11-10',20,200),(25,2,90000,90000,'2017-11-10','19:22:49','2017-11-11',10,100),(26,2,50000,50000,'2017-11-10','19:33:17','2017-11-11',300,200),(27,2,50000,50000,'2017-11-10','22:03:54','2017-11-12',20,200),(28,2,60000,60000,'2017-11-10','22:04:49','2017-11-11',100,200),(29,3,2500,2500,'2017-11-11','17:58:31','2017-11-14',100,200),(30,2,25000,25000,'2017-11-11','18:00:59','2017-11-14',10,100),(31,2,25000,24500,'2017-11-11','18:01:39','2017-11-14',10,100),(32,3,35000,35000,'2017-11-12','02:10:10','2017-11-14',10,200),(33,9,4000,4000,'2017-11-12','02:36:59','2017-11-12',10,100),(34,9,60000,60000,'2017-11-12','02:44:42','2017-11-13',10,400);
/*!40000 ALTER TABLE `SupplyOrder` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 trigger purchaseCheck before insert on SupplyOrder for each row if new.Paid>new.Sum then set new.Paid=new.Sum; end if */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 trigger purchaseUpdate before update on SupplyOrder for each row if new.Paid>new.Sum then set new.Paid=new.Sum; end if */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add group',4,'add_group'),(11,'Can change group',4,'change_group'),(12,'Can delete group',4,'delete_group'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(50) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_email_1c89df09_uniq` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$30000$n64unNS7b9Tu$+W830YVp80i8NxU5p7G5NMtCF2Cx4jytut4gcUAZQbM=','2017-11-12 09:52:48.544788',1,'cb1996','Chaitanya','Bhatia','chaitanyabhatia1996@gmail.com',1,1,'2017-10-27 14:48:26.000000'),(2,'pbkdf2_sha256$30000$Z15Ym4nTAMOF$FTZYqK5BhS5czuYyKWlvA0rtP9+HpbBJ8PwfbeqqnVE=','2017-11-12 09:47:30.304605',0,'random_user','random','user','rd@gmail.com',0,1,'2017-10-27 14:50:30.000000'),(3,'pbkdf2_sha256$30000$FJxliUx0dgxx$BntrOSgyl5a/EGNdrzo+v5jXsJFagxxMJsqGbA+P5dU=',NULL,0,'kanta','Krishnakant','Swarnakar','ks@gmail.com',0,1,'2017-10-27 18:15:46.000000'),(13,'pbkdf2_sha256$30000$4lgelxsR8x6d$BS/FJULSZWxlZWQSm1NWAPoPif5o4OMIl9RuwQN9P3o=','2017-11-04 14:37:40.121068',0,'albRaj','Albela','Raju','a@b.com',0,1,'2017-10-28 12:09:02.688586'),(14,'pbkdf2_sha256$30000$9m1oMuBr7jJF$+PBQ/iZRIAa0RoyexWZvuCPw0qKk8NF5AqH/MfU1Q3s=','2017-10-28 14:18:10.603403',0,'cbhatia','chaitanya','bhatia','chaitanya@bhatia.com',0,1,'2017-10-28 14:18:10.303614'),(17,'pbkdf2_sha256$30000$p5KLVf6BW00F$fH3MTwexGL9XULkDTKlLxScwsl980IBSEUKdFVuAs/0=','2017-10-28 14:37:22.325902',0,'dasdas','asdasdasasd','asdasd','rad@gmail.com',0,1,'2017-10-28 14:37:21.940978'),(22,'pbkdf2_sha256$30000$IV2cxIM1Jm3D$x8KVUfwbDqhvm7GiS1JfVMgF70zHescMbg1/Bzuzs3o=','2017-10-28 17:52:50.187636',0,'cbhatia','Chaitanya','Bhatia','uiuhi@live.com',0,1,'2017-10-28 17:52:49.894243'),(30,'pbkdf2_sha256$30000$IlcJHcXwv9ju$BPkLfb5F43GB1w10yjnvZDDceD++b33V9N6CPEj8jkY=','2017-10-31 06:57:05.079847',0,'pw190','Police','Wala','pols@gmail.com',0,1,'2017-10-31 06:57:04.874777'),(31,'pbkdf2_sha256$30000$agbjHQxam824$suEkQv78+7VJQ5r2EV2I9UZEewiRrPpMjXbO4CUvq88=','2017-11-09 15:24:11.982072',0,'ProfessorRossEForp','Platypus','Perry','kanta@ac.com',0,1,'2017-10-31 18:38:15.354743');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2017-10-27 14:50:30.369119','2','',1,'[{\"added\": {}}]',3,1),(2,'2017-10-27 14:50:59.184749','2','rd@gmail.com',2,'[{\"changed\": {\"fields\": [\"first_name\", \"last_name\", \"email\"]}}]',3,1),(3,'2017-10-27 18:15:46.843004','3','',1,'[{\"added\": {}}]',3,1),(4,'2017-10-27 18:17:45.791452','3','ks@gmail.com',2,'[{\"changed\": {\"fields\": [\"first_name\", \"last_name\", \"email\"]}}]',3,1),(5,'2017-11-11 13:41:21.708772','1','chaitanyabhatia1996@gmail.com',2,'[{\"changed\": {\"fields\": [\"first_name\", \"last_name\"]}}]',3,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(4,'auth','group'),(2,'auth','permission'),(3,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-10-27 14:26:34.230968'),(2,'auth','0001_initial','2017-10-27 14:26:40.963648'),(3,'admin','0001_initial','2017-10-27 14:26:42.479973'),(4,'admin','0002_logentry_remove_auto_add','2017-10-27 14:26:42.580619'),(5,'contenttypes','0002_remove_content_type_name','2017-10-27 14:26:43.539953'),(6,'auth','0002_alter_permission_name_max_length','2017-10-27 14:26:43.640585'),(7,'auth','0003_alter_user_email_max_length','2017-10-27 14:26:43.764942'),(8,'auth','0004_alter_user_username_opts','2017-10-27 14:26:43.807270'),(9,'auth','0005_alter_user_last_login_null','2017-10-27 14:26:44.275718'),(10,'auth','0006_require_contenttypes_0002','2017-10-27 14:26:44.309223'),(11,'auth','0007_alter_validators_add_error_messages','2017-10-27 14:26:44.353224'),(12,'auth','0008_alter_user_username_max_length','2017-10-27 14:26:44.645166'),(13,'auth','0009_auto_20161104_0708','2017-10-27 14:26:46.147883'),(14,'auth','0010_auto_20161104_0715','2017-10-27 14:26:46.192101'),(15,'sessions','0001_initial','2017-10-27 14:26:46.661319');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0wo2why59b1874m2myhf5fx9ns6d5xnh','OTFiNzk4YTE5ZWRhNGI3MTc0NWE3YzA1YmMxNWJlOGU0ZDYyMDg3ODp7Il9hdXRoX3VzZXJfaGFzaCI6ImY3ODIwYjYwMzkwY2U2MGNlZTUwN2IwMGRiOTIxNjk1ZWNhMGI1NDUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2017-11-25 21:19:05.382830'),('cli4a3v1cx6ygkhno95j6qcmwepj50oz','MmE2Y2Q5NjEzNjg5ZWM2MTJkMzE0MTY1YmE0NzlkNzc4ZjNjZjMyZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjZiMGY4MGNiMGQwODU5Njk3N2MyZThmMDg0ZjFkNDgwZGRmMTJmYjQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-11-18 18:58:16.102374'),('jy235rehgkjf5w6oa5rltgtwv5wlpy77','MmE2Y2Q5NjEzNjg5ZWM2MTJkMzE0MTY1YmE0NzlkNzc4ZjNjZjMyZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjZiMGY4MGNiMGQwODU5Njk3N2MyZThmMDg0ZjFkNDgwZGRmMTJmYjQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-11-14 12:04:18.356333'),('mf9gvxqvhdsmjp6hekfukppzyqqfuw23','MmE2Y2Q5NjEzNjg5ZWM2MTJkMzE0MTY1YmE0NzlkNzc4ZjNjZjMyZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjZiMGY4MGNiMGQwODU5Njk3N2MyZThmMDg0ZjFkNDgwZGRmMTJmYjQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-11-11 09:21:35.610924');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-12 16:31:16
