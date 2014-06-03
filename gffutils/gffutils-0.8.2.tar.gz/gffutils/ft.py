import gffutils
fn = gffutils.example_filename('FBgn0031208.gff')
db = gffutils.create_db(fn, ':memory:')
print [str(i[0]) for i in db._execute('select id from features', ())]


"chr2L	FlyBase	gene	7529	9484	.	+	.	Ontology_term=SO:0000010,SO:0000087,GO:0008234,GO:0006508;gbunit=AE014134;derived_computed_cyto=21A5-21A5;Dbxref=FlyBase:FBan0011023,FlyBase_Annotation_IDs:CG11023,GB:AE003590,GB_protein:AAO41164,GB:AI944728,GB:AJ564667,GB_protein:CAD92822,GB:BF495604,UniProt/TrEMBL:Q6KEV3,UniProt/TrEMBL:Q86BM6,INTERPRO:IPR003653,BIOGRID:59420,dedb:5870,GenomeRNAi_gene:33155,ihop:59383;ID=FBgn0031208;Name=CG11023"
