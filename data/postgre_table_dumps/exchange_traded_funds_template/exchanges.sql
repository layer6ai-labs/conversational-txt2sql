
-- 表定义和数据: "exchanges"
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
-- Name: exchanges; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.exchanges (
    xchgnum bigint NOT NULL,
    marketcode character varying(10) NOT NULL,
    tradingvenue text NOT NULL,
    exchangetime text NOT NULL
);


ALTER TABLE public.exchanges OWNER TO root;

--
-- Name: exchanges_xchgnum_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.exchanges_xchgnum_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exchanges_xchgnum_seq OWNER TO root;

--
-- Name: exchanges_xchgnum_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.exchanges_xchgnum_seq OWNED BY public.exchanges.xchgnum;


--
-- Name: exchanges xchgnum; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.exchanges ALTER COLUMN xchgnum SET DEFAULT nextval('public.exchanges_xchgnum_seq'::regclass);


--
-- Data for Name: exchanges; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.exchanges (xchgnum, marketcode, tradingvenue, exchangetime) VALUES (1, 'PCX', 'NYSEArca', 'ny');
INSERT INTO public.exchanges (xchgnum, marketcode, tradingvenue, exchangetime) VALUES (2, 'NGM', 'NasdaqGM', 'New York');
INSERT INTO public.exchanges (xchgnum, marketcode, tradingvenue, exchangetime) VALUES (6, 'BTS', 'BATS', 'America/NYC');
INSERT INTO public.exchanges (xchgnum, marketcode, tradingvenue, exchangetime) VALUES (2122, 'PNK', 'Other OTC', 'nyc');


--
-- Name: exchanges_xchgnum_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.exchanges_xchgnum_seq', 2310, true);


--
-- Name: exchanges exchanges_marketcode_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.exchanges
    ADD CONSTRAINT exchanges_marketcode_key UNIQUE (marketcode);


--
-- Name: exchanges exchanges_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.exchanges
    ADD CONSTRAINT exchanges_pkey PRIMARY KEY (xchgnum);


--
-- PostgreSQL database dump complete
--

