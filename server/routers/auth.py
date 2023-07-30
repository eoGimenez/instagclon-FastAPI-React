from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from enviroment import config_env, envirom



router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)

@router.get('/')
def setting(settings: Annotated[config_env.Settings, Depends(envirom.get_settings)]):
    return settings