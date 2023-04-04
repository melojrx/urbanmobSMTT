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

CREATE SEQUENCE credencial.tipo_solicitacao_documento_seq
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
  txt_resolucao_tis varchar(50) NOT NULL,
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
  txt_documento_doc varchar(200) NOT NULL,
	dat_inicio_doc timestamp without time zone NOT null default now(),
	dat_fim_doc timestamp without time zone default null,
	CONSTRAINT documento_pkey PRIMARY KEY (id_documento_doc)
);

CREATE TABLE credencial.tb_tipo_solicitacao_documento_tsd (
	id_tipo_solicitacao_documento_tsd integer NOT NULL DEFAULT nextval('credencial.tipo_solicitacao_documento_seq'::regclass),
  id_tipo_solicitacao_tsd integer NOT NULL,
  id_documento_tsd integer NOT NULL,
	dat_inicio_tsd timestamp without time zone NOT null default now(),
	dat_fim_tsd timestamp without time zone default null,
	CONSTRAINT tipo_solicitacaodocumento_pkey PRIMARY KEY (id_tipo_solicitacao_documento_tsd)
);
ALTER TABLE credencial.tb_tipo_solicitacao_documento_tsd ADD CONSTRAINT tipo_solicitacao_fkey FOREIGN KEY (id_tipo_solicitacao_tsd) REFERENCES credencial.tb_tipo_solicitacao_tis (id_tipo_solicitacao_tis);
ALTER TABLE credencial.tb_tipo_solicitacao_documento_tsd ADD CONSTRAINT documento_fkey FOREIGN KEY (id_documento_tsd) REFERENCES credencial.tb_documento_doc (id_documento_doc);

CREATE TABLE credencial.tb_solicitacao_sol (
	id_solicitacao_sol integer NOT NULL DEFAULT nextval('credencial.solicitacao_seq'::regclass),
  id_tipo_solicitacao_sol integer NOT NULL,
	txt_protocolo_sol varchar(50) NOT NULL,
  txt_cpf_sol varchar(11) NOT NULL,
  txt_nome_sol varchar(200) NOT NULL,
  txt_email_sol varchar(50) NOT NULL,
  txt_endereco_sol varchar(200) NOT NULL,
  txt_whatsapp_sol varchar(15) NOT NULL,
	CONSTRAINT solicitacao_pkey PRIMARY KEY (id_solicitacao_sol)
);
ALTER TABLE credencial.tb_solicitacao_sol ADD CONSTRAINT tipo_solicitacao_fkey FOREIGN KEY (id_tipo_solicitacao_sol) REFERENCES credencial.tb_tipo_solicitacao_tis (id_tipo_solicitacao_tis);

CREATE TABLE credencial.tb_solicitacao_documento_sdo (
	id_solicitacao_documento_sdo integer NOT NULL DEFAULT nextval('credencial.solicitacao_documento_seq'::regclass),
  id_solicitacao_sdo integer NOT NULL,
  id_documento_sdo integer NOT NULL,
  img_file_sdo bytea NOT NULL,
  txt_contenttype_sdo varchar(50) NOT NULL,
  txt_filename_sdo varchar(50) NOT NULL,
  flg_deferido_sdo boolean default null,
	dat_inicio_sdo timestamp without time zone NOT null default now(),
	dat_fim_sdo timestamp without time zone default null,
	CONSTRAINT solicitacao_documento_pkey PRIMARY KEY (id_solicitacao_documento_sdo)
);
ALTER TABLE credencial.tb_solicitacao_documento_sdo ADD CONSTRAINT solicitacao_fkey FOREIGN KEY (id_solicitacao_sdo) REFERENCES credencial.tb_solicitacao_sol (id_solicitacao_sol);
ALTER TABLE credencial.tb_solicitacao_documento_sdo ADD CONSTRAINT documento_fkey FOREIGN KEY (id_documento_sdo) REFERENCES credencial.tb_documento_doc (id_documento_doc);

CREATE TABLE credencial.tb_solicitacao_historico_shi (
	id_solicitacao_historico_shi integer NOT NULL DEFAULT nextval('credencial.solicitacao_historico_seq'::regclass),
  id_solicitacao_shi integer NOT NULL,
  id_status_shi integer NOT NULL,
  id_usuario_shi integer,
  txt_observacao_shi varchar(500),
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

INSERT INTO credencial.tb_usuario_usu (txt_nome_usu, txt_email_usu, txt_cpf_usu) VALUES('SMTT', 'usergoverno@urbanmob.com', '1111111111');

INSERT INTO credencial.tb_status_sta (id_status_sta, txt_status_sta, dat_inicio_sta, dat_fim_sta) VALUES(1,'Aguardando Atendimento', now(), null);
INSERT INTO credencial.tb_status_sta (id_status_sta, txt_status_sta, dat_inicio_sta, dat_fim_sta) VALUES(2,'Em andamento', now(), null);
INSERT INTO credencial.tb_status_sta (id_status_sta, txt_status_sta, dat_inicio_sta, dat_fim_sta) VALUES(3,'Deferido', now(), null);
INSERT INTO credencial.tb_status_sta (id_status_sta, txt_status_sta, dat_inicio_sta, dat_fim_sta) VALUES(4,'Indeferido', now(), null);
INSERT INTO credencial.tb_status_sta (id_status_sta, txt_status_sta, dat_inicio_sta, dat_fim_sta) VALUES(5,'Finalizado', now(), null);
INSERT INTO credencial.tb_status_sta (id_status_sta, txt_status_sta, dat_inicio_sta, dat_fim_sta) VALUES(6,'Reenviado', now(), null);
SELECT setval('credencial.status_seq', 6);

INSERT INTO credencial.tb_tipo_solicitacao_tis (id_tipo_solicitacao_tis, txt_tipo_solicitacao_tis, txt_icone_tis, txt_resolucao_tis, dat_inicio_tis, dat_fim_tis) VALUES(1, 'Deficiente', 'bi bi-person-square', 'CONFORME RESOLUÇÃO Nº 304/08 DO CONTRAN' , now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_tis (id_tipo_solicitacao_tis, txt_tipo_solicitacao_tis, txt_icone_tis, txt_resolucao_tis, dat_inicio_tis, dat_fim_tis) VALUES(2, 'Idoso', 'bi bi-person-plus-fill', 'CONFORME RESOLUÇÃO Nº 303/08 DO CONTRAN', now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_tis (id_tipo_solicitacao_tis, txt_tipo_solicitacao_tis, txt_icone_tis, txt_resolucao_tis, dat_inicio_tis, dat_fim_tis) VALUES(3, 'ônibus', 'bi bi-bus-front-fill', 'CONFORME RESOLUÇÃO Nº 303/08 DO CONTRAN', now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_tis (id_tipo_solicitacao_tis, txt_tipo_solicitacao_tis, txt_icone_tis, txt_resolucao_tis, dat_inicio_tis, dat_fim_tis) VALUES(4, 'Táxi', 'bi bi-taxi-front-fill', 'CONFORME RESOLUÇÃO Nº 303/08 DO CONTRAN', now(), null);
SELECT setval('credencial.tipo_solicitacao_seq', 4);

INSERT INTO credencial.tb_documento_doc(id_documento_doc, txt_documento_doc, dat_inicio_doc, dat_fim_doc) VALUES(1, 'RG', now(), null);
INSERT INTO credencial.tb_documento_doc(id_documento_doc, txt_documento_doc, dat_inicio_doc, dat_fim_doc) VALUES(2, 'CPF', now(), null);
SELECT setval('credencial.documento_seq', 2);

INSERT INTO credencial.tb_tipo_solicitacao_documento_tsd (id_tipo_solicitacao_documento_tsd, id_tipo_solicitacao_tsd, id_documento_tsd, dat_inicio_tsd, dat_fim_tsd) VALUES(1, 1, 1, now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_documento_tsd (id_tipo_solicitacao_documento_tsd, id_tipo_solicitacao_tsd, id_documento_tsd, dat_inicio_tsd, dat_fim_tsd) VALUES(2, 1, 2, now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_documento_tsd (id_tipo_solicitacao_documento_tsd, id_tipo_solicitacao_tsd, id_documento_tsd, dat_inicio_tsd, dat_fim_tsd) VALUES(3, 2, 1, now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_documento_tsd (id_tipo_solicitacao_documento_tsd, id_tipo_solicitacao_tsd, id_documento_tsd, dat_inicio_tsd, dat_fim_tsd) VALUES(4, 2, 2, now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_documento_tsd (id_tipo_solicitacao_documento_tsd, id_tipo_solicitacao_tsd, id_documento_tsd, dat_inicio_tsd, dat_fim_tsd) VALUES(5, 3, 1, now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_documento_tsd (id_tipo_solicitacao_documento_tsd, id_tipo_solicitacao_tsd, id_documento_tsd, dat_inicio_tsd, dat_fim_tsd) VALUES(6, 3, 2, now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_documento_tsd (id_tipo_solicitacao_documento_tsd, id_tipo_solicitacao_tsd, id_documento_tsd, dat_inicio_tsd, dat_fim_tsd) VALUES(7, 4, 1, now(), null);
INSERT INTO credencial.tb_tipo_solicitacao_documento_tsd (id_tipo_solicitacao_documento_tsd, id_tipo_solicitacao_tsd, id_documento_tsd, dat_inicio_tsd, dat_fim_tsd) VALUES(8, 4, 2, now(), null);
SELECT setval('credencial.tipo_solicitacao_documento_seq', 8);