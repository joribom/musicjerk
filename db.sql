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

--
-- Name: update_score(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_score() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  UPDATE albums SET score=(SELECT AVG(rating) FROM ratings WHERE album_id=NEW.album_id) WHERE id=NEW.album_id;
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_score() OWNER TO postgres;

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
    url character varying NOT NULL,
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
-- Name: albums id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums ALTER COLUMN id SET DEFAULT nextval('public.albums_id_seq'::regclass);


--
-- Name: users uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN uid SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: albums albums_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_id_key UNIQUE (id);


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
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: worst_tracks_votes worst_tracks_votes_uid_album_id_index_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.worst_tracks_votes
    ADD CONSTRAINT worst_tracks_votes_uid_album_id_index_key UNIQUE (uid, album_id, index);


--
-- Name: ratings update_score_on_insert; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_score_on_insert AFTER INSERT ON public.ratings FOR EACH ROW EXECUTE PROCEDURE public.update_score();


--
-- Name: ratings update_score_on_update; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_score_on_update AFTER UPDATE ON public.ratings FOR EACH ROW EXECUTE PROCEDURE public.update_score();


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

