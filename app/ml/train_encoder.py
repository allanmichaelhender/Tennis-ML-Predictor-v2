import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from app.ml.tennis_encoder import TennisEncoder

def train_encoder():
    # 1. Load Processed Data
    print("📡 Loading processed dataset...")
    df = pd.read_pickle('app/ml/data/processed_training_data.pkl')
    
    # 2. Define Feature Groups
    # Categorical Indexes
    p1_idx = torch.tensor(df['p1_id_idx'].values, dtype=torch.long)
    p2_idx = torch.tensor(df['p2_id_idx'].values, dtype=torch.long)
    surf_idx = torch.tensor(df['surface_idx'].values, dtype=torch.long)
    
    # Continuous Stats (All the rolling averages and Elos)
    cont_cols = [c for c in df.columns if c.startswith(('p1_', 'p2_')) and not c.endswith('_idx')]
    
    #Converting to floats
    for col in cont_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)


    performance_stats = torch.tensor(df[cont_cols].values, dtype=torch.float32)

    input_dim = performance_stats.shape[1] # This will be 12, 22, or 24 depending on your data
    print(f"📊 Model Input Dimension: {input_dim}")
    
    # Target (1.0 = P1 wins, 0.0 = P2 wins)
    target = torch.tensor(df['target'].values, dtype=torch.float32).unsqueeze(1)

    # 3. Train/Val Split (80/20)
    dataset = TensorDataset(p1_idx, p2_idx, surf_idx, performance_stats, target)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_db, val_db = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_db, batch_size=256, shuffle=True)
    val_loader = DataLoader(val_db, batch_size=256)

    # 4. Initialize the Encoder
    num_players = len(joblib.load('app/ml/models/player_encoder.pkl').classes_)
    num_surfaces = len(joblib.load('app/ml/models/surface_encoder.pkl').classes_)
    
    model = TennisEncoder(num_players, num_surfaces, input_dim=input_dim)
    criterion = nn.BCELoss() # Binary Cross Entropy for Win/Loss
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 5. Training Loop
    print(f"🚀 Training on {train_size} rows...")
    for epoch in range(10): # 10 Epochs is a good start for 88k rows
        model.train()
        total_loss = 0
        for p1, p2, surf, stats, y in train_loader:
            optimizer.zero_grad()
            outputs = model(p1, p2, surf, stats)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        # Validation Check
        model.eval()
        correct = 0
        with torch.no_grad():
            for p1, p2, surf, stats, y in val_loader:
                outputs = model(p1, p2, surf, stats)
                predicted = (outputs > 0.5).float()
                correct += (predicted == y).sum().item()
        
        accuracy = correct / val_size
        print(f"Epoch {epoch+1}/10 | Loss: {total_loss/len(train_loader):.4f} | Val Acc: {accuracy:.2%}")

    # 6. Save the "Brain"
    torch.save(model.state_dict(), 'app/ml/models/tennis_encoder.pt')
    print("✅ Encoder trained and saved to app/ml/models/tennis_encoder.pt")

if __name__ == "__main__":
    train_encoder()
