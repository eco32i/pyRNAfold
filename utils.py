import pandas as pd
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
            curr_i = prob_vector.get(posi, 0)
            curr_j = prob_vector.get(posj, 0)
            prob_vector.update({
                int(posi): curr_i + float(sqrt_prob)**2,
                int(posj): curr_j + float(sqrt_prob)**2,
            })
    if prob_paired:
        return prob_vector
    else:
        return dict([(pos, 1-p) for pos,p in prob_vector.items()])
    
def trange_df(base_name, trange=range(35,43), abs_value=True):
    '''
    Same as `compute_diff_df` but builds dataframe in a long format
    suitable for ggplot faceting.
    '''
    T0 = trange[0]
    prob0 = pd.Series(compute_prob_vector('%s_%d.txt' % (base_name, T0)).values())
    chunks = []
    for temp in trange[1:]:
        df = pd.DataFrame()
        prob_vector = compute_prob_vector('%s_%d.txt' % (base_name,temp))
        df['pos'] = prob_vector.keys()
        if abs_value:
            df['Diff'] = abs(pd.Series(prob_vector.values()) - prob0)
        else:
            df['Diff'] = pd.Series(prob_vector.values()) - prob0
        df['Temp'] = temp
        chunks.append(df)
    return pd.concat(chunks)

def compute_diff_df(base_name, trange=range(35,43), abs_value=True):
    '''
    Given the base_name for tab-delimited files containing base
    pairing probabilities calculated by RNAfold computes a
    dataframe containing probability difference vectors for each
    temperature value in the range relative to the lowest T in the
    range.
    '''
    T0 = trange[0]
    prob = compute_prob_vector('%s_%d.txt' % (base_name, T0))
    df = pd.DataFrame(prob.items(), columns=['Position', 'Prob_%d' % T0])
    for temp in trange[1:]:
        prob = compute_prob_vector('%s_%d.txt' % (base_name, temp))
        prob_key = 'Prob_%d' % temp
        df[prob_key] = pd.Series(prob.values())
        if abs_value:
            df['Diff_%d' % temp] = abs(df[prob_key] - df['Prob_%d' % T0])
        else:
            df['Diff_%d' % temp] = df[prob_key] - df['Prob_%d' % T0]
    return df

def get_sig_positions(df, trange=range(37,43), num_sigma=6):
    '''
    Given the dataframe of probability differences for a T range
    and the level of significannce in sigmas returns positions in the
    dataframe where the probability difference at the highest T
    exceeds the sigma threshold.
    '''
    colnames = ['Diff_%d' % temp for temp in trange[1:]]
    diff_cols = [df[colname] for colname in colnames]
    all_diff = pd.concat(diff_cols)
    mean = all_diff.mean()
    sigma = all_diff.std()
    threshold = num_sigma * sigma
    print 'Mean:\t%f\nSigma:\t%f\nThreshold:\t%f\n' % (mean, sigma, threshold)
    return df[abs(df['Diff_%d' % trange[-1]] - mean) > threshold].sort(['Position'])

def plot_RSMD(df, trange=range(37,43)):
   df_sum = pd.DataFrame()
   df_sum['Temp'] = trange[1:]
   df_sum['RMSD'] = [np.sqrt(((df[df['Temp'] == T]['Diff'])**2).sum()) for T in trange[1:]]
   p = ggplot(df_sum, aes(x='Temp', y='RMSD')) + geom_line()
   return p
