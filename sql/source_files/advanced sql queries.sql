USE gadget_renting;
SELECT COUNT(*) AS total_customers from customers;
SELECT SUM(amount) AS total_revenue FROM payments;
SELECT AVG(rent_per_day) AS average_rent FROM gadgets;
SELECT MAX(rent_per_day) FROM gadgets;
SELECT MIN(rent_per_day) from gadgets;
SELECT category, COUNT(*) AS total_gadgets FROM gadgets GROUP BY category;
SELECT payment_method, SUM(amount) AS total from payments GROUP BY payment_method;
SELECT r.rental_id, c.customer_name, g.gadget_name, r.start_date, r.end_date, r.total_amount
FROM rentals r 
JOIN customers c on r.customer_id = c.customer_id
JOIN gadgets g on r.gadget_id = g.gadget_id;
SELECT gadget_name, rent_per_day
from gadgets
where rent_per_day > (select AVG(rent_per_day) from gadgets);
CREATE VIEW Rental_Details AS 
select r.rental_id, c.customer_name, g.gadget_name, r.total_amount, r.rental_status
from rentals r
join customers c on r.customer_id = c.customer_id
join gadgets g on r.gadget_id = g.gadget_id;
DESCRIBE rentals;
SELECT * FROM Rental_Details;
