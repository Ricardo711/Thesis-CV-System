from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.auth_deps import get_current_user
from app.core.config import settings
from app.models.quiz import QuizQuestionOut
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/question", response_model=QuizQuestionOut)
async def get_quiz_question(
    current_user: dict = Depends(get_current_user),
) -> QuizQuestionOut:
    result = await QuizService.get_quiz_question(settings.quiz_target_class)
    return result
