# Host: localhost  (Version 5.6.17)
# Date: 2017-10-30 16:12:33
# Generator: MySQL-Front 5.3  (Build 5.39)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "dayinfo"
#

DROP TABLE IF EXISTS `dayinfo`;
CREATE TABLE `dayinfo` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `day` varchar(255) DEFAULT NULL,
  `open` float(10,2) DEFAULT NULL,
  `close` float(10,2) DEFAULT NULL,
  `change_price` float(10,2) DEFAULT NULL,
  `change_ratio` float(10,2) DEFAULT NULL,
  `low` float(10,2) DEFAULT NULL,
  `high` float(10,2) DEFAULT NULL,
  `unknow1` int(255) DEFAULT NULL,
  `unknow2` float(10,2) DEFAULT NULL,
  `unknow3` float(10,2) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `name_day_index` (`name`,`day`)
) ENGINE=InnoDB AUTO_INCREMENT=734477 DEFAULT CHARSET=utf8;
