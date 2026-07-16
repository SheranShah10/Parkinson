import pandas as pd
import numpy as np

class PCARepresentation:
    def __init__(self, n_components=5):
        self.n_components = n_components
        self.is_fitted = False
        
    def fit(self, X):
        X_num = X.select_dtypes(include=np.number).fillna(0).values
        X_centered = X_num - np.mean(X_num, axis=0)
        cov_matrix = np.cov(X_centered, rowvar=False)
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        sorted_index = np.argsort(eigenvalues)[::-1]
        self.eigenvectors = eigenvectors[:, sorted_index][:, 0:self.n_components]
        self.mean = np.mean(X_num, axis=0)
        self.is_fitted = True
        return self
        
    def transform(self, X):
        X_num = X.select_dtypes(include=np.number).fillna(0).values
        X_centered = X_num - self.mean
        proj = np.dot(X_centered, self.eigenvectors)
        return pd.DataFrame(proj, columns=[f'PCA_{i}' for i in range(self.n_components)])

class MockAutoencoder:
    def __init__(self, latent_dim=10):
        self.latent_dim = latent_dim
        self.is_fitted = False
        
    def fit(self, X):
        self.is_fitted = True
        return self
        
    def transform(self, X):
        # Proxy autoencoder embedding using fixed random projection to guarantee determinism
        np.random.seed(42)
        X_num = X.select_dtypes(include=np.number).fillna(0).values
        proj_matrix = np.random.randn(X_num.shape[1], self.latent_dim)
        proj = np.dot(X_num, proj_matrix)
        return pd.DataFrame(proj, columns=[f'AE_{i}' for i in range(self.latent_dim)])
