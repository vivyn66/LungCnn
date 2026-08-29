-- Sanitized SQL Schema for LungCnn
-- Excludes all patient, doctor, and administrator credentials/records.

SET FOREIGN_KEY_CHECKS=0;
SET SESSION sql_require_primary_key=0;


--
-- Table structure for table `admintb`
--
DROP TABLE IF EXISTS `admintb`;
CREATE TABLE `admintb` (
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `apptb`
--
DROP TABLE IF EXISTS `apptb`;
CREATE TABLE `apptb` (
  `id` bigint(250) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `DoctorName` varchar(250) NOT NULL,
  `Date` date NOT NULL,
  `Specialist` varchar(250) NOT NULL,
  `Disease` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;

--
-- Table structure for table `doctortb`
--
DROP TABLE IF EXISTS `doctortb`;
CREATE TABLE `doctortb` (
  `Name` varchar(250) NOT NULL,
  `Gender` varchar(250) NOT NULL,
  `Age` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `Specialist` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Location` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `drugtb`
--
DROP TABLE IF EXISTS `drugtb`;
CREATE TABLE `drugtb` (
  `id` bigint(250) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `EmailId` varchar(250) NOT NULL,
  `DoctorName` varchar(250) NOT NULL,
  `Medicine` varchar(250) NOT NULL,
  `OtherInfo` varchar(500) NOT NULL,
  `Report` varchar(500) NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;

--
-- Table structure for table `regtb`
--
DROP TABLE IF EXISTS `regtb`;
CREATE TABLE `regtb` (
  `Name` varchar(250) NOT NULL,
  `Gender` varchar(250) NOT NULL,
  `Age` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Location` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS=1;
