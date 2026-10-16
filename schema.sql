CREATE DATABASE IF NOT EXISTS expense_tracker
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE expense_tracker;

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    category VARCHAR(40) NOT NULL,
    expense_date DATE NOT NULL,
    payment_method VARCHAR(30) NOT NULL DEFAULT 'Other',
    notes VARCHAR(500) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_expense_date (expense_date),
    INDEX idx_category (category)
);

-- Optional demo data. Run this section only if you want sample records.
INSERT INTO expenses (title, amount, category, expense_date, payment_method, notes) VALUES
('Lunch with friends', 280.00, 'Food', CURDATE(), 'UPI', 'Demo record'),
('Metro recharge', 150.00, 'Transport', CURDATE(), 'UPI', 'Demo record'),
('Monthly internet', 799.00, 'Bills', CURDATE(), 'Debit Card', 'Demo record');
