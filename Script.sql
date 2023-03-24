-- ################
-- #    SCHEMA    #
-- ################

CREATE SCHEMA credencial;

-- ################
-- #  SEQUENCES   #
-- ################

CREATE SEQUENCE credencial.usuario_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;


--CREATE SEQUENCE credencial.pessoa_seq
--  INCREMENT 1
--  MINVALUE 1
--  MAXVALUE 9223372036854775807
--  START 1
--  CACHE 1;

CREATE SEQUENCE credencial.tipo_solicitacao_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

CREATE SEQUENCE credencial.status_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

CREATE SEQUENCE credencial.documento_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

CREATE SEQUENCE credencial.solicitacao_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

CREATE SEQUENCE credencial.solicitacao_documento_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

CREATE SEQUENCE credencial.solicitacao_historico_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  -- ################
-- #    TABLES    #
-- ################

CREATE TABLE credencial.tb_usuario_usu (
	id_usuario_usu integer NOT NULL DEFAULT nextval('credencial.usuario_seq'::regclass),
	txt_nome_usu varchar(200) NOT NULL,
	txt_email_usu varchar(200) NOT NULL,
  txt_cpf_usu varchar(11) NOT NULL,
	CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario_usu)
);

--CREATE TABLE credencial.tb_pessoa_pes (
--	id_pessoa_pes integer NOT NULL DEFAULT nextval('credencial.pessoa_seq'::regclass),
--	txt_nome_pes varchar(50) NOT NULL,
--  txt_cpf_pes varchar(11) NOT NULL,
--  dat_nascimento_pes date NOT NULL,
--	dat_inicio_pes timestamp without time zone NOT NULL,
--	dat_fim_pes timestamp without time zone,
--	CONSTRAINT pessoa_pkey PRIMARY KEY (id_pessoa_pes)
--);

CREATE TABLE credencial.tb_tipo_solicitacao_tis (
	id_tipo_solicitacao_tis integer NOT NULL DEFAULT nextval('credencial.tipo_solicitacao_seq'::regclass),
	txt_tipo_solicitacao_tis varchar(200) NOT NULL,
  txt_icone_tis varchar(50) NOT NULL,
	dat_inicio_tis timestamp without time zone NOT null default now(),
	dat_fim_tis timestamp without time zone default null,
	CONSTRAINT tipo_solicitacao_pkey PRIMARY KEY (id_tipo_solicitacao_tis)
);

CREATE TABLE credencial.tb_status_sta (
	id_status_sta integer NOT NULL DEFAULT nextval('credencial.status_seq'::regclass),
	txt_status_sta varchar(200) NOT NULL,
	dat_inicio_sta timestamp without time zone NOT null default now(),
	dat_fim_sta timestamp without time zone default null,
	CONSTRAINT status_pkey PRIMARY KEY (id_status_sta)
);

CREATE TABLE credencial.tb_documento_doc (
	id_documento_doc integer NOT NULL DEFAULT nextval('credencial.documento_seq'::regclass),
  id_tipo_solicitacao_doc integer NOT NULL,
  txt_documento_doc varchar(200) NOT NULL,
	dat_inicio_doc timestamp without time zone NOT null default now(),
	dat_fim_doc timestamp without time zone default null,
	CONSTRAINT documento_pkey PRIMARY KEY (id_documento_doc)
);
ALTER TABLE credencial.tb_documento_doc ADD CONSTRAINT tipo_solicitacao_fkey FOREIGN KEY (id_tipo_solicitacao_doc) REFERENCES credencial.tb_tipo_solicitacao_tis (id_tipo_solicitacao_tis);

CREATE TABLE credencial.tb_solicitacao_sol (
	id_solicitacao_sol integer NOT NULL DEFAULT nextval('credencial.solicitacao_seq'::regclass),
  id_tipo_solicitacao_sol integer NOT NULL,
	txt_protocolo_sol varchar(50) NOT NULL,
	CONSTRAINT solicitacao_pkey PRIMARY KEY (id_solicitacao_sol)
);
ALTER TABLE credencial.tb_solicitacao_sol ADD CONSTRAINT tipo_solicitacao_fkey FOREIGN KEY (id_tipo_solicitacao_sol) REFERENCES credencial.tb_tipo_solicitacao_tis (id_tipo_solicitacao_tis);

CREATE TABLE credencial.tb_solicitacao_documento_sdo (
	id_solicitacao_documento_sdo integer NOT NULL DEFAULT nextval('credencial.solicitacao_documento_seq'::regclass),
  id_solicitacao_sdo integer NOT NULL,
  img_file_sdo bytea NOT NULL,
	dat_inicio_sdo timestamp without time zone NOT null default now(),
	dat_fim_sdo timestamp without time zone default null,
	CONSTRAINT solicitacao_documento_pkey PRIMARY KEY (id_solicitacao_documento_sdo)
);
ALTER TABLE credencial.tb_solicitacao_documento_sdo ADD CONSTRAINT solicitacao_fkey FOREIGN KEY (id_solicitacao_sdo) REFERENCES credencial.tb_solicitacao_sol (id_solicitacao_sol);

CREATE TABLE credencial.tb_solicitacao_historico_shi (
	id_solicitacao_historico_shi integer NOT NULL DEFAULT nextval('credencial.solicitacao_historico_seq'::regclass),
  id_solicitacao_shi integer NOT NULL,
  id_status_shi integer NOT NULL,
  id_usuario_shi integer NOT NULL,
  txt_observacao_shi varchar(500) NOT NULL,
	dat_inicio_shi timestamp without time zone NOT null default now(),
	dat_fim_shi timestamp without time zone default null,
	CONSTRAINT solicitacao_historico_pkey PRIMARY KEY (id_solicitacao_historico_shi)
);
ALTER TABLE credencial.tb_solicitacao_historico_shi ADD CONSTRAINT solicitacao_fkey FOREIGN KEY (id_solicitacao_shi) REFERENCES credencial.tb_solicitacao_sol (id_solicitacao_sol);
ALTER TABLE credencial.tb_solicitacao_historico_shi ADD CONSTRAINT status_fkey FOREIGN KEY (id_status_shi) REFERENCES credencial.tb_status_sta (id_status_sta);
ALTER TABLE credencial.tb_solicitacao_historico_shi ADD CONSTRAINT usuario_fkey FOREIGN KEY (id_usuario_shi) REFERENCES credencial.tb_usuario_usu (id_usuario_usu);


-- ####################################
-- #        INSERTS PARA TESTES       #
-- ####################################

INSERT INTO credencial.tb_status_sta (txt_status_sta, dat_inicio_sta, dat_fim_sta) VALUES('Aguardando Atendimento', now(), null);
INSERT INTO credencial.tb_status_sta (txt_status_sta, dat_inicio_sta, dat_fim_sta) VALUES('Em andamento', now(), null);
INSERT INTO credencial.tb_status_sta (txt_status_sta, dat_inicio_sta, dat_fim_sta) VALUES('Finalizado', now(), null);

INSERT INTO credencial.tb_tipo_solicitacao_tis (txt_tipo_solicitacao_tis, txt_icone_tis, dat_inicio_tis, dat_fim_tis) VALUES('Deficiente', 'bi bi-person-plus-fill', now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_tis (txt_tipo_solicitacao_tis, txt_icone_tis, dat_inicio_tis, dat_fim_tis) VALUES('Idoso', 'bi bi-person-plus-fill', now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_tis (txt_tipo_solicitacao_tis, txt_icone_tis, dat_inicio_tis, dat_fim_tis) VALUES('ônibus', 'bi bi-bus-front-fill', now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_tis (txt_tipo_solicitacao_tis, txt_icone_tis, dat_inicio_tis, dat_fim_tis) VALUES('Táxi', 'bi bi-taxi-front-fill', now(), null);

INSERT INTO credencial.tb_documento_doc(id_tipo_solicitacao_doc, txt_documento_doc, dat_inicio_doc, dat_fim_doc) VALUES(1, 'RG', now(), null);
INSERT INTO credencial.tb_documento_doc(id_tipo_solicitacao_doc, txt_documento_doc, dat_inicio_doc, dat_fim_doc) VALUES(2, 'RG', now(), null);
INSERT INTO credencial.tb_documento_doc(id_tipo_solicitacao_doc, txt_documento_doc, dat_inicio_doc, dat_fim_doc) VALUES(3, 'RG', now(), null);
INSERT INTO credencial.tb_documento_doc(id_tipo_solicitacao_doc, txt_documento_doc, dat_inicio_doc, dat_fim_doc) VALUES(4, 'RG', now(), null);
