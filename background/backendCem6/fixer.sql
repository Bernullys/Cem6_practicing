-- SELECT "lecture_time" FROM "lectures";

-- DELETE FROM "lectures"
-- WHERE "lecture_time" LIKE '_';

-- UPDATE "lectures"
-- SET "lecture_time" = '20' || "lecture_time"
-- WHERE "lecture_time" LIKE '25%';

-- UPDATE "historical_lectures"
-- SET "monthly_consumption" = 289.00
-- WHERE "month" = 'March' AND "year" = '2025';

-- SELECT COUNT("active_energy_consumption_kWh")
-- FROM "lectures"
-- WHERE "sensor_id" = 2 AND "active_energy_consumption_kWh" > 0;

-- INSERT INTO "historical_lectures" ("sensor_id", "month", "year", "monthly_consumption")
-- VALUES 
--     (4, 'february', '2025', 332.4),
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

-- SELECT active_energy_consumption_kWh
-- FROM lectures
-- WHERE sensor_id = 2;

-- SELECT COUNT(*) FROM "lectures"
-- WHERE  "sensor_id" = 4 AND "active_energy_consumption_kWh" > 0;

-- DELETE FROM "historical_lectures"
-- WHERE "month" = 'April';