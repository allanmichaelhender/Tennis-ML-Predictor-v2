from fastapi import APIRouter, HTTPException, Security
from datetime import datetime
from app.api.deps import get_api_key
from app.database.session import async_session
from app.schemas.predict import ManualPredictRequest, ManualPredictResponse
from app.services.ml.inference_service import inference_service
from sqlalchemy import select
from app.models.player_state import PlayerState

router = APIRouter()

# Path for manually prediciting a match with two player name/ids and surface past in
@router.post(
    "/manual-predict",
    dependencies=[Security(get_api_key)],
    response_model=ManualPredictResponse,
)
async def manual_predict(data: ManualPredictRequest):
    async with async_session() as session:

        # Selecting the two rows associated with the chosen players
        stmt = select(PlayerState).where(
            PlayerState.player_id.in_([data.p1_id, data.p2_id])
        )
        result = await session.execute(stmt)

        # .scalars unpacks result into an iterable, .all puts all the rows into a list, we use a dict comprehension to make data access easier
        player_rows = {p.player_id: p for p in result.scalars().all()}

        p1_row = player_rows.get(data.p1_id)
        p2_row = player_rows.get(data.p2_id)

        if not p1_row or not p2_row:
            raise HTTPException(status_code=404, detail="Player data missing from DB")

        # Now we parse the date into our inference service, we get returned a dict of the probabilites
        prediction = await inference_service.predict(
            session=session,
            p1_row=p1_row,
            p2_row=p2_row,
            surface=data.surface,
            commence_time=datetime.now().isoformat(),
        )

        return {
            "p1_prob": prediction["p1_prob"],
            "p2_prob": prediction["p2_prob"],
            "p1_stats": p1_row,
            "p2_stats": p2_row,
        }
