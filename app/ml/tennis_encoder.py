import torch
import torch.nn as nn

class TennisEncoder(nn.Module):
    def __init__(self, num_players, num_surfaces, input_dim, embedding_dim=16):
        super(TennisEncoder, self).__init__()
        
        # 1. Identity Embeddings (Categorical Tower)
        # Learns the 'Style' and 'Identity' of each player
        self.player_embed = nn.Embedding(num_players, embedding_dim)
        self.surface_embed = nn.Embedding(num_surfaces, 4)
        
        # 2. Performance Tower (Continuous Features)
        # Processes Elo, Form, Fatigue, and Efficiency metrics
        self.performance_head = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64), # Keeps gradients stable during training
            nn.Dropout(0.2)
        )
        
        # 3. The Fusion Head
        # Concatenates: [P1_Vec (16), P2_Vec (16), Surf_Vec (4), Perf_Vec (64)] = 100
        self.fusion = nn.Sequential(
            nn.Linear(100, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid() # Binary probability: 0 (P2 Wins) to 1 (P1 Wins)
        )

    def forward(self, p1_idx, p2_idx, surface_idx, performance_stats):
        # 1. Generate Player & Surface Vectors
        p1_vec = self.player_embed(p1_idx)
        p2_vec = self.player_embed(p2_idx)
        surf_vec = self.surface_embed(surface_idx)
        
        # 2. Process Stats
        perf_vec = self.performance_head(performance_stats)
        
        # 3. Concatenate and Predict
        combined = torch.cat([p1_vec, p2_vec, surf_vec, perf_vec], dim=1)
        
        return self.fusion(combined)

    def get_player_vector(self, player_idx):
        """Helper to extract the 16-D vector for XGBoost later."""
        return self.player_embed(player_idx).detach()