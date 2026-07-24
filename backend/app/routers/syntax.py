from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.models import User
from app.schemas import SyntaxTagRequest, SyntaxTagResponse
from app.services.assamese_tagger import tag_syntax

router = APIRouter(prefix="/syntax", tags=["Syntax Tagging"])


@router.post("/tag", response_model=SyntaxTagResponse)
def tag_syntax_endpoint(
    payload: SyntaxTagRequest,
    current_user: User = Depends(get_current_user),
):
    result = tag_syntax(payload.text)

    return SyntaxTagResponse(
        tokens=result["tokens"],
        pos_tags=result["pos_tags"],
        named_entities=result["named_entities"],
        syntax_tree=result["syntax_tree"],
    )
