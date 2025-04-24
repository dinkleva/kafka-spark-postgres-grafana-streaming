\c amazon;
CREATE TABLE IF NOT EXISTS amazon_products (
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    discounted_price DOUBLE PRECISION,
    actual_price DOUBLE PRECISION,
    discount_percentage DOUBLE PRECISION,
    rating DOUBLE PRECISION,
    rating_count INTEGER,
    about_product TEXT,
    user_id TEXT,
    user_name TEXT,
    review_id TEXT,
    review_title TEXT,
    review_content TEXT,
    img_link TEXT,
    product_link TEXT
);
