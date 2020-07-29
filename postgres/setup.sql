-- create solar db
CREATE DATABASE solar;

-- connect to db
-- \c solar;

-- create solaredge table
CREATE TABLE public.solaredge(
    id                      SERIAL PRIMARY KEY,
    ts                      TIMESTAMP NOT NULL UNIQUE,
    status                  VARCHAR(100),
    ac_power                INTEGER,
    dc_power                INTEGER,
    total_production        INTEGER,
    ac_voltage              REAL,
    ac_current              REAL,
    dc_voltage              REAL,
    dc_current              REAL,
    temperature             REAL,
    exported_energy_m1      INTEGER,
    imporoted_energy_m1     INTEGER,
    exported_energy_m2      INTEGER,
    imported_energy_m2      INTEGER
);


 -- setup grafana user for reading
 CREATE USER grafana WITH PASSWORD 'password';
 GRANT USAGE ON SCHEMA public TO grafana;
 GRANT SELECT ON public.solaredge TO grafana;