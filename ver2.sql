-- MySQL dump 10.14  Distrib 5.5.40-MariaDB, for Win64 (x86)
--
-- Host: localhost    Database: vmver2
-- ------------------------------------------------------
-- Server version	5.5.40-MariaDB

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_58c48ba9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth_permissi_content_type_id_51277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add company',7,'add_company'),(20,'Can change company',7,'change_company'),(21,'Can delete company',7,'delete_company'),(22,'Can add node host',8,'add_nodehost'),(23,'Can change node host',8,'change_nodehost'),(24,'Can delete node host',8,'delete_nodehost'),(25,'Can add instance',9,'add_instance'),(26,'Can change instance',9,'change_instance'),(27,'Can delete instance',9,'delete_instance'),(28,'Can add ip',10,'add_ip'),(29,'Can change ip',10,'change_ip'),(30,'Can delete ip',10,'delete_ip'),(31,'Can add mac',11,'add_mac'),(32,'Can change mac',11,'change_mac'),(33,'Can delete mac',11,'delete_mac'),(34,'Can add usb port',12,'add_usbport'),(35,'Can change usb port',12,'change_usbport'),(36,'Can delete usb port',12,'delete_usbport'),(37,'Can add dog sn',13,'add_dogsn'),(38,'Can change dog sn',13,'change_dogsn'),(39,'Can delete dog sn',13,'delete_dogsn'),(40,'Can add log',14,'add_log'),(41,'Can change log',14,'change_log'),(42,'Can delete log',14,'delete_log'),(43,'Can add perm',15,'add_perm'),(44,'Can change perm',15,'change_perm'),(45,'Can delete perm',15,'delete_perm');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$xDJX2ISFD3WZ$sj20K3g2EnVazrS5v8idbfm/f8r+xomCSjZxuIzdO3I=','2014-12-01 12:34:38',1,'admin','','','sdfsad@fsda.dd',1,1,'2014-12-01 12:29:09');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_30a071c9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_24702650_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_1c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin__content_type_id_5151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'company','hrmsapp','company'),(8,'node host','hrmsapp','nodehost'),(9,'instance','hrmsapp','instance'),(10,'ip','hrmsapp','ip'),(11,'mac','hrmsapp','mac'),(12,'usb port','hrmsapp','usbport'),(13,'dog sn','hrmsapp','dogsn'),(14,'log','log','log'),(15,'perm','userprofile','perm');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2014-12-01 12:29:01'),(2,'auth','0001_initial','2014-12-01 12:29:01'),(3,'admin','0001_initial','2014-12-01 12:29:01'),(4,'sessions','0001_initial','2014-12-01 12:29:01');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('va8giwyh6xt2g9fry6pddqx1x650hlbn','ZjMyMjRjY2VhMzg2NmI2ZDM4ZTZiOTI1ZGVkZjA1MmE4YmNiMmU4NDp7Il9hdXRoX3VzZXJfaGFzaCI6IjM4ZDA2NzdhNmYzMjU1ODJjZjU0ODlhNDY5Y2QyNTI3YTc4ZGQ0MTEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOjF9','2014-12-15 12:34:38');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hrmsapp_company`
--

DROP TABLE IF EXISTS `hrmsapp_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hrmsapp_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `companyName` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `companyName` (`companyName`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrmsapp_company`
--

LOCK TABLES `hrmsapp_company` WRITE;
/*!40000 ALTER TABLE `hrmsapp_company` DISABLE KEYS */;
INSERT INTO `hrmsapp_company` VALUES (1,'a');
/*!40000 ALTER TABLE `hrmsapp_company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hrmsapp_dogsn`
--

DROP TABLE IF EXISTS `hrmsapp_dogsn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hrmsapp_dogsn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(20) NOT NULL,
  `port_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sn` (`sn`),
  UNIQUE KEY `port_id` (`port_id`),
  CONSTRAINT `port_id_refs_id_2b443e3e` FOREIGN KEY (`port_id`) REFERENCES `hrmsapp_usbport` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrmsapp_dogsn`
--

LOCK TABLES `hrmsapp_dogsn` WRITE;
/*!40000 ALTER TABLE `hrmsapp_dogsn` DISABLE KEYS */;
INSERT INTO `hrmsapp_dogsn` VALUES (1,'abc',1);
/*!40000 ALTER TABLE `hrmsapp_dogsn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hrmsapp_instance`
--

DROP TABLE IF EXISTS `hrmsapp_instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hrmsapp_instance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `instanceName` varchar(10) NOT NULL,
  `vcpus` varchar(10) NOT NULL,
  `mem` varchar(10) NOT NULL,
  `dataDisk` varchar(10) NOT NULL,
  `startTime` datetime NOT NULL,
  `useInterval` int(11) NOT NULL,
  `bandwidth` varchar(4) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `nodeHost_id` int(11) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `instanceName` (`instanceName`),
  KEY `hrmsapp_instance_6340c63c` (`user_id`),
  KEY `hrmsapp_instance_75bb5448` (`nodeHost_id`),
  KEY `hrmsapp_instance_0316dde1` (`company_id`),
  CONSTRAINT `nodeHost_id_refs_id_4e800f9a` FOREIGN KEY (`nodeHost_id`) REFERENCES `hrmsapp_nodehost` (`id`),
  CONSTRAINT `company_id_refs_id_bdf3bd7f` FOREIGN KEY (`company_id`) REFERENCES `hrmsapp_company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrmsapp_instance`
--

LOCK TABLES `hrmsapp_instance` WRITE;
/*!40000 ALTER TABLE `hrmsapp_instance` DISABLE KEYS */;
INSERT INTO `hrmsapp_instance` VALUES (1,'vm1','8','8','8','2014-11-30 16:00:00',30,'8',1,1,1);
/*!40000 ALTER TABLE `hrmsapp_instance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hrmsapp_ip`
--

DROP TABLE IF EXISTS `hrmsapp_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hrmsapp_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ipAddress` char(15) NOT NULL,
  `instance_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ipAddress` (`ipAddress`),
  KEY `hrmsapp_ip_19349866` (`instance_id`),
  CONSTRAINT `instance_id_refs_id_8dd1c992` FOREIGN KEY (`instance_id`) REFERENCES `hrmsapp_instance` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrmsapp_ip`
--

LOCK TABLES `hrmsapp_ip` WRITE;
/*!40000 ALTER TABLE `hrmsapp_ip` DISABLE KEYS */;
INSERT INTO `hrmsapp_ip` VALUES (1,'192.168.1.1',1),(2,'192.168.1.2',1),(3,'192.168.1.3',NULL),(4,'192.168.1.4',NULL);
/*!40000 ALTER TABLE `hrmsapp_ip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hrmsapp_mac`
--

DROP TABLE IF EXISTS `hrmsapp_mac`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hrmsapp_mac` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `macAddress` varchar(17) NOT NULL,
  `instance_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `macAddress` (`macAddress`),
  KEY `hrmsapp_mac_19349866` (`instance_id`),
  CONSTRAINT `instance_id_refs_id_28dd921e` FOREIGN KEY (`instance_id`) REFERENCES `hrmsapp_instance` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrmsapp_mac`
--

LOCK TABLES `hrmsapp_mac` WRITE;
/*!40000 ALTER TABLE `hrmsapp_mac` DISABLE KEYS */;
INSERT INTO `hrmsapp_mac` VALUES (1,'11:11:11:11:11:11',1),(2,'22:22:22:22:22:22',NULL),(3,'33:33:33:33:33:33',NULL),(4,'44:44:44:44:44:44',NULL);
/*!40000 ALTER TABLE `hrmsapp_mac` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hrmsapp_nodehost`
--

DROP TABLE IF EXISTS `hrmsapp_nodehost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hrmsapp_nodehost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node` varchar(17) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `node` (`node`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrmsapp_nodehost`
--

LOCK TABLES `hrmsapp_nodehost` WRITE;
/*!40000 ALTER TABLE `hrmsapp_nodehost` DISABLE KEYS */;
INSERT INTO `hrmsapp_nodehost` VALUES (1,'12.34.56.78'),(2,'87.65.43.21');
/*!40000 ALTER TABLE `hrmsapp_nodehost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hrmsapp_usbport`
--

DROP TABLE IF EXISTS `hrmsapp_usbport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hrmsapp_usbport` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `port` varchar(20) NOT NULL,
  `nodeHost_id` int(11) NOT NULL,
  `instance_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `port` (`port`,`nodeHost_id`),
  KEY `hrmsapp_usbport_75bb5448` (`nodeHost_id`),
  KEY `hrmsapp_usbport_19349866` (`instance_id`),
  CONSTRAINT `instance_id_refs_id_8974e314` FOREIGN KEY (`instance_id`) REFERENCES `hrmsapp_instance` (`id`),
  CONSTRAINT `nodeHost_id_refs_id_3a6daf8d` FOREIGN KEY (`nodeHost_id`) REFERENCES `hrmsapp_nodehost` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrmsapp_usbport`
--

LOCK TABLES `hrmsapp_usbport` WRITE;
/*!40000 ALTER TABLE `hrmsapp_usbport` DISABLE KEYS */;
INSERT INTO `hrmsapp_usbport` VALUES (1,'123',1,1),(2,'456',1,NULL),(3,'1234',2,NULL),(4,'5678',2,NULL);
/*!40000 ALTER TABLE `hrmsapp_usbport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_log`
--

DROP TABLE IF EXISTS `log_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `logTime` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `log_log_6340c63c` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_log`
--

LOCK TABLES `log_log` WRITE;
/*!40000 ALTER TABLE `log_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userprofile_perm`
--

DROP TABLE IF EXISTS `userprofile_perm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userprofile_perm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `query_permission` longtext NOT NULL,
  `modify_permission` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userprofile_perm`
--

LOCK TABLES `userprofile_perm` WRITE;
/*!40000 ALTER TABLE `userprofile_perm` DISABLE KEYS */;
/*!40000 ALTER TABLE `userprofile_perm` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-12-01 23:46:05
