from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from sport_network_api.application.interfaces import ProfileGatewayInterface
from sport_network_api.infrastructure.models.profile import Profile as ProfileModel
from sport_network_api.domain.profile import Profile

class ProfileGateway(ProfileGatewayInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: int) -> Profile | None:
        query = select(ProfileModel).where(ProfileModel.user_id == user_id)
        res = await self.session.execute(query)
        model = res.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def create(self, profile: Profile) -> Profile:
        profile_model = self._from_domain(profile)
        self.session.add(profile_model)
        await self.session.flush()
        return self._to_domain(profile_model)

    async def update(self, profile: Profile) -> Profile:
        query = select(ProfileModel).where(ProfileModel.user_id == profile.user_id)
        res = await self.session.execute(query)
        profile_model = res.scalar_one()

        if profile.bio is not None:
            profile_model.bio = profile.bio
        if profile.avatar_url is not None:
            profile_model.avatar_url = profile.avatar_url
        if profile.date_of_birth is not None:
            profile_model.date_of_birth = profile.date_of_birth
        if profile.gender is not None:
            profile_model.gender = profile.gender

        await self.session.flush()
        await self.session.refresh(profile_model)
        return self._to_domain(profile_model)

    async def delete(self, user_id: int) -> bool:
        query = delete(ProfileModel).where(ProfileModel.user_id == user_id)
        res = await self.session.execute(query)
        await self.session.flush()
        return res.rowcount > 0

    def _to_domain(self, profile_model: ProfileModel) -> Profile:
        return Profile(
            id=profile_model.id,
            user_id=profile_model.user_id,
            bio=profile_model.bio,
            avatar_url=profile_model.avatar_url,
            date_of_birth=profile_model.date_of_birth,
            gender=profile_model.gender.value if profile_model.gender else None,
        )

    def _from_domain(self, profile: Profile) -> ProfileModel:
        from sport_network_api.infrastructure.models.profile import GenderEnum

        gender_value = None
        if profile.gender:
            try:
                gender_value = GenderEnum(profile.gender)
            except ValueError:
                gender_value = GenderEnum.MAN

        return ProfileModel(
            bio=profile.bio,
            avatar_url=profile.avatar_url,
            date_of_birth=profile.date_of_birth,
            gender=gender_value,
            user_id=profile.user_id,
        )

