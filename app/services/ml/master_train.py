import asyncio
import sys
from app.ml.processor import TennisDataProcessor
from app.ml.train_encoder import train_encoder
from app.ml.generate_embeddings import generate_final_dataset
from app.ml.train_xgboost import train_xgboost

async def run_unified_pipeline():
    print("\n" + "="*50)
    print("🎾 STARTING VANTAGE POINT MASTER TRAINING")
    print("="*50)

    try:
        # --- 1. Data Preprocessing & Scaling ---
        proc = TennisDataProcessor()
        raw = proc.fetch_raw_data()
        final = proc.process_and_balance(raw)
        
        # Save the processed data for PyTorch
        final.to_pickle('app/ml/data/processed_training_data.pkl')
        proc.save_processors()
        print(f"✅ Preprocessing Complete. Dataset size: {len(final)}")

        # --- 2. Train Neural Encoder ---
        print("\n🧠 STEP 2: Training Neural Encoder (PyTorch)...")
        # Removing 'await' if these aren't async functions
        train_encoder() 
        print("✅ Step 2 Complete. Encoder weights (.pth) updated.")

        # --- 3. Generate Player Embeddings ---
        print("\n🧬 STEP 3: Synchronizing Player Embeddings...")
        generate_final_dataset()
        print("✅ Step 3 Complete. Embeddings refreshed.")

        # --- 4. Train XGBoost ---
        print("\n🚀 STEP 4: Training Final XGBoost Model...")
        train_xgboost()
        
        

    except Exception as e:
        print(f"\n❌ PIPELINE FAILED at Step {sys.exc_info()[-1].tb_lineno}:")
        print(f"   Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_unified_pipeline())
