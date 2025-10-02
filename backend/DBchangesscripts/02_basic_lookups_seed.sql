-- 02_basic_lookups.sql
-- Insert basic lookup data that doesn't require users (Level 2)
-- Note: These will not have created_by initially - can be updated later

BEGIN;

-- Units of Measure (without created_by for now)
INSERT INTO units_of_measure (name_eng, created_at) VALUES
('piece', NOW())
ON CONFLICT (name_eng) DO NOTHING;

-- Day Categories (without created_by for now) 
INSERT INTO day_categories (name, start_time, end_time, created_at) VALUES
('allday', '00:00:00', '23:59:59', NOW()),
('breakfast', '06:00:00', '11:00:00', NOW()),
('lunch', '11:00:00', '16:00:00', NOW()),
('dinner', '16:00:00', '23:00:00', NOW())
ON CONFLICT (name) DO NOTHING;

-- Food Categories (without created_by for now)
INSERT INTO food_categories (name, created_at) VALUES
('drinks', NOW()),
('main', NOW()),
('sides', NOW())
ON CONFLICT (name) DO NOTHING;

COMMIT;

-- Show results
SELECT 'Basic lookup data inserted:' as info;
SELECT 'Units:' as type, COUNT(*) as count FROM units_of_measure
UNION ALL
SELECT 'Day Categories:', COUNT(*) FROM day_categories  
UNION ALL
SELECT 'Food Categories:', COUNT(*) FROM food_categories;