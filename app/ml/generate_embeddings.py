import torch
import pandas as pd
import numpy as np
import joblib
from app.ml.tennis_encoder import TennisEncoder

def generate_final_dataset():
    # 1. Load the Encoders and the Processed Data
    print("📡 Loading data and encoders...")
    df = pd.read_pickle('app/ml/data/processed_training_data.pkl')
    player_le = joblib.load('app/ml/models/player_encoder.pkl')
    surface_le = joblib.load('app/ml/models/surface_encoder.pkl')
    
    num_players = len(player_le.classes_)
    num_surfaces = len(surface_le.classes_)
    
    # 2. Initialize and Load the Trained Neural Network
    # Use the same input_dim from your training (likely 12 or 22)
    cont_cols = [c for c in df.columns if c.startswith(('p1_', 'p2_')) and not c.endswith('_idx')]
    input_dim = len(cont_cols)
    
    model = TennisEncoder(num_players, num_surfaces, input_dim=input_dim)
    model.load_state_dict(torch.load('app/ml/models/tennis_encoder.pt'))
    model.eval()
    
    print("🧠 Extracting learned Player Embeddings...")
    with torch.no_grad():
        # Get the weight matrix from the embedding layer (NumPy format)
        embedding_matrix = model.player_embed.weight.data.numpy()
        
    # 3. Map Embeddings to the DataFrame
    # We create 16 columns for P1 and 16 for P2
    p1_embeddings = embedding_matrix[df['p1_id_idx'].values]
    p2_embeddings = embedding_matrix[df['p2_id_idx'].values]
    
    # Create column names: p1_emb_0, p1_emb_1 ...
    p1_emb_cols = [f'p1_emb_{i}' for i in range(16)]
    p2_emb_cols = [f'p2_emb_{i}' for i in range(16)]
    
    p1_emb_df = pd.DataFrame(p1_embeddings, columns=p1_emb_cols, index=df.index)
    p2_emb_df = pd.DataFrame(p2_embeddings, columns=p2_emb_cols, index=df.index)
    
    # 4. Combine everything into the "Super-Dataset"
    final_df = pd.concat([df, p1_emb_df, p2_emb_df], axis=1)
    
    # Save as Parquet (Preserves all types perfectly for XGBoost)
    final_df.to_parquet('app/ml/data/final_training_set.parquet')
    print(f"✅ Created Super-Dataset: {final_df.shape[1]} features, {len(final_df)} rows.")

if __name__ == "__main__":
    generate_final_dataset()
