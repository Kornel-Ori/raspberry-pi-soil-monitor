USE soil_monitor_db;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(320) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS plant_species (
    id INT AUTO_INCREMENT PRIMARY KEY,
    common_name VARCHAR(100) NOT NULL,
    botanical_name VARCHAR(100),
    description TEXT,
    min_moisture FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS plant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    species_id INT NOT NULL,
    plant_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    min_moisture FLOAT,
    image_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (species_id) REFERENCES plant_species(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS node (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'offline',
    led_status VARCHAR(20) DEFAULT 'off',
    last_seen DATETIME NULL,
    plant_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plant_id) REFERENCES plant(id)
);

CREATE TABLE IF NOT EXISTS reading (
    id INT AUTO_INCREMENT PRIMARY KEY,
    moisture_percent FLOAT NOT NULL,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    node_id INT NOT NULL,
    FOREIGN KEY (node_id) REFERENCES node(id)
);

CREATE TABLE IF NOT EXISTS alert (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    plant_id INT NOT NULL,
    reading_id INT NULL,
    resolved_at DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plant_id) REFERENCES plant(id),
    FOREIGN KEY (reading_id) REFERENCES reading(id)
);
