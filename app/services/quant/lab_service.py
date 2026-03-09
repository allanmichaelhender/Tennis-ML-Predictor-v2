import pandas as pd
import numpy as np

class LabService:
    def __init__(self, file_path: str = "app/ml/data/betting_results.csv"):
        self.file_path = file_path

    async def get_model_performance(self):
        df = pd.read_csv(self.file_path)
        df['date'] = pd.to_datetime(df['date'])

        # 🎯 1. GLOBAL BRAIN CHECK (Scientific Accuracy)
        # P1 is always the winner in your DB, so outcome is always 1.0
        brier_df = df.dropna(subset=['p1_prob'])
        global_brier = np.mean((brier_df['p1_prob'] - 1.0)**2)

        # 🎯 2. FINANCIAL FILTER (Only your actual bets)
        bet_df = df[df['bet_on'] != "None"].copy()
        
        total_wagered = bet_df['bet_amount'].sum()
        total_pnl = bet_df['pnl'].sum()

        summary = {
            "roi": total_pnl / total_wagered if total_wagered > 0 else 0,
            "total_profit": total_pnl,
            "win_rate": bet_df['is_win'].mean() if not bet_df.empty else 0,
            "brier_score": global_brier, # Scientific IQ
            "total_bets": len(bet_df)
        }

        # 🎯 3. Weekly Equity Curve (Use bet_df only!)
        # We want to see how the bankroll moved after each BET
        weekly = bet_df.set_index('date')['balance'].resample('W').last().ffill().reset_index()
        equity_curve = [
            {"date": row.date.strftime('%Y-%m-%d'), "balance": row.balance} 
            for row in weekly.itertuples()
        ]

        # 🎯 4. Monthly Stats (Use bet_df only!)
        monthly_df = bet_df.set_index('date').resample('ME').agg({
            'pnl': 'sum',
            'bet_amount': 'sum'
        }).reset_index()
        
        monthly_breakdown = [
            {
                "month": row.date.strftime('%b %Y'), 
                "roi": row.pnl / row.bet_amount if row.bet_amount > 0 else 0,
                "profit": row.pnl
            } 
            for row in monthly_df.itertuples()
        ]

        return {
            "summary": summary,
            "equity_curve": equity_curve,
            "monthly_breakdown": monthly_breakdown
        }

    
    async def get_edge_analysis(self):
        df = pd.read_csv(self.file_path)

        df = df[df['bet_on'] != "None"].copy()
    
        if df.empty:
            return []
        
        # 1. IDENTIFY THE CHOSEN SIDE'S DATA
        # We create columns for the probability and odds of the player we actually bet on
        df['bet_prob'] = np.where(df['bet_on'] == 'P1', df['p1_prob'], df['p2_prob'])
        df['bet_odds'] = np.where(df['bet_on'] == 'P1', df['p1_odds'], df['p2_odds'])
        
        # 2. CALCULATE THE ACTUAL EDGE (Matches your PNLService +0.05 logic)
        df['edge'] = df['bet_prob'] - (1 / df['bet_odds'])
        
        # 3. DEFINE THE BUCKETS (Starting at 5% to match your PNLService)
        # We use a very small number (0.049) to ensure 0.05 is included in the first bucket
        bins = [0, 0.029, 0.049, 0.07, 0.10, 0.15, 1.0]
        labels = ["0-3% (Smallest)", "3-5% (Small)","5-7% (Thin)", "7-10% (Value)", "10-15% (Strong)", "15%+ (Elite)"]
        df['bucket'] = pd.cut(df['edge'], bins=bins, labels=labels)
        
        # 4. AGGREGATE METRICS
        # Note: Brier Score is (Prob - Outcome)^2. Since we only bet on the winner 
        # (P1) or loser (P2), we compare bet_prob against is_win (1 or 0)
        analysis = df.groupby('bucket', observed=True).apply(lambda x: pd.Series({
            "roi": x['pnl'].sum() / x['bet_amount'].sum() if x['bet_amount'].sum() > 0 else 0,
            "brier_score": np.mean((x['bet_prob'] - x['is_win'].astype(int))**2),
            "match_count": int(len(x)),
            "avg_edge": x['edge'].mean()
        })).reset_index()

        return analysis.to_dict(orient='records')
    
    async def get_calibration(self):
        df = pd.read_csv(self.file_path)
        
        # 🎯 1. THE "FOLD": Always look at the Favourite
        # If p1_prob is 0.10, we look at p2_prob (0.90) and check if P2 won.
        df['fav_prob'] = np.where(df['p1_prob'] >= 0.5, df['p1_prob'], df['p2_prob'])
        
        # In your current CSV, P1 is always the winner. 
        # So if we 'bet' on the favourite (p1_prob >= 0.5), did we win?
        df['fav_won'] = np.where(df['p1_prob'] >= 0.5, 1.0, 0.0)
        
        # 🎯 2. BINS (Only 50% to 100%)
        bins = np.arange(0.5, 1.05, 0.05)
        labels = [f"{int(i*100)}-{int((i+0.05)*100)}%" for i in bins[:-1]]
        
        df['prob_bucket'] = pd.cut(df['fav_prob'], bins=bins, labels=labels, include_lowest=True)
        
        # 🎯 3. AGGREGATE
        calibration = df.groupby('prob_bucket', observed=True).apply(lambda x: pd.Series({
            "avg_predicted": x['fav_prob'].mean(),
            "actual_win_rate": x['fav_won'].mean(),
            "match_count": int(len(x))
        })).reset_index()

        df.to_csv("app/ml/data/calibration_results.csv", index=False)


        return calibration.to_dict(orient='records')

    


lab_service = LabService()
