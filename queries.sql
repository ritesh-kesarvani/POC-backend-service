CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(250) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    theme VARCHAR(50) DEFAULT 'light',
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emp_org_id INT  NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    work_email VARCHAR(200) NOT NULL UNIQUE,
    compentency VARCHAR(100),
    reporting_to INTEGER,
    grade VARCHAR(20),
    project_id INT,
    doj DATE,
    allocation_type VARCHAR(50),
    allocation_percent INTEGER,
    designation VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE if not exists projects (
id SERIAL PRIMARY KEY,
name VARCHAR(255) NOT NULL,
bussines_group TEXT,
hd INT,
customer_id INT,
project_currency VARCHAR(50) DEFAULT 'INR',
status VARCHAR(50) DEFAULT 'ongoing',
manager_id INT REFERENCES employees(id),
created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE  if not exists reporting_managers (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
email VARCHAR(150) UNIQUE NOT NULL,
created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE  if not exists bussiness_groups (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE  if not exists customers (
id SERIAL PRIMARY KEY,
bussiness_group_id INT NOT NULL,
customer_name VARCHAR(100) NOT NULL,
customer_code VARCHAR(150) UNIQUE NOT NULL,
created_at TIMESTAMP DEFAULT NOW()
);


-- DROP TABLE `helloworld`.`customers`;
-- DROP TABLE `helloworld`.`bussiness_groups`;
-- DROP TABLE `helloworld`.`reporting_managers`;
-- DROP TABLE `helloworld`.`projects`;
-- DROP TABLE `helloworld`.`employees`;


