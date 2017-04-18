import pandas as pd
import numpy as np
from ggplot import *

def compute_prob_vector(ps_file, prob_paired=True):
    '''
    Given a text file derived from the RNAfold output of the form
    
    i    j    sqrt(prob)   ubox
    
    computes a vector (dict) of probabilities for every nucleotide
    to be in paired (or unpaired) state.
    '''
    prob_vector = {}
    with open(ps_file) as fi:
        for line in fi.readlines():
            line = line.strip()
            posi, posj, sqrt_prob, box = line.split()
            curr_i = prob_vector.get(int(posi), 0)
            curr_j = prob_vector.get(int(posj), 0)
            curr_prob = float(sqrt_prob)**2
            indi = int(posi)
            indj = int(posj)
            if indi in prob_vector:
                if curr_prob > prob_vector[indi]:
                    prob_vector[indi] = curr_prob
            else:
                prob_vector[indi] = curr_prob
            if indj in prob_vector:
                if curr_prob > prob_vector[indj]:
                    prob_vector[indj] = curr_prob
            else:
                prob_vector[indj] = curr_prob
                
    if prob_paired:
        return prob_vector
    else:
        return dict([(pos, 1-p) for pos,p in prob_vector.items()])
    

def trange_df(base_name, prob_func=compute_prob_vector, 
              trange=range(35,43), abs_value=True):
    '''
    Same as `compute_diff_df` but builds dataframe in a long format
    suitable for ggplot faceting.
    '''
    T0 = trange[0]
    prob0 = prob_func('%s_%d.txt' % (base_name, T0))
    chunks = []
    for temp in trange[1:]:
        df = pd.DataFrame()
        prob_vector = prob_func('%s_%d.txt' % (base_name,temp))
        npos = max(set(prob0.keys()) | set(prob_vector.keys())) + 1
        d0 = np.zeros(npos)
        dt = np.zeros(npos)
        d0[list(prob0.keys())] = list(prob0.values())
        dt[list(prob_vector.keys())] = list(prob_vector.values())
        df['pos'] = range(npos)
        if abs_value:
            df['Diff'] = abs(d0 - dt)
        else:
            df['Diff'] = dt - d0
        df['Temp'] = temp
        chunks.append(df)
    return pd.concat(chunks)

def sig_positions(df, num_sigma=6):
    mean = df['Diff'].mean()
    sigma = df['Diff'].std()
    threshold = num_sigma * sigma
    return abs(df['Diff'] - mean) > threshold


def plot_RSMD(df, trange=range(37,43)):
   df_sum = pd.DataFrame()
   df_sum['Temp'] = trange[1:]
   df_sum['RMSD'] = [np.sqrt(((df[df['Temp'] == T]['Diff'])**2).sum()) for T in trange[1:]]
   p = ggplot(df_sum, aes(x='Temp', y='RMSD')) + geom_line()
   return p
