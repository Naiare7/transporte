--
-- PostgreSQL database dump
--

\restrict t4AnysKuYaphG5Rh0MyguUru0GRLgosvtEegNPZNbZQwQU0UJZUv7MNxTCBqzGy

-- Dumped from database version 15.17
-- Dumped by pg_dump version 15.17

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO camiones;

--
-- Name: clientes; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.clientes (
    id integer NOT NULL,
    razon_social character varying(150) NOT NULL,
    cif_nif character varying(20) NOT NULL,
    telefono character varying(20),
    direccion character varying(250)
);


ALTER TABLE public.clientes OWNER TO camiones;

--
-- Name: clientes_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.clientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clientes_id_seq OWNER TO camiones;

--
-- Name: clientes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.clientes_id_seq OWNED BY public.clientes.id;


--
-- Name: conductores; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.conductores (
    id integer NOT NULL,
    nombre_completo character varying(150) NOT NULL,
    dni character varying(20) NOT NULL,
    carnet_conducir character varying(50) NOT NULL,
    telefono character varying(20),
    disponible boolean
);


ALTER TABLE public.conductores OWNER TO camiones;

--
-- Name: conductores_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.conductores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.conductores_id_seq OWNER TO camiones;

--
-- Name: conductores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.conductores_id_seq OWNED BY public.conductores.id;


--
-- Name: detalles_pedido; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.detalles_pedido (
    id integer NOT NULL,
    descripcion_carga character varying(150) NOT NULL,
    cantidad double precision NOT NULL,
    unidad_medida character varying(20),
    tarifa_flete double precision NOT NULL,
    subtotal double precision NOT NULL,
    requerimientos_especiales text,
    pedido_id integer NOT NULL
);


ALTER TABLE public.detalles_pedido OWNER TO camiones;

--
-- Name: detalles_pedido_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.detalles_pedido_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.detalles_pedido_id_seq OWNER TO camiones;

--
-- Name: detalles_pedido_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.detalles_pedido_id_seq OWNED BY public.detalles_pedido.id;


--
-- Name: facturas; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.facturas (
    id integer NOT NULL,
    fecha_emision timestamp without time zone,
    total double precision NOT NULL,
    pagada boolean,
    pedido_id integer NOT NULL
);


ALTER TABLE public.facturas OWNER TO camiones;

--
-- Name: facturas_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.facturas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.facturas_id_seq OWNER TO camiones;

--
-- Name: facturas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.facturas_id_seq OWNED BY public.facturas.id;


--
-- Name: incidencias_viaje; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.incidencias_viaje (
    id integer NOT NULL,
    fecha_incidencia timestamp without time zone,
    descripcion text NOT NULL,
    gravedad character varying(50),
    viaje_id integer NOT NULL
);


ALTER TABLE public.incidencias_viaje OWNER TO camiones;

--
-- Name: incidencias_viaje_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.incidencias_viaje_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.incidencias_viaje_id_seq OWNER TO camiones;

--
-- Name: incidencias_viaje_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.incidencias_viaje_id_seq OWNED BY public.incidencias_viaje.id;


--
-- Name: pedidos; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.pedidos (
    id integer NOT NULL,
    fecha_pedido timestamp without time zone,
    estado character varying(50),
    observaciones_entrega text,
    cliente_id integer NOT NULL,
    usuario_id integer NOT NULL
);


ALTER TABLE public.pedidos OWNER TO camiones;

--
-- Name: pedidos_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.pedidos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pedidos_id_seq OWNER TO camiones;

--
-- Name: pedidos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.pedidos_id_seq OWNED BY public.pedidos.id;


--
-- Name: rutas; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.rutas (
    id integer NOT NULL,
    origen character varying(100) NOT NULL,
    destino character varying(100) NOT NULL,
    distancia_km double precision,
    tiempo_estimado_horas double precision
);


ALTER TABLE public.rutas OWNER TO camiones;

--
-- Name: rutas_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.rutas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rutas_id_seq OWNER TO camiones;

--
-- Name: rutas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.rutas_id_seq OWNED BY public.rutas.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(255) NOT NULL,
    fecha_creacion timestamp without time zone
);


ALTER TABLE public.usuarios OWNER TO camiones;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.usuarios_id_seq OWNER TO camiones;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: vehiculos; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.vehiculos (
    id integer NOT NULL,
    patente character varying(20) NOT NULL,
    capacidad_toneladas double precision NOT NULL,
    tipo_grano character varying(50),
    disponible boolean
);


ALTER TABLE public.vehiculos OWNER TO camiones;

--
-- Name: vehiculos_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.vehiculos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vehiculos_id_seq OWNER TO camiones;

--
-- Name: vehiculos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.vehiculos_id_seq OWNED BY public.vehiculos.id;


--
-- Name: viajes; Type: TABLE; Schema: public; Owner: camiones
--

CREATE TABLE public.viajes (
    id integer NOT NULL,
    fecha_creacion timestamp without time zone,
    se_entrego boolean,
    fecha_salida timestamp without time zone,
    estado character varying(50),
    conductor_id integer NOT NULL,
    vehiculo_id integer NOT NULL,
    ruta_id integer NOT NULL,
    pedido_id integer NOT NULL,
    usuario_id integer NOT NULL
);


ALTER TABLE public.viajes OWNER TO camiones;

--
-- Name: viajes_id_seq; Type: SEQUENCE; Schema: public; Owner: camiones
--

CREATE SEQUENCE public.viajes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.viajes_id_seq OWNER TO camiones;

--
-- Name: viajes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: camiones
--

ALTER SEQUENCE public.viajes_id_seq OWNED BY public.viajes.id;


--
-- Name: clientes id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.clientes ALTER COLUMN id SET DEFAULT nextval('public.clientes_id_seq'::regclass);


--
-- Name: conductores id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.conductores ALTER COLUMN id SET DEFAULT nextval('public.conductores_id_seq'::regclass);


--
-- Name: detalles_pedido id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.detalles_pedido ALTER COLUMN id SET DEFAULT nextval('public.detalles_pedido_id_seq'::regclass);


--
-- Name: facturas id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.facturas ALTER COLUMN id SET DEFAULT nextval('public.facturas_id_seq'::regclass);


--
-- Name: incidencias_viaje id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.incidencias_viaje ALTER COLUMN id SET DEFAULT nextval('public.incidencias_viaje_id_seq'::regclass);


--
-- Name: pedidos id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.pedidos ALTER COLUMN id SET DEFAULT nextval('public.pedidos_id_seq'::regclass);


--
-- Name: rutas id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.rutas ALTER COLUMN id SET DEFAULT nextval('public.rutas_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Name: vehiculos id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.vehiculos ALTER COLUMN id SET DEFAULT nextval('public.vehiculos_id_seq'::regclass);


--
-- Name: viajes id; Type: DEFAULT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.viajes ALTER COLUMN id SET DEFAULT nextval('public.viajes_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.clientes (id, razon_social, cif_nif, telefono, direccion) FROM stdin;
\.


--
-- Data for Name: conductores; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.conductores (id, nombre_completo, dni, carnet_conducir, telefono, disponible) FROM stdin;
\.


--
-- Data for Name: detalles_pedido; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.detalles_pedido (id, descripcion_carga, cantidad, unidad_medida, tarifa_flete, subtotal, requerimientos_especiales, pedido_id) FROM stdin;
\.


--
-- Data for Name: facturas; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.facturas (id, fecha_emision, total, pagada, pedido_id) FROM stdin;
\.


--
-- Data for Name: incidencias_viaje; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.incidencias_viaje (id, fecha_incidencia, descripcion, gravedad, viaje_id) FROM stdin;
\.


--
-- Data for Name: pedidos; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.pedidos (id, fecha_pedido, estado, observaciones_entrega, cliente_id, usuario_id) FROM stdin;
\.


--
-- Data for Name: rutas; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.rutas (id, origen, destino, distancia_km, tiempo_estimado_horas) FROM stdin;
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.usuarios (id, nombre, email, password_hash, fecha_creacion) FROM stdin;
1	admin	admin@transporte.com	scrypt:32768:8:1$WyI67ZMFb0W4JhNk$5523f9e9d3334dba637c6837b55126a5eec8208ce62d2223e9e6f2805240ed62515648c9f52bf34b231415d3bd481896c32c3a27935a78c8f5e635e83a5342b8	2026-04-23 12:05:06.690952
2	Administrador 2	nuevo@transporte.com	scrypt:32768:8:1$RvgIbQja6tev6HrD$2e592208aa770f48e8c5893d264aaf6584c0187b5c14bb242c190d377fb75c793a1a0562da7f42774b3e5a1400c184630d3650e40556abc4202b1f8f409758f9	2026-04-24 07:11:44.593859
\.


--
-- Data for Name: vehiculos; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.vehiculos (id, patente, capacidad_toneladas, tipo_grano, disponible) FROM stdin;
2	ABC-1234	25	\N	t
\.


--
-- Data for Name: viajes; Type: TABLE DATA; Schema: public; Owner: camiones
--

COPY public.viajes (id, fecha_creacion, se_entrego, fecha_salida, estado, conductor_id, vehiculo_id, ruta_id, pedido_id, usuario_id) FROM stdin;
\.


--
-- Name: clientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.clientes_id_seq', 1, false);


--
-- Name: conductores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.conductores_id_seq', 1, false);


--
-- Name: detalles_pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.detalles_pedido_id_seq', 1, false);


--
-- Name: facturas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.facturas_id_seq', 1, false);


--
-- Name: incidencias_viaje_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.incidencias_viaje_id_seq', 1, false);


--
-- Name: pedidos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.pedidos_id_seq', 1, false);


--
-- Name: rutas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.rutas_id_seq', 1, false);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 3, true);


--
-- Name: vehiculos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.vehiculos_id_seq', 5, true);


--
-- Name: viajes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: camiones
--

SELECT pg_catalog.setval('public.viajes_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: clientes clientes_cif_nif_key; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_cif_nif_key UNIQUE (cif_nif);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (id);


--
-- Name: conductores conductores_dni_key; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.conductores
    ADD CONSTRAINT conductores_dni_key UNIQUE (dni);


--
-- Name: conductores conductores_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.conductores
    ADD CONSTRAINT conductores_pkey PRIMARY KEY (id);


--
-- Name: detalles_pedido detalles_pedido_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.detalles_pedido
    ADD CONSTRAINT detalles_pedido_pkey PRIMARY KEY (id);


--
-- Name: facturas facturas_pedido_id_key; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_pedido_id_key UNIQUE (pedido_id);


--
-- Name: facturas facturas_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_pkey PRIMARY KEY (id);


--
-- Name: incidencias_viaje incidencias_viaje_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.incidencias_viaje
    ADD CONSTRAINT incidencias_viaje_pkey PRIMARY KEY (id);


--
-- Name: pedidos pedidos_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_pkey PRIMARY KEY (id);


--
-- Name: rutas rutas_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.rutas
    ADD CONSTRAINT rutas_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: vehiculos vehiculos_patente_key; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.vehiculos
    ADD CONSTRAINT vehiculos_patente_key UNIQUE (patente);


--
-- Name: vehiculos vehiculos_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.vehiculos
    ADD CONSTRAINT vehiculos_pkey PRIMARY KEY (id);


--
-- Name: viajes viajes_pkey; Type: CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.viajes
    ADD CONSTRAINT viajes_pkey PRIMARY KEY (id);


--
-- Name: detalles_pedido detalles_pedido_pedido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.detalles_pedido
    ADD CONSTRAINT detalles_pedido_pedido_id_fkey FOREIGN KEY (pedido_id) REFERENCES public.pedidos(id);


--
-- Name: facturas facturas_pedido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_pedido_id_fkey FOREIGN KEY (pedido_id) REFERENCES public.pedidos(id);


--
-- Name: incidencias_viaje incidencias_viaje_viaje_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.incidencias_viaje
    ADD CONSTRAINT incidencias_viaje_viaje_id_fkey FOREIGN KEY (viaje_id) REFERENCES public.viajes(id);


--
-- Name: pedidos pedidos_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.clientes(id);


--
-- Name: pedidos pedidos_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: viajes viajes_conductor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.viajes
    ADD CONSTRAINT viajes_conductor_id_fkey FOREIGN KEY (conductor_id) REFERENCES public.conductores(id);


--
-- Name: viajes viajes_pedido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.viajes
    ADD CONSTRAINT viajes_pedido_id_fkey FOREIGN KEY (pedido_id) REFERENCES public.pedidos(id);


--
-- Name: viajes viajes_ruta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.viajes
    ADD CONSTRAINT viajes_ruta_id_fkey FOREIGN KEY (ruta_id) REFERENCES public.rutas(id);


--
-- Name: viajes viajes_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.viajes
    ADD CONSTRAINT viajes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: viajes viajes_vehiculo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: camiones
--

ALTER TABLE ONLY public.viajes
    ADD CONSTRAINT viajes_vehiculo_id_fkey FOREIGN KEY (vehiculo_id) REFERENCES public.vehiculos(id);


--
-- PostgreSQL database dump complete
--

\unrestrict t4AnysKuYaphG5Rh0MyguUru0GRLgosvtEegNPZNbZQwQU0UJZUv7MNxTCBqzGy

