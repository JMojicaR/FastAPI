# After
# Before
# Wrap

from pydantic import BaseModel, model_validator
from typing_extensions import Self

class UserModel(BaseModel):
    username: str
    email: str
    password: str
    password_confirm: str

    """ @model_validator(mode='after')
    def check_email_domain(cls, model: Self) -> Self:
        if not model.email.endswith('@example.com'):
            raise ValueError('Email must be from the domain @example.com')
        return model """

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self
    
user: UserModel = UserModel(
    username='john_doe',
    email='john@example.com',
    password='securepassword',
    password_confirm='securepassword'
)