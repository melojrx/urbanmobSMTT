-- ################
-- #    SCHEMA    #
-- ################

CREATE SCHEMA cidade;

-- ################
-- #  SEQUENCES   #
-- ################

CREATE SEQUENCE cidade.usuario_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;


CREATE SEQUENCE cidade.categoria_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cidade.subcategoria_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  
  CREATE SEQUENCE cidade.evento_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cidade.evento_historico_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cidade.status_evento_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cidade.evento_observacao_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

-- ################
-- #    TABLES    #
-- ################

CREATE TABLE cidade.tb_usuario_usu (
	id_usuario_usu integer NOT NULL DEFAULT nextval('cidade.usuario_seq'::regclass),
	txt_nome_usu varchar(200) NOT NULL,
	txt_email_usu varchar(200) NOT NULL,
  txt_cpf_usu varchar(11) NOT NULL,
	CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario_usu)
);

CREATE TABLE cidade.tb_categoria_cat (
	id_categoria_cat integer NOT NULL DEFAULT nextval('cidade.categoria_seq'::regclass),
	txt_categoria_cat varchar(50) NOT NULL,
	dat_inicio_cat timestamp without time zone NOT NULL,
	dat_fim_cat timestamp without time zone,
	CONSTRAINT categoria_pkey PRIMARY KEY (id_categoria_cat)
);

CREATE TABLE cidade.tb_status_evento_sev (
	id_status_evento_sev integer NOT NULL DEFAULT nextval('cidade.status_evento_seq'::regclass),
	txt_status_evento_sev varchar(50) NOT NULL,
	dat_inicio_sev timestamp without time zone NOT NULL,
	dat_fim_sev timestamp without time zone,
	CONSTRAINT status_evento_pkey PRIMARY KEY (id_status_evento_sev)
);

CREATE TABLE cidade.tb_subcategoria_sub (
	id_subcategoria_sub integer NOT NULL DEFAULT nextval('cidade.subcategoria_seq'::regclass),
  id_categoria_sub integer NOT NULL,
	txt_subcategoria_sub varchar(50) NOT NULL,
	dat_inicio_sub timestamp without time zone NOT NULL,
	dat_fim_sub timestamp without time zone,
	CONSTRAINT subcategoria_pkey PRIMARY KEY (id_subcategoria_sub)
);
ALTER TABLE cidade.tb_subcategoria_sub ADD CONSTRAINT categoria_fkey FOREIGN KEY (id_categoria_sub) REFERENCES cidade.tb_categoria_cat (id_categoria_cat);

CREATE TABLE cidade.tb_evento_eve (
	id_evento_eve integer NOT NULL DEFAULT nextval('cidade.evento_seq'::regclass),
  id_subcategoria_eve integer NOT NULL,
  id_usuario_eve integer NOT NULL,
  num_ocorrencia_eve varchar(15) NOT NULL,
	txt_problema_eve varchar(1000) NOT NULL,
  txt_endereco_eve varchar(1000) NOT NULL,
  txt_latitude_eve varchar(20) NOT NULL,
  txt_longitude_eve varchar(20) NOT NULL,
  img_file_eve bytea NOT NULL,
	dat_inicio_eve timestamp without time zone NOT null default now(),
	dat_fim_eve timestamp without time zone default null,
	CONSTRAINT evento_pkey PRIMARY KEY (id_evento_eve)
);
ALTER TABLE cidade.tb_evento_eve ADD CONSTRAINT subcategoria_fkey FOREIGN KEY (id_subcategoria_eve) REFERENCES cidade.tb_subcategoria_sub (id_subcategoria_sub);
ALTER TABLE cidade.tb_evento_eve ADD CONSTRAINT usuario_fkey FOREIGN KEY (id_usuario_eve) REFERENCES cidade.tb_usuario_usu (id_usuario_usu);

CREATE TABLE cidade.tb_evento_historico_ehi (
	id_evento_historico_ehi integer NOT NULL DEFAULT nextval('cidade.evento_historico_seq'::regclass),
  id_evento_ehi integer NOT NULL,
	id_status_evento_ehi integer NOT NULL,
  id_usuario_ehi integer NOT NULL,
	dat_inicio_ehi timestamp without time zone NOT null default now(),
	dat_fim_ehi timestamp without time zone default null,
	CONSTRAINT evento_historico_pkey PRIMARY KEY (id_evento_historico_ehi)
);
ALTER TABLE cidade.tb_evento_historico_ehi ADD CONSTRAINT evento_fkey FOREIGN KEY (id_evento_ehi) REFERENCES cidade.tb_evento_eve (id_evento_eve);
ALTER TABLE cidade.tb_evento_historico_ehi ADD CONSTRAINT status_fkey FOREIGN KEY (id_status_evento_ehi) REFERENCES cidade.tb_status_evento_sev (id_status_evento_sev);
ALTER TABLE cidade.tb_evento_historico_ehi ADD CONSTRAINT usuario_fkey FOREIGN KEY (id_usuario_ehi) REFERENCES cidade.tb_usuario_usu (id_usuario_usu);

CREATE TABLE cidade.tb_evento_observacao_eob (
	id_evento_observacao_eob integer NOT NULL DEFAULT nextval('cidade.evento_observacao_seq'::regclass),
  id_evento_historico_eob integer NOT NULL,
  id_usuario_eob integer NOT NULL,
	txt_evento_observacao_eob varchar(500) NOT NULL,
	dat_inicio_eob timestamp without time zone NOT NULL,
	dat_fim_eob timestamp without time zone,
	CONSTRAINT evento_observacao_pkey PRIMARY KEY (id_evento_observacao_eob)
);
ALTER TABLE cidade.tb_evento_observacao_eob ADD CONSTRAINT evento_observacao_fkey FOREIGN KEY (id_evento_historico_eob) REFERENCES cidade.tb_evento_historico_ehi (id_evento_historico_ehi);
ALTER TABLE cidade.tb_evento_observacao_eob ADD CONSTRAINT usuario_observacao_fkey FOREIGN KEY (id_usuario_eob) REFERENCES cidade.tb_usuario_usu (id_usuario_usu);

-- ####################################
-- #        INSERTS PARA TESTES       #
-- ####################################

--INSERT INTO cidade.tb_usuario_usu
--(txt_nome_usu, txt_email_usu, txt_cpf_usu, txt_password_usu, flg_governo_usu, flg_admin_usu)
--VALUES('Usuário', 'usuario@gmail.com', '11111111111','pbkdf2:sha256:260000$FUnuJtPVxUVIAbbO$14563e437e0e8c2c603fa509bd6f0c0461bb1cf62beba90aae238f07539f70d4', NULL, NULL);

--INSERT INTO cidade.tb_usuario_usu
--(txt_nome_usu, txt_email_usu, txt_cpf_usu, txt_password_usu, flg_governo_usu, flg_admin_usu)
--VALUES('admin', 'admin@gmail.com', '22222222222','pbkdf2:sha256:260000$JQwgcuStn5qtjS3f$953618c6e160f2efa171d1467897752561cd3d6c294aac521d046c195e8e47de', NULL, true);

--INSERT INTO cidade.tb_usuario_usu
--(txt_nome_usu, txt_email_usu, txt_cpf_usu, txt_password_usu, flg_governo_usu, flg_admin_usu)
--VALUES('Governo', 'governo@gmail.com', '33333333333','pbkdf2:sha256:260000$vBlSzVoaRjC9MwlR$30b687a8d23140c53ecc80aa6523c3abff23eb45652daa5b369918a5368fefa8', true, true);


INSERT INTO cidade.tb_categoria_cat(txt_categoria_cat, dat_inicio_cat, dat_fim_cat)VALUES('Urbanismo', now(), null);
INSERT INTO cidade.tb_categoria_cat(txt_categoria_cat, dat_inicio_cat, dat_fim_cat)VALUES('Paisagismo', now(), null);
INSERT INTO cidade.tb_categoria_cat(txt_categoria_cat,dat_inicio_cat,dat_fim_cat) VALUES ('Transporte',now(),null);

INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(1, 'Buraco', now(), null);
INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(1, 'Calçada Irregular', 'now()', null);

INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(2, 'Pixações', now(), null);
INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(2, 'Placas de Publicidade', 'now()', null);

INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(3, 'Abrigo de ônibus', now(), null);
INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(3, 'Cadeira Quebrada', now(), null);
INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(3, 'Ônibus Lotado', now(), null);
INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(3, 'Limpeza do ônibus', now(), null);
INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(3, 'Teto Quebrado', now(), null);
INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(3, 'Wifi sem Funcionar', now(), null);
INSERT INTO cidade.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(3, 'Ar-condicionado Quebrado', now(), null);

INSERT INTO cidade.tb_status_evento_sev (txt_status_evento_sev, dat_inicio_sev, dat_fim_sev) VALUES('Aguardando Atendimento', now(), null);
INSERT INTO cidade.tb_status_evento_sev (txt_status_evento_sev, dat_inicio_sev, dat_fim_sev) VALUES('Em andamento', now(), null);
INSERT INTO cidade.tb_status_evento_sev (txt_status_evento_sev, dat_inicio_sev, dat_fim_sev) VALUES('Finalizado', now(), null);
