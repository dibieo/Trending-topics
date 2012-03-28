-- phpMyAdmin SQL Dump
-- version 3.4.10.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 16, 2012 at 10:09 AM
-- Server version: 5.1.41
-- PHP Version: 5.3.2-1ubuntu4.14

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `trendingTopics`
--

-- --------------------------------------------------------

--
-- Table structure for table `feed`
--

CREATE TABLE IF NOT EXISTS `feed` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_id` int(11) NOT NULL,
  `last_build_date` int(11) DEFAULT NULL,
  `pub_date` int(11) DEFAULT NULL,
  `last_check_date` int(11) DEFAULT NULL,
  `category` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `language` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `ttl` int(11) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'insertion date',
  PRIMARY KEY (`id`),
  KEY `source_id` (`source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `feeditem_tag`
--

CREATE TABLE IF NOT EXISTS `feeditem_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feeditem_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `feeditem_id` (`feeditem_id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `feed_item`
--

CREATE TABLE IF NOT EXISTS `feed_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `link` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `guid` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `pub_date` int(11) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `feed_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`feed_id`),
  KEY `fk_feed_item_feed1` (`feed_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- Table structure for table `feed_tag`
--

CREATE TABLE IF NOT EXISTS `feed_tag` (
  `tag_id` int(11) NOT NULL,
  `feed_id` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`tag_id`,`feed_id`,`id`),
  KEY `fk_tag_has_feed_feed1` (`feed_id`),
  KEY `fk_tag_has_feed_tag1` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `source`
--

CREATE TABLE IF NOT EXISTS `source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `link` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=23 ;

--
-- Dumping data for table `source`
--

INSERT INTO `source` (`id`, `title`, `description`, `link`, `date`) VALUES
(21, 'Science News', 'News about science', 'http://www.sciencenews.org/view/feed/type/news/name/articles.rss', '2012-03-16 14:33:45'),
(22, 'Science News', 'News about science', 'http://www.sciencenews.org/view/feed/type/news/name/articles.rss', '2012-03-16 15:10:04');

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE IF NOT EXISTS `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `url` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `count` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `feed`
--
ALTER TABLE `feed`
  ADD CONSTRAINT `feed_ibfk_1` FOREIGN KEY (`source_id`) REFERENCES `source` (`id`);

--
-- Constraints for table `feeditem_tag`
--
ALTER TABLE `feeditem_tag`
  ADD CONSTRAINT `feeditem_tag_ibfk_1` FOREIGN KEY (`feeditem_id`) REFERENCES `feed_item` (`id`),
  ADD CONSTRAINT `feeditem_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`);

--
-- Constraints for table `feed_tag`
--
ALTER TABLE `feed_tag`
  ADD CONSTRAINT `fk_tag_has_feed_tag1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_tag_has_feed_feed1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Adding the weight returned by WikipediaMiner, soheil
--
ALTER TABLE `feeditem_tag` ADD COLUMN `weight_miner` DECIMAL(11) NULL  AFTER `date` ;

--
-- Adding column to tag table to store the topic-id returned by wikipedieminer's wikifer service
--
ALTER TABLE `tag` ADD COLUMN `id_miner` INT(11) NULL  AFTER `date` ;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
