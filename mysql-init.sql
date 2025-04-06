CREATE TABLE IF NOT EXISTS sales_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(255),
    price DECIMAL(10,2),
    quantity INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO sales_data (product_name, category, price, quantity) VALUES
('Laptop', 'Electronics', 799.99, 5),
('Phone', 'Electronics', 499.99, 10),
('Headphones', 'Accessories', 99.99, 15),
('Monitor', 'Electronics', 199.99, 7),
('Keyboard', 'Accessories', 49.99, 12);
