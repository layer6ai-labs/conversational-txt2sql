
-- 表定义和数据: "family_exchanges"
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
-- Name: family_exchanges; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.family_exchanges (
    connectref bigint NOT NULL,
    familyref character varying(50),
    exchangeref character varying(10)
);


ALTER TABLE public.family_exchanges OWNER TO root;

--
-- Name: family_exchanges_connectref_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.family_exchanges_connectref_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.family_exchanges_connectref_seq OWNER TO root;

--
-- Name: family_exchanges_connectref_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.family_exchanges_connectref_seq OWNED BY public.family_exchanges.connectref;


--
-- Name: family_exchanges connectref; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.family_exchanges ALTER COLUMN connectref SET DEFAULT nextval('public.family_exchanges_connectref_seq'::regclass);


--
-- Data for Name: family_exchanges; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1, 'DWS', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2, 'Virtus', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (3, 'American Century Investments', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (4, 'Thrivent Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (5, 'American Century Investments', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (6, 'American Century Investments', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (11, 'Horizon Investments', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (14, 'DWS', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (16, 'DWS', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (17, 'American Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (22, 'Cavanal Hill funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (23, 'Putnam', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (25, 'Thrivent Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (30, 'Cavanal Hill funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (31, 'American Beacon', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (37, 'American Beacon', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (42, 'Invesco', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (55, 'American Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (61, 'American Beacon', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (64, 'Aasgard', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (70, 'Invesco', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (84, 'Alger', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (96, 'Aberdeen', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (100, 'Ancora', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (104, 'Cavanal Hill funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (107, 'Absolute Capital', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (108, 'Thrivent Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (109, 'Absolute Capital', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (111, 'Alger', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (122, 'Ancora', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (128, 'AllianceBernstein', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (129, 'AllianceBernstein', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (133, 'AllianceBernstein', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (142, 'Columbia Threadneedle', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (144, 'Aberdeen', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (160, 'AMG Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (166, 'AMG Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (170, 'American Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (171, 'Aberdeen', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (189, 'Invesco', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (191, 'AmericaFirst Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (193, 'ABR', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (226, 'Abbey Capital', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (227, 'Abbey Capital', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (229, 'Abbey Capital', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (234, 'Alger', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (235, 'RBC Global Asset Management.', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (236, 'RBC Global Asset Management.', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (252, 'RBC Global Asset Management.', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (271, 'Columbia Threadneedle', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (273, 'Arbitrage Fund', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (308, 'Argent', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (313, 'Virtus', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (315, 'Horizon Investments', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (322, 'Advisors Capital', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (333, 'Advisors Capital', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (353, 'Catalyst Mutual Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (357, 'AQR Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (358, 'AQR Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (377, 'Aperture Investors', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (378, 'Azzad Fund', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (379, 'Virtus', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (380, 'Adirondack Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (381, 'AMG Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (382, 'Adler', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (383, '361 Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (391, 'ACM', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (393, 'ACM', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (402, 'North Square', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (403, 'Vaughan Nelson', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (405, 'Vaughan Nelson', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (407, 'North Square', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (420, 'Arbitrage Fund', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (441, 'Acadian Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (447, 'Acadian Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (462, 'Yorktown Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (463, 'Applied Finance Advisors', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (466, 'ProFunds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (467, 'ProFunds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (486, 'Yorktown Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (498, 'Angel Oak', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (499, 'Anfield', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (501, 'Anfield', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (503, 'Acuitas Investments', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (506, 'AAM', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (508, 'Archer', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (509, 'Aperture Investors', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (512, 'Ariel Investments', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (514, 'AmericaFirst Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (517, 'Alpha Fiduciary', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (526, 'Applied Finance Advisors', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (529, 'AAM', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (534, '361 Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (589, 'Ariel Investments', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (594, 'PGIM Funds (Prudential)', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (599, 'AGF Investments', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (601, 'AGF Investments', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (704, 'Crow Point', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (719, 'AQR Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (747, 'Akre', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (751, 'ALPS', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (766, 'Lord Abbett', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (767, 'Lord Abbett', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (786, 'ALPS', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (809, 'FS Investments', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (810, 'FS Investments', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (822, 'Amana', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (836, 'Amana', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (840, 'Natixis Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (842, 'AAMA', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (844, 'AAMA', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (857, 'AlphaMark', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (858, 'MainGate Trust', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (860, 'Aegon Asset Management US', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (869, 'American Growth', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (904, 'Ancora', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (915, 'Angel Oak', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (920, 'Angel Oak', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (963, 'Amundi US', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (996, 'Artisan', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (997, 'Artisan', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1000, 'Artisan', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1034, 'Yorktown Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1055, 'Appleseed Fund', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1060, 'Fiera Capital', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1061, 'Pinnacle', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1062, 'Fiera Capital', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1072, 'LKCM', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1079, 'Alta Capital', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1091, 'Absolute Strategies', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1096, 'Archer', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1156, 'Franklin Templeton Investments', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1157, 'AGRA', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1171, 'Aristotle', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1173, 'Archer', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1175, 'Aristotle', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1179, 'Aristotle', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1180, 'Nuveen', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1221, 'Lisanti SmallCap', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1236, 'Nuveen', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1237, 'Nuveen', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1239, 'Natixis Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1240, 'Arrow Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1243, 'Arrow Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1247, 'Transamerica', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1281, 'Astor', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1299, 'Astor', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1320, 'ATAC Fund', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1321, 'American Trust Company', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1322, 'Anchor', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1323, 'Anchor', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1325, 'Anchor', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1327, 'ATAC Fund', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1350, 'Aquila', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1351, 'ATLAS US. TACTICAL INCOME FUND, INC.', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1353, 'PIMCO', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1354, 'PIMCO', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1361, 'Aquila', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1364, 'Arbitrage Fund', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1365, 'Catalyst Mutual Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1366, 'Catalyst Mutual Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1373, 'Athena Fund', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1374, 'Athena Fund', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1388, 'Auer', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1414, 'Auxier Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1416, 'Auxier Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1419, 'Aegis', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1422, 'Avantis Investors', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1424, 'Avantis Investors', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1425, 'Ave Maria Mutual Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1426, 'Ave Maria Mutual Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1434, 'BNY Mellon', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1435, 'BNY Mellon', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1439, 'Avantis Investors', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1442, 'Nottingham', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1445, 'ALPS', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1459, 'CIBC Private Wealth Management', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1460, 'CIBC Private Wealth Management', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1481, 'CIBC Private Wealth Management', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1485, 'Innealta Capital', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1487, 'Axonic', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1489, 'AXS', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1491, 'Innealta Capital', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1522, 'BlackRock', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1524, 'BMO Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1526, 'BMO Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1529, 'BlackRock', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1530, 'BlackRock', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1533, 'BMO Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1534, 'Brown Advisory Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1540, 'Sterling Capital Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1544, 'Brown Advisory Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1556, 'Baird', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1568, 'Amundi US', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1574, 'Baron Capital Group, Inc.', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1577, 'Baron Capital Group, Inc.', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1578, 'Beacon Investment Advisory', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1580, 'Brown Advisory Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1582, 'Sterling Capital Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1597, 'Northern Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1598, 'BBH', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1600, 'Bridge Builder', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1601, 'William Blair', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1602, 'Bridge Builder', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1630, 'Boston Common', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1631, 'Baillie Gifford Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1642, 'Blue Current Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1648, 'Blue Chip Investor Fund', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1649, 'Brown Capital Management', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1650, 'Brown Capital Management', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1659, 'Brandes', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1660, 'Brandes', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1661, 'Brandes', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1684, 'Baron Capital Group, Inc.', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1692, 'Liberty Street', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1693, 'Liberty Street', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1694, 'Liberty Street', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1715, 'Federated', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1719, 'BeeHive', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1726, 'Boston Partners', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1733, 'Chartwell Investment Partners', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1760, 'Berkshire', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1761, 'Biondo Investment Advisor', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1766, 'BFS', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1784, 'Baillie Gifford Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1788, 'Baillie Gifford Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1806, 'William Blair', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1817, 'Brookfield Investment Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1819, 'Boston Partners', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1834, 'Barrett', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1847, 'Soundwatch Capital', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1848, 'Bishop Street', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1850, 'Beech Hill', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1880, 'Sterling Capital Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1909, 'Monteagle Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1913, 'Buffalo', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1917, 'DoubleLine', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1921, 'Baird', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1923, 'Baird', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1931, 'ProFunds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1940, 'UBS Asset Management', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1950, 'Invenomic', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1951, 'Invenomic', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1976, 'Lord Abbett', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1988, 'Meeder Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1989, 'Standpoint Asset Management', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1990, 'Meeder Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (1999, 'Brookfield Investment Funds', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2006, 'Blueprint Fund Management', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2007, 'Blueprint Fund Management', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2038, 'BNY Mellon Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2041, 'BNY Mellon Funds', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2051, 'Beck, Mack & Oliver', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2058, 'MFS', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2060, 'MFS', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2079, 'UBS Asset Management', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2085, 'Bogle', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2086, 'Oak Associates', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2092, 'Boston Trust Walden Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2093, 'Bridgeway', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2094, 'BNY Mellon', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2095, 'Bridgeway', 'NGM');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2096, 'Boyar Value Fund', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2121, 'Bright Rock', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2122, 'Bright Rock', 'PNK');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2124, 'Bridgeway', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2125, 'BlackRock', 'PNK');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2145, 'Bridges', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2173, 'Bramshill Investments', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2195, 'Bretton Fund', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2198, 'Bruce', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2237, 'Bernzott Capital Advisors', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2278, 'BTS', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2281, 'BTS', 'BTS');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2284, 'Belmont Capital Group', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2290, 'Boston Trust Walden Funds', 'PNK');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2294, 'Baird', 'PNK');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2295, 'Salient Funds', 'PCX');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2300, 'BTS', 'PNK');
INSERT INTO public.family_exchanges (connectref, familyref, exchangeref) VALUES (2302, 'CBOE Vest', 'PCX');


--
-- Name: family_exchanges_connectref_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.family_exchanges_connectref_seq', 2310, true);


--
-- Name: family_exchanges family_exchanges_familyref_exchangeref_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.family_exchanges
    ADD CONSTRAINT family_exchanges_familyref_exchangeref_key UNIQUE (familyref, exchangeref);


--
-- Name: family_exchanges family_exchanges_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.family_exchanges
    ADD CONSTRAINT family_exchanges_pkey PRIMARY KEY (connectref);


--
-- Name: family_exchanges family_exchanges_exchangeref_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.family_exchanges
    ADD CONSTRAINT family_exchanges_exchangeref_fkey FOREIGN KEY (exchangeref) REFERENCES public.exchanges(marketcode);


--
-- Name: family_exchanges family_exchanges_familyref_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.family_exchanges
    ADD CONSTRAINT family_exchanges_familyref_fkey FOREIGN KEY (familyref) REFERENCES public.families(groupname);


--
-- PostgreSQL database dump complete
--

