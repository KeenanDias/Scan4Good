CREATE DATABASE scan4good;
USE scan4good;

CREATE TABLE health_tips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    risk_level VARCHAR(20), -- 'Low', 'Medium', 'High'
    advice_text TEXT,
    resource_link VARCHAR(255)
);