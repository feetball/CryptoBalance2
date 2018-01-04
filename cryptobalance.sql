-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: cryptobalance_db
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.17.10.1

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
-- Table structure for table `Coin`
--

DROP TABLE IF EXISTS `Coin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Coin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `symbol` varchar(10) NOT NULL,
  `coin_api_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `symbol` (`symbol`),
  KEY `coin_api_id` (`coin_api_id`),
  CONSTRAINT `Coin_ibfk_1` FOREIGN KEY (`coin_api_id`) REFERENCES `CoinApi` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Coin`
--

LOCK TABLES `Coin` WRITE;
/*!40000 ALTER TABLE `Coin` DISABLE KEYS */;
INSERT INTO `Coin` VALUES (4,'Litecoin','LTC',4),(5,'Bitcoin','BTC',2),(6,'Ethereum','ETH',3),(7,'Z-Cash','ZEC',5),(8,'Decred','DCR',6),(9,'Ripple','XRP',4);
/*!40000 ALTER TABLE `Coin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CoinApi`
--

DROP TABLE IF EXISTS `CoinApi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CoinApi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `key` varchar(100) DEFAULT NULL,
  `qty_extract_format` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CoinApi`
--

LOCK TABLES `CoinApi` WRITE;
/*!40000 ALTER TABLE `CoinApi` DISABLE KEYS */;
INSERT INTO `CoinApi` VALUES (1,'default','default','default','default'),(2,'CryptoID','https://chainz.cryptoid.info/{symbol}/api.dws?q=getbalance&key={key}&a={address}','1a29b449d778','float(url_response.text)'),(3,'Etherscan.io','https://api.etherscan.io/api?module=account&action=balance&tag=latest&apikey={key}&address={address}','UUS5UI9VIRY8N5CARUWJTT1IQ5FT4F2UYR','float(ast.literal_eval(url_response.text)[\'result\'])/10e17'),(4,'Ripple.com','https://data.ripple.com/v2/accounts/{address}','n/a','float(ast.literal_eval(url_response.text)[\'account_data\'][\'initial_balance\'])'),(5,'Zcha.in (Z-Cash)','https://api.zcha.in/v2/mainnet/accounts/{address}','n/a','float(ast.literal_eval(url_response.text)[\'balance\'])'),(6,'Decred.org','https://mainnet.decred.org/api/addr/{address}/?noTxList=1','n/a','float(ast.literal_eval(url_response.text)[\'balance\'])'),(7,'CoinPrices','https://api.coinmarketcap.com/v1/ticker/','n/a','');
/*!40000 ALTER TABLE `CoinApi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CoinPrice`
--

DROP TABLE IF EXISTS `CoinPrice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CoinPrice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` float DEFAULT NULL,
  `coin_id` int(11) NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `coin_id` (`coin_id`),
  CONSTRAINT `CoinPrice_ibfk_1` FOREIGN KEY (`coin_id`) REFERENCES `Coin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CoinPrice`
--

LOCK TABLES `CoinPrice` WRITE;
/*!40000 ALTER TABLE `CoinPrice` DISABLE KEYS */;
INSERT INTO `CoinPrice` VALUES (1,215.039,4,'2017-12-30 18:19:01'),(2,12783.9,5,'2017-12-30 18:19:20'),(3,710.119,6,'2017-12-30 18:19:09'),(4,481.243,7,'2017-12-30 18:19:08'),(5,82.924,8,'2017-12-30 18:19:05'),(6,2.17626,9,'2017-12-30 18:19:01'),(7,221.186,4,'2017-12-30 19:14:01'),(8,13253.7,5,'2017-12-30 19:14:21'),(9,726.55,6,'2017-12-30 19:14:09'),(10,500.406,7,'2017-12-30 19:14:08'),(11,86.1745,8,'2017-12-30 19:14:06'),(12,2.1545,9,'2017-12-30 19:14:00'),(13,225.155,4,'2017-12-30 20:54:01'),(14,13570.2,5,'2017-12-30 20:54:20'),(15,727.995,6,'2017-12-30 20:54:09'),(16,505.44,7,'2017-12-30 20:54:08'),(17,87.933,8,'2017-12-30 20:54:05'),(18,1.98867,9,'2017-12-30 20:54:01'),(19,227.944,4,'2017-12-30 21:19:01'),(20,13508.9,5,'2017-12-30 21:19:20'),(21,724.019,6,'2017-12-30 21:19:09'),(22,502.46,7,'2017-12-30 21:19:08'),(23,87.4115,8,'2017-12-30 21:19:06'),(24,2.01228,9,'2017-12-30 21:19:01'),(25,230.168,4,'2017-12-30 21:24:01'),(26,13534.6,5,'2017-12-30 21:24:20'),(27,724.454,6,'2017-12-30 21:24:08'),(28,501.836,7,'2017-12-30 21:24:08'),(29,87.6657,8,'2017-12-30 21:24:06'),(30,2.00997,9,'2017-12-30 21:24:01'),(31,232.253,4,'2017-12-30 21:39:01'),(32,13596.8,5,'2017-12-30 21:39:19'),(33,727.499,6,'2017-12-30 21:39:10'),(34,506.603,7,'2017-12-30 21:39:08'),(35,87.89,8,'2017-12-30 21:39:05'),(36,1.98552,9,'2017-12-30 21:39:01'),(37,224.41,4,'2017-12-30 22:29:01'),(38,13303.2,5,'2017-12-30 22:29:20'),(39,723.52,6,'2017-12-30 22:29:10'),(40,491.307,7,'2017-12-30 22:29:08'),(41,86.3824,8,'2017-12-30 22:29:06'),(42,1.8703,9,'2017-12-30 22:29:01'),(43,222.771,4,'2017-12-30 22:49:01'),(44,13205.6,5,'2017-12-30 22:49:20'),(45,719.827,6,'2017-12-30 22:49:10'),(46,491.413,7,'2017-12-30 22:49:08'),(47,86.3698,8,'2017-12-30 22:49:06'),(48,1.97258,9,'2017-12-30 22:49:01'),(49,222.714,4,'2017-12-30 23:04:01'),(50,13305.1,5,'2017-12-30 23:04:20'),(51,721.456,6,'2017-12-30 23:04:09'),(52,493.283,7,'2017-12-30 23:04:09'),(53,87.1731,8,'2017-12-30 23:04:06'),(54,2.04674,9,'2017-12-30 23:04:01');
/*!40000 ALTER TABLE `CoinPrice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Department`
--

DROP TABLE IF EXISTS `Department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Department`
--

LOCK TABLES `Department` WRITE;
/*!40000 ALTER TABLE `Department` DISABLE KEYS */;
INSERT INTO `Department` VALUES (1,'dept1','dept1'),(2,'dept2','dept2');
/*!40000 ALTER TABLE `Department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Message`
--

DROP TABLE IF EXISTS `Message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `text` varchar(200) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Message`
--

LOCK TABLES `Message` WRITE;
/*!40000 ALTER TABLE `Message` DISABLE KEYS */;
INSERT INTO `Message` VALUES (1,'GET_COIN_PRICES','Execution Time: 0:00:09.338869','2017-12-30 20:55:41'),(2,'GET_COIN_PRICES','Execution Time: 0:00:08.073841','2017-12-30 20:56:11'),(3,'GET_COIN_PRICES','Execution Time: 0:00:04.654736','2017-12-30 21:23:07'),(4,'GET_COIN_PRICES','Execution Time: 0:00:00.809457','2017-12-30 21:25:51'),(5,'GET_COIN_PRICES','Execution Time: 0:00:01.433052','2017-12-30 21:27:59'),(6,'GET_COIN_PRICES','Execution Time: 0:00:00.918416','2017-12-30 21:41:12'),(7,'GET_COIN_PRICES','Execution Time: 0:00:00.229018','2017-12-30 22:33:13'),(8,'GET_COIN_PRICES','Execution Time: 0:00:00.383293','2017-12-30 22:50:11'),(9,'GET_COIN_PRICES','Execution Time: 0:00:00.377518','2017-12-30 23:07:45');
/*!40000 ALTER TABLE `Message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Role`
--

DROP TABLE IF EXISTS `Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Role`
--

LOCK TABLES `Role` WRITE;
/*!40000 ALTER TABLE `Role` DISABLE KEYS */;
/*!40000 ALTER TABLE `Role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(60) DEFAULT NULL,
  `username` varchar(60) DEFAULT NULL,
  `first_name` varchar(60) DEFAULT NULL,
  `last_name` varchar(60) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_User_email` (`email`),
  UNIQUE KEY `ix_User_username` (`username`),
  KEY `department_id` (`department_id`),
  KEY `role_id` (`role_id`),
  KEY `ix_User_first_name` (`first_name`),
  KEY `ix_User_last_name` (`last_name`),
  CONSTRAINT `User_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `Department` (`id`),
  CONSTRAINT `User_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `Role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (3,'daniel@kuecker.net','feetball','d','k','pbkdf2:sha256:50000$GckjO7kR$420ed9492e9e58ed2cab4118c201ea83e2637a5ce2183fd9410329f6adb81ac3',NULL,NULL,1),(4,'feetball@gmail.com','feetballz','d','krd','pbkdf2:sha256:50000$jFK7pCMG$002208079fedfcbbf459a2741b3214e2c16a0bc9e3292d3d1ab3c732999ca2fa',NULL,NULL,0);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Wallet`
--

DROP TABLE IF EXISTS `Wallet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Wallet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(128) NOT NULL,
  `user_id` int(11) NOT NULL,
  `coin_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `coin_id` (`coin_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Wallet_ibfk_1` FOREIGN KEY (`coin_id`) REFERENCES `Coin` (`id`),
  CONSTRAINT `Wallet_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Wallet`
--

LOCK TABLES `Wallet` WRITE;
/*!40000 ALTER TABLE `Wallet` DISABLE KEYS */;
INSERT INTO `Wallet` VALUES (7,'33VKBmdsykMZ6Yd3LzKEDoZ7BaN8VCS67b',4,5),(8,'0x216E2887C0bdDCe42Ef94AEDA49bA57333Bd77F6',4,6),(9,'r9ayPXR8R2VnNgxSmaJAvTXAfGin3K3oED',4,9),(10,'MGNcrwA1FG2hSBg6A1FPrKoFcjN4k1JByV',4,4),(11,'t1bk26TjvuxEUQ4jMThxZKkuSeXu23oHTvB',4,7);
/*!40000 ALTER TABLE `Wallet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-30 23:51:51
