DROP DATABASE IF EXISTS office_management;
CREATE DATABASE office_management;
USE office_management;

-- =========================================
-- TABLE: Departments (CHỈ 1 BẢNG DUY NHẤT)
-- =========================================
CREATE TABLE Departments (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL
);

-- =========================================
-- TABLE: Equipment
-- =========================================
CREATE TABLE Equipment (
    EquipmentID INT AUTO_INCREMENT PRIMARY KEY,
    EquipmentName VARCHAR(100) NOT NULL,
    Type VARCHAR(50),
    Unit VARCHAR(20),
    Status VARCHAR(50),
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- =========================================
-- TABLE: Maintenance
-- =========================================
CREATE TABLE Maintenance (
    MaintenanceID INT AUTO_INCREMENT PRIMARY KEY,
    EquipmentID INT,
    MaintenanceDate DATE,
    Description TEXT,
    Cost DECIMAL(10,2),
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID)
);

-- =========================================
-- TABLE: Purchases (CÓ QUANTITY)
-- =========================================
CREATE TABLE Purchases (
    PurchaseID INT AUTO_INCREMENT PRIMARY KEY,
    EquipmentID INT,
    PurchaseDate DATE,
    Value DECIMAL(10,2),
    Quantity INT,
    Vendor VARCHAR(100),
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID)
);

-- =========================================
-- INSERT DATA: Departments
-- =========================================
INSERT INTO Departments (DepartmentName) VALUES
('IT'),
('Human Resources'),
('Finance'),
('Marketing');

-- =========================================
-- INSERT DATA: Equipment
-- =========================================
INSERT INTO Equipment (EquipmentName, Type, Unit, Status, DepartmentID) VALUES
('Dell Latitude 5420', 'Laptop', 'Piece', 'In Use', 1),
('Dell Inspiron 15', 'Laptop', 'Piece', 'Available', 1),
('Lenovo ThinkPad X1', 'Laptop', 'Piece', 'In Use', 2),
('Asus Vivobook', 'Laptop', 'Piece', 'Available', 2),
('Macbook Pro M2', 'Laptop', 'Piece', 'In Use', 1),
('HP Pavilion', 'Laptop', 'Piece', 'Maintenance', 3),
('Acer Aspire 7', 'Laptop', 'Piece', 'Available', 3),
('MSI Modern 14', 'Laptop', 'Piece', 'In Use', 4),
('HP LaserJet Printer', 'Printer', 'Piece', 'Available', 1),
('Canon LBP2900', 'Printer', 'Piece', 'In Use', 2),
('Daikin Air Conditioner', 'Electronics', 'Piece', 'Maintenance', 3),
('Panasonic Air Conditioner', 'Electronics', 'Piece', 'Available', 4),
('Office Desk', 'Furniture', 'Set', 'In Use', 2),
('Office Chair', 'Furniture', 'Piece', 'In Use', 2),
('Projector Epson', 'Electronics', 'Piece', 'Available', 1),
('Security Camera', 'Electronics', 'Piece', 'In Use', 4),
('Coffee Machine', 'Electrical Appliance', 'Piece', 'Available', 4),
('Microwave Oven', 'Electrical Appliance', 'Piece', 'Broken', 3),
('Vacuum Cleaner', 'Cleaning Tool', 'Piece', 'Available', 2),
('Water Dispenser', 'Electrical Appliance', 'Piece', 'In Use', 1);

-- =========================================
-- INSERT DATA: Maintenance
-- =========================================
INSERT INTO Maintenance (EquipmentID, MaintenanceDate, Description, Cost) VALUES
(6, '2026-05-01', 'Laptop battery replacement', 120.00),
(11, '2026-05-03', 'Air conditioner gas refill', 150.00),
(18, '2026-05-05', 'Microwave repair', 80.00),
(9, '2026-05-10', 'Printer cleaning', 30.00);

-- =========================================
-- INSERT DATA: Purchases
-- =========================================
INSERT INTO Purchases (EquipmentID, PurchaseDate, Value, Quantity, Vendor) VALUES
(1, '2025-01-10', 1200.00, 1, 'Dell Vietnam'),
(2, '2025-01-15', 950.00, 1, 'Dell Vietnam'),
(3, '2025-02-05', 1400.00, 1, 'Lenovo Vietnam'),
(4, '2025-02-20', 800.00, 1, 'Asus Vietnam'),
(5, '2025-03-01', 2100.00, 1, 'Apple Vietnam'),
(6, '2025-03-15', 900.00, 1, 'HP Vietnam'),
(9, '2025-04-01', 350.00, 1, 'HP Vietnam'),
(10, '2025-04-08', 250.00, 1, 'Canon Vietnam'),
(11, '2025-04-15', 950.00, 1, 'Daikin Vietnam'),
(17, '2025-04-20', 180.00, 1, 'Philips Store');

-- =========================================
-- VIEW: Equipment by Department
-- =========================================
CREATE VIEW EquipmentByDepartment AS
SELECT
    e.EquipmentID,
    e.EquipmentName,
    e.Type,
    e.Status,
    d.DepartmentName
FROM Equipment e
JOIN Departments d ON e.DepartmentID = d.DepartmentID;

-- =========================================
-- VIEW: Summary
-- =========================================
CREATE VIEW EquipmentSummary AS
SELECT EquipmentName, Type, Status
FROM Equipment;

-- =========================================
-- FUNCTION: Total Asset Value
-- =========================================
DELIMITER //

CREATE FUNCTION TotalAssetValue()
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(15,2);

    SELECT SUM(Value)
    INTO total
    FROM Purchases;

    RETURN total;
END //

DELIMITER ;

-- =========================================
-- PROCEDURE: Add Equipment
-- =========================================
DELIMITER //

CREATE PROCEDURE AddEquipment(
    IN p_name VARCHAR(100),
    IN p_type VARCHAR(50),
    IN p_unit VARCHAR(20),
    IN p_status VARCHAR(50),
    IN p_department INT
)
BEGIN
    INSERT INTO Equipment
    (EquipmentName, Type, Unit, Status, DepartmentID)
    VALUES
    (p_name, p_type, p_unit, p_status, p_department);
END //

DELIMITER ;

-- =========================================
-- PROCEDURE: Count Equipment
-- =========================================
DELIMITER //

CREATE PROCEDURE GetEquipmentCount()
BEGIN
    SELECT COUNT(*) AS TotalEquipment FROM Equipment;
END //

DELIMITER ;

-- =========================================
-- TRIGGER 1: Auto set default status
-- =========================================
DELIMITER //

CREATE TRIGGER default_status
BEFORE INSERT ON Equipment
FOR EACH ROW
BEGIN
    IF NEW.Status IS NULL OR NEW.Status = '' THEN
        SET NEW.Status = 'Available';
    END IF;
END //

DELIMITER ;

-- =========================================
-- TRIGGER 2: Update status after maintenance
-- =========================================
DELIMITER //

CREATE TRIGGER UpdateEquipmentStatus
AFTER INSERT ON Maintenance
FOR EACH ROW
BEGIN
    UPDATE Equipment
    SET Status = 'Maintenance'
    WHERE EquipmentID = NEW.EquipmentID;
END //

DELIMITER ;

-- =========================================
-- INDEX
-- =========================================
CREATE INDEX idx_equipment_name
ON Equipment(EquipmentName);

-- =========================================
-- TEST QUERIES
-- =========================================
SELECT * FROM Equipment;
SELECT * FROM Maintenance;
SELECT * FROM Purchases;
SELECT * FROM EquipmentSummary;

CALL GetEquipmentCount();
SELECT TotalAssetValue();

SELECT Type, COUNT(*) AS Quantity
FROM Equipment
GROUP BY Type;

SHOW DATABASES;
ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
USE office_management;
ALTER TABLE Purchases
MODIFY COLUMN Quantity INT DEFAULT 1;
UPDATE Purchases SET Quantity = 2 WHERE PurchaseID = 1;
UPDATE Purchases SET Quantity = 3 WHERE PurchaseID = 2;
UPDATE Purchases SET Quantity = 1 WHERE PurchaseID = 3;
UPDATE Purchases SET Quantity = 4 WHERE PurchaseID = 4;
UPDATE Purchases SET Quantity = 5 WHERE PurchaseID = 5;
UPDATE Purchases SET Quantity = 2 WHERE PurchaseID = 6;
UPDATE Purchases SET Quantity = 6 WHERE PurchaseID = 7;
UPDATE Purchases SET Quantity = 3 WHERE PurchaseID = 8;
UPDATE Purchases SET Quantity = 7 WHERE PurchaseID = 9;
UPDATE Purchases SET Quantity = 1 WHERE PurchaseID = 10;
