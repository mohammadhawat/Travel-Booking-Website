-- MySQL dump 10.13  Distrib 9.2.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: ht_booking_db
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `journey_id` int DEFAULT NULL,
  `seats_booked` int DEFAULT NULL,
  `booking_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `journey_id` (`journey_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`journey_id`) REFERENCES `journeys` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (17,5,2,2,'2025-04-21 22:54:52'),(18,5,16,2,'2025-04-21 23:01:53'),(19,5,2,2,'2025-04-21 23:13:13'),(20,5,2,2,'2025-04-21 23:22:51');
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journeys`
--

DROP TABLE IF EXISTS `journeys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `journeys` (
  `id` int NOT NULL AUTO_INCREMENT,
  `origin` varchar(100) DEFAULT NULL,
  `destination` varchar(100) DEFAULT NULL,
  `departure_time` time DEFAULT NULL,
  `arrival_time` time DEFAULT NULL,
  `fare` decimal(6,2) DEFAULT NULL,
  `seat_capacity` int DEFAULT NULL,
  `travel_class` enum('Economy','Business') DEFAULT NULL,
  `travel_day` enum('Mon','Tue','Wed','Thu','Fri') DEFAULT NULL,
  `seats_booked` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journeys`
--

LOCK TABLES `journeys` WRITE;
/*!40000 ALTER TABLE `journeys` DISABLE KEYS */;
INSERT INTO `journeys` VALUES (1,'Bristol','Manchester','12:30:00','13:30:00',80.00,104,'Economy','Mon',8),(2,'Bristol','Manchester','12:30:00','13:30:00',160.00,26,'Business','Mon',6),(3,'Manchester','Bristol','18:25:00','19:30:00',80.00,104,'Economy','Tue',0),(4,'Manchester','Bristol','18:25:00','19:30:00',160.00,26,'Business','Tue',0),(5,'Bristol','Newcastle','09:00:00','10:15:00',90.00,104,'Economy','Wed',0),(6,'Bristol','Newcastle','09:00:00','10:15:00',180.00,26,'Business','Wed',0),(7,'Bristol','London','07:40:00','08:20:00',80.00,104,'Economy','Thu',0),(8,'Bristol','London','07:40:00','08:20:00',160.00,26,'Business','Thu',0),(10,'Newcastle','Bristol','17:45:00','19:00:00',100.00,50,'Economy','Mon',0),(11,'Bristol','Newcastle','09:00:00','10:15:00',90.00,50,'Economy','Tue',0),(12,'Cardiff','Edinburgh','07:00:00','08:30:00',90.00,50,'Economy','Wed',0),(13,'Bristol','Manchester','12:30:00','13:30:00',80.00,50,'Economy','Thu',0),(14,'Manchester','Bristol','13:20:00','14:20:00',80.00,50,'Economy','Fri',0),(15,'Bristol','London','07:40:00','08:20:00',80.00,50,'Economy','Mon',0),(16,'London','Manchester','13:00:00','14:00:00',100.00,50,'Economy','Tue',2),(17,'Manchester','Glasgow','12:20:00','13:30:00',100.00,50,'Economy','Wed',0),(18,'Bristol','Glasgow','08:40:00','09:45:00',110.00,50,'Economy','Thu',0),(19,'Glasgow','Newcastle','14:30:00','15:45:00',100.00,50,'Economy','Fri',0),(20,'Newcastle','Manchester','16:15:00','17:05:00',100.00,50,'Economy','Mon',0),(21,'Manchester','Bristol','18:25:00','19:30:00',80.00,50,'Economy','Tue',0),(22,'Bristol','Manchester','06:20:00','07:20:00',80.00,50,'Economy','Wed',0),(23,'Portsmouth','Dundee','12:00:00','14:00:00',120.00,50,'Economy','Thu',0),(24,'Dundee','Portsmouth','10:00:00','12:00:00',120.00,50,'Economy','Fri',0),(25,'Edinburgh','Cardiff','18:30:00','20:00:00',90.00,50,'Economy','Mon',0),(26,'Southampton','Manchester','12:00:00','13:30:00',90.00,50,'Economy','Tue',0),(27,'Manchester','Southampton','19:00:00','20:30:00',90.00,50,'Economy','Wed',0),(28,'Birmingham','Newcastle','17:00:00','17:45:00',100.00,50,'Economy','Thu',0),(29,'Newcastle','Birmingham','07:00:00','07:45:00',100.00,50,'Economy','Fri',0),(30,'Aberdeen','Portsmouth','08:00:00','09:30:00',100.00,50,'Economy','Mon',0),(31,'Newcastle','Bristol','17:45:00','19:00:00',100.00,50,'Economy','Mon',0),(32,'Bristol','Newcastle','09:00:00','10:15:00',90.00,50,'Economy','Tue',0),(33,'Cardiff','Edinburgh','07:00:00','08:30:00',90.00,50,'Economy','Wed',0),(34,'Bristol','Manchester','12:30:00','13:30:00',80.00,50,'Economy','Thu',0),(35,'Manchester','Bristol','13:20:00','14:20:00',80.00,50,'Economy','Fri',0),(36,'Bristol','London','07:40:00','08:20:00',80.00,50,'Economy','Mon',0),(37,'London','Manchester','13:00:00','14:00:00',100.00,50,'Economy','Tue',0),(38,'Manchester','Glasgow','12:20:00','13:30:00',100.00,50,'Economy','Wed',0),(39,'Bristol','Glasgow','08:40:00','09:45:00',110.00,50,'Economy','Thu',0),(40,'Glasgow','Newcastle','14:30:00','15:45:00',100.00,50,'Economy','Fri',0),(41,'Newcastle','Manchester','16:15:00','17:05:00',100.00,50,'Economy','Mon',0),(42,'Manchester','Bristol','18:25:00','19:30:00',80.00,50,'Economy','Tue',0),(43,'Bristol','Manchester','06:20:00','07:20:00',80.00,50,'Economy','Wed',0),(44,'Portsmouth','Dundee','12:00:00','14:00:00',120.00,50,'Economy','Thu',0),(45,'Dundee','Portsmouth','10:00:00','12:00:00',120.00,50,'Economy','Fri',0),(46,'Edinburgh','Cardiff','18:30:00','20:00:00',90.00,50,'Economy','Mon',0),(47,'Southampton','Manchester','12:00:00','13:30:00',90.00,50,'Economy','Tue',0),(48,'Manchester','Southampton','19:00:00','20:30:00',90.00,50,'Economy','Wed',0),(49,'Birmingham','Newcastle','17:00:00','17:45:00',100.00,50,'Economy','Thu',0),(50,'Newcastle','Birmingham','07:00:00','07:45:00',100.00,50,'Economy','Fri',0),(51,'Aberdeen','Portsmouth','08:00:00','09:30:00',100.00,50,'Economy','Mon',0),(53,'Bristol','Riyadh','12:30:00','19:30:00',400.00,2,'Economy','Mon',0);
/*!40000 ALTER TABLE `journeys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'mohammad hawat','mohamed.hawat@gmail.com','Sam132465'),(5,'mohammad hawat','Mohamad2.Elhawat@live.uwe.ac.uk','scrypt:32768:8:1$J86iEpJG5wU8cDug$078fa4dd98db063a9b3058b798c326902ceb19c5c039852097ad1c874c2d4db5e4ac9391b106f72b7ae52058582841201de9a7cddec41e3fa9cf6e3b69bb7c68');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-21 23:48:32
