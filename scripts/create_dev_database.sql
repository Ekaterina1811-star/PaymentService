/*
This file is used to bootstrap development database locally.

Note: ONLY development database;
*/

CREATE USER "payment-service" SUPERUSER;
CREATE DATABASE "payment-service" OWNER "payment-service" ENCODING 'utf-8';
