CREATE DATABASE  IF NOT EXISTS `foxy_ege` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `foxy_ege`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: foxy_ege
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
-- Table structure for table `tasks_subtopic`
--

DROP TABLE IF EXISTS `tasks_subtopic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks_subtopic` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `topic_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tasks_subtopic_topic_id_4e59340f_fk_tasks_topic_id` (`topic_id`),
  CONSTRAINT `tasks_subtopic_topic_id_4e59340f_fk_tasks_topic_id` FOREIGN KEY (`topic_id`) REFERENCES `tasks_topic` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks_subtopic`
--

LOCK TABLES `tasks_subtopic` WRITE;
/*!40000 ALTER TABLE `tasks_subtopic` DISABLE KEYS */;
INSERT INTO `tasks_subtopic` VALUES (1,'math','Планиметрия',2),(2,'math','Стереометрия',2),(3,'math','Логарифмические выражения',1),(4,'math','Показательные уравнения',1),(5,'math','Логарифмические уравнения',1),(6,'math','Тригонометрические уравнения',1),(7,'math','Тригонометрические выражения',1),(8,'math','Текстовые задачи',1),(9,'math','Экономические задачи',1),(10,'math','Векторы',1),(11,'math','Простая вероятность',3),(12,'math','Сложная вероятность',3),(13,'math','Иррациональные уравнения',1),(14,'math','Дробно-рациональные уравнения',1),(15,'math','Вычисления и преобразования',1),(16,'math','Функции, производные и их графики',1),(17,'phys','Кинематика',5);
/*!40000 ALTER TABLE `tasks_subtopic` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-12  7:52:34
