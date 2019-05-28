import pandas as pd


def remove_unused_rows(cohorts, path_to_data="./"):
    """This function removes redundant samples (rows) in phenotype data.

    Args:
        cohorts (str or list): A list of cohorts for which the unused rows
            will be removed.
        path_to_data (str, optional): Path to the data stored. If nothing is
            passed the current directly will be considered.
    """
    dest = "GDC_phenotype"
    # rows represent IDs
    xena_dtype_row_ID = [
        "htseq_counts",
        "htseq_fpkm-uq",
        "htseq_fpkm",
        "mirna",
        "methylation450",
    ]
    # corresponding column represents IDs
    xena_dtype_col_ID = {
        "masked_cnv": "sample",
        "muse_snv": "Sample_ID",
        "mutect2_snv": "Sample_ID",
        "somaticsniper_snv": "Sample_ID",
        "varscan2_snv": "Sample_ID",
    }
    if isinstance(cohorts, str):
        cohorts = [cohorts]
    for cohort in cohorts:
        matrix_path = path_to_data + cohort + "/Xena_Matrices/" + cohort + "."
        rows = []
        for dtype in xena_dtype_row_ID:
            df = pd.read_csv(matrix_path + dtype + ".tsv", sep="\t")
            row = list(df)[1:]
            rows.extend(row)
        for dtype in xena_dtype_col_ID.keys():
            df = pd.read_csv(matrix_path + dtype + ".tsv", sep="\t")
            row = df[xena_dtype_col_ID[dtype]]
            rows.extend(row)
        rows = set(rows)
        dest_df = pd.read_csv(matrix_path + dest + ".tsv", sep="\t")
        dest_rows = set(dest_df["submitter_id.samples"])
        to_remove = list(dest_rows - rows)
        dest_df = dest_df.set_index("submitter_id.samples")
        dest_df = dest_df.drop(to_remove, axis=0)
        dest_df.to_csv(matrix_path + dest + ".tsv", sep="\t")
