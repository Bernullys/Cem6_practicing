-- SELECT "lecture_time" FROM "lectures";

-- DELETE FROM "lectures"
-- WHERE "lecture_time" LIKE '_';

-- UPDATE "lectures"
-- SET "lecture_time" = '20' || "lecture_time"
-- WHERE "lecture_time" LIKE '25%';

SELECT MAX(active_energy_consumption_kWh), MIN(active_energy_consumption_kWh)
FROM lectures 
WHERE sensor_id = 4 AND lecture_time BETWEEN '2025-03-00 00:00:00' AND '2025-03-28 23:59:59';

-- SELECT COUNT("active_energy_consumption_kWh")
-- FROM "lectures"
-- WHERE "sensor_id" = 2 AND "active_energy_consumption_kWh" > 0;
