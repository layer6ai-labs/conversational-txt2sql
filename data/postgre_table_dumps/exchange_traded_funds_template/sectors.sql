
-- 表定义和数据: "sectors"
--
-- PostgreSQL database dump
--

-- Dumped from database version 14.12 (Debian 14.12-1.pgdg120+1)
-- Dumped by pg_dump version 17.5 (Debian 17.5-1)

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

SET default_table_access_method = heap;

--
-- Name: sectors; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sectors (
    secid bigint NOT NULL,
    industrytag text NOT NULL
);


ALTER TABLE public.sectors OWNER TO root;

--
-- Name: sectors_secid_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sectors_secid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sectors_secid_seq OWNER TO root;

--
-- Name: sectors_secid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sectors_secid_seq OWNED BY public.sectors.secid;


--
-- Name: sectors secid; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sectors ALTER COLUMN secid SET DEFAULT nextval('public.sectors_secid_seq'::regclass);


--
-- Data for Name: sectors; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.sectors (secid, industrytag) VALUES (1, 'basic_materials');
INSERT INTO public.sectors (secid, industrytag) VALUES (2, 'communication_services');
INSERT INTO public.sectors (secid, industrytag) VALUES (3, 'consumer_cyclical');
INSERT INTO public.sectors (secid, industrytag) VALUES (4, 'consumer_defensive');
INSERT INTO public.sectors (secid, industrytag) VALUES (5, 'energy');
INSERT INTO public.sectors (secid, industrytag) VALUES (6, 'financial_services');
INSERT INTO public.sectors (secid, industrytag) VALUES (7, 'healthcare');
INSERT INTO public.sectors (secid, industrytag) VALUES (8, 'industrials');
INSERT INTO public.sectors (secid, industrytag) VALUES (9, 'real_estate');
INSERT INTO public.sectors (secid, industrytag) VALUES (10, 'technology');
INSERT INTO public.sectors (secid, industrytag) VALUES (11, 'utilities');


--
-- Name: sectors_secid_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sectors_secid_seq', 11, true);


--
-- Name: sectors sectors_industrytag_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sectors
    ADD CONSTRAINT sectors_industrytag_key UNIQUE (industrytag);


--
-- Name: sectors sectors_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sectors
    ADD CONSTRAINT sectors_pkey PRIMARY KEY (secid);


--
-- PostgreSQL database dump complete
--

