

CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(64),
    phone_number INT(30),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    customer_create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) engine=InnoDB;

CREATE TABLE IF NOT EXISTS customer_info (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(100),
    patronymic VARCHAR(100),
    phone_number INT(30),
    locality VARCHAR(100),
    delivery_service VARCHAR(20),
    branch_number INT(5),
    customer_id INT(20),
    FOREIGN KEY (customer_id)
    REFERENCES customers (id)
) engine=InnoDB;


CREATE TABLE IF NOT EXISTS customer_payment (
    id INT PRIMARY KEY,
    payment_type VARCHAR(50),
    provider VARCHAR(50),
    card_number INT(16),
    card_validity VARCHAR(5),
    cvv INT(3),
    customer_id INT(20),
    FOREIGN KEY (customer_id)
    REFERENCES customers (id)
) engine=InnoDB;


CREATE TABLE IF NOT EXISTS photo (
    id VARCHAR(150) PRIMARY KEY,
    image_blob BLOB DEFAULT NULL
) engine=InnoDB;


CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(500),
    tags VARCHAR(100),
    image_id VARCHAR(150),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_ad TIMESTAMP,
    FOREIGN KEY (image_id)
    REFERENCES photo (id)
) engine=InnoDB;

CREATE TABLE IF NOT EXISTS promotion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    short_description VARCHAR(150),
    description VARCHAR(500),
    active BOOLEAN NOT NULL DEFAULT FALSE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    image_id VARCHAR(150)
) engine=InnoDB;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(30) NOT NULL,
    short_description VARCHAR(150),
    description VARCHAR(500),
    price FLOAT NOT NULL,
    quantity_in_stock INT NOT NULL,
    quantity_purchased INT NOT NULL,
    category_id INT NOT NULL,
    promotion_id INT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_ad TIMESTAMP,
    image_id VARCHAR(150),
    FOREIGN KEY (image_id)
    REFERENCES photo (id),
    FOREIGN KEY (category_id)
    REFERENCES category (id),
    FOREIGN KEY (promotion_id)
    REFERENCES promotion (id),
    FULLTEXT(name, description)
) engine=InnoDB;

CREATE TABLE IF NOT EXISTS favorite(
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE (customer_id, product_id)
);

CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(150) PRIMARY KEY,
    price FLOAT NOT NULL,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
    REFERENCES customers (id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (product_id)
    REFERENCES products (id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) engine=InnoDB;


