from Bio import SeqIO
import rstoolbox.components as cp

def fasta_parser(fastafile=""):
        """Reading fasta file into dataframe with full fasta description as index and sequences in first column."""
        indx = [seq_record.description for seq_record in SeqIO.parse(fastafile, "fasta")]
        sequences = [str(seq_record.seq) for seq_record in SeqIO.parse(fastafile, "fasta")]
        return cp.DesignFrame( data=sequences, index=indx, columns=["sequences"] )
