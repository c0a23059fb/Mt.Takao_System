CREATE DATABASE IF NOT EXISTS main_db;
USE main_db;

-- ユーザー情報とクーポン情報
CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    coupon_code VARCHAR(255) NOT NULL,
    coupon_valid BOOLEAN DEFAULT TRUE
);

-- チェックポイント状態
CREATE TABLE IF NOT EXISTS Check_Point (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    check_valid BOOLEAN DEFAULT FALSE,
    goal_valid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);