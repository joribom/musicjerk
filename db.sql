--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: albums; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.albums (
    id integer NOT NULL,
    week integer NOT NULL,
    mandatory boolean NOT NULL,
    title character varying NOT NULL,
    artist character varying NOT NULL,
    selected_by integer NOT NULL,
    url varchar NOT NULL,
    score numeric,
    image_url character varying,
    summary character varying,
    spotify_id character varying,
    genres text[],
    styles text[]
);


ALTER TABLE public.albums OWNER TO postgres;

--
-- Name: albums_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.albums_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.albums_id_seq OWNER TO postgres;

--
-- Name: albums_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.albums_id_seq OWNED BY public.albums.id;


--
-- Name: best_tracks_votes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.best_tracks_votes (
    uid integer,
    album_id integer,
    index integer
);


ALTER TABLE public.best_tracks_votes OWNER TO postgres;

--
-- Name: passwords; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.passwords (
    uid integer NOT NULL,
    hash character(128),
    salt character(32)
);


ALTER TABLE public.passwords OWNER TO postgres;

--
-- Name: ratings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ratings (
    uid integer NOT NULL,
    album_id integer NOT NULL,
    rating integer
);


ALTER TABLE public.ratings OWNER TO postgres;

--
-- Name: songs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.songs (
    album_id integer NOT NULL,
    index integer NOT NULL
);


ALTER TABLE public.songs OWNER TO postgres;

--
-- Name: spotify_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.spotify_tokens (
    uid integer NOT NULL,
    access_token character varying(200),
    access_until timestamp without time zone,
    refresh_token character varying(200)
);


ALTER TABLE public.spotify_tokens OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    uid integer NOT NULL,
    name character varying(50) NOT NULL,
    session character varying(100) DEFAULT NULL::character varying,
    cookie character varying(100) DEFAULT NULL::character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.uid;


--
-- Name: worst_tracks_votes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.worst_tracks_votes (
    uid integer,
    album_id integer,
    index integer
);


ALTER TABLE public.worst_tracks_votes OWNER TO postgres;


--
-- Name: albums uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums ALTER COLUMN id SET DEFAULT nextval('public.albums_id_seq'::regclass);


--
-- Name: users uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN uid SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: albums; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.albums (id, week, mandatory, title, artist, selected_by, score, image_url, summary, spotify_id, genres, styles) FROM stdin;
\.


--
-- Data for Name: best_tracks_votes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.best_tracks_votes (uid, album_id, index) FROM stdin;
\.


--
-- Data for Name: passwords; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.passwords (uid, hash, salt) FROM stdin;
2	442c24a5a0e6b775a970625faef649fb518224a32c24aa3e54e046483046414171c7fcb7e1ed34b86e909c6058c352144b2379aec16afaaf5dd47a474f653d61	39aeca08fea44d11a0f81190f2afab3e
\.


--
-- Data for Name: ratings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ratings (uid, album_id, rating) FROM stdin;
\.


--
-- Data for Name: songs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.songs (album_id, index) FROM stdin;
\.


--
-- Data for Name: spotify_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spotify_tokens (uid, access_token, access_until, refresh_token) FROM stdin;
2	BQDPQSdtCKFK6xZoqPU_R-cXnx2ZQL97csO5742iH4p1tidq8dv2LvBsFUZfWyWTB26QSIJeRykLZJtP4QyFMXW4uTipyBdc6WSh9cK477j64wnVZ76WC1ywjnqO36YfVnvHeKm5PqXUkNL8gsxwocc	\N	AQAOaONy61gZ96umZUWXZHLTq24pSwf5dkYYMutOkGGVqDhODpRkfyrkssVCZrLextsc8B6HRvBZRttF1Rl-oEWoKkIFyJxUDcIJAeJe_jKBz5jeqESLYbFuockXy4i3lawwKw
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (uid, name, session, cookie) FROM stdin;
2	johan	WOULiyna8chpB6f_icjZlA	\N
\.


--
-- Data for Name: worst_tracks_votes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.worst_tracks_votes (uid, album_id, index) FROM stdin;
\.


--
-- Name: albums_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.albums_id_seq', 2, true);

--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: albums albums_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_pkey PRIMARY KEY (id);


--
-- Name: albums albums_week_mandatory_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_week_mandatory_key UNIQUE (week, mandatory);


--
-- Name: albums albums_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_id_key UNIQUE (id);


--
-- Name: best_tracks_votes best_tracks_votes_uid_album_id_index_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.best_tracks_votes
    ADD CONSTRAINT best_tracks_votes_uid_album_id_index_key UNIQUE (uid, album_id, index);


--
-- Name: passwords passwords_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.passwords
    ADD CONSTRAINT passwords_pkey PRIMARY KEY (uid);


--
-- Name: ratings ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (uid, album_id);


--
-- Name: songs songs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.songs
    ADD CONSTRAINT songs_pkey PRIMARY KEY (album_id, index);


--
-- Name: spotify_tokens spotify_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spotify_tokens
    ADD CONSTRAINT spotify_tokens_pkey PRIMARY KEY (uid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: worst_tracks_votes worst_tracks_votes_uid_album_id_index_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.worst_tracks_votes
    ADD CONSTRAINT worst_tracks_votes_uid_album_id_index_key UNIQUE (uid, album_id, index);


--
-- Name: albums albums_selected_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_selected_by_fkey FOREIGN KEY (selected_by) REFERENCES public.users(uid);


--
-- Name: albums albums_selected_by_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_selected_by_fkey1 FOREIGN KEY (selected_by) REFERENCES public.users(uid);


--
-- Name: best_tracks_votes best_tracks_votes_album_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.best_tracks_votes
    ADD CONSTRAINT best_tracks_votes_album_id_fkey FOREIGN KEY (album_id, index) REFERENCES public.songs(album_id, index);


--
-- Name: best_tracks_votes best_tracks_votes_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.best_tracks_votes
    ADD CONSTRAINT best_tracks_votes_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- Name: passwords passwords_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.passwords
    ADD CONSTRAINT passwords_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- Name: ratings ratings_album_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_album_id_fkey FOREIGN KEY (album_id) REFERENCES public.albums(id);


--
-- Name: ratings ratings_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- Name: songs songs_album_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.songs
    ADD CONSTRAINT songs_album_id_fkey FOREIGN KEY (album_id) REFERENCES public.albums(id);


--
-- Name: spotify_tokens spotify_tokens_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spotify_tokens
    ADD CONSTRAINT spotify_tokens_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- Name: worst_tracks_votes worst_tracks_votes_album_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.worst_tracks_votes
    ADD CONSTRAINT worst_tracks_votes_album_id_fkey FOREIGN KEY (album_id, index) REFERENCES public.songs(album_id, index);


--
-- Name: worst_tracks_votes worst_tracks_votes_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.worst_tracks_votes
    ADD CONSTRAINT worst_tracks_votes_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- PostgreSQL database dump complete
--
