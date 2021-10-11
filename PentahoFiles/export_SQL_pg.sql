-- Table: public.dim_cinema

-- DROP TABLE public.dim_cinema;

CREATE TABLE public.dim_cinema
(
  id_cinema integer NOT NULL DEFAULT nextval('dim_cinema_id_cinema_seq'::regclass),
  cinema text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.dim_cinema
  OWNER TO postgres;
 

 -- Table: public.dim_format

-- DROP TABLE public.dim_format;

CREATE TABLE public.dim_format
(
  id_format integer NOT NULL DEFAULT nextval('dim_format_id_format_seq'::regclass),
  format text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.dim_format
  OWNER TO postgres;
 
 -- Table: public.dim_movies

-- DROP TABLE public.dim_movies;

CREATE TABLE public.dim_movies
(
  id_movie integer NOT NULL DEFAULT nextval('dim_movies_id_movie_seq'::regclass),
  movie text,
  release_date date,
  vote_average text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.dim_movies
  OWNER TO postgres;
 

 -- Table: public.dim_promotion

-- DROP TABLE public.dim_promotion;

CREATE TABLE public.dim_promotion
(
  id_promotion integer NOT NULL DEFAULT nextval('dim_promotion_id_promotion_seq'::regclass),
  promotion text,
  type integer
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.dim_promotion
  OWNER TO postgres;
 

 -- Table: public.dw_fact

-- DROP TABLE public.dw_fact;

CREATE TABLE public.dw_fact
(
  id_fact integer NOT NULL DEFAULT nextval('dw_fact_id_fact_seq'::regclass),
  sex text,
  screen_number text,
  type integer,
  total_sales numeric,
  total_tickets numeric,
  id_format integer,
  id_cinema integer,
  id_movie integer,
  age integer,
  project_time text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.dw_fact
  OWNER TO postgres;
 