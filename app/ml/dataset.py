import torch
from torch.utils.data import Dataset

# Building a torch dataset
class TennisDataset(Dataset):
    def __init__(self, dataframe):
        # Categorical Features (already mapped to integers for Embeddings), dytpe for integers is torchl'long
        self.surface = torch.tensor(dataframe['surface_idx'].values, dtype=torch.long)
        self.player_w = torch.tensor(dataframe['w_id_idx'].values, dtype=torch.long)
        self.player_l = torch.tensor(dataframe['l_id_idx'].values, dtype=torch.long)
        
        # Continuous Features (Elo, Age, Days Off)
        self.continuous = torch.tensor(
            dataframe[['w_elo_before', 'l_elo_before', 'w_days_off', 'l_days_off']].values, 
            dtype=torch.float32
        )
        
        # Target (1 = Winner won, 0 = Winner lost - after we flip)
        self.target = torch.tensor(dataframe['target'].values, dtype=torch.float32)

    # Returns the length of the dataset, for ease we take the length of a column with entries for every match
    def __len__(self):
        return len(self.target)

    # Defining our own get item logic
    def __getitem__(self, idx):
        return {
            'cat': (self.surface[idx], self.player_w[idx], self.player_l[idx]),
            'cont': self.continuous[idx],
            'target': self.target[idx]
        }
