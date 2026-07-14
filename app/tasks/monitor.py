import asyncio
import httpx
from datetime import datetime
from sqlalchemy import select

from app.tasks.worker import celery_app
from app.database import AsyncSessionMaker
from app.models import Site

async def run_monitoring():
    async with AsyncSessionMaker() as db:
        query = select(Site)
        result = await db.execute(query)
        sites = result.scalars().all()

        async with httpx.AsyncClient() as client:
            for site in sites:
                try:
                    response = await client.get(site.url, timeout=10.0)
                    site.status_code = response.status_code

                    if site.status_code == 200:
                        site.is_online = True
                    else:
                        site.is_online = False
                except httpx.HTTPError:
                    site.status_code = None
                    site.is_online = False
                site.last_checked = datetime.utcnow()
            await db.commit()

@celery_app.task
def check_all_sites():
    asyncio.run(run_monitoring())