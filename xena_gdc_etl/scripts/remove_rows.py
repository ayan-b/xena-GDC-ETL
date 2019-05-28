import pandas as pd


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

# specify the cohorts here
cohorts = [
    "TCGA-CHOL",
]

dest = "GDC_phenotype"

# path to the project data
PATH = "/run/media/ayanb/New Volume1/GDC-Data/"

def remove_unused_rows():
    for cohort in cohorts:
        matrix_path = PATH + cohort + "/Xena_Matrices/" + cohort + "."
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


if __name__ == "__main__":
    remove_unused_rows()
