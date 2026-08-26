USE helpdesk_db;
SELECT DATABASE();
SHOW TABLES;
DESC users;
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('CUSTOMER', 'AGENT', 'ADMIN') NOT NULL
);
CREATE TABLE categories (
	id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE tickets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED') DEFAULT 'OPEN',
    priority ENUM('LOW', 'MEDIUM', 'HIGH') DEFAULT 'MEDIUM',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    customer_id INT NOT NULL,
    agent_id INT,
    category_id INT NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES users(id),
    FOREIGN KEY (agent_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
CREATE TABLE comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    body TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    ticket_id INT NOT NULL,
    user_id INT NOT NULL,

    FOREIGN KEY (ticket_id) REFERENCES tickets(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO users (name, email, role)
VALUES
('John Customer', 'john@gmail.com', 'CUSTOMER'),
('Sarah Customer', 'sarah@gmail.com', 'CUSTOMER'),
('Mike Agent', 'mike@helpdesk.com', 'AGENT'),
('David Agent', 'david@helpdesk.com', 'AGENT'),
('Admin User', 'admin@helpdesk.com', 'ADMIN');

INSERT INTO categories (name)
VALUES
('Hardware'),
('Software'),
('Network'),
('Account');

INSERT INTO tickets
(title, description, priority, customer_id, agent_id, category_id)
VALUES
(
    'Wi-Fi not working',
    'My laptop cannot connect to the office Wi-Fi.',
    'HIGH',
    1,
    3,
    3
);
INSERT INTO comments
(body, ticket_id, user_id)
VALUES
(
    'Please restart your router and try connecting again.',
    1,
    3
);
SELECT * FROM users;
SELECT * FROM tickets;
SELECT * FROM comments;

