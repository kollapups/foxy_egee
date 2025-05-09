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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'tasks','0001_initial','2025-03-31 16:57:29.018169'),(2,'contenttypes','0001_initial','2025-03-31 16:57:29.052769'),(3,'contenttypes','0002_remove_content_type_name','2025-03-31 16:57:29.119916'),(4,'auth','0001_initial','2025-03-31 16:57:29.297198'),(5,'auth','0002_alter_permission_name_max_length','2025-03-31 16:57:29.337752'),(6,'auth','0003_alter_user_email_max_length','2025-03-31 16:57:29.342521'),(7,'auth','0004_alter_user_username_opts','2025-03-31 16:57:29.351104'),(8,'auth','0005_alter_user_last_login_null','2025-03-31 16:57:29.356136'),(9,'auth','0006_require_contenttypes_0002','2025-03-31 16:57:29.358136'),(10,'auth','0007_alter_validators_add_error_messages','2025-03-31 16:57:29.362152'),(11,'auth','0008_alter_user_username_max_length','2025-03-31 16:57:29.366959'),(12,'auth','0009_alter_user_last_name_max_length','2025-03-31 16:57:29.371540'),(13,'auth','0010_alter_group_name_max_length','2025-03-31 16:57:29.382260'),(14,'auth','0011_update_proxy_permissions','2025-03-31 16:57:29.389886'),(15,'auth','0012_alter_user_first_name_max_length','2025-03-31 16:57:29.394559'),(16,'users','0001_initial','2025-03-31 16:57:30.191813'),(17,'admin','0001_initial','2025-03-31 16:57:30.292765'),(18,'admin','0002_logentry_remove_auto_add','2025-03-31 16:57:30.301783'),(19,'admin','0003_logentry_add_action_flag_choices','2025-03-31 16:57:30.311503'),(20,'oauth2_provider','0001_initial','2025-03-31 16:57:30.839677'),(21,'oauth2_provider','0002_auto_20190406_1805','2025-03-31 16:57:30.933362'),(22,'oauth2_provider','0003_auto_20201211_1314','2025-03-31 16:57:31.007825'),(23,'oauth2_provider','0004_auto_20200902_2022','2025-03-31 16:57:31.351681'),(24,'oauth2_provider','0005_auto_20211222_2352','2025-03-31 16:57:31.414635'),(25,'oauth2_provider','0006_alter_application_client_secret','2025-03-31 16:57:31.438852'),(26,'oauth2_provider','0007_application_post_logout_redirect_uris','2025-03-31 16:57:31.494213'),(27,'oauth2_provider','0008_alter_accesstoken_token','2025-03-31 16:57:31.506042'),(28,'oauth2_provider','0009_add_hash_client_secret','2025-03-31 16:57:31.573394'),(29,'oauth2_provider','0010_application_allowed_origins','2025-03-31 16:57:31.627327'),(30,'oauth2_provider','0011_refreshtoken_token_family','2025-03-31 16:57:31.680441'),(31,'oauth2_provider','0012_add_token_checksum','2025-03-31 16:57:31.881915'),(32,'sessions','0001_initial','2025-03-31 16:57:31.905849'),(33,'tasks','0002_initial','2025-03-31 16:57:32.723927'),(34,'tasks','0003_alter_comment_author_name','2025-03-31 16:57:32.740155'),(35,'tasks','0003_remove_task_latex_formula_task_solution_svg_formulas_and_more','2025-04-17 11:45:32.880656'),(36,'tasks','0004_alter_solutionimage_width','2025-04-18 10:12:55.705714'),(37,'tasks','0005_alter_task_options_alter_task_answer_and_more','2025-04-18 11:25:51.470281'),(38,'tasks','0006_alter_comment_options_alter_examline_options_and_more','2025-04-18 11:44:14.787138'),(39,'tasks','0007_alter_task_solution_svg_formulas_and_more','2025-04-18 11:53:27.247527'),(40,'tasks','0003_alter_solutionimage_width_renderedformula','2025-04-21 18:59:27.796188'),(41,'tasks','0003_renderedformula_alter_examline_options_and_more','2025-04-22 06:18:56.918837'),(42,'tasks','0003_task_formula_image_task_latex_formula_svg_and_more','2025-04-22 15:39:29.320502');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
