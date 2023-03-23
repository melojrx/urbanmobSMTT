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


CREATE SEQUENCE credencial.pessoa_seq
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

CREATE TABLE credencial.tb_pessoa_pes (
	id_pessoa_pes integer NOT NULL DEFAULT nextval('credencial.pessoa_seq'::regclass),
	txt_nome_pes varchar(50) NOT NULL,
  txt_cpf_pes varchar(11) NOT NULL,
  dat_nascimento_pes date NOT NULL,
	dat_inicio_pes timestamp without time zone NOT NULL,
	dat_fim_pes timestamp without time zone,
	CONSTRAINT pessoa_pkey PRIMARY KEY (id_pessoa_pes)
);

