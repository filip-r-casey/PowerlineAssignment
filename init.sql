--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5 (Debian 10.5-2.pgdg90+1)
-- Dumped by pg_dump version 14.7 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

--
-- Name: charger_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.charger_data (
    id character varying(50) NOT NULL,
    network_name character varying(100),
    num_available integer,
    num_total integer,
    rated_power double precision,
    lat double precision,
    lon double precision
);


ALTER TABLE public.charger_data OWNER TO postgres;

--
-- Data for Name: charger_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.charger_data (id, network_name, num_available, num_total, rated_power, lat, lon) FROM stdin;
\.


--
-- Name: charger_data charger_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charger_data
    ADD CONSTRAINT charger_data_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

