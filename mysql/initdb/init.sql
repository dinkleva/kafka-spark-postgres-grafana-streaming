CREATE DATABASE IF NOT EXISTS amazon;

USE amazon;

DROP TABLE IF EXISTS amazon_sales_data;

CREATE TABLE amazon_sales_data (
    product_id VARCHAR(100),
    product_name TEXT,
    category VARCHAR(255),
    discounted_price VARCHAR(20),
    actual_price VARCHAR(20),
    discount_percentage VARCHAR(10),
    rating VARCHAR(10),
    rating_count VARCHAR(50),
    about_product TEXT,
    user_id VARCHAR(255),
    user_name VARCHAR(255),
    review_id VARCHAR(255),
    review_title TEXT,
    review_content TEXT,
    img_link TEXT,
    product_link TEXT
);

LOAD DATA INFILE '/var/lib/mysql-files/amazon_sales_data.csv'
INTO TABLE amazon_sales_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
