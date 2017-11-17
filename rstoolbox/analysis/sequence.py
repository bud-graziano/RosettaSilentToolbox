from SimilarityMatrix import SimilarityMatrix as SM
import pandas as pd
import numpy as np

def _extract_key_residue_sequence( seq, key_residues=None ):
    if key_residues is None:
        return seq
    tmp_seq = ""
    for k in key_residues:
        tmp_seq += seq[k-1]
    return tmp_seq

def _calculate_linear_sequence_similarity( qseq, rseq, matrix, key_residues=None ):
    score = 0;
    qseq = _extract_key_residue_sequence( qseq, key_residues ).replace("-", "*")
    rseq = _extract_key_residue_sequence( rseq, key_residues ).replace("-", "*")
    assert len(qseq) == len(rseq)
    for i in range(len(qseq)):
        score += matrix[qseq[i]][rseq[i]]
    return score

def _calculate_binary_sequence_similarity( qseq, rseq, matrix, key_residues=None ):
    new_seq = ""
    qseq = _extract_key_residue_sequence( qseq, key_residues ).replace("-", "*")
    rseq = _extract_key_residue_sequence( rseq, key_residues ).replace("-", "*")
    assert len(qseq) == len(rseq)
    for i in range(len(qseq)):
        if  matrix[qseq[i]][rseq[i]] >= 1:
            new_seq += "1"
        else:
            new_seq += "0"
    return new_seq

def linear_sequence_similarity( df, ref_seq, matrix="BLOSUM62", seq_column="sequence", prefix=None, key_residues=None ):
    mat       = SM.get_matrix(matrix)
    all_seqs  = df[[seq_column]]
    sims      = []
    max_value = _calculate_linear_sequence_similarity( ref_seq, ref_seq, mat, key_residues )
    if prefix is None:
        prefix = matrix.lower()
    else:
        prefix = str(prefix) + matrix.lower()
    for v in all_seqs.values:
        sims.append( _calculate_linear_sequence_similarity( v[0], ref_seq, mat, key_residues ) )
    simsperc = np.array(sims) / float(max_value)
    wdf = df.copy()
    if prefix + "_raw" in wdf:
        wdf = wdf.drop([prefix + "_raw", prefix + "_perc"], axis=1)
    wdf.insert( wdf.shape[1], prefix + "_raw", pd.Series( sims, index=wdf.index ) )
    wdf.insert( wdf.shape[1], prefix + "_perc", pd.Series( simsperc, index=wdf.index ) )
    return wdf

def binary_similarity( df, ref_seq, matrix="IDENTITY", seq_column="sequence", prefix=None, key_residues=None ):
    mat       = SM.get_matrix(matrix)
    all_seqs  = df[[seq_column]]
    sims      = []
    if prefix is None:
        prefix = matrix.lower()
    else:
        prefix = str(prefix) + matrix.lower()
    for v in all_seqs.values:
        sims.append( _calculate_binary_sequence_similarity( v[0], ref_seq, mat, key_residues ) )
    wdf = df.copy()
    if prefix + "_binary" in df:
        wdf = wdf.drop([prefix + "_binary"], axis=1)
    wdf.insert( wdf.shape[1], prefix + "_binary", pd.Series( sims, index=wdf.index ) )
    return wdf

def binary_overlap( df, column_name="identity_binary" ):
    a = df[column_name].values
    x = len(a[0])
    result = [0] * x
    for seq in a:
        for _, b in enumerate(seq):
            if bool(int(b)): result[_] = 1
    return result

def sequence_frequency_matrix( series, seq_column="sequence" ):
    sserie = series[seq_column].values
    table = {
        'C' : [], 'D' : [], 'S' : [], 'Q' : [], 'K' : [],
        'I' : [], 'P' : [], 'T' : [], 'F' : [], 'N' : [],
        'G' : [], 'H' : [], 'L' : [], 'R' : [], 'W' : [],
        'A' : [], 'V' : [], 'E' : [], 'Y' : [], 'M' : [],
        "-" : []
    }

    for x in range(len(sserie[0])):
        for k in table:
            table[k].append(float(0))
        for y in range(len(sserie)):
            aa = sserie[y][x]
            if aa in table:
                table[aa][-1] += float(1)
            else:
                table["-"][-1] += float(1)
    for k in table:
        for x in range(len(table[k])):
            if table[k][x] != 0:
                table[k][x] /= float(len(sserie))

    df = pd.DataFrame( table )
    df.index = df.index + 1
    return df
