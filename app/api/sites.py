from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.schemas import SiteCreate, SiteResponse
from app.models import Site
from app.api.auth import get_current_user, User

router = APIRouter(prefix='/sites', tags=['Sites'])

@router.post('/', response_model=SiteResponse)
async def add_site(site_data: SiteCreate, current_user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    new_site = Site(url=site_data.url, name=site_data.name, user_id=current_user.id)

    db.add(new_site)
    await db.commit()
    await db.refresh(new_site)

    return new_site

@router.get('/', response_model=list[SiteResponse])
async def get_my_sites(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(Site).where(Site.user_id == current_user.id)
    result = await db.execute(query)
    sites = result.scalars().all()

    return sites

@router.delete('/{site_id}')
async def delete_site(site_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(Site).where(Site.id == site_id)
    result = await db.execute(query)
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=404, detail='Сайт не найден')
    
    if site.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='У вас нет прав на удаление этого сайта')
    
    await db.delete(site)
    await db.commit()

    return {'message': 'Сайт успешно удален'}