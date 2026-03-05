import pandas as pd
import joblib
import numpy as np
import asyncio
import random
from sqlalchemy import select
from app.database.session import async_session
from app.models.match import Match
from app.services.feature_assembler import FeatureAssembler
from datetime import date


class PNLService:
    def __init__(self, initial_bankroll=1000.0, kelly_fraction=0.05):
        self.bankroll = initial_bankroll
        self.fraction = kelly_fraction
        self.max_bet_pct = 0.02

        self.xgb = joblib.load("app/ml/models/final_xgboost_model.pkl")
        self.assembler = FeatureAssembler()

    def get_bet_size(self, model_prob, odds):
        b = odds - 1
        p = model_prob
        q = 1 - p
        kelly = (b * p - q) / b
        suggested_pct = max(0, kelly * self.fraction)
        return min(suggested_pct, self.max_bet_pct)

    async def run_backtest(self):
        cutoff_date = date(2025, 1, 1) 
        print(f"💰 Starting Full-Tour Backtest from {cutoff_date}...")

        async with async_session() as session:
            # 1. Fetch matches with any odds (PS preferred, B365 fallback)
            stmt = (
                select(Match)
                .where(
                    (Match.ps_w.isnot(None)) | (Match.b365_w.isnot(None)),
                    Match.w_elo_before.isnot(None),
                    Match.tourney_date >= cutoff_date,
                )
                .order_by(Match.tourney_date, Match.match_num)
            )

            result = await session.execute(stmt)
            matches = result.scalars().all()

            history = []
            current_balance = self.bankroll

            for m in matches:
                # 2. SYMMETRIC INFERENCE (The "Double Check")
                # Get both perspectives to cancel out positional bias
                x_norm = self.assembler.assemble_match(m, flip=False)
                x_flip = self.assembler.assemble_match(m, flip=True)

                if x_norm is None or x_flip is None:
                    continue

                # Probability P1 wins from both perspectives
                p1_v1 = self.xgb.predict_proba(x_norm)[0][1]
                p1_v2 = 1.0 - self.xgb.predict_proba(x_flip)[0][1]

                # The "Honest" Probabilities
                p1_prob = (p1_v1 + p1_v2) / 2
                p2_prob = 1.0 - p1_prob

                # 3. SELECT ODDS (Pinnacle -> B365)
                # In our DB, P1 is ALWAYS the winner (m.w_...)
                p1_odds = m.ps_w if m.ps_w else m.b365_w
                p2_odds = m.ps_l if m.ps_l else m.b365_l
                # p1_odds = m.b365_w
                # p2_odds = m.b365_l

                #Fair Price comparison
                total_implied_prob = (1 / p1_odds) + (1 / p2_odds)
                overround = total_implied_prob - 1.0

                # 3. CALCULATE THE "FAIR" (NO-VIG) PROBABILITIES
                # We normalize the bookie's odds by the total implied probability
                fair_market_p1_prob = (1 / p1_odds) / total_implied_prob
                fair_market_p2_prob = (1 / p2_odds) / total_implied_prob

                # 4. CALCULATE THE "FAIR" ODDS
                # These are the odds if the bookie took ZERO commission
                fair_p1_odds = 1 / fair_market_p1_prob
                fair_p2_odds = 1 / fair_market_p2_prob


                # 4. BETTING LOGIC
                bet_placed = False
                pnl = 0
                bet_on = ""

                # Try P1 Side (The Actual Winner)
                if p1_prob > (1 / fair_p1_odds) + 0.05:
                    pct = self.get_bet_size(p1_prob, fair_p1_odds)
                    bet_amount = current_balance * pct
                    # bet_amount = 10
                    pnl = (fair_p1_odds - 1) * bet_amount  # WIN
                    bet_on = "P1 (Winner)"
                    bet_placed = True

                # Try P2 Side (The Actual Loser)
                elif p2_prob > (1 / fair_p2_odds) + 0.05:
                    pct = self.get_bet_size(p2_prob, fair_p2_odds)
                    bet_amount = current_balance * pct
                    # bet_amount = 10
                    pnl = -bet_amount  # LOSS
                    bet_on = "P2 (Loser)"
                    bet_placed = True

                # 5. UPDATE BANKROLL
                if bet_placed and bet_amount > 0:
                    current_balance += pnl
                    history.append(
                        {
                            "date": m.tourney_date,
                            "match": f"{m.winner_id} vs {m.loser_id}",
                            "bet_on": bet_on,
                            "bet_amount": bet_amount,
                            "p1_prob": f"{p1_prob:.2%}",
                            "odds": p1_odds if bet_on == "P1 (Winner)" else p2_odds,
                            "pnl": round(pnl, 2),
                            "balance": round(current_balance, 2),
                        }
                    )
                print(f"{m.winner_name} vs {m.loser_name} | Model: {p1_prob:.2%} | Fair: {fair_market_p1_prob:.2%}")


            # 6. RESULTS
            results_df = pd.DataFrame(history)
            results_df.to_csv("app/ml/data/betting_results.csv", index=False)

            print("🏁 Backtest Finished.")
            print(f"📈 Final Bankroll: £{current_balance:.2f}")
            print(f"📊 Total Bets: {len(history)}")

            total_wagered = sum(h["bet_amount"] for h in history)
            total_profit = current_balance - self.bankroll

            # 1. Yield (The Model's Edge)
            yield_pct = (total_profit / total_wagered) if total_wagered > 0 else 0

            # 2. ROC (The Bankroll Growth)
            roc_pct = total_profit / self.bankroll

            print(f"📈 Bankroll Growth (ROC): {roc_pct:.2%}")
            print(f"🚀 Model Yield (ROI): {yield_pct:.2%}")


if __name__ == "__main__":
    # SET THE SEED: This ensures 'random.choice' picks the same sequence every time
    # random.seed(42)
    # np.random.seed(42)

    service = PNLService()
    asyncio.run(service.run_backtest())
