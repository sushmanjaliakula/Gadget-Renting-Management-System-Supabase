USE gadget_renting;

-- =====================================
-- 1. CREATE (INSERT)
-- =====================================

START TRANSACTION;

INSERT INTO Customers
(customer_name, phone, email, address)
VALUES
('CRUD Test User', '9000000099',
 'crudtest@example.com', 'Vizag');

-- Store the newly generated customer ID
SET @test_id = LAST_INSERT_ID();

-- Display inserted customer
SELECT * FROM Customers
WHERE customer_id = @test_id;


-- =====================================
-- 2. READ (SELECT)
-- =====================================

-- Display all customers
SELECT * FROM Customers;

-- Display all gadgets
SELECT * FROM Gadgets;

-- Display available gadgets
SELECT * FROM Gadgets
WHERE availability_status = 'Available';

-- Search customer by address
SELECT * FROM Customers
WHERE address = 'Vizag';


-- =====================================
-- 3. UPDATE
-- =====================================

-- Update test customer's address
UPDATE Customers
SET address = 'MVP Colony'
WHERE customer_id = @test_id;

-- Display updated customer
SELECT * FROM Customers
WHERE customer_id = @test_id;

-- Update gadget rent
UPDATE Gadgets
SET rent_per_day = 999
WHERE gadget_id = 1;

-- Display updated gadget
SELECT * FROM Gadgets
WHERE gadget_id = 1;


-- =====================================
-- 4. DELETE
-- =====================================

-- Delete related payment records
DELETE p
FROM Payments AS p
JOIN Rentals AS r
ON p.rental_id = r.rental_id
WHERE r.customer_id = @test_id;

-- Delete related return records
DELETE rt
FROM Returns AS rt
JOIN Rentals AS r
ON rt.rental_id = r.rental_id
WHERE r.customer_id = @test_id;

-- Delete rental records
DELETE FROM Rentals
WHERE customer_id = @test_id;

-- Delete customer record
DELETE FROM Customers
WHERE customer_id = @test_id;

-- Verify deletion
SELECT * FROM Customers
WHERE customer_id = @test_id;


-- =====================================
-- 5. ROLLBACK
-- =====================================

-- Undo all changes made in this demonstration
ROLLBACK;

-- Verify original database records
SELECT * FROM Customers;
SELECT * FROM Gadgets;
SELECT * FROM Rentals;
SELECT * FROM Payments;
SELECT * FROM Returns;

