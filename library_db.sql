-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 26, 2025 at 06:05 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `lb_books`
--

CREATE TABLE `lb_books` (
  `book_id` int(11) NOT NULL,
  `book_title` varchar(255) NOT NULL,
  `book_author` varchar(255) DEFAULT NULL,
  `book_publisher` varchar(255) DEFAULT NULL,
  `book_category` varchar(100) DEFAULT NULL,
  `shelf_number` varchar(50) DEFAULT NULL,
  `status` enum('available','borrowed','lost') DEFAULT 'available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lb_borrow_transactions`
--

CREATE TABLE `lb_borrow_transactions` (
  `transaction_id` int(11) NOT NULL,
  `book_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  `borrow_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `status` enum('borrowed','returned','overdue') DEFAULT 'borrowed'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lb_penalties`
--

CREATE TABLE `lb_penalties` (
  `penalty_id` int(11) NOT NULL,
  `transaction_id` int(11) DEFAULT NULL,
  `days_late` int(11) DEFAULT NULL,
  `duty_hours` int(11) DEFAULT NULL,
  `is_served` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lb_students`
--

CREATE TABLE `lb_students` (
  `student_id` int(11) NOT NULL,
  `student_number` varchar(20) NOT NULL,
  `student_full_name` varchar(255) NOT NULL,
  `student_course` varchar(100) DEFAULT NULL,
  `student_year_level` int(11) DEFAULT NULL,
  `student_email` varchar(100) DEFAULT NULL,
  `student_contact_number` varchar(20) DEFAULT NULL,
  `student_address` varchar(100) DEFAULT NULL,
  `registration_date` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lb_users`
--

CREATE TABLE `lb_users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `role` enum('admin','librarian') DEFAULT 'librarian'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `lb_books`
--
ALTER TABLE `lb_books`
  ADD PRIMARY KEY (`book_id`);

--
-- Indexes for table `lb_borrow_transactions`
--
ALTER TABLE `lb_borrow_transactions`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `lb_borrow_transactions_ibfk_1` (`book_id`),
  ADD KEY `fk_student_id` (`student_id`);

--
-- Indexes for table `lb_penalties`
--
ALTER TABLE `lb_penalties`
  ADD PRIMARY KEY (`penalty_id`),
  ADD KEY `fk_transaction` (`transaction_id`);

--
-- Indexes for table `lb_students`
--
ALTER TABLE `lb_students`
  ADD PRIMARY KEY (`student_id`),
  ADD UNIQUE KEY `student_number` (`student_number`);

--
-- Indexes for table `lb_users`
--
ALTER TABLE `lb_users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `lb_books`
--
ALTER TABLE `lb_books`
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `lb_borrow_transactions`
--
ALTER TABLE `lb_borrow_transactions`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `lb_penalties`
--
ALTER TABLE `lb_penalties`
  MODIFY `penalty_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `lb_students`
--
ALTER TABLE `lb_students`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `lb_users`
--
ALTER TABLE `lb_users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `lb_borrow_transactions`
--
ALTER TABLE `lb_borrow_transactions`
  ADD CONSTRAINT `fk_student_id` FOREIGN KEY (`student_id`) REFERENCES `lb_students` (`student_id`),
  ADD CONSTRAINT `lb_borrow_transactions_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `lb_books` (`book_id`);

--
-- Constraints for table `lb_penalties`
--
ALTER TABLE `lb_penalties`
  ADD CONSTRAINT `fk_transaction` FOREIGN KEY (`transaction_id`) REFERENCES `lb_borrow_transactions` (`transaction_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lb_penalties_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `lb_borrow_transactions` (`transaction_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
