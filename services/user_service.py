from sqlmodel.ext.asyncio.session import AsyncSession
from schema.user_schema import UserCreateModel
from sqlmodel import text, select, desc
from models.user_model import User
from utils.utils import generate_password_hash, verify_password


class UserService:

    async def get_all_users(self, session: AsyncSession):
        statement = select(User).order_by(desc(User.created_at))
        users = await session.exec(statement)

        if users:
            return users
        else:
            return None

    async def get_user(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        if user:
            return user
        else:
            return None

    async def user_exist(self, email, session: AsyncSession):
        user = await self.get_user(email, session)
        if user is None:
            return False
        else:
            return True

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = UserCreateModel(**user_data_dict)
        new_user.password = generate_password_hash(user_data_dict["password"])
        await session.add(new_user)
        await session.commit()
        return new_user
