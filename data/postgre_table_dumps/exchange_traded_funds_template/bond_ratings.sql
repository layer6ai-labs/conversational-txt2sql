
-- 表定义和数据: "bond_ratings"
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
-- Name: bond_ratings; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.bond_ratings (
    ratekey bigint NOT NULL,
    creditmark text NOT NULL
);


ALTER TABLE public.bond_ratings OWNER TO root;

--
-- Name: bond_ratings_ratekey_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.bond_ratings_ratekey_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bond_ratings_ratekey_seq OWNER TO root;

--
-- Name: bond_ratings_ratekey_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.bond_ratings_ratekey_seq OWNED BY public.bond_ratings.ratekey;


--
-- Name: bond_ratings ratekey; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.bond_ratings ALTER COLUMN ratekey SET DEFAULT nextval('public.bond_ratings_ratekey_seq'::regclass);


--
-- Data for Name: bond_ratings; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.bond_ratings (ratekey, creditmark) VALUES (1, 'us_government');
INSERT INTO public.bond_ratings (ratekey, creditmark) VALUES (2, 'aaa');
INSERT INTO public.bond_ratings (ratekey, creditmark) VALUES (3, 'aa');
INSERT INTO public.bond_ratings (ratekey, creditmark) VALUES (4, 'a');
INSERT INTO public.bond_ratings (ratekey, creditmark) VALUES (5, 'bbb');
INSERT INTO public.bond_ratings (ratekey, creditmark) VALUES (6, 'bb');
INSERT INTO public.bond_ratings (ratekey, creditmark) VALUES (7, 'b');
INSERT INTO public.bond_ratings (ratekey, creditmark) VALUES (8, 'below_b');
INSERT INTO public.bond_ratings (ratekey, creditmark) VALUES (9, 'others');


--
-- Name: bond_ratings_ratekey_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.bond_ratings_ratekey_seq', 9, true);


--
-- Name: bond_ratings bond_ratings_creditmark_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.bond_ratings
    ADD CONSTRAINT bond_ratings_creditmark_key UNIQUE (creditmark);


--
-- Name: bond_ratings bond_ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.bond_ratings
    ADD CONSTRAINT bond_ratings_pkey PRIMARY KEY (ratekey);


--
-- PostgreSQL database dump complete
--

