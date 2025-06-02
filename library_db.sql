-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 02, 2025 at 12:35 PM
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

--
-- Dumping data for table `lb_books`
--

INSERT INTO `lb_books` (`book_id`, `book_title`, `book_author`, `book_publisher`, `book_category`, `shelf_number`, `status`) VALUES
(10, 'Introduction to Algorithms', 'Thomas H. Cormen', 'MIT Press', 'Computer Science', '1', 'available'),
(11, 'Clean Code', 'Robert C. Martin', 'Prentice Hall', 'Software Engineering', '2', 'available'),
(12, 'The Pragmatic Programmer', 'Andrew Hunt', 'Addison-Wesley', 'Programming', '3', 'available'),
(13, 'Artificial Intelligence: A Modern Approach', 'Stuart Russell', 'Pearson', 'AI', '4', 'available'),
(14, 'Database System Concepts', 'Abraham Silberschatz', 'McGraw-Hill', 'Database', '5', 'borrowed'),
(15, 'Operating System Concepts', 'Abraham Silberschatz', 'Wiley', 'Operating Systems', '6', 'available'),
(16, 'Computer Networks', 'Andrew S. Tanenbaum', 'Pearson', 'Networking', '7', 'available'),
(17, 'Modern Control Engineering', 'Katsuhiko Ogata', 'Pearson', 'Control Systems', '8', 'available'),
(18, 'Digital Design', 'M. Morris Mano', 'Pearson', 'Digital Electronics', '9', 'available'),
(19, 'Software Engineering', 'Ian Sommerville', 'Pearson', 'Software Engineering', '10', 'available');

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

--
-- Dumping data for table `lb_borrow_transactions`
--

INSERT INTO `lb_borrow_transactions` (`transaction_id`, `book_id`, `student_id`, `borrow_date`, `due_date`, `return_date`, `status`) VALUES
(25, 11, 16, '2025-05-18', '2025-05-23', '2025-05-25', 'returned'),
(26, 14, 16, '2025-06-02', '2025-06-09', NULL, 'borrowed'),
(27, 10, 14, '2025-05-22', '2025-05-25', '2025-05-29', 'returned');

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

--
-- Dumping data for table `lb_penalties`
--

INSERT INTO `lb_penalties` (`penalty_id`, `transaction_id`, `days_late`, `duty_hours`, `is_served`) VALUES
(9, 27, 4, 4, 1),
(10, 25, 2, 2, 1);

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

--
-- Dumping data for table `lb_students`
--

INSERT INTO `lb_students` (`student_id`, `student_number`, `student_full_name`, `student_course`, `student_year_level`, `student_email`, `student_contact_number`, `student_address`, `registration_date`) VALUES
(13, '20230001', 'Juan Dela Cruz', 'BSIT', 2, 'juan@example.com', '09123456789', 'Barangay Uno, Cityville', '2025-06-02'),
(14, '20230002', 'Maria Santos', 'BSCS', 1, 'maria@example.com', '09123456780', 'Purok 3, Townsville', '2025-06-02'),
(15, '20230003', 'Pedro Reyes', 'BSIT', 3, 'pedro@example.com', '09123456781', 'Zone 5, Sitio Kalikasan', '2025-06-02'),
(16, '20230004', 'Ana Lopez', 'BSCS', 4, 'ana@example.com', '09123456782', 'Blk 7 Lot 8, Greenfield', '2025-06-02'),
(17, '20230005', 'Carlos Mendoza', 'BSIT', 2, 'carlos@example.com', '09123456783', 'Street 12, Cavite City', '2025-06-02'),
(18, '20230006', 'Liza Ramirez', 'BSCS', 3, 'liza@example.com', '09123456784', 'Purok 6, Hilltop', '2025-06-02'),
(19, '20230007', 'Mark Villanueva', 'BSIT', 1, 'mark@example.com', '09123456785', 'Barangay Central, Baytown', '2025-06-02'),
(20, '20230008', 'Sophia Cruz', 'BSCS', 2, 'sophia@example.com', '09123456786', 'Sitio Mabuhay, Northside', '2025-06-02'),
(21, '20230009', 'Rico Fernandez', 'BSIT', 4, 'rico@example.com', '09123456787', 'Zone 8, Eastfield', '2025-06-02'),
(22, '20230010', 'Elena Torres', 'BSCS', 3, 'elena@example.com', '09123456788', 'Blk 4 Lot 3, Lakeside', '2025-06-02'),
(23, '202245502', 'Juan Dimakatuwid', 'BSCS', 1, 'juan.dimakatuwid@gmail.com', '09998796504', 'Brgy. Inocencio, Trece Martires City, Cavite', '2025-06-02');

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
-- Dumping data for table `lb_users`
--

INSERT INTO `lb_users` (`user_id`, `username`, `password`, `full_name`, `role`) VALUES
(7, 'kaito', '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c', 'Armand Christian N. Sta. Maria', 'admin'),
(8, 'mama', '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c', 'Armand Christian N. Sta. Maria', 'librarian');

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
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `lb_borrow_transactions`
--
ALTER TABLE `lb_borrow_transactions`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `lb_penalties`
--
ALTER TABLE `lb_penalties`
  MODIFY `penalty_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `lb_students`
--
ALTER TABLE `lb_students`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `lb_users`
--
ALTER TABLE `lb_users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

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
