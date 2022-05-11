-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 11, 2022 at 11:00 AM
-- Server version: 10.3.34-MariaDB-0ubuntu0.20.04.1
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ercot`
--

-- --------------------------------------------------------

--
-- Table structure for table `demand`
--

CREATE TABLE `demand` (
  `id` bigint(11) UNSIGNED NOT NULL,
  `Demand` float NOT NULL COMMENT 'Total system demand',
  `datetime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='System-wide demand';

-- --------------------------------------------------------

--
-- Table structure for table `downloads`
--

CREATE TABLE `downloads` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `ercot_report_id` int(11) NOT NULL,
  `ercot_doc_id` bigint(11) UNSIGNED NOT NULL,
  `status_code` int(11) NOT NULL COMMENT 'HTTP status code',
  `downloaded` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='"Meta" table to track which documents have been downloaded';

-- --------------------------------------------------------

--
-- Table structure for table `generation`
--

CREATE TABLE `generation` (
  `id` bigint(11) UNSIGNED NOT NULL,
  `SE_MW` float NOT NULL COMMENT 'State estimator - MW',
  `SE_MVAR` float NOT NULL COMMENT 'State estimator - MVAR',
  `SCADA_MW` float NOT NULL COMMENT 'SCADA - MW',
  `SCADA_MVAR` float NOT NULL COMMENT 'SCADA - MVAR',
  `datetime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Total ERCOT Generation';

-- --------------------------------------------------------

--
-- Table structure for table `solar`
--

CREATE TABLE `solar` (
  `id` bigint(11) UNSIGNED NOT NULL,
  `SYSTEM_WIDE` float NOT NULL COMMENT 'Solar power generated system wide in MW',
  `datetime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Holds 5-minute interval system-wide solar generation';

-- --------------------------------------------------------

--
-- Table structure for table `wind`
--

CREATE TABLE `wind` (
  `id` bigint(11) UNSIGNED NOT NULL,
  `SYSTEM_WIDE` float NOT NULL COMMENT 'Wind power generated system wide in MW',
  `LZ_SOUTH_HOUSTON` float NOT NULL,
  `LZ_WEST` float NOT NULL,
  `LZ_NORTH` float NOT NULL,
  `datetime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Holds 5-minute interval system-wide wind generation';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `demand`
--
ALTER TABLE `demand`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `datetime` (`datetime`);

--
-- Indexes for table `downloads`
--
ALTER TABLE `downloads`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ercot_doc_id` (`ercot_doc_id`);

--
-- Indexes for table `generation`
--
ALTER TABLE `generation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `datetime` (`datetime`);

--
-- Indexes for table `solar`
--
ALTER TABLE `solar`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `datetime` (`datetime`);

--
-- Indexes for table `wind`
--
ALTER TABLE `wind`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `datetime` (`datetime`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `demand`
--
ALTER TABLE `demand`
  MODIFY `id` bigint(11) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `downloads`
--
ALTER TABLE `downloads`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `generation`
--
ALTER TABLE `generation`
  MODIFY `id` bigint(11) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `solar`
--
ALTER TABLE `solar`
  MODIFY `id` bigint(11) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wind`
--
ALTER TABLE `wind`
  MODIFY `id` bigint(11) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
