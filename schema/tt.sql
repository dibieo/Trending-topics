-- phpMyAdmin SQL Dump
-- version 3.4.5deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 01, 2012 at 02:31 AM
-- Server version: 5.1.62
-- PHP Version: 5.3.6-13ubuntu3.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `tt`
--

-- --------------------------------------------------------

--
-- Table structure for table `feed`
--

CREATE TABLE IF NOT EXISTS `feed` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text,
  `description` text,
  `link` text NOT NULL,
  `link_hash` varchar(128) NOT NULL,
  `last_build_date` text,
  `category` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `language` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `ttl` int(11) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'insertion date',
  PRIMARY KEY (`id`),
  UNIQUE KEY `link_hash` (`link_hash`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=584 ;

-- --------------------------------------------------------

--
-- Table structure for table `feeditem`
--

CREATE TABLE IF NOT EXISTS `feeditem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `link` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `link_hash` varchar(128) NOT NULL COMMENT 'hash of link on which a unique index is defined',
  `guid` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `title_hash` varchar(128) NOT NULL COMMENT 'hash of the feeditem''s title on which a unique index is defined',
  `pub_date` text,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'insertion date',
  `feed_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`feed_id`),
  UNIQUE KEY `guid_hash` (`title_hash`),
  UNIQUE KEY `link_hash` (`link_hash`),
  KEY `feed_id` (`feed_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `feeditem_tag`
--

CREATE TABLE IF NOT EXISTS `feeditem_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feeditem_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'insertion date',
  `weight_miner` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `feeditem_id` (`feeditem_id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `feed_tag`
--

CREATE TABLE IF NOT EXISTS `feed_tag` (
  `tag_id` int(11) NOT NULL,
  `feed_id` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'insertion date',
  PRIMARY KEY (`tag_id`,`feed_id`,`id`),
  KEY `fk_tag_has_feed_feed1` (`feed_id`),
  KEY `fk_tag_has_feed_tag1` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE IF NOT EXISTS `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `url` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `count` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'insertion date',
  `id_miner` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `feeditem`
--
ALTER TABLE `feeditem`
  ADD CONSTRAINT `feeditem_ibfk_1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`id`);

--
-- Constraints for table `feeditem_tag`
--
ALTER TABLE `feeditem_tag`
  ADD CONSTRAINT `feeditem_tag_ibfk_4` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`),
  ADD CONSTRAINT `feeditem_tag_ibfk_3` FOREIGN KEY (`feeditem_id`) REFERENCES `feeditem` (`id`);

--
-- Constraints for table `feed_tag`
--
ALTER TABLE `feed_tag`
  ADD CONSTRAINT `fk_tag_has_feed_feed1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_tag_has_feed_tag1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
