-- 创建所需的枚举类型


-- 表定义和数据: "families"
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
-- Name: families; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.families (
    famcode bigint NOT NULL,
    groupname text NOT NULL
);


ALTER TABLE public.families OWNER TO root;

--
-- Name: families_famcode_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.families_famcode_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.families_famcode_seq OWNER TO root;

--
-- Name: families_famcode_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.families_famcode_seq OWNED BY public.families.famcode;


--
-- Name: families famcode; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.families ALTER COLUMN famcode SET DEFAULT nextval('public.families_famcode_seq'::regclass);


--
-- Data for Name: families; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.families (famcode, groupname) VALUES (1, 'DWS');
INSERT INTO public.families (famcode, groupname) VALUES (2, 'Virtus');
INSERT INTO public.families (famcode, groupname) VALUES (3, 'American Century Investments');
INSERT INTO public.families (famcode, groupname) VALUES (4, 'Thrivent Funds');
INSERT INTO public.families (famcode, groupname) VALUES (11, 'Horizon Investments');
INSERT INTO public.families (famcode, groupname) VALUES (17, 'American Funds');
INSERT INTO public.families (famcode, groupname) VALUES (22, 'Cavanal Hill funds');
INSERT INTO public.families (famcode, groupname) VALUES (23, 'Putnam');
INSERT INTO public.families (famcode, groupname) VALUES (31, 'American Beacon');
INSERT INTO public.families (famcode, groupname) VALUES (42, 'Invesco');
INSERT INTO public.families (famcode, groupname) VALUES (64, 'Aasgard');
INSERT INTO public.families (famcode, groupname) VALUES (84, 'Alger');
INSERT INTO public.families (famcode, groupname) VALUES (96, 'Aberdeen');
INSERT INTO public.families (famcode, groupname) VALUES (100, 'Ancora');
INSERT INTO public.families (famcode, groupname) VALUES (107, 'Absolute Capital');
INSERT INTO public.families (famcode, groupname) VALUES (128, 'AllianceBernstein');
INSERT INTO public.families (famcode, groupname) VALUES (142, 'Columbia Threadneedle');
INSERT INTO public.families (famcode, groupname) VALUES (160, 'AMG Funds');
INSERT INTO public.families (famcode, groupname) VALUES (191, 'AmericaFirst Funds');
INSERT INTO public.families (famcode, groupname) VALUES (193, 'ABR');
INSERT INTO public.families (famcode, groupname) VALUES (226, 'Abbey Capital');
INSERT INTO public.families (famcode, groupname) VALUES (235, 'RBC Global Asset Management.');
INSERT INTO public.families (famcode, groupname) VALUES (273, 'Arbitrage Fund');
INSERT INTO public.families (famcode, groupname) VALUES (308, 'Argent');
INSERT INTO public.families (famcode, groupname) VALUES (322, 'Advisors Capital');
INSERT INTO public.families (famcode, groupname) VALUES (353, 'Catalyst Mutual Funds');
INSERT INTO public.families (famcode, groupname) VALUES (357, 'AQR Funds');
INSERT INTO public.families (famcode, groupname) VALUES (377, 'Aperture Investors');
INSERT INTO public.families (famcode, groupname) VALUES (378, 'Azzad Fund');
INSERT INTO public.families (famcode, groupname) VALUES (380, 'Adirondack Funds');
INSERT INTO public.families (famcode, groupname) VALUES (382, 'Adler');
INSERT INTO public.families (famcode, groupname) VALUES (383, '361 Funds');
INSERT INTO public.families (famcode, groupname) VALUES (391, 'ACM');
INSERT INTO public.families (famcode, groupname) VALUES (402, 'North Square');
INSERT INTO public.families (famcode, groupname) VALUES (403, 'Vaughan Nelson');
INSERT INTO public.families (famcode, groupname) VALUES (441, 'Acadian Funds');
INSERT INTO public.families (famcode, groupname) VALUES (462, 'Yorktown Funds');
INSERT INTO public.families (famcode, groupname) VALUES (463, 'Applied Finance Advisors');
INSERT INTO public.families (famcode, groupname) VALUES (466, 'ProFunds');
INSERT INTO public.families (famcode, groupname) VALUES (498, 'Angel Oak');
INSERT INTO public.families (famcode, groupname) VALUES (499, 'Anfield');
INSERT INTO public.families (famcode, groupname) VALUES (503, 'Acuitas Investments');
INSERT INTO public.families (famcode, groupname) VALUES (506, 'AAM');
INSERT INTO public.families (famcode, groupname) VALUES (508, 'Archer');
INSERT INTO public.families (famcode, groupname) VALUES (512, 'Ariel Investments');
INSERT INTO public.families (famcode, groupname) VALUES (517, 'Alpha Fiduciary');
INSERT INTO public.families (famcode, groupname) VALUES (594, 'PGIM Funds (Prudential)');
INSERT INTO public.families (famcode, groupname) VALUES (599, 'AGF Investments');
INSERT INTO public.families (famcode, groupname) VALUES (704, 'Crow Point');
INSERT INTO public.families (famcode, groupname) VALUES (747, 'Akre');
INSERT INTO public.families (famcode, groupname) VALUES (751, 'ALPS');
INSERT INTO public.families (famcode, groupname) VALUES (766, 'Lord Abbett');
INSERT INTO public.families (famcode, groupname) VALUES (809, 'FS Investments');
INSERT INTO public.families (famcode, groupname) VALUES (822, 'Amana');
INSERT INTO public.families (famcode, groupname) VALUES (840, 'Natixis Funds');
INSERT INTO public.families (famcode, groupname) VALUES (842, 'AAMA');
INSERT INTO public.families (famcode, groupname) VALUES (857, 'AlphaMark');
INSERT INTO public.families (famcode, groupname) VALUES (858, 'MainGate Trust');
INSERT INTO public.families (famcode, groupname) VALUES (860, 'Aegon Asset Management US');
INSERT INTO public.families (famcode, groupname) VALUES (869, 'American Growth');
INSERT INTO public.families (famcode, groupname) VALUES (963, 'Amundi US');
INSERT INTO public.families (famcode, groupname) VALUES (996, 'Artisan');
INSERT INTO public.families (famcode, groupname) VALUES (1055, 'Appleseed Fund');
INSERT INTO public.families (famcode, groupname) VALUES (1060, 'Fiera Capital');
INSERT INTO public.families (famcode, groupname) VALUES (1061, 'Pinnacle');
INSERT INTO public.families (famcode, groupname) VALUES (1072, 'LKCM');
INSERT INTO public.families (famcode, groupname) VALUES (1079, 'Alta Capital');
INSERT INTO public.families (famcode, groupname) VALUES (1091, 'Absolute Strategies');
INSERT INTO public.families (famcode, groupname) VALUES (1156, 'Franklin Templeton Investments');
INSERT INTO public.families (famcode, groupname) VALUES (1157, 'AGRA');
INSERT INTO public.families (famcode, groupname) VALUES (1171, 'Aristotle');
INSERT INTO public.families (famcode, groupname) VALUES (1180, 'Nuveen');
INSERT INTO public.families (famcode, groupname) VALUES (1221, 'Lisanti SmallCap');
INSERT INTO public.families (famcode, groupname) VALUES (1240, 'Arrow Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1247, 'Transamerica');
INSERT INTO public.families (famcode, groupname) VALUES (1281, 'Astor');
INSERT INTO public.families (famcode, groupname) VALUES (1320, 'ATAC Fund');
INSERT INTO public.families (famcode, groupname) VALUES (1321, 'American Trust Company');
INSERT INTO public.families (famcode, groupname) VALUES (1322, 'Anchor');
INSERT INTO public.families (famcode, groupname) VALUES (1350, 'Aquila');
INSERT INTO public.families (famcode, groupname) VALUES (1351, 'ATLAS US. TACTICAL INCOME FUND, INC.');
INSERT INTO public.families (famcode, groupname) VALUES (1353, 'PIMCO');
INSERT INTO public.families (famcode, groupname) VALUES (1373, 'Athena Fund');
INSERT INTO public.families (famcode, groupname) VALUES (1388, 'Auer');
INSERT INTO public.families (famcode, groupname) VALUES (1414, 'Auxier Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1419, 'Aegis');
INSERT INTO public.families (famcode, groupname) VALUES (1422, 'Avantis Investors');
INSERT INTO public.families (famcode, groupname) VALUES (1425, 'Ave Maria Mutual Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1434, 'BNY Mellon');
INSERT INTO public.families (famcode, groupname) VALUES (1442, 'Nottingham');
INSERT INTO public.families (famcode, groupname) VALUES (1459, 'CIBC Private Wealth Management');
INSERT INTO public.families (famcode, groupname) VALUES (1485, 'Innealta Capital');
INSERT INTO public.families (famcode, groupname) VALUES (1487, 'Axonic');
INSERT INTO public.families (famcode, groupname) VALUES (1489, 'AXS');
INSERT INTO public.families (famcode, groupname) VALUES (1522, 'BlackRock');
INSERT INTO public.families (famcode, groupname) VALUES (1524, 'BMO Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1534, 'Brown Advisory Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1540, 'Sterling Capital Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1556, 'Baird');
INSERT INTO public.families (famcode, groupname) VALUES (1574, 'Baron Capital Group, Inc.');
INSERT INTO public.families (famcode, groupname) VALUES (1578, 'Beacon Investment Advisory');
INSERT INTO public.families (famcode, groupname) VALUES (1597, 'Northern Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1598, 'BBH');
INSERT INTO public.families (famcode, groupname) VALUES (1600, 'Bridge Builder');
INSERT INTO public.families (famcode, groupname) VALUES (1601, 'William Blair');
INSERT INTO public.families (famcode, groupname) VALUES (1630, 'Boston Common');
INSERT INTO public.families (famcode, groupname) VALUES (1631, 'Baillie Gifford Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1642, 'Blue Current Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1648, 'Blue Chip Investor Fund');
INSERT INTO public.families (famcode, groupname) VALUES (1649, 'Brown Capital Management');
INSERT INTO public.families (famcode, groupname) VALUES (1659, 'Brandes');
INSERT INTO public.families (famcode, groupname) VALUES (1692, 'Liberty Street');
INSERT INTO public.families (famcode, groupname) VALUES (1715, 'Federated');
INSERT INTO public.families (famcode, groupname) VALUES (1719, 'BeeHive');
INSERT INTO public.families (famcode, groupname) VALUES (1726, 'Boston Partners');
INSERT INTO public.families (famcode, groupname) VALUES (1733, 'Chartwell Investment Partners');
INSERT INTO public.families (famcode, groupname) VALUES (1760, 'Berkshire');
INSERT INTO public.families (famcode, groupname) VALUES (1761, 'Biondo Investment Advisor');
INSERT INTO public.families (famcode, groupname) VALUES (1766, 'BFS');
INSERT INTO public.families (famcode, groupname) VALUES (1817, 'Brookfield Investment Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1834, 'Barrett');
INSERT INTO public.families (famcode, groupname) VALUES (1847, 'Soundwatch Capital');
INSERT INTO public.families (famcode, groupname) VALUES (1848, 'Bishop Street');
INSERT INTO public.families (famcode, groupname) VALUES (1850, 'Beech Hill');
INSERT INTO public.families (famcode, groupname) VALUES (1909, 'Monteagle Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1913, 'Buffalo');
INSERT INTO public.families (famcode, groupname) VALUES (1917, 'DoubleLine');
INSERT INTO public.families (famcode, groupname) VALUES (1940, 'UBS Asset Management');
INSERT INTO public.families (famcode, groupname) VALUES (1950, 'Invenomic');
INSERT INTO public.families (famcode, groupname) VALUES (1988, 'Meeder Funds');
INSERT INTO public.families (famcode, groupname) VALUES (1989, 'Standpoint Asset Management');
INSERT INTO public.families (famcode, groupname) VALUES (2006, 'Blueprint Fund Management');
INSERT INTO public.families (famcode, groupname) VALUES (2038, 'BNY Mellon Funds');
INSERT INTO public.families (famcode, groupname) VALUES (2051, 'Beck, Mack & Oliver');
INSERT INTO public.families (famcode, groupname) VALUES (2058, 'MFS');
INSERT INTO public.families (famcode, groupname) VALUES (2085, 'Bogle');
INSERT INTO public.families (famcode, groupname) VALUES (2086, 'Oak Associates');
INSERT INTO public.families (famcode, groupname) VALUES (2092, 'Boston Trust Walden Funds');
INSERT INTO public.families (famcode, groupname) VALUES (2093, 'Bridgeway');
INSERT INTO public.families (famcode, groupname) VALUES (2096, 'Boyar Value Fund');
INSERT INTO public.families (famcode, groupname) VALUES (2121, 'Bright Rock');
INSERT INTO public.families (famcode, groupname) VALUES (2145, 'Bridges');
INSERT INTO public.families (famcode, groupname) VALUES (2173, 'Bramshill Investments');
INSERT INTO public.families (famcode, groupname) VALUES (2195, 'Bretton Fund');
INSERT INTO public.families (famcode, groupname) VALUES (2198, 'Bruce');
INSERT INTO public.families (famcode, groupname) VALUES (2237, 'Bernzott Capital Advisors');
INSERT INTO public.families (famcode, groupname) VALUES (2278, 'BTS');
INSERT INTO public.families (famcode, groupname) VALUES (2284, 'Belmont Capital Group');
INSERT INTO public.families (famcode, groupname) VALUES (2295, 'Salient Funds');
INSERT INTO public.families (famcode, groupname) VALUES (2302, 'CBOE Vest');


--
-- Name: families_famcode_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.families_famcode_seq', 2310, true);


--
-- Name: families families_groupname_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_groupname_key UNIQUE (groupname);


--
-- Name: families families_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (famcode);


--
-- PostgreSQL database dump complete
--

