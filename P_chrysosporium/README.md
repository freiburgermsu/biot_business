# P_chrysosporium

Data for the white-rot basidiomycete *Phanerochaete chrysosporium* (JGI MycoCosm genome portal code: `Phchr4_2`).

## Contents

### `Pchry_genome/`
Reference genome and gene catalog from JGI MycoCosm (annotation release 2021-04-19).

| File | Description |
| --- | --- |
| `Phchr4_2_AssemblyScaffolds.fasta.gz` | Nucleotide scaffold assembly (FASTA, gzipped). |
| `Phchr4_2_GeneCatalog_20210419.gff3.gz` | Gene models / annotations in GFF3 format (gzipped). |
| `Phchr4_2_GeneCatalog_proteins_20210419.aa.fasta.gz` | Predicted protein sequences (amino acid FASTA, gzipped). |

### `Pchry_transcriptomics_data/`
DESeq2 differential-expression results (dated 2025-08-27) across four conditions: `blank`, `SACA`, `GFCA`, and `cellulose`. Each pairwise contrast contributes six columns (`baseMean`, `log2FoldChange`, `lfcSE`, `stat`, `pvalue`, `padj`) for the contrasts: `SACA_v_blank`, `GFCA_v_blank`, `cellulose_v_blank`, `cellulose_v_SACA`, `GFCA_v_SACA`, `GFCA_v_cellulose`.

| File | Description |
| --- | --- |
| `Pc_DESeq_jgi_08272025.csv` | DESeq2 results keyed by `GeneID` (JGI gene IDs), no additional annotation columns. |
| `TPM_filtered_DESeq_cazyme_anno_08272025.csv` | TPM-filtered DESeq2 results keyed by `ProteinID` + `GeneID`, augmented with `padjmin`, `Protein_name`, `TranscriptID`, `Name`, and CAZyme annotation (`CAZ_anno`). |
