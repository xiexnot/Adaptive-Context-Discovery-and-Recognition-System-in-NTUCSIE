import numpy as np
def pca_raw_cov(X):
    cov_mat = np.cov(X.T)
    eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mat)
    eig_pairs_cov = [(np.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_val_cov))]
    eig_pairs_cov = [[i[0],list(i[1])] for i in eig_pairs_cov]
    eig_pairs_cov.sort()
    eig_pairs_cov.reverse()
    return eig_pairs_cov