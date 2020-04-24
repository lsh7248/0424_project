--
-- Table structure for table `tb_members`
--
 
 
CREATE TABLE `tb_members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `profile` varchar(200) DEFAULT NULL,
  `password` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
);
 
--
-- Dumping data for table `tb_members`
--
 
INSERT INTO `tb_members` VALUES (1,'egoing','developer', SHA2('egoing', 256));
INSERT INTO `tb_members` VALUES (2,'duru','database administrator', SHA2('duru', 256));
INSERT INTO `tb_members` VALUES (3,'taeho','data scientist, developer', SHA2('taeho', 256));
INSERT INTO `tb_members` VALUES (4,'sookbu ','data engineer, developer', SHA2('sookbun', 256));
 
--
-- Table structure for table `tb_diary`
--
 
CREATE TABLE `tb_diary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `content` text,
  `created` datetime NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
 
--
-- Dumping data for table `tb_diary`
--
 
INSERT INTO `tb_diary` VALUES (1,'MySQL','MySQL is...','2018-01-01 12:10:11',1);
INSERT INTO `tb_diary` VALUES (2,'Oracle','Oracle is ...','2018-01-03 13:01:10',1);
INSERT INTO `tb_diary` VALUES (3,'SQL Server','SQL Server is ...','2018-01-20 11:01:10',2);
INSERT INTO `tb_diary` VALUES (4,'PostgreSQL','PostgreSQL is ...','2018-01-23 01:03:03',3);
INSERT INTO `tb_diary` VALUES (5,'MongoDB','MongoDB is ...','2018-01-30 12:31:03',1);
INSERT INTO `tb_diary` VALUES (6,'Python','Python is ...','2020-04-20 12:31:03',4);
INSERT INTO `tb_diary` VALUES (7,'Flask','Flask is ...','2020-04-21 12:31:03',4);