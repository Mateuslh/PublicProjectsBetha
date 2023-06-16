SELECT top 1

		(SELECT id_gerado from bethadba.controle_migracao_registro cmr WHERE  cmr.tipo_registro= tipo_registro2 and cmr.i_chave_dsk1 = id_desktop and cmr.i_chave_dsk2 = (dt_alteracoes+'000')) as id_gerado,
		 i_imoveis,
         cast(dt_alteracoes as varchar) as dt_alteracoes,
         i_usuarios,
         i_campos,
         tipo,
         '335' as sistema,
         'auditoria-imoveis' as tipo_registro2,
         cast(i_imoveis as varchar) as id_desktop,
         valor_antigo = (IF i_campos = 'i_pessoas' THEN
                 (SELECT string(vw_nome_pessoas.i_pessoas, ' ', vw_nome_pessoas.nome ) FROM bethadba.vw_nome_pessoas WHERE vw_nome_pessoas.i_pessoas = auditoria_imoveis.valor_antigo )
                             ELSE
                                    auditoria_imoveis.valor_antigo
                            ENDIF),
         valor_novo   =  (IF i_campos = 'i_pessoas' THEN
                                    (SELECT string(vw_nome_pessoas.i_pessoas, ' ', vw_nome_pessoas.nome ) FROM bethadba.vw_nome_pessoas WHERE vw_nome_pessoas.i_pessoas = auditoria_imoveis.valor_novo )
                             ELSE
                                    auditoria_imoveis.valor_novo
                            ENDIF),
         processo,
         desc_campo = (IF i_campos = 'campo1' THEN
                                (SELECT campo1 FROM bethadba.config_imovel)
                            ELSE IF i_campos = 'campo2' THEN
                                (SELECT campo2 FROM bethadba.config_imovel)
                            ELSE IF i_campos = 'campo3' THEN
                                (SELECT campo3 FROM bethadba.config_imovel)
                            ELSE IF i_campos = 'campo4' THEN
                                (SELECT campo4 FROM bethadba.config_imovel)
                            ELSE IF i_campos = 'campo5' THEN
                                (SELECT campo5 FROM bethadba.config_imovel)
                            ELSE IF i_campos = 'campo6' THEN
                                (SELECT campo6 FROM bethadba.config_imovel)
                            ELSE IF i_campos = 'campo7' THEN
                                (SELECT campo7 FROM bethadba.config_imovel)
                            ELSE
                                (SELECT remarks FROM sys.syscolumns WHERE creator = 'bethadba' AND tname = 'imoveis' AND cname = i_campos AND cname <> 'i_imoveis')
                            ENDIF ENDIF ENDIF ENDIF ENDIF ENDIF ENDIF),
         insc_imo=bethadba.dbf_inscricao(auditoria_imoveis.i_imoveis,0),
         (SELECT imoveis.i_pessoas FROM bethadba.imoveis WHERE imoveis.i_imoveis = auditoria_imoveis.i_imoveis),
         contrib = (SELECT nome FROM bethadba.pessoas WHERE pessoas.i_pessoas = (SELECT imoveis.i_pessoas FROM bethadba.imoveis WHERE imoveis.i_imoveis = auditoria_imoveis.i_imoveis))
  FROM bethadba.auditoria_imoveis
 WHERE i_campos <> 'i_imoveis' AND 1 = 1
 AND tipo = 'U'
 AND id_gerado is null