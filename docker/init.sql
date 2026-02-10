CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    email TEXT,
    password TEXT
);

INSERT INTO users (username, email, password) VALUES
('admin', 'admin@corp.com', 'adminpass'),
('darshit', 'darshit@corp.com', 'test123'),
('test', 'test@test.com', 'test');
