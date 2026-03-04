import torch
import torch.nn as nn

class PlayerEncoder(nn.Module):
    def __init__(self, num_players, embedding_dim=16):
        super(PlayerEncoder, self).__init__()
        # This is the "Magic" layer that learns the player styles
        self.player_embeddings = nn.Embedding(num_players, embedding_dim)
        
        # This layer processes the 'Continuous' stats (Elo, Form, etc.)
        self.stats_layer = nn.Linear(12, 32) 
        
        # The final head to "Train" the embeddings on Win/Loss
        self.fc = nn.Sequential(
            nn.Linear(embedding_dim * 2 + 32, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, p1_idx, p2_idx, stats):
        p1_vec = self.player_embeddings(p1_idx)
        p2_vec = self.player_embeddings(p2_idx)
        stat_vec = torch.relu(self.stats_layer(stats))
        
        # Combine everything into one "Super-Vector"
        combined = torch.cat([p1_vec, p2_vec, stat_vec], dim=1)
        return self.fc(combined)
