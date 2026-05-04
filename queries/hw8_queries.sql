--Query 1--
WITH requested_dates AS (
  SELECT generate_series('2026-07-15'::date, '2026-07-16'::date, '1 day') AS day
),
season_for_date AS (
  SELECT s.name
  FROM season s
  WHERE s.hotel_id = 1
    AND '2026-07-15'::date BETWEEN s.start_date AND s.end_date
),
daily_prices AS (
  SELECT rd.day,
         p.cost
  FROM requested_dates rd
  JOIN season_for_date sd ON TRUE
  JOIN pricing p
    ON p.hotel_id = 1
   AND p.season = sd.name
   AND p.day_of_week = to_char(rd.day, 'Dy')
),
avg_daily_price AS (
  SELECT AVG(cost)::numeric AS avg_cost
  FROM daily_prices
),
type_inventory AS (
  SELECT rt.type,
         rt.price AS base_price,
         COUNT(*) AS total_rooms
  FROM room_type rt
  JOIN room rm
    ON rm.hotel_id = rt.hotel_id
   AND rm.room_type = rt.type
  WHERE rt.hotel_id = 1
  GROUP BY rt.type, rt.price
),
reserved_by_type AS (
  SELECT room_type,
         SUM(num_rooms) AS reserved_rooms
  FROM reservation
  WHERE hotel_id = 1
    AND start_date < '2026-07-17'::date
    AND end_date > '2026-07-15'::date
  GROUP BY room_type
),
vip_discount AS (
  SELECT COALESCE(MAX(percentage::numeric), 0) AS pct
  FROM cat_discount
  WHERE lower(type) = 'VIP'
)
SELECT ti.type AS room_type,
       ti.total_rooms,
       COALESCE(r.reserved_rooms, 0) AS reserved_rooms,
       ti.total_rooms - COALESCE(r.reserved_rooms, 0) AS available_rooms,
       ROUND(
         (
           (ti.base_price + ad.avg_cost)
           * (1 - vd.pct / 100.0)
         )::numeric,
         2
       ) AS avg_cost_per_night
FROM type_inventory ti
LEFT JOIN reserved_by_type r
  ON r.room_type = ti.type
CROSS JOIN avg_daily_price ad
CROSS JOIN vip_discount vd
WHERE ti.total_rooms - COALESCE(r.reserved_rooms, 0) > 0
ORDER BY ti.type;
BEGIN;

INSERT INTO guest (id, id_type, first_name, last_name, address, home_phone, mobile_phone, category)
VALUES (14, 'passport', 'Victor', 'Deadlock', '555 VIP Ave', '999-9999', '888-8888', 'VIP');

INSERT INTO stay (id, hotel_id, start_date, end_date, room_num)
VALUES (16, 1, '2026-07-15'::date, '2026-07-17'::date, NULL);

INSERT INTO reservation (id, hotel_id, stay_id, guest_id, start_date, end_date, num_rooms, room_type)
VALUES (16, 1, 16, 14, '2026-07-15'::date, '2026-07-17'::date, 1, 'double');

COMMIT;

--Query 2--
SELECT rm.room_num
FROM room rm
JOIN room_type rt
  ON rm.hotel_id = rt.hotel_id
 AND rm.room_type = rt.type
WHERE rm.hotel_id = 2
  AND rt.type = 'double'
  AND NOT EXISTS (
    SELECT 1
    FROM stay s
    WHERE s.hotel_id = rm.hotel_id
      AND s.room_num = rm.room_num
      AND '2026-07-19'::date >= s.start_date
	  AND '2026-07-19'::date < s.end_date
  )
ORDER BY rm.room_num;
BEGIN;

UPDATE stay
SET room_num = 205
WHERE id = 11;

INSERT INTO occupant (guest_id, stay_id, name)
VALUES (
  (SELECT guest_id FROM reservation WHERE stay_id = 11),
  11,
  'Mr. Smith'
);

COMMIT;

--Query 3--
BEGIN;

INSERT INTO billing (id, stay_id, total)
VALUES (4, 11, 285);

INSERT INTO room_service (bill_id, cost)
VALUES (4, 50);

UPDATE stay
SET room_num = NULL
WHERE id = 11;

COMMIT;
SELECT s.start_date,
       s.end_date,
       r.room_type,
       STRING_AGG(o.name, ', ') AS occupants,
       b.total + COALESCE(SUM(rs.cost), 0) AS total_cost
FROM stay s
JOIN reservation r
  ON r.stay_id = s.id
JOIN billing b
  ON b.stay_id = s.id
LEFT JOIN occupant o
  ON o.stay_id = s.id
LEFT JOIN room_service rs
  ON rs.bill_id = b.id
WHERE s.id = 11
GROUP BY s.start_date, s.end_date, r.room_type, b.total;

--Query 4--
WITH selected_stay AS (
  SELECT s.id
  FROM stay s
  	JOIN reservation r ON r.stay_id = s.id
  WHERE s.hotel_id = 2
  AND s.room_num = 205
  AND '2026-07-20'::date BETWEEN s.start_date AND s.end_date
)
SELECT g.first_name || ' ' || g.last_name AS person_name, 'reserver' AS role
FROM selected_stay ss
	JOIN reservation r ON r.stay_id = ss.id
	JOIN guest g ON g.id = r.guest_id
UNION ALL
SELECT o.name AS person_name, 'occupant' AS role
FROM selected_stay ss
	JOIN occupant o ON o.stay_id = ss.id;

--Query 5--
SELECT g.id AS guest_id,
       COUNT(DISTINCT r.hotel_id) AS hotels_visited,
       SUM(b.total + COALESCE(rs.cost, 0)) AS total_spent
FROM guest g
	JOIN reservation r ON r.guest_id = g.id
	JOIN billing b ON b.stay_id = r.stay_id
	LEFT JOIN room_service rs ON rs.bill_id = b.id
WHERE g.id = 13
  AND r.start_date BETWEEN '2026-01-01'::date AND '2026-12-31'::date
GROUP BY g.id
HAVING COUNT(DISTINCT r.hotel_id) >= 2;