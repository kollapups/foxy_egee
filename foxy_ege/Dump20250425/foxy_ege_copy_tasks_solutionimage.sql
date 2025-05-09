-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: foxy_ege_copy
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tasks_solutionimage`
--

DROP TABLE IF EXISTS `tasks_solutionimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks_solutionimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `order` int unsigned NOT NULL,
  `width` int unsigned NOT NULL,
  `task_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tasks_solutionimage_task_id_7cadbc25_fk_tasks_task_id` (`task_id`),
  CONSTRAINT `tasks_solutionimage_task_id_7cadbc25_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`),
  CONSTRAINT `tasks_solutionimage_chk_1` CHECK ((`order` >= 0)),
  CONSTRAINT `tasks_solutionimage_chk_2` CHECK ((`width` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks_solutionimage`
--

LOCK TABLES `tasks_solutionimage` WRITE;
/*!40000 ALTER TABLE `tasks_solutionimage` DISABLE KEYS */;
INSERT INTO `tasks_solutionimage` VALUES (1,'solution_images/solution1_aUdrM9h.jpg',0,100,111),(2,'solution_images/solution1_rhsDcpM.jpg',0,300,104),(3,'solution_images/solution2_PGv1CrR.jpg',0,300,107),(4,'solution_images/solution1_Nmxc1Xx.jpg',0,300,142),(5,'solution_images/solution2_GJWclcU.jpg',0,300,143),(6,'solution_images/solution3.jpg',0,300,144),(7,'solution_images/solution4.jpg',0,300,145),(8,'solution_images/solution5.jpg',0,300,146);
/*!40000 ALTER TABLE `tasks_solutionimage` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-25 17:00:54
