CREATE DATABASE gadget_renting;
USE gadget_renting;

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE,
    email VARCHAR(100),
    address VARCHAR(200)
);
SHOW TABLES;
DESC Customers;

USE gadget_renting;

CREATE TABLE IF NOT EXISTS Gadgets (
    gadget_id INT PRIMARY KEY AUTO_INCREMENT,
    gadget_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    brand VARCHAR(50),
    rent_per_day DECIMAL(10,2) NOT NULL,
    availability_status VARCHAR(20) DEFAULT 'Available'
);

CREATE TABLE IF NOT EXISTS Rentals (
    rental_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    gadget_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    rental_status VARCHAR(20) DEFAULT 'Active',

    FOREIGN KEY (customer_id)
        REFERENCES Customers(customer_id),

    FOREIGN KEY (gadget_id)
        REFERENCES Gadgets(gadget_id)
);

CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    rental_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE,
    payment_method VARCHAR(30),

    FOREIGN KEY (rental_id)
        REFERENCES Rentals(rental_id)
);

CREATE TABLE IF NOT EXISTS Returns (
    return_id INT PRIMARY KEY AUTO_INCREMENT,
    rental_id INT NOT NULL UNIQUE,
    return_date DATE NOT NULL,
    gadget_condition VARCHAR(50),

    FOREIGN KEY (rental_id)
        REFERENCES Rentals(rental_id)
);

CREATE TABLE IF NOT EXISTS Maintenance (
    maintenance_id INT PRIMARY KEY AUTO_INCREMENT,
    gadget_id INT NOT NULL,
    issue_description VARCHAR(200),
    repair_cost DECIMAL(10,2),
    repair_status VARCHAR(30),

    FOREIGN KEY (gadget_id)
        REFERENCES Gadgets(gadget_id)
);
SHOW TABLES;
DESC Customers;
DESC Gadgets;
DESC Maintenance;
DESC Payments;
DESC Rentals;
DESC Returns;
INSERT INTO Customers
(customer_name, phone, email, address)
VALUES
('Rahul', '9876543210', 'rahul@gmail.com', 'Vizag'),
('Priya', '9876543211', 'priya@gmail.com', 'Gajuwaka'),
('Kiran', '9876543212', 'kiran@gmail.com', 'MVP Colony'),
('Sneha', '9876543213', 'sneha@gmail.com', 'Akkayyapalem'),
('Arjun', '9876543214', 'arjun@gmail.com', 'Madhurawada');
SELECT *FROM Customers;
INSERT INTO Gadgets
(gadget_name, category, brand, rent_per_day,
 availability_status)
VALUES
('Laptop', 'Electronics', 'HP', 500, 'Rented'),
('Camera', 'Photography', 'Canon', 800, 'Rented'),
('Projector', 'Electronics', 'Epson', 600, 'Available'),
('Tablet', 'Electronics', 'Samsung', 300, 'Maintenance'),
('Headphones', 'Accessories', 'Sony', 100, 'Available'),
('Smart Watch', 'Accessories', 'Noise', 150, 'Available'),
('Keyboard', 'Accessories', 'Logitech', 80, 'Available');
SELECT *FROM Gadgets;
INSERT INTO Rentals
(customer_id, gadget_id, start_date, end_date,
 total_amount, rental_status)
VALUES
(1, 1, CURRENT_DATE,
 DATE_ADD(CURRENT_DATE, INTERVAL 2 DAY), 1500, 'Active'),

(2, 2, CURRENT_DATE,
 DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY), 1600, 'Active'),

(3, 3, DATE_SUB(CURRENT_DATE, INTERVAL 5 DAY),
 DATE_SUB(CURRENT_DATE, INTERVAL 3 DAY), 1800, 'Completed');
 SELECT *FROM Rentals;
 INSERT INTO Payments
(rental_id, amount, payment_date, payment_method)
VALUES
(1, 1500, CURRENT_DATE, 'UPI'),
(2, 1600, CURRENT_DATE, 'Cash'),
(3, 1800, CURRENT_DATE, 'Card');
INSERT INTO Returns
(rental_id, return_date, gadget_condition)
VALUES
(3, DATE_SUB(CURRENT_DATE, INTERVAL 3 DAY), 'Good');
INSERT INTO Maintenance
(gadget_id, issue_description, repair_cost, repair_status)
VALUES
(4, 'Tablet screen damage', 2000, 'Pending');
SELECT *FROM Customers;
SELECT *FROM Gadgets;
SELECT *FROM Rentals;
SELECT *FROM Payments;
SELECT *FROM Returns;
SELECT *FROM Maintenance; 





