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
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2gl679hqr9v25ypgrvi1717mjt5e67lz','eyJ0YXNrcyI6Wzk5XX0:1u0jKN:BUyF5S6BBcrYRnUl6tm-YLA9tZo2aPGduxk3kSKti_Q','2025-04-18 15:51:31.029130'),('cc737yxidxo69qhh7pz50l088b6gqfbn','.eJxVjM0OgjAQhN-l5w3ptqW7cvTuExhDtj8IaiChcDK-u5Bw0OPMfPO9VSvr0rdryXM7JNUoVPDbBYnPPO5Desh4n6o4jcs8hGpHqmMt1WVK-XU-2D9BL6Xf3jYwhlrI6Kw9OnNiYuYckrYsW4oxZUfCzqD2NebEVneeowmWuoBmky5SnkU119qC90AWUDOgB3TgHZABS2Do9vkCW-1Abw:1u7BrM:oyzcPRm7RI-uqpTAOD-TA7mJWdOZ80ReVbSpaRAI4Dk','2025-05-06 11:32:16.112919'),('p1n911xan0v5e3oe1bnp4p3kl5rob55j','.eJxVT9luwjAQ_Jd9tiIfSezwGAmqAj1UqqoFVZFjmxKOJNiGghD_XgfRqjytZmdmZ_YEXrqVg96MsBgJlHEkGMowIjhBJKEoY4iRTwSN3PlF4ZuVqaF3AqmUce4XQzuVT41u79rjbmi3_O0xnwz53sdjelwexoDAHNrKGldUQc1SjBFcrIU_tib4cyOtsUHnVNMtZmCN1AF_28obCPnWzIP_rwH0V1P6fF-PBtvxhu7f82z50peD181oPfkY9v8lSg89wuOYCkFwGqW4G-SMoLh8tHPGFpUOFwnc7EqpQlJH6KWsv5pINbW3VRl1kujKuuih0WadX7U3BxbSLYKblYKUieQUm5Ab00xwIYQpNWZCBqSUNjGXIqahV0KMFgzPU6Foyfi8JBTOP26BhJM:1u3FkR:XKM7xB-xP8Xit2wifOnm3xVZnyyP2w8Mwq-FeMtxLDg','2025-04-25 14:52:51.945741');
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

-- Dump completed on 2025-04-25 17:00:54
