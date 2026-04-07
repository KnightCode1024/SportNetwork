from dataclasses import dataclass, field
from datetime import date


@dataclass
class Profile:
    id: int | None = None
    user_id: int | None = None
    bio: str | None = None
    avatar_url: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None

    def update_bio(self, bio: str | None) -> None:
        if bio is not None and len(bio) > 5000:
            raise ValueError("Bio must be 5000 characters or less")
        self.bio = bio

    def set_date_of_birth(self, date_of_birth: date | None) -> None:
        if date_of_birth is not None:
            age = (date.today() - date_of_birth).days // 365
            if age < 14 or age > 120:
                raise ValueError("Age must be between 14 and 120")
        self.date_of_birth = date_of_birth

    @property
    def age(self) -> int | None:
        if self.date_of_birth is None:
            return None
        return (date.today() - self.date_of_birth).days // 365

    def set_avatar(self, avatar_url: str | None) -> None:
        self.avatar_url = avatar_url

    def set_gender(self, gender: str | None) -> None:
        self.gender = gender

