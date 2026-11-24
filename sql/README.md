# SQL folder guide

## Original source files
`source_files/` stores the SQL files uploaded for this project, for traceability.

- `Gadget_renting.sql`: database/table creation and sample records
- `phase1.sql`: CRUD/transaction demonstration
- `advanced sql queries.sql`: aggregate queries, joins and Rental_Details view

## Critical data-preservation note
The application connects to an existing database. It does not execute SQL scripts automatically.

The original `Gadget_renting.sql` contains `CREATE DATABASE gadget_renting` and sample `INSERT` statements. Do not rerun the entire file on a populated production database. For deployment, export your existing local database and import that backup into your cloud MySQL instance. This preserves the actual records and schema.

The application expects these columns:
- Customers: customer_id, customer_name, phone, email, address
- Gadgets: gadget_id, gadget_name, category, brand, rent_per_day, availability_status
- Rentals: rental_id, customer_id, gadget_id, start_date, end_date, total_amount, rental_status
- Payments: payment_id, rental_id, amount, payment_date, payment_method
- Returns: return_id, rental_id, return_date, gadget_condition
- Maintenance: maintenance_id, gadget_id, issue_description, repair_cost, repair_status
