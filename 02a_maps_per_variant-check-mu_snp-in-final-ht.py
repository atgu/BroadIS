import hail as hl
from bokeh.io import output_notebook,show
import gnomad.utils.vep
from hail.ggplot import *
import plotly
import plotly.io as pio
pio.renderers.default='iframe'

def main():
    ht_final = hl.read_table('gs://janucik-dataproc-stage/01_maps/data_full_ht/02a_f_ht_final.ht')

    # Import mutation rates from gnomAD paper
    ht_mu = hl.import_table('gs://janucik-dataproc-stage/01_maps/supplementary_dataset_10_mutation_rates.tsv.gz',
                    delimiter='\t', impute=True, force_bgz=True)

    # Convert mu_snp into string
    ht_mu = ht_mu.key_by('context', 'ref', 'alt', 'methylation_level') # has to have a key in order to join using foreign key

    ht_final = ht_final.annotate(**ht_mu[ht_final.context, ht_final.ref, ht_final.alt, ht_final.methylation_level])

    ht_f_inframe_del = ht_final.filter(ht_final.vep.most_severe_consequence == "inframe_deletion")
    ht_f_inframe_ins = ht_final.filter(ht_final.vep.most_severe_consequence == "inframe_insertion")

    ht_f_inframe_del_mu = ht_f_inframe_del.filter(hl.is_defined(ht_f_inframe_del.mu_snp))

    ht_f_inframe_ins_mu = ht_f_inframe_ins.filter(hl.is_defined(ht_f_inframe_ins.mu_snp))

    print('INFRAME DELETION')

    ht_f_inframe_del_mu.show()

    print('INFRAME INSERTION')

    ht_f_inframe_ins_mu.show()

if __name__ == '__main__':
    main()