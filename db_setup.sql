CREATE TABLE roles(role_id SERIAL PRIMARY KEY, role_name VARCHAR(50) NOT NULL UNIQUE);
CREATE TABLE users(user_id SERIAL PRIMARY KEY, last_name VARCHAR(50) NOT NULL, first_name VARCHAR(50) NOT NULL, middle_name VARCHAR(50), login VARCHAR(50) NOT NULL UNIQUE, role_id INT NOT NULL REFERENCES roles(role_id));
CREATE TABLE products(product_id SERIAL PRIMARY KEY, category VARCHAR(50), subcategory VARCHAR(50), product_name VARCHAR(100) NOT NULL, manufacturer VARCHAR(100), image_path VARCHAR(255), description TEXT, composition TEXT, price NUMERIC(10,2) NOT NULL);
CREATE TABLE sizes(size_id SERIAL PRIMARY KEY, size_value VARCHAR(10) NOT NULL UNIQUE);
CREATE TABLE stock_items(stock_item_id SERIAL PRIMARY KEY, product_id INT NOT NULL REFERENCES products(product_id), size_id INT NOT NULL REFERENCES sizes(size_id), quantity_available INT NOT NULL CHECK(quantity_available>=0), UNIQUE(product_id,size_id));
CREATE TABLE orders(order_id SERIAL PRIMARY KEY, order_date DATE NOT NULL, user_id INT NOT NULL REFERENCES users(user_id));
CREATE TABLE order_items(order_item_id SERIAL PRIMARY KEY, order_id INT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE, product_id INT NOT NULL REFERENCES products(product_id), size_id INT NOT NULL REFERENCES sizes(size_id), quantity INT NOT NULL CHECK(quantity>0), price NUMERIC(10,2) NOT NULL);
