-- ATENÇÃO! UTILIZAR O SEPARADOR INDICADO NA DOCUMENTAÇÃO ENTRE OS COMANDOS

--
--  1 - CRIA TABELA controle_migracao_registro
--
CREATE TABLE public.controle_migracao_registro
(
    sistema integer NOT NULL,
    tipo_registro text NOT NULL,
    hash_chave_dsk text NOT NULL UNIQUE,
    descricao_tipo_registro text NOT NULL,
    id_desktop integer,
    id_gerado integer,
    i_chave_dsk1 text NOT NULL,
    i_chave_dsk2 text,
    i_chave_dsk3 text,
    i_chave_dsk4 text,
    i_chave_dsk5 text,
    i_chave_dsk6 text,
    i_chave_dsk7 text,
    i_chave_dsk8 text,
    i_chave_dsk9 text,
    i_chave_dsk10 text,
    i_chave_dsk11 text,
    i_chave_dsk12 text,
    json_enviado text
);
--%/%

ALTER TABLE public.controle_migracao_registro
    OWNER to postgres;
--%/%
--
--  2 - CRIA TABELA controle_migracao_registro_ocor
--
CREATE TABLE public.controle_migracao_registro_ocor
(
    i_sequencial SERIAL,
    hash_chave_dsk text NOT NULL,
    sistema integer NOT NULL,
    tipo_registro text NOT NULL,
    id_gerado text,
    origem smallint NOT NULL,
    situacao smallint NOT NULL,
    resolvido smallint NOT NULL,
    i_sequencial_lote numeric,
    id_integracao text NOT NULL,
    mensagem_erro text,
    mensagem_ajuda text,
    json_enviado text,
    id_existente text
);
--%/%

ALTER TABLE public.controle_migracao_registro_ocor
    OWNER to postgres;
--%/%

--
--  3 - CRIA TABELA controle_migracao_lotes
--
CREATE TABLE public.controle_migracao_lotes
(
    i_sequencial SERIAL,
    sistema integer NOT NULL,
    tipo_registro text NOT NULL,
    data_hora_env timestamp without time zone NOT NULL,
    data_hora_ret timestamp without time zone,
    usuario text  NOT NULL,
    url_consulta text NOT NULL,
    Status smallint,
    id_lote text,
    conteudo_json text
);
--%/%

ALTER TABLE public.controle_migracao_lotes
    OWNER to postgres;
--%/%


--
--  5 - CRIA FUNCTION  bth_get_hash_chave_dsk
--
CREATE OR REPLACE FUNCTION bth_get_hash_chave
(
	arg_1 text,
	arg_2 text default null,
	arg_3 text default null,
	arg_4 text default null,
	arg_5 text default null,
	arg_6 text default null,
	arg_7 text default null,
	arg_8 text default null,
	arg_9 text default null,
	arg_10 text default null,
	arg_11 text default null,
	arg_12 text default null,
	arg_13 text default null,
	arg_14 text default null
)
RETURNS text LANGUAGE plpgsql AS $$
DECLARE
	w_separador text = '';
	w_chave text = '' ;
	w_vl_1 text = '';
	w_vl_2 text = '';
	w_vl_3 text = '';
	w_vl_4 text = '';
	w_vl_5 text = '';
	w_vl_6 text = '';
	w_vl_7 text = '';
	w_vl_8 text = '';
	w_vl_9 text = '';
	w_vl_10 text = '';
	w_vl_11 text = '';
	w_vl_12 text = '';
	w_vl_13 text = '';
	w_vl_14 text = '';
BEGIN
	IF arg_1 IS NULL THEN w_vl_1 := ''; ELSE w_vl_1 := CONCAT(arg_1, w_separador); END IF;
	IF arg_2 IS NULL THEN w_vl_2 := ''; ELSE w_vl_2 := CONCAT(arg_2, w_separador); END IF;
	IF arg_3 IS NULL THEN w_vl_3 := ''; ELSE w_vl_3 := CONCAT(arg_3, w_separador); END IF;
	IF arg_4 IS NULL THEN w_vl_4 := ''; ELSE w_vl_4 := CONCAT(arg_4, w_separador); END IF;
	IF arg_5 IS NULL THEN w_vl_5 := ''; ELSE w_vl_5 := CONCAT(arg_5, w_separador); END IF;
	IF arg_6 IS NULL THEN w_vl_6 := ''; ELSE w_vl_6 := CONCAT(arg_6, w_separador); END IF;
	IF arg_7 IS NULL THEN w_vl_7 := ''; ELSE w_vl_7 := CONCAT(arg_7, w_separador); END IF;
	IF arg_8 IS NULL THEN w_vl_8 := ''; ELSE w_vl_8 := CONCAT(arg_8, w_separador); END IF;
	IF arg_9 IS NULL THEN w_vl_9 := ''; ELSE w_vl_9 := CONCAT(arg_9, w_separador); END IF;
	IF arg_10 IS NULL THEN w_vl_10 := ''; ELSE w_vl_10 := CONCAT(arg_10, w_separador); END IF;
	IF arg_11 IS NULL THEN w_vl_11 := ''; ELSE w_vl_11 := CONCAT(arg_11, w_separador); END IF;
	IF arg_12 IS NULL THEN w_vl_12 := ''; ELSE w_vl_12 := CONCAT(arg_12, w_separador); END IF;
	IF arg_13 IS NULL THEN w_vl_13 := ''; ELSE w_vl_13 := CONCAT(arg_13, w_separador); END IF;
	IF arg_14 IS NULL THEN w_vl_14 := ''; ELSE w_vl_14 := CONCAT(arg_14, w_separador); END IF;
	w_chave := CONCAT(w_vl_1, w_vl_2, w_vl_3, w_vl_4, w_vl_5, w_vl_6, w_vl_7, w_vl_8,
					 w_vl_9, w_vl_10, w_vl_11, w_vl_12, w_vl_13, w_vl_14);
	return md5(w_chave);
END $$;
--%/%

--
--  6 - CRIA FUNCTION  bth_get_id_gerado
--
CREATE OR REPLACE FUNCTION bth_get_id_gerado
(
	arg_1 text,
	arg_2 text default '',
	arg_3 text default '',
	arg_4 text default '',
	arg_5 text default '',
	arg_6 text default '',
	arg_7 text default '',
	arg_8 text default '',
	arg_9 text default '',
	arg_10 text default '',
	arg_11 text default '',
	arg_12 text default '',
	arg_13 text default '',
	arg_14 text default ''
)
RETURNS integer LANGUAGE plpgsql AS $$
DECLARE
	id_cloud integer;
BEGIN
	SELECT id_gerado
	INTO id_cloud
	FROM controle_migracao_registro
	WHERE hash_chave_dsk = public.bth_get_hash_chave(arg_1, arg_2, arg_3, arg_4, arg_5, arg_6, arg_7, arg_8,arg_9,
	arg_10, arg_11, arg_12, arg_13, arg_14)
	LIMIT 1;

	RETURN id_cloud;
END $$;
--%/%

--
--  7 - CRIA FUNCTION  bth_get_id_gerado
--
CREATE OR REPLACE FUNCTION bth_get_situacao_registro
(
	arg_1 text,
	arg_2 text default '',
	arg_3 text default '',
	arg_4 text default '',
	arg_5 text default '',
	arg_6 text default '',
	arg_7 text default '',
	arg_8 text default '',
	arg_9 text default '',
	arg_10 text default '',
	arg_11 text default '',
	arg_12 text default '',
	arg_13 text default '',
	arg_14 text default ''
)
RETURNS integer LANGUAGE plpgsql AS $$
DECLARE
	ret_situacao integer;
	w_hash_chave_dsk text = '';
BEGIN
	w_hash_chave_dsk := public.bth_get_hash_chave(arg_1, arg_2, arg_3, arg_4, arg_5, arg_6, arg_7, arg_8,arg_9,
												  arg_10, arg_11, arg_12, arg_13, arg_14);

	IF EXISTS(SELECT id_gerado
			  FROM controle_migracao_registro
			  WHERE hash_chave_dsk = w_hash_chave_dsk
			  AND id_gerado IS NOT NULL)
	THEN
		ret_situacao := 4;
	ELSE
		SELECT
			CASE
				WHEN (situacao = 1 AND resolvido = 1) THEN 1
				WHEN (situacao = 4) THEN 2
				WHEN (situacao = 2 AND resolvido = 1) THEN 3
				ELSE 0
			END situacao
		FROM public.controle_migracao_registro_ocor
		INTO ret_situacao
	    WHERE hash_chave_dsk = w_hash_chave_dsk AND situacao IS NOT NULL;
	END IF;

	IF ret_situacao IS NULL THEN ret_situacao:= 0; END IF;

	RETURN ret_situacao;
END $$;
--%/%

--
--  8 - CRIA FUNCTION  dbf_valida_cpf
--
CREATE OR REPLACE FUNCTION dbf_valida_cpf(text)
    RETURNS text LANGUAGE plpgsql AS $$
DECLARE
	param_cpf VARCHAR := $1;
	digts VARCHAR[];
	tempp integer := 0;
	counter integer := 0;
	multi INTEGER := 10;
	verif1 INTEGER := 0;
	verif2 INTEGER := 0;
	counterfalse integer := 0;
	cnpj1 INTEGER[];
	cnpj2 INTEGER[];
BEGIN
	if(length(param_cpf) = 11) then
		digts := ('{'|| substring(param_cpf,1,1) ||', '|| substring(param_cpf,2,1) ||', '|| substring(param_cpf,3,1)
		||', '|| substring(param_cpf,4,1)  ||', '||  substring(param_cpf,5,1)      ||', '|| substring(param_cpf,6,1)
		||', '|| substring(param_cpf,7,1)  ||', '||  substring(param_cpf,8,1)      ||', '||  substring(param_cpf,9,1)
		||', '|| substring(param_cpf,10,1) ||', '||  substring(param_cpf,11,1)     ||'}');
		for counter IN 1..11 LOOP
			IF(digts[counter] = digts[1]) then
				counterfalse = counterfalse + 1;
			end if;
		end LOOP;
		if(counterfalse = 11) then
			 return null;
		else
			for counter IN 1..9 LOOP
				tempp := digts[counter];
				verif1 := verif1 + (tempp * multi);
				multi := multi - 1;
			END LOOP;
			verif1 := ((verif1  % 11));
			if(verif1 < 2) THEN
				verif1 := 0;
			ELSE
				verif1 := 11 - verif1;
			end if;
			multi := 11;
			for counter IN 1..10 LOOP
				tempp := digts[counter];
				verif2 := verif2 + (tempp * multi);
				multi := multi - 1;
			END LOOP;
			verif2 := ((verif2  % 11));
			if(verif2 < 2) THEN
				verif2 := 0;
			ELSE
				verif2 := 11 - verif2;
			end if;
		        if (verif1::varchar = substring(param_cpf,10,1)) AND (verif2::varchar = substring(param_cpf,11,1)) THEN
		        return $1;
		        ELSE
		        return null;
		        END IF;
		end if;
	elsif (length(param_cpf) = 14) THEN
		digts := ('{'|| substring(param_cpf,1,1) ||', '|| substring(param_cpf,2,1) ||', '|| substring(param_cpf,3,1)
		||', '|| substring(param_cpf,4,1)  ||', '||  substring(param_cpf,5,1)      ||', '|| substring(param_cpf,6,1)
		||', '|| substring(param_cpf,7,1)  ||', '||  substring(param_cpf,8,1)      ||', '|| substring(param_cpf,9,1)
		||', '|| substring(param_cpf,10,1) ||', '||  substring(param_cpf,11,1)     ||', '|| SUBSTRING(param_cpf,12,1)
		||', '||  substring(param_cpf,13,1)     ||', '|| SUBSTRING(param_cpf,14,1) ||'}');
		for counter IN 1..14 LOOP
			IF(digts[counter] = digts[1]) then
				counterfalse = counterfalse + 1;
			end if;
		end LOOP;
		if(counterfalse = 14) then
			return null;
		else
		cnpj1 := ('{'||5||','||4||','||3||','||2||','||9||','||8||','||7||','||6||','||5||','||4||','||3||','||2||'}');
		cnpj2 := ('{'||6||','||5||','||4||','||3||','||2||','||9||','||8||','||7||','||6||','||5||','||4||','||3||','||2||'}');
			for counter IN 1..12 LOOP
				tempp := digts[counter];
				verif1 := verif1 + (tempp * cnpj1[counter]);
			END LOOP;
			verif1 := ((verif1  % 11));
			if(verif1 < 2) THEN
				verif1 := 0;
			ELSE
				verif1 := 11 - verif1;
			end if;
			for counter IN 1..13 LOOP
				tempp := digts[counter];
				verif2 := verif2 + (tempp * cnpj2[counter]);
			END LOOP;
			verif2 := ((verif2  % 11));
			if(verif2 < 2) THEN
				verif2 := 0;
			ELSE
				verif2 := 11 - verif2;
			end if;
			if (verif1::varchar = substring(param_cpf,13,1)) AND (verif2::varchar = substring(param_cpf,14,1)) THEN
				return $1;
		        ELSE
		        return null;
		        END IF;
		end if;
	ELSE
		return null;
	END IF;
end $$;

--
--  9 - CRIA FUNCTION  dbf_valida_pis_pasep
--
CREATE OR REPLACE FUNCTION public.dbf_valida_pis_pasep(text)
 RETURNS text LANGUAGE plpgsql AS $$
declare
  pispasep varchar:=$1;
  peso varchar(10):='3298765432';
  total integer :=0;
  c integer := 1;
  resto integer:=0;
  resultado integer:=0;
  r varchar:=null;
  t integer:=0;
begin
  if(pispasep is null) then
    r=null;
    return(r);
  end if;
  if(select LENGTH(pispasep)) <> 11 then
    r=null;
    return(r);
  end if;
  if cast(pispasep as bigint) = 0 then
    r=null;
    return(r);
  end if;
  while(c <= 10) loop
    resultado=cast(SUBSTRING(pispasep,c,1) as bigint)*cast(SUBSTRING(peso,c,1) as bigint);
    total=total+resultado;
    c=c+1;
  end loop;
  resultado=(total/11);
  resto= 11 - mod(total,11);
  if(resto = 10 or resto = 11) then
    resto=0;
  end if;
  if(resto <> cast(SUBSTRING(pispasep,11,1) as bigint)) then
    r=null;
  else
    r=pispasep;
  end if;
  return(r);
end $$;

--ALTER FUNCTION public.dbf_valida_cpf() OWNER to postgres;