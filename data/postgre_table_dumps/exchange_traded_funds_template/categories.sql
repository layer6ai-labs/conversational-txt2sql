
-- 表定义和数据: "categories"
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
-- Name: categories; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.categories (
    catref bigint NOT NULL,
    classtype text NOT NULL
);


ALTER TABLE public.categories OWNER TO root;

--
-- Name: categories_catref_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.categories_catref_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_catref_seq OWNER TO root;

--
-- Name: categories_catref_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.categories_catref_seq OWNED BY public.categories.catref;


--
-- Name: categories catref; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.categories ALTER COLUMN catref SET DEFAULT nextval('public.categories_catref_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.categories (catref, classtype) VALUES (1, 'Foreign Large Growth');
INSERT INTO public.categories (catref, classtype) VALUES (2, 'Pacific/Asia ex-Japan Stk');
INSERT INTO public.categories (catref, classtype) VALUES (3, 'Large Value');
INSERT INTO public.categories (catref, classtype) VALUES (4, 'Miscellaneous Sector');
INSERT INTO public.categories (catref, classtype) VALUES (5, 'Large Blend');
INSERT INTO public.categories (catref, classtype) VALUES (6, 'Small Value');
INSERT INTO public.categories (catref, classtype) VALUES (7, 'Foreign Large Blend');
INSERT INTO public.categories (catref, classtype) VALUES (8, 'Multisector Bond');
INSERT INTO public.categories (catref, classtype) VALUES (10, 'Diversified Emerging Mkts');
INSERT INTO public.categories (catref, classtype) VALUES (11, 'Emerging Markets Bond');
INSERT INTO public.categories (catref, classtype) VALUES (14, 'Miscellaneous Region');
INSERT INTO public.categories (catref, classtype) VALUES (16, 'Mid-Cap Blend');
INSERT INTO public.categories (catref, classtype) VALUES (17, 'Small Blend');
INSERT INTO public.categories (catref, classtype) VALUES (18, 'China Region');
INSERT INTO public.categories (catref, classtype) VALUES (19, 'Intermediate-Term Bond');
INSERT INTO public.categories (catref, classtype) VALUES (20, 'Health');
INSERT INTO public.categories (catref, classtype) VALUES (21, 'Tactical Allocation');
INSERT INTO public.categories (catref, classtype) VALUES (22, 'Trading--Leveraged Commodities');
INSERT INTO public.categories (catref, classtype) VALUES (23, 'Short Government');
INSERT INTO public.categories (catref, classtype) VALUES (24, 'Nontraditional Bond');
INSERT INTO public.categories (catref, classtype) VALUES (26, 'Large Growth');
INSERT INTO public.categories (catref, classtype) VALUES (27, 'Industrials');
INSERT INTO public.categories (catref, classtype) VALUES (29, 'Allocation--70% to 85% Equity');
INSERT INTO public.categories (catref, classtype) VALUES (30, 'Energy Limited Partnership');
INSERT INTO public.categories (catref, classtype) VALUES (35, 'High Yield Bond');
INSERT INTO public.categories (catref, classtype) VALUES (37, 'Allocation--30% to 50% Equity');
INSERT INTO public.categories (catref, classtype) VALUES (39, 'Allocation--50% to 70% Equity');
INSERT INTO public.categories (catref, classtype) VALUES (40, 'Natural Resources');
INSERT INTO public.categories (catref, classtype) VALUES (41, 'Ultrashort Bond');
INSERT INTO public.categories (catref, classtype) VALUES (43, 'Technology');
INSERT INTO public.categories (catref, classtype) VALUES (45, 'Mid-Cap Growth');
INSERT INTO public.categories (catref, classtype) VALUES (53, 'Long-Short Equity');
INSERT INTO public.categories (catref, classtype) VALUES (57, 'Muni National Interm');
INSERT INTO public.categories (catref, classtype) VALUES (58, 'Consumer Cyclical');
INSERT INTO public.categories (catref, classtype) VALUES (69, 'Europe Stock');
INSERT INTO public.categories (catref, classtype) VALUES (71, 'Japan Stock');
INSERT INTO public.categories (catref, classtype) VALUES (74, 'Real Estate');
INSERT INTO public.categories (catref, classtype) VALUES (75, 'Commodities Broad Basket');
INSERT INTO public.categories (catref, classtype) VALUES (83, 'Trading--Leveraged Equity');
INSERT INTO public.categories (catref, classtype) VALUES (87, 'Trading--Inverse Equity');
INSERT INTO public.categories (catref, classtype) VALUES (89, 'Financial');
INSERT INTO public.categories (catref, classtype) VALUES (98, 'Short-Term Bond');
INSERT INTO public.categories (catref, classtype) VALUES (102, 'Long-Term Bond');
INSERT INTO public.categories (catref, classtype) VALUES (112, 'Latin America Stock');
INSERT INTO public.categories (catref, classtype) VALUES (130, 'World Bond');
INSERT INTO public.categories (catref, classtype) VALUES (138, 'Emerging-Markets Local-Currency Bond');
INSERT INTO public.categories (catref, classtype) VALUES (165, 'Foreign Large Value');
INSERT INTO public.categories (catref, classtype) VALUES (175, 'Muni California Long');
INSERT INTO public.categories (catref, classtype) VALUES (178, 'Equity Energy');
INSERT INTO public.categories (catref, classtype) VALUES (184, 'Corporate Bond');
INSERT INTO public.categories (catref, classtype) VALUES (188, 'Trading--Miscellaneous');
INSERT INTO public.categories (catref, classtype) VALUES (199, 'Convertibles');
INSERT INTO public.categories (catref, classtype) VALUES (202, 'Single Currency');
INSERT INTO public.categories (catref, classtype) VALUES (205, 'World Allocation');
INSERT INTO public.categories (catref, classtype) VALUES (217, 'Managed Futures');
INSERT INTO public.categories (catref, classtype) VALUES (220, 'Mid-Cap Value');
INSERT INTO public.categories (catref, classtype) VALUES (221, 'Foreign Small/Mid Value');
INSERT INTO public.categories (catref, classtype) VALUES (246, 'Trading--Inverse Commodities');
INSERT INTO public.categories (catref, classtype) VALUES (268, 'Global Real Estate');
INSERT INTO public.categories (catref, classtype) VALUES (283, 'Small Growth');
INSERT INTO public.categories (catref, classtype) VALUES (300, 'Utilities');
INSERT INTO public.categories (catref, classtype) VALUES (309, 'Long Government');
INSERT INTO public.categories (catref, classtype) VALUES (354, 'India Equity');
INSERT INTO public.categories (catref, classtype) VALUES (362, 'Foreign Small/Mid Growth');
INSERT INTO public.categories (catref, classtype) VALUES (385, 'Communications');
INSERT INTO public.categories (catref, classtype) VALUES (459, 'Bank Loan');
INSERT INTO public.categories (catref, classtype) VALUES (463, 'Intermediate Government');
INSERT INTO public.categories (catref, classtype) VALUES (467, 'Muni National Long');
INSERT INTO public.categories (catref, classtype) VALUES (502, 'Preferred Stock');
INSERT INTO public.categories (catref, classtype) VALUES (514, 'Muni National Short');
INSERT INTO public.categories (catref, classtype) VALUES (515, 'Consumer Defensive');
INSERT INTO public.categories (catref, classtype) VALUES (571, 'Equity Precious Metals');
INSERT INTO public.categories (catref, classtype) VALUES (575, 'Infrastructure');
INSERT INTO public.categories (catref, classtype) VALUES (610, 'Inflation-Protected Bond');
INSERT INTO public.categories (catref, classtype) VALUES (642, 'Allocation--85%+ Equity');
INSERT INTO public.categories (catref, classtype) VALUES (647, 'Allocation--15% to 30% Equity');
INSERT INTO public.categories (catref, classtype) VALUES (649, 'Foreign Small/Mid Blend');
INSERT INTO public.categories (catref, classtype) VALUES (658, 'High Yield Muni');
INSERT INTO public.categories (catref, classtype) VALUES (727, 'Diversified Pacific/Asia');
INSERT INTO public.categories (catref, classtype) VALUES (890, 'Muni Minnesota');
INSERT INTO public.categories (catref, classtype) VALUES (1207, 'Trading--Inverse Debt');
INSERT INTO public.categories (catref, classtype) VALUES (1332, 'Trading--Leveraged Debt');
INSERT INTO public.categories (catref, classtype) VALUES (1658, 'Muni New York Intermediate');


--
-- Name: categories_catref_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.categories_catref_seq', 1687, true);


--
-- Name: categories categories_classtype_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_classtype_key UNIQUE (classtype);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (catref);


--
-- PostgreSQL database dump complete
--

