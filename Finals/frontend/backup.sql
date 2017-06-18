-- MySQL dump 10.16  Distrib 10.1.21-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: localhost
-- ------------------------------------------------------
-- Server version	10.1.21-MariaDB

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
-- Table structure for table `admin_data_table`
--

DROP TABLE IF EXISTS `admin_data_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_data_table` (
  `username` text,
  `failed_login_attempts` double DEFAULT NULL,
  `verified_email` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_data_table`
--

LOCK TABLES `admin_data_table` WRITE;
/*!40000 ALTER TABLE `admin_data_table` DISABLE KEYS */;
INSERT INTO `admin_data_table` VALUES ('aru',0,'yes'),('arundhathi',3,'yes');
/*!40000 ALTER TABLE `admin_data_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_ip_table`
--

DROP TABLE IF EXISTS `login_ip_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_ip_table` (
  `IP_address` text,
  `login_attempt` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_ip_table`
--

LOCK TABLES `login_ip_table` WRITE;
/*!40000 ALTER TABLE `login_ip_table` DISABLE KEYS */;
INSERT INTO `login_ip_table` VALUES ('192.168.1.232','0');
/*!40000 ALTER TABLE `login_ip_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_data_table`
--

DROP TABLE IF EXISTS `sensor_data_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor_data_table` (
  `username` text,
  `sensor_name` text,
  `sensor_key` text,
  `sensor_data` text,
  `lower_limit` text,
  `upper_limit` text,
  `alert_value` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_data_table`
--

LOCK TABLES `sensor_data_table` WRITE;
/*!40000 ALTER TABLE `sensor_data_table` DISABLE KEYS */;
INSERT INTO `sensor_data_table` VALUES ('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','5','100','300','0'),('aru','plant','p1','5','100','300','0'),('aru','plant','p1','5','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','','','0','0','100','8'),('aru','plant2','p2','0','0','100','8'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant3','p3','0','0','100','8'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0'),('aru','plant','p1','1','100','300','0');
/*!40000 ALTER TABLE `sensor_data_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_data_table`
--

DROP TABLE IF EXISTS `user_data_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_data_table` (
  `username` text,
  `email_id` text,
  `password` text,
  `salt` text,
  `register` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_data_table`
--

LOCK TABLES `user_data_table` WRITE;
/*!40000 ALTER TABLE `user_data_table` DISABLE KEYS */;
INSERT INTO `user_data_table` VALUES ('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('arsw7501','arundhathirs1993@gmail.com','7b75700a08d8afc20ce543ac3933582b','jfzvntZZ0OAL9tGXXwM1NEGh+GWh0uLiiuewf1lHHwg=\n','True'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('aru','arundhathirs1993@gmail.com','327e67f1e14414a335c718b201513832','Xp6QmV6QC93hMBaeV3G5iZ6Z8vbuITruBvOHlfJ+cXE=\n','True'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('-','-','-','-','-'),('arundhathi','arundhathirs1993@gmail.com','3c383142902e9c4d4254a0485fa6ff71','Tv3mbkBkLDjL1lYZv0KKDJueDYHul4XnnWgFYdozTvQ=\n','True'),('-','-','-','-','-');
/*!40000 ALTER TABLE `user_data_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-24 17:22:12
