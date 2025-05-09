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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add application',6,'add_application'),(22,'Can change application',6,'change_application'),(23,'Can delete application',6,'delete_application'),(24,'Can view application',6,'view_application'),(25,'Can add access token',7,'add_accesstoken'),(26,'Can change access token',7,'change_accesstoken'),(27,'Can delete access token',7,'delete_accesstoken'),(28,'Can view access token',7,'view_accesstoken'),(29,'Can add grant',8,'add_grant'),(30,'Can change grant',8,'change_grant'),(31,'Can delete grant',8,'delete_grant'),(32,'Can view grant',8,'view_grant'),(33,'Can add refresh token',9,'add_refreshtoken'),(34,'Can change refresh token',9,'change_refreshtoken'),(35,'Can delete refresh token',9,'delete_refreshtoken'),(36,'Can view refresh token',9,'view_refreshtoken'),(37,'Can add id token',10,'add_idtoken'),(38,'Can change id token',10,'change_idtoken'),(39,'Can delete id token',10,'delete_idtoken'),(40,'Can view id token',10,'view_idtoken'),(41,'Can add student homework file',11,'add_studenthomeworkfile'),(42,'Can change student homework file',11,'change_studenthomeworkfile'),(43,'Can delete student homework file',11,'delete_studenthomeworkfile'),(44,'Can view student homework file',11,'view_studenthomeworkfile'),(45,'Can add user',12,'add_customuser'),(46,'Can change user',12,'change_customuser'),(47,'Can delete user',12,'delete_customuser'),(48,'Can view user',12,'view_customuser'),(49,'Can add homework',13,'add_homework'),(50,'Can change homework',13,'change_homework'),(51,'Can delete homework',13,'delete_homework'),(52,'Can view homework',13,'view_homework'),(53,'Can add homework file',14,'add_homeworkfile'),(54,'Can change homework file',14,'change_homeworkfile'),(55,'Can delete homework file',14,'delete_homeworkfile'),(56,'Can view homework file',14,'view_homeworkfile'),(57,'Can add student homework',15,'add_studenthomework'),(58,'Can change student homework',15,'change_studenthomework'),(59,'Can delete student homework',15,'delete_studenthomework'),(60,'Can view student homework',15,'view_studenthomework'),(61,'Can add student teacher',16,'add_studentteacher'),(62,'Can change student teacher',16,'change_studentteacher'),(63,'Can delete student teacher',16,'delete_studentteacher'),(64,'Can view student teacher',16,'view_studentteacher'),(65,'Can add comment',17,'add_comment'),(66,'Can change comment',17,'change_comment'),(67,'Can delete comment',17,'delete_comment'),(68,'Can view comment',17,'view_comment'),(69,'Can add exam line',18,'add_examline'),(70,'Can change exam line',18,'change_examline'),(71,'Can delete exam line',18,'delete_examline'),(72,'Can view exam line',18,'view_examline'),(73,'Can add exam part',19,'add_exampart'),(74,'Can change exam part',19,'change_exampart'),(75,'Can delete exam part',19,'delete_exampart'),(76,'Can view exam part',19,'view_exampart'),(77,'Can add ?????????????????? ??????????????',20,'add_favorite'),(78,'Can change ?????????????????? ??????????????',20,'change_favorite'),(79,'Can delete ?????????????????? ??????????????',20,'delete_favorite'),(80,'Can view ?????????????????? ??????????????',20,'view_favorite'),(81,'Can add ?????????????????????????????? ??????????????',21,'add_generatedvariant'),(82,'Can change ?????????????????????????????? ??????????????',21,'change_generatedvariant'),(83,'Can delete ?????????????????????????????? ??????????????',21,'delete_generatedvariant'),(84,'Can view ?????????????????????????????? ??????????????',21,'view_generatedvariant'),(85,'Can add solution image',22,'add_solutionimage'),(86,'Can change solution image',22,'change_solutionimage'),(87,'Can delete solution image',22,'delete_solutionimage'),(88,'Can view solution image',22,'view_solutionimage'),(89,'Can add source',23,'add_source'),(90,'Can change source',23,'change_source'),(91,'Can delete source',23,'delete_source'),(92,'Can view source',23,'view_source'),(93,'Can add subtopic',24,'add_subtopic'),(94,'Can change subtopic',24,'change_subtopic'),(95,'Can delete subtopic',24,'delete_subtopic'),(96,'Can view subtopic',24,'view_subtopic'),(97,'Can add task',25,'add_task'),(98,'Can change task',25,'change_task'),(99,'Can delete task',25,'delete_task'),(100,'Can view task',25,'view_task'),(101,'Can add topic',26,'add_topic'),(102,'Can change topic',26,'change_topic'),(103,'Can delete topic',26,'delete_topic'),(104,'Can view topic',26,'view_topic'),(105,'Can add rendered formula',27,'add_renderedformula'),(106,'Can change rendered formula',27,'change_renderedformula'),(107,'Can delete rendered formula',27,'delete_renderedformula'),(108,'Can view rendered formula',27,'view_renderedformula');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
