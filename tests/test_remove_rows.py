import pandas as pd

from xena_gdc_etl.scripts.remove_rows import remove_unused_rows


def test_remove_unused_rows():
    cohorts = "TCGA-CHOL"
    path_to_data = "tests/fixtures/"
    remove_unused_rows(cohorts, path_to_data)
    actual = pd.read_csv(
        "tests/fixtures/TCGA-CHOL/Xena_Matrices/TCGA-CHOL.GDC_phenotype.tsv",
        sep="\t",
    )
    expected = pd.read_csv(
        "tests/fixtures/modified_TCGA-CHOL_phenotype.tsv",
        sep="\t",
    )
    actual.equals(expected)
