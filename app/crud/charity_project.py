from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_projects_by_completion_rate(
        session: AsyncSession,
    ):
        charity_project = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(
                func.DATE(CharityProject.close_date) -
                func.DATE(CharityProject.create_date)
            )
        )
        return charity_project.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
