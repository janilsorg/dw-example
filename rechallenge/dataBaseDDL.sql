CREATE TABLE public.dim_pcinema
(
  cinema text,
  id_cinema bigint
)                
CREATE TABLE public.dim_pformat
(
  format text,
  price bigint,
  id_format bigint
)                 
CREATE TABLE public.dim_pmovie
(
  movie text,
  id_movie bigint,
  budget text,
  runtime text,
  vote_average text
) 

CREATE TABLE public.dim_ppromotion
(
  promotion text,
  id_promotion bigint,
  type text
)                   

CREATE TABLE public.pfact_sales
(                                                                                    
  age double precision,
  id_format bigint,
  proj_time text,
  qty_tickets double precision,
  screen_number bigint,
  sex text,
  total_paid double precision,
  type text,
  "user" double precision,
  id_movie bigint,
  id_cinema bigint,
  id_fact bigint
)                

