INSERT INTO ingestion.location (
    country_id,
    city,
    address,
    postal_code,
    latitude,
    longitude
)
VALUES
    (1, 'Stockholm', 'Central Stockholm', '11120', 59.329300, 18.068600),
    (1, 'Uppsala', 'Uppsala East', '75431', 59.858600, 17.638900),
    (1, 'Vasteras', 'Vasteras North', '72212', 59.609900, 16.544800),
    (1, 'Sodertalje', 'Sodertalje South', '15136', 59.195500, 17.625300)
ON CONFLICT DO NOTHING;

