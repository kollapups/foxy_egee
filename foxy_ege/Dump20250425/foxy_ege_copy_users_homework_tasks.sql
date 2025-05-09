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
-- Table structure for table `users_homework_tasks`
--

DROP TABLE IF EXISTS `users_homework_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_homework_tasks` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `homework_id` bigint NOT NULL,
  `task_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_homework_tasks_homework_id_task_id_3be62c09_uniq` (`homework_id`,`task_id`),
  KEY `users_homework_tasks_task_id_b15831b6_fk_tasks_task_id` (`task_id`),
  CONSTRAINT `users_homework_tasks_homework_id_373650b1_fk_users_homework_id` FOREIGN KEY (`homework_id`) REFERENCES `users_homework` (`id`),
  CONSTRAINT `users_homework_tasks_task_id_b15831b6_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_homework_tasks`
--

LOCK TABLES `users_homework_tasks` WRITE;
/*!40000 ALTER TABLE `users_homework_tasks` DISABLE KEYS */;
INSERT INTO `users_homework_tasks` VALUES (8,3,118),(9,3,119),(7,3,120);
/*!40000 ALTER TABLE `users_homework_tasks` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-25 17:00:53
