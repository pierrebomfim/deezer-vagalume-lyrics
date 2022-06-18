text = 'eu te amo'

novo_text = text.replace(' ', '%20')

print(novo_text)



start_url = "https://devbusiness.un.org/solr-sitesearch-output/10//0/ds_field_last_updated/desc?bundle_fq =procurement_notice&sm_vid_Institutions_fq=&sm_vid_Procurement_Type_fq=&sm_vid_Countries_fq=&sm_vid_Sectors_fq= &sm_vid_Languages_fq=English&sm_vid_Notice_Type_fq=&deadline_multifield_fq=&ts_field_project_name_fq=&label_fq=&sm_field_db_ref_no__fq=&sm_field_loan_no__fq=&dm_field_deadlineFrom_fq=&dm_field_deadlineTo_fq =&ds_field_future_posting_dateFrom_fq=&ds_field_future_posting_dateTo_fq=&bm_field_individual_consulting_fq="

start_url = "https://devbusiness.un.org/solr-sitesearch-output/10//0/ds_field_last_updated/desc?bundle_fq =procurement_notice&sm_vid_Institutions_fq=&sm_vid_Procurement_Type_fq=&sm_vid_Countries_fq=&sm_vid_Sectors_fq= &sm_vid_Languages_fq=English&sm_vid_Notice_Type_fq=&deadline_multifield_fq=&ts_field_project_name_fq=&label_fq=&sm_field_db_ref_no__fq=&sm_field_loan_no__fq=&dm_field_deadlineFrom_fq=&dm_field_deadlineTo_fq =&ds_field_future_posting_dateFrom_fq=&ds_field_future_posting_dateTo_fq=&bm_field_individual_consulting_fq="

url = 'https://api.vagalume.com.br/search.php?art=Irmã%20Kelly%20Patrícia&mus=O%20Amado&apikey=5bf325dd4cf0161ca30f8444ce58c48c'

    translation = result.get_translation_to('pt-br')
    if not translation:
        print('Translation not found')
    else:
        cur.execute('''INSERT OR IGNORE INTO Translation (letra) VALUES ( ? )''',
                    (translation.lyric, ))
        cur.execute('''SELECT id FROM Translation WHERE letra = ? ''',
                    (translation.lyric, ))
        translation_id = cur.fetchone()[0]
        print('A tradução foi salva no banco de dados')