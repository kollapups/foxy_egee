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
-- Table structure for table `users_studenthomework_submission_files`
--

DROP TABLE IF EXISTS `users_studenthomework_submission_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_studenthomework_submission_files` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `studenthomework_id` bigint NOT NULL,
  `studenthomeworkfile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_studenthomework_su_studenthomework_id_stude_6e968dbb_uniq` (`studenthomework_id`,`studenthomeworkfile_id`),
  KEY `users_studenthomewor_studenthomeworkfile__66c0c3f2_fk_users_stu` (`studenthomeworkfile_id`),
  CONSTRAINT `users_studenthomewor_studenthomework_id_8b08723c_fk_users_stu` FOREIGN KEY (`studenthomework_id`) REFERENCES `users_studenthomework` (`id`),
  CONSTRAINT `users_studenthomewor_studenthomeworkfile__66c0c3f2_fk_users_stu` FOREIGN KEY (`studenthomeworkfile_id`) REFERENCES `users_studenthomeworkfile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_studenthomework_submission_files`
--

LOCK TABLES `users_studenthomework_submission_files` WRITE;
/*!40000 ALTER TABLE `users_studenthomework_submission_files` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_studenthomework_submission_files` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-25 17:00:52
