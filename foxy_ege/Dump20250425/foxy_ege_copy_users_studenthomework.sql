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
-- Table structure for table `users_studenthomework`
--

DROP TABLE IF EXISTS `users_studenthomework`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_studenthomework` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `student_answers` json DEFAULT NULL,
  `results` json DEFAULT NULL,
  `percentage` double DEFAULT NULL,
  `homework_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  `submission_file` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `users_studenthomework_homework_id_32c0f284_fk_users_homework_id` (`homework_id`),
  KEY `users_studenthomework_student_id_b9b3bbf8_fk_users_customuser_id` (`student_id`),
  CONSTRAINT `users_studenthomework_homework_id_32c0f284_fk_users_homework_id` FOREIGN KEY (`homework_id`) REFERENCES `users_homework` (`id`),
  CONSTRAINT `users_studenthomework_student_id_b9b3bbf8_fk_users_customuser_id` FOREIGN KEY (`student_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_studenthomework`
--

LOCK TABLES `users_studenthomework` WRITE;
/*!40000 ALTER TABLE `users_studenthomework` DISABLE KEYS */;
INSERT INTO `users_studenthomework` VALUES (1,'completed',NULL,'2025-04-05 09:34:02.881166',NULL,'{\"118\": {\"correct_answer\": \"30\", \"student_answer\": \"21\"}, \"119\": {\"correct_answer\": \"5\", \"student_answer\": \"3\"}, \"120\": {\"correct_answer\": \"20\", \"student_answer\": \"11\"}}',NULL,3,3,'');
/*!40000 ALTER TABLE `users_studenthomework` ENABLE KEYS */;
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
