import torch
from torch.utils.data import Dataset

class TennisDataset(Dataset):
    def __init__(self, dataframe):
        # 1. Categorical Features (mapped to integers for Embeddings)
        self.surface = torch.tensor(dataframe['surface_idx'].values, dtype=torch.long)
        self.player_w = torch.tensor(dataframe['w_id_idx'].values, dtype=torch.long)
        self.player_l = torch.tensor(dataframe['l_id_idx'].values, dtype=torch.long)
        
        # 2. Continuous Features (Elo, Age, Days Off)
        self.continuous = torch.tensor(
            dataframe[['w_elo_before', 'l_elo_before', 'w_days_off', 'l_days_off']].values, 
            dtype=torch.float32
        )
        
        # 3. Target (1 = Winner won, 0 = Winner lost - after we shuffle/flip)
        self.target = torch.tensor(dataframe['target'].values, dtype=torch.float32)

    def __len__(self):
        return len(self.target)

    def __getitem__(self, idx):
        return {
            'cat': (self.surface[idx], self.player_w[idx], self.player_l[idx]),
            'cont': self.continuous[idx],
            'target': self.target[idx]
        }
