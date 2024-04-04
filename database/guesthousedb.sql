-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 04, 2024 at 02:54 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `guesthousedb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `adminId` bigint(20) NOT NULL,
  `adminName` varchar(100) DEFAULT NULL,
  `adminEmail` varchar(100) DEFAULT NULL,
  `adminPassword` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`adminId`, `adminName`, `adminEmail`, `adminPassword`) VALUES
(1, 'admin', 'admin@admin.com', '$2a$12$th1Z6zsejiNdjl9r4.aZX.9pd3EJ.IDaejvgbFhiOLwP0lkTXyjHq');

-- --------------------------------------------------------

--
-- Table structure for table `house`
--

CREATE TABLE `house` (
  `houseId` bigint(20) NOT NULL,
  `houseName` varchar(100) DEFAULT NULL,
  `houseCategory` varchar(100) DEFAULT NULL,
  `houseDescription` text DEFAULT NULL,
  `houseThumbnail` text DEFAULT NULL,
  `houseBed` int(11) DEFAULT NULL,
  `housePeople` int(11) DEFAULT NULL,
  `housePrice` double DEFAULT NULL,
  `houseStatus` varchar(50) DEFAULT NULL,
  `houseAvailability` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `house`
--

INSERT INTO `house` (`houseId`, `houseName`, `houseCategory`, `houseDescription`, `houseThumbnail`, `houseBed`, `housePeople`, `housePrice`, `houseStatus`, `houseAvailability`) VALUES
(11, 'Bougainvilla', 'Homestay', 'Fitted with air conditioning and tiled flooring, this comfortable house features a dining area and a spacious living room with sofa and flat-screen satellite TV. The kitchen is well-equipped with a stove, fridge, oven and kitchenware. En suite bathroom comes with shower facility. Guests booking 6-person rate will get 2 bedrooms, and the other room will be locked.', '64d63f70a6154347bc50e4694315d575.jpeg', 4, 8, 165, 'Free', '1'),
(13, 'Freesia Studio', 'Studio', 'This air-conditioned double room has a TV and a refrigerator. The en suite bathroom is fitted with shower and free toiletries. The double room includes 2 single-size beds that can accommodate up to 2 guests.', 'e520baab745a42d3a9c4ebd30789f00f.jpeg', 2, 4, 190, 'Free', '1'),
(14, 'Ixora Studio', 'Studio', 'This air-conditioned double room has a TV and refrigerator. The en suite bathroom is fitted with shower and free toiletries. The double room includes 1 queen-size bed that can accommodate up to 2 guests.', '92eb72a26e78480fa224b8ce8bf42e2c.jpeg', 1, 2, 150, 'Free', '1'),
(15, 'Rose House', 'House', 'This air-conditioned holiday home also has a fan option. It features a dining area and a kitchen equipped with an electric stovetop, rice cooker, refrigerator, oven and kitchenware. It is fitted with a flat-screen satellite TV and a sofa. The en suite bathroom includes shower facilities. The house includes 2 queen-sized beds that can accommodate up to 4 guests.', '3627abef27a44e518bc7cc2a302bcd09.jpeg', 2, 4, 100, 'Free', '1'),
(16, 'Tulip House', 'House', 'This air-conditioned holiday home also has a fan option. It features a dining area and a kitchen equipped with an electric stovetop, rice cooker, refrigerator, oven and kitchenware. It is fitted with a flat-screen satellite TV and a sofa. The en suite bathroom includes shower facilities. The house includes 1 queen-size bed that can accommodate up to 2 guests.', 'db197dcda3544ea181b6d402d0725134.jpeg', 1, 3, 90, 'Free', '1'),
(17, 'Tulip House Tester', 'Villa', 'sadfsdf sdafsadl;fl klsdakfsadq sadfsdf sdafsadl;fl klsdakfsadq', 'e66b362d633a41e9be0f523e2e3e1505.jpeg', 8, 12, 200, 'Free', '1'),
(18, 'Tulip House Tester', 'Villa', 'sadfsdf sdafsadl;fl klsdakfsadq', '3efeee71793841cbbfa6f1f070a729a7.jpeg', 8, 12, 100, 'Free', '1');

-- --------------------------------------------------------

--
-- Table structure for table `housefacilities`
--

CREATE TABLE `housefacilities` (
  `facId` int(11) NOT NULL,
  `houseId` bigint(20) DEFAULT NULL,
  `facName` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `housefacilities`
--

INSERT INTO `housefacilities` (`facId`, `houseId`, `facName`) VALUES
(88, 11, 'Kitchen'),
(89, 11, 'Private bathroom'),
(90, 11, 'Garden view'),
(91, 11, 'Swimming Pool'),
(92, 11, 'Air Conditioner'),
(93, 11, 'Patio'),
(94, 11, 'Flat-screen TV'),
(95, 11, 'Barbecue'),
(96, 11, 'Room Service'),
(97, 11, 'Wifi'),
(108, 13, 'Kitchen'),
(109, 13, 'Private bathroom'),
(110, 13, 'Garden view'),
(111, 13, 'Swimming Pool'),
(112, 13, 'Air Conditioner'),
(113, 13, 'Wifi'),
(114, 14, 'Air Conditioner'),
(115, 14, 'Patio'),
(116, 14, 'Flat-screen TV'),
(117, 14, 'Barbecue'),
(118, 14, 'Room Service'),
(119, 14, 'Wifi'),
(120, 15, 'Kitchen'),
(121, 15, 'Private bathroom'),
(122, 15, 'Garden view'),
(123, 15, 'Swimming Pool'),
(124, 15, 'Barbecue'),
(125, 15, 'Room Service'),
(126, 15, 'Wifi'),
(127, 16, 'Kitchen'),
(128, 16, 'Private bathroom'),
(129, 16, 'Patio'),
(130, 16, 'Flat-screen TV'),
(131, 16, 'Barbecue'),
(132, 16, 'Room Service'),
(133, 16, 'Wifi'),
(134, 17, 'Kitchen'),
(135, 17, 'Swimming Pool'),
(136, 17, 'Air Conditioner'),
(137, 17, 'Patio'),
(138, 17, 'Wifi'),
(139, 17, 'Room Service'),
(140, 17, 'Barbecue'),
(141, 17, 'Flat-screen TV'),
(142, 18, 'Kitchen'),
(143, 18, 'Swimming Pool'),
(144, 18, 'Air Conditioner'),
(145, 18, 'Patio'),
(146, 18, 'Wifi'),
(147, 18, 'Room Service'),
(148, 18, 'Barbecue'),
(149, 18, 'Flat-screen TV');

-- --------------------------------------------------------

--
-- Table structure for table `houseimages`
--

CREATE TABLE `houseimages` (
  `id` int(11) NOT NULL,
  `houseId` bigint(20) DEFAULT NULL,
  `images` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `houseimages`
--

INSERT INTO `houseimages` (`id`, `houseId`, `images`) VALUES
(91, 11, '7834d44d027d4d2fb3999481adff9ee2.jpeg'),
(92, 11, '1cabe97c60994038b56f550f148fadc1.jpeg'),
(93, 11, '70263edd02f246e694276cfda993b19f.jpeg'),
(94, 11, '7eefc163d7594d4e8e009031798da5f2.jpeg'),
(95, 11, 'eb38c4901cdf4312b9ba9584fd7bc1f5.jpeg'),
(96, 11, 'c23851ac859340f0bd52dfd7815dcba7.jpeg'),
(97, 11, 'd89ff7623e0144179a736c4982303567.jpeg'),
(105, 13, 'b1a4dbb81edc4d5bb5d34bfdec8dcd40.jpeg'),
(106, 13, 'b4e9b2741fbf40e5b617719288f13657.jpeg'),
(107, 13, 'd7fff2f86835469e8549b8f9d71a4af2.jpeg'),
(108, 13, '07d615b9da054572bc945a41fa697eb0.jpeg'),
(109, 13, '1d299fbe3e2d4ef0b5f87b4eccd89fcc.jpeg'),
(110, 14, 'cd631b6dc9c54fffb4dc953e704001d0.jpeg'),
(111, 14, 'acab1d94ff2548e6a289aa8b87535387.jpeg'),
(112, 14, '5d93a0e7f60a4743beae51736ebcca8d.jpeg'),
(113, 14, '2763854d7b5e455c8fc5c109d3625ade.jpeg'),
(114, 14, 'e93f7b98a5104c0ea2f6eaacb6255f10.jpeg'),
(115, 15, '0af6d14c1a884d87ae0f71d96f7a468d.jpeg'),
(116, 15, '84b9f92d26124bb696a6d7dd846fb425.jpeg'),
(117, 15, '2115a4dd377348e08e5128b596c9d0fb.jpeg'),
(118, 15, '8b1b2177441e4be0a978916061a6254c.jpeg'),
(119, 15, '5eb3649dd1fd4c309fe7d657712107b5.jpeg'),
(120, 15, '0a47ccd3f1214802b38a9337d86fbd3e.jpeg'),
(121, 16, '7e937d8edd194d04aa963f2b4daabc11.jpeg'),
(122, 16, '39634575dc5b4310aac060ecc8935903.jpeg'),
(123, 16, 'c7dea60a7ce741e5b7c6d80f63f8cb1b.jpeg'),
(124, 16, 'a16986df3ddd41f28297c855eeaa312e.jpeg'),
(125, 17, '56eaeb2c6a484862b6fbc3d745798fae.jpeg'),
(126, 17, '1e8b257416e24378a596232444a0c5da.jpeg'),
(127, 17, 'c5090e9991964d789d3cbdd1442e77e4.jpeg'),
(128, 17, 'a6faa05cb57c4c93a7789e83dee01a90.jpeg'),
(129, 17, 'b36eb5cdf3de408598b4fbe1855f97e0.jpeg'),
(130, 17, '762926ae9c6046e1a1ca41c12846736b.jpeg'),
(131, 17, '584e73208639412cae92dda6113b5bc9.jpeg'),
(132, 17, '511204c508234b6e9d2c1f3f6d17dac4.jpeg'),
(133, 18, '775ba1e27b8046eb8bebb4d05e5a6707.jpeg'),
(134, 18, 'f42be20d76fe4590a10a49b4e446b872.jpeg'),
(135, 18, '8277704c15b14d2898a3428c53c1bd20.jpeg'),
(136, 18, '97bc8e8952944694955927c4691ec118.jpeg'),
(137, 18, '98881b93b7724b30a3f6dc9aa06ca3a3.jpeg'),
(138, 18, '4a1ca2bde5ea4800912ffb3c2913da7f.jpeg'),
(139, 18, '62926ad66f134cd5b1eaf92d5336a425.jpeg'),
(140, 18, '4f1ae78db1ed4348b2d3dbfbad803ae6.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `houselocation`
--

CREATE TABLE `houselocation` (
  `id` int(11) NOT NULL,
  `houseId` bigint(20) DEFAULT NULL,
  `houseLocation` varchar(300) DEFAULT NULL,
  `houseAddress` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `houselocation`
--

INSERT INTO `houselocation` (`id`, `houseId`, `houseLocation`, `houseAddress`) VALUES
(10, 11, 'Pantai Cenang, Langkawi', 'No.53A, Lot 1721,Kg.Perana,Mk.Kedawang,Langkawi, 07000 Pantai Cenang, Malaysia'),
(12, 13, 'Pantai Cenang, Langkawi', 'No.53A, Lot 1721,Kg.Perana,Mk.Kedawang,Langkawi, 07000 Pantai Cenang, Malaysia'),
(13, 14, 'Pantai Cenang, Langkawi', 'No.53A, Lot 1721,Kg.Perana,Mk.Kedawang,Langkawi, 07000 Pantai Cenang, Malaysia'),
(14, 15, 'Pantai Cenang, Langkawi', 'No.53A, Lot 1721,Kg.Perana,Mk.Kedawang,Langkawi, 07000 Pantai Cenang, Malaysia'),
(15, 16, 'Pantai Cenang, Langkawi', 'No.53A, Lot 1721,Kg.Perana,Mk.Kedawang,Langkawi, 07000 Pantai Cenang, Malaysia'),
(16, 17, 'Pantai Cenang, Langkawi', 'NMo 83 Kuala Kurau Perak'),
(17, 18, 'Pantai Cenang, Langkawi', 'NMo 83 Kuala Kurau Perak');

-- --------------------------------------------------------

--
-- Table structure for table `policy`
--

CREATE TABLE `policy` (
  `policyId` int(11) NOT NULL,
  `policyNote` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `policy`
--

INSERT INTO `policy` (`policyId`, `policyNote`) VALUES
(1, 'Check-in time is from 14:30 PM and check-out time is until 12:00 PM'),
(2, 'Guests will be held responsible for any loss or damage to Kapal Terbang Guest House caused by themselves, their friends or any person for whom they are responsible.'),
(3, 'Guest House Management is not responsible for guest’s personal belongings and valuables like money, jewelry, smartphones, laptops or any other valuables left by guests in the guest house.'),
(4, 'Hours of swimming pool operation are from 8:30 am to 7:30 pm.'),
(5, 'Children below 12 years old must be accompanied by an adult.'),
(6, 'Guests swim at their own risk and the guest house management will not responsible for any injuries while using the Kapal Terbang Guest House facilities.'),
(7, 'A damage deposit of RM 100.00 is required during arrival. Guest deposit will be refunded in full in cash during check out, subject to an inspection of the guest house.'),
(8, 'These rules and regulations are subject to change any time without notice.'),
(9, 'Once check in, the cancellation of booking will not be entertained. The money will not be refunded.'),
(10, 'Regardless of charge instructions, I acknowledge that I am personally liable for the payment all charges occurred by me during my stay at Kapal Terbang Guest House.');

-- --------------------------------------------------------

--
-- Table structure for table `rating`
--

CREATE TABLE `rating` (
  `ratingId` int(11) NOT NULL,
  `houseId` bigint(20) DEFAULT NULL,
  `ratingScore` double DEFAULT NULL,
  `totalReviews` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

CREATE TABLE `reservation` (
  `reservationId` varchar(20) NOT NULL,
  `userId` bigint(20) DEFAULT NULL,
  `bookStartDate` date DEFAULT NULL,
  `bookEndDate` date DEFAULT NULL,
  `bookStatus` varchar(50) DEFAULT 'Pending',
  `houseId` bigint(20) DEFAULT NULL,
  `totalAmount` double DEFAULT NULL,
  `bookHouseStatus` varchar(15) DEFAULT 'Pending',
  `adultNumber` int(11) DEFAULT NULL,
  `childrenNumber` int(11) DEFAULT NULL,
  `bookingNote` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `servicerequest`
--

CREATE TABLE `servicerequest` (
  `serviceId` varchar(12) NOT NULL,
  `userId` bigint(20) DEFAULT NULL,
  `userServiceNote` text DEFAULT NULL,
  `serviceStatus` varchar(20) DEFAULT 'Pending',
  `reservationId` varchar(15) DEFAULT NULL,
  `adminServiceNote` text DEFAULT NULL,
  `serviceDate` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `userfavourite`
--

CREATE TABLE `userfavourite` (
  `favId` bigint(20) NOT NULL,
  `userId` bigint(20) DEFAULT NULL,
  `houseId` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userfavourite`
--

INSERT INTO `userfavourite` (`favId`, `userId`, `houseId`) VALUES
(24, 10000, 14),
(33, 10000, 17);

-- --------------------------------------------------------

--
-- Table structure for table `userreview`
--

CREATE TABLE `userreview` (
  `reviewId` bigint(20) NOT NULL,
  `userId` bigint(20) DEFAULT NULL,
  `houseId` bigint(20) DEFAULT NULL,
  `reviewNote` text DEFAULT NULL,
  `rate` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userreview`
--

INSERT INTO `userreview` (`reviewId`, `userId`, `houseId`, `reviewNote`, `rate`) VALUES
(8, 10000, 15, 'asdasd', 3),
(9, 10000, 11, 'all okay and nice', 5),
(10, 10000, 11, 'asdasd', 4.5),
(11, 10000, 13, 'asdfsdfsdfdfv sdfgsdfg sdgd', 1),
(12, 10000, 11, 'rumah terbaik, service terbaik gila', 5);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userId` bigint(20) NOT NULL,
  `userFullName` varchar(100) DEFAULT NULL,
  `userEmail` varchar(100) DEFAULT NULL,
  `userPassword` varchar(500) DEFAULT NULL,
  `userImage` text DEFAULT NULL,
  `phoneNumber` bigint(20) DEFAULT NULL,
  `userCountry` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userId`, `userFullName`, `userEmail`, `userPassword`, `userImage`, `phoneNumber`, `userCountry`) VALUES
(10000, 'Muhamad Azim bin Mohd Fauzi', 'azim@gmail.com', '$2a$12$6HsH3adGydSiwcJCvoXxSOrANuox.cDgxZxD8LADxjaT1GgLFbBSy', '388fd462e5b14543919fd11ebd819a2d.jpeg', 6011332222233, 'Malaysia'),
(10006, 'Muhamad Haiqals', 'haiqal@gmail.co1', '$2b$12$Vqaf7h/rf67v8aPfhh0DPOEYZ2qUmZPjYrjol1HvZ/LhHjCIltwgm', 'e979d70f583447839d943d0e83079ed5.jpeg', 6060113322222, 'Malaysia'),
(10007, 'asdas', 'azim@gma', '$2b$12$c/l7A4v88PbYLvXIbgRXfuL.AQlfkGzrXgyehbc6jy0L4.JE0phvK', '77141e3b94e140beb521c1c3cfe9eb9f.jpeg', 601134234, 'Malaysia');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`adminId`);

--
-- Indexes for table `house`
--
ALTER TABLE `house`
  ADD PRIMARY KEY (`houseId`);

--
-- Indexes for table `housefacilities`
--
ALTER TABLE `housefacilities`
  ADD PRIMARY KEY (`facId`),
  ADD KEY `houseId` (`houseId`);

--
-- Indexes for table `houseimages`
--
ALTER TABLE `houseimages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `houseId` (`houseId`);

--
-- Indexes for table `houselocation`
--
ALTER TABLE `houselocation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `houseId` (`houseId`);

--
-- Indexes for table `policy`
--
ALTER TABLE `policy`
  ADD PRIMARY KEY (`policyId`);

--
-- Indexes for table `rating`
--
ALTER TABLE `rating`
  ADD PRIMARY KEY (`ratingId`),
  ADD KEY `houseId` (`houseId`);

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`reservationId`),
  ADD KEY `userId` (`userId`),
  ADD KEY `fk_houseId` (`houseId`);

--
-- Indexes for table `servicerequest`
--
ALTER TABLE `servicerequest`
  ADD PRIMARY KEY (`serviceId`),
  ADD KEY `userId` (`userId`),
  ADD KEY `fk_reservationId` (`reservationId`);

--
-- Indexes for table `userfavourite`
--
ALTER TABLE `userfavourite`
  ADD PRIMARY KEY (`favId`),
  ADD KEY `userId` (`userId`),
  ADD KEY `houseId` (`houseId`);

--
-- Indexes for table `userreview`
--
ALTER TABLE `userreview`
  ADD PRIMARY KEY (`reviewId`),
  ADD KEY `userId` (`userId`),
  ADD KEY `houseId` (`houseId`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `adminId` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `house`
--
ALTER TABLE `house`
  MODIFY `houseId` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `housefacilities`
--
ALTER TABLE `housefacilities`
  MODIFY `facId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=158;

--
-- AUTO_INCREMENT for table `houseimages`
--
ALTER TABLE `houseimages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=148;

--
-- AUTO_INCREMENT for table `houselocation`
--
ALTER TABLE `houselocation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `policy`
--
ALTER TABLE `policy`
  MODIFY `policyId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `rating`
--
ALTER TABLE `rating`
  MODIFY `ratingId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `userfavourite`
--
ALTER TABLE `userfavourite`
  MODIFY `favId` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `userreview`
--
ALTER TABLE `userreview`
  MODIFY `reviewId` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userId` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10008;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `housefacilities`
--
ALTER TABLE `housefacilities`
  ADD CONSTRAINT `housefacilities_ibfk_1` FOREIGN KEY (`houseId`) REFERENCES `house` (`houseId`);

--
-- Constraints for table `houseimages`
--
ALTER TABLE `houseimages`
  ADD CONSTRAINT `houseimages_ibfk_1` FOREIGN KEY (`houseId`) REFERENCES `house` (`houseId`);

--
-- Constraints for table `houselocation`
--
ALTER TABLE `houselocation`
  ADD CONSTRAINT `houselocation_ibfk_1` FOREIGN KEY (`houseId`) REFERENCES `house` (`houseId`);

--
-- Constraints for table `rating`
--
ALTER TABLE `rating`
  ADD CONSTRAINT `rating_ibfk_1` FOREIGN KEY (`houseId`) REFERENCES `house` (`houseId`);

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `fk_houseId` FOREIGN KEY (`houseId`) REFERENCES `house` (`houseId`),
  ADD CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`);

--
-- Constraints for table `servicerequest`
--
ALTER TABLE `servicerequest`
  ADD CONSTRAINT `fk_reservationId` FOREIGN KEY (`reservationId`) REFERENCES `reservation` (`reservationId`),
  ADD CONSTRAINT `servicerequest_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`);

--
-- Constraints for table `userfavourite`
--
ALTER TABLE `userfavourite`
  ADD CONSTRAINT `userfavourite_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`),
  ADD CONSTRAINT `userfavourite_ibfk_2` FOREIGN KEY (`houseId`) REFERENCES `house` (`houseId`);

--
-- Constraints for table `userreview`
--
ALTER TABLE `userreview`
  ADD CONSTRAINT `userReview_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`),
  ADD CONSTRAINT `userReview_ibfk_2` FOREIGN KEY (`houseId`) REFERENCES `house` (`houseId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
