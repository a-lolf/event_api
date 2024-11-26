# event_api

POSTMAN COLLECTION: https://api.postman.com/collections/18976061-f8c9fcc4-b790-4723-b3ea-7ba96853452f?access_key=PMAT-01JDMH2BXFVSV4DS3FBP5YM440

The postman collection can be imported via the above link

SQL Query:

SELECT 
    e.id AS event_id,
    e.name AS event_name,
    e.date AS event_date,
    e.total_tickets AS total_tickets_available,
    e.tickets_sold AS total_tickets_sold
FROM 
    events_event e
ORDER BY 
    e.tickets_sold DESC
LIMIT 3;
