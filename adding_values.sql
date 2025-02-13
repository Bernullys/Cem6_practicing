CREATE TABLE IF NOT EXISTS "lectures" (
    "id" INTEGER,
    "sensor_id" INTEGER NOT NULL,
    "voltage_V" REAL,
    "current_A" REAL,
    "frecuency_Hz" REAL,
    "active_power_W" REAL,
    "reactive_power_var" REAL,
    "aparent_power_VA" REAL,
    "power_factor" REAL,
    "active_energy_consumption_kWh" REAL,
    "lecture_time" TEXT,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "historical_lectures" (
    "id" INTEGER,
    "sensor_id" INTEGER NOT NULL,
    "month" TEXT NOT NULL,
    "year" TEXT NOT NULL,
    "monthly_consumption" REAL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "rut" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "address" TEXT NOT NULL,
    "sensor_id" INTEGER NOT NULL,
    PRIMARY KEY("id")
);

-- INSERT INTO "historical_lectures" ("sensor_id", "month", "year", "monthly_consumption")
-- VALUES 
--     (4, 'january', '2025', 330.2),
--     (4, 'december', '2024', 340.2),
--     (4, 'november', '2024', 330.2),
--     (4, 'october', '2024', 345.2),
--     (4, 'september', '2024', 330.2),
--     (4, 'agost', '2024', 340.2),
--     (4, 'july', '2024', 320.2),
--     (4, 'june', '2024', 330.2),
--     (4, 'may', '2024', 350.2),
--     (4, 'april', '2024', 310.2),
--     (4, 'march', '2024', 320.2),
--     (4, 'february', '2024', 325.2)
-- ;


-- INSERT INTO "users" ("first_name", "last_name", "rut", "phone", "email", "address", "sensor_id")
-- VALUES
--     ('Bernardo Antonio', 'Dávila Rondón', '25674085-0', '+56977545456', 'bernardoantoniod@gmail.com', 'Belisario Prats 1850, Dpto. 610, Independencia, RM.', 4)
-- ;

INSERT INTO "lectures" (
    "sensor_id",
    "voltage_V",
    "current_A",
    "frecuency_Hz",
    "active_power_W",
    "reactive_power_var",
    "aparent_power_VA",
    "power_factor",
    "active_energy_consumption_kWh",
    "lecture_time")
VALUES
    (4, 225, 10, 50, 100, 50, 120, 1, 118, '25-02-05 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 114, '25-02-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 110, '25-01-31 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 106, '25-01-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 102, '24-12-31 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 98, '24-12-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 94, '24-11-30 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 90, '24-11-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 86, '24-10-31 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 82, '24-10-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 78, '24-09-30 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 74, '24-09-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 70, '24-08-31 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 66, '24-08-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 62, '24-07-31 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 58, '24-07-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 54, '24-06-30 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 50, '24-06-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 46, '24-05-31 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 42, '24-05-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 38, '24-04-30 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 34, '24-04-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 30, '24-03-31 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 26, '24-03-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 22, '24-02-28 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 18, '24-02-01 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 14, '24-01-31 13:55:51'),
    (4, 225, 10, 50, 100, 50, 120, 1, 12, '24-01-01 13:55:51')
;
    
