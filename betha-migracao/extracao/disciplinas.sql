select
	*
from (
	select
		(select id_gerado from public.controle_migracao_registro where hash_chave_dsk = md5(concat(sistema,tipo_registro,descricao)) limit 1) as id_gerado,
		*
	from (
		select
			'1' as sistema,
			'disciplinas' as tipo_registro,
			iddis as id_desktop,
			trim(left(upper(replace(longdesc,'  ',' ')),60)) as descricao,
			(
				select
					case when s3.linha = 1 then s3.sigla else (left(s3.sigla,4) || s3.linha) end as sigla
				from (
						select
							row_number() OVER (partition by s2.sigla) as linha,
							s2.sigla,
							s2.iddis
						from (
								select
							 		left(string_agg(left(s1.sigla, 1) || right(s1.sigla, 1), ''),5) sigla,
							 		s1.iddis
								from (
										select
											tt13.iddis,
								    		tt13.longdesc,
								    		unnest(string_to_array(regexp_replace(trim(tt13.longdesc), '[^a-zA-Z ]', '', 'g'),' ')) sigla
									    from
									    	public.pdis as tt13
									) s1
								group by s1.longdesc,s1.iddis
						) s2
				) s3
				where s3.iddis = t13.iddis
			) as sigla,
--			abreviatura as  sigla,
			case
				when upper(longdesc) ~ 'BIOLO' then 'Ciências da Natureza - Biologia'
				when upper(longdesc) ~ 'NCIA' then 'Ciências da Natureza - Ciências'
				when upper(longdesc) ~ '^(?!E).+SICA' then 'Ciências da Natureza - Física'
				when upper(longdesc) ~ 'MICA' then 'Ciências da Natureza - Química'
				when upper(longdesc) ~ 'SOCIA' then 'Ciências Humanas e Sociais - Estudos Sociais'
				when upper(longdesc) ~ 'FILOSOFI' then 'Ciências Humanas e Sociais - Filosofia'
				when upper(longdesc) ~ 'GEOGRA' then 'Ciências Humanas e Sociais - Geografia'
				when upper(longdesc) ~ 'HIST' then 'Ciências Humanas e Sociais - História'
				when upper(longdesc) ~ 'SOCIOLO' then 'Ciências Humanas e Sociais - Sociologia'
				when upper(longdesc) ~ 'ART' then 'Linguagens - Arte (Educação Artística, Teatro, Dança, Música, Artes Plásticas e outras)'
				when upper(longdesc) ~ '^EDUCA+.+SICA$' then 'Linguagens - Educação Física'
				when upper(longdesc) ~ 'LIBRA' then 'Linguagens - Libras'
				when upper(longdesc) ~ 'IND' then 'Linguagens - Lingua indígena'
				when upper(longdesc) ~ 'ESPANH' then 'Linguagens - Língua /Literatura estrangeira - Espanhol'
				when upper(longdesc) ~ 'FRANC' then 'Linguagens - Língua/Literatura estrangeira - Francês'
				when upper(longdesc) ~ 'INGLE' then 'Linguagens - Língua /Literatura estrangeira - Inglês'
				when upper(longdesc) ~ 'OUTRA' then 'Linguagens - Língua /Literatura estrangeira - outra'
				when upper(longdesc) ~ 'PORTUG+.+SEGU' then 'Linguagens - Língua Portuguesa como Segunda Língua'
				when upper(longdesc) ~ 'PORTUG' then 'Linguagens - Língua /Literatura Portuguesa'
				when upper(longdesc) ~ 'MATE' then 'Matemática - Matemática'
				when upper(longdesc) ~ 'PEDAG' then 'Outras áreas - Áreas do conhecimento pedagógicas'
				when upper(longdesc) ~ 'PROFISS' then 'Outras áreas - Áreas do conhecimento profissionalizantes'
				when upper(longdesc) ~ 'SOCIOCUL' then 'Outras áreas - Disciplinas voltadas à diversidade sociocultural (disciplinas pedagógicas)'
				when upper(longdesc) ~ 'INCLUS' then 'Outras áreas - Disciplinas voltadas ao atendimento às necessidades educacionais específicas dos alunos que são público alvo da educação especial e às práticas educacionais inclusivas.'
				when upper(longdesc) ~ 'RELIG' then 'Outras áreas - Ensino religioso'
				when upper(longdesc) ~ 'EST' then 'Outras áreas - Estágio curricular supervisionado'
				when upper(longdesc) ~ '(INF|COMP|TECNO)' then 'Outras áreas - Informática/Computação'
				else 'Outras áreas - Outras áreas do conhecimento'
			end as inepDescricao,
			case
				when upper(longdesc) ~ 'BIOLO' then 4
				when upper(longdesc) ~ 'NCIA' then 5
				when upper(longdesc) ~ '^(?!E).+SICA' then 2
				when upper(longdesc) ~ 'MICA' then 1
				when upper(longdesc) ~ 'SOCIA' then 16
				when upper(longdesc) ~ 'FILOSOFI' then 22
				when upper(longdesc) ~ 'GEOGRA' then 21
				when upper(longdesc) ~ 'HIST' then 20
				when upper(longdesc) ~ 'SOCIOLO' then 17
				when upper(longdesc) ~ 'ART' then 10
				when upper(longdesc) ~ '^EDUCA+.+SICA$' then 19
				when upper(longdesc) ~ 'LIBRA' then 11
				when upper(longdesc) ~ 'IND' then 14
				when upper(longdesc) ~ 'ESPANH' then 8
				when upper(longdesc) ~ 'FRANC' then 18
				when upper(longdesc) ~ 'INGLE' then 7
				when upper(longdesc) ~ 'OUTRA' then 9
				when upper(longdesc) ~ 'PORTUG' then 6
				when upper(longdesc) ~ 'PORTUG+.+SEGU' then 28
				when upper(longdesc) ~ 'MATE' then 3
				when upper(longdesc) ~ 'PEDAG' then 12
				when upper(longdesc) ~ 'PROFISS' then 24
				when upper(longdesc) ~ 'SOCIOCUL' then 26
				when upper(longdesc) ~ 'INCLUS' then 25
				when upper(longdesc) ~ 'RELIG' then 13
				when upper(longdesc) ~ 'EST' then 29
				when upper(longdesc) ~ '(INF|COMP|TECNO)' then 23
				else 27
			end as inep
		FROM
			public.pdis as t13
	) as consulta
) as consulta
where id_gerado is null