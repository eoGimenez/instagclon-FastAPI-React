from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from enviroment.config import Settings, get_settings



router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)

@router.get('/')
def setting(settings: Annotated[Settings, Depends(get_settings)]):
    return settings