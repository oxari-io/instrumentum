from __future__ import annotations
"""
    Schemas
"""
import warnings
import secrets
import uuid
import enum
from typing import Union, Literal, ClassVar
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    AnyHttpUrl,
    conlist,
    conint,
    conset,
)
from typing import List, Optional, Union
from datetime import datetime as dt
import datetime


class PlanType(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "grow"
    GROW = "pro"
    FULL = "full"


class LegalDocumentType(str, enum.Enum):
    DLA_STRICT = "dla_strict"
    DLA_STANDARD = "dla_standard"
    SLA = "sla"
    INVOICE = "invoice"


class ScopeEnum(enum.IntEnum):
    SCOPE_1 = 1
    SCOPE_2 = 2
    SCOPE_3 = 3


class User(BaseModel):
    user_id: str = Field(default="default", title="User Id", description="User ID", example="23456-23456-6543-1167")


class UserEmail(User):
    email: EmailStr = Field(title="Email", description="User e-mail address", example="joe.doe@company.com")


class UserCredentials(UserEmail):
    password: str = Field(title="Password", description="User password", example="thepassword")


class UserIdentity(UserCredentials):
    username: str = Field(title="Username", description="Your user name", example="joedoe12")


class UserWithWallet(UserIdentity):
    n_credits: int = Field(title="Number of Credits", description="Your credit budget", example=200)


class JWTToken(BaseModel):
    access_token: str


class DocumentKey(BaseModel):
    order_id: str = Field(title="Order Id", example="9999-9999-99999-999999")
    document_type: LegalDocumentType = Field(
        title="document_type",
        description="Type of legal documents",
        example=LegalDocumentType.SLA,
    )


class UserAddressInformation(BaseModel):
    city: str = Field(example="Las Vegas")
    country: str = Field(example="USA")
    street: str = Field(example="Route-66")
    zip_code: str = Field(example="123456")


class UserContactInformation(BaseModel):
    user_id: Optional[str] = Field(example="0209-1993-1234-1111")
    customer_name: str = Field(example="John Doe")
    phone: str = Field(example="+49 (0)176 666 42 69")
    email: EmailStr = Field(example="John@Doe.de")
    company_name: str = Field(default="", example="Doe Ltd.")
    vat_number: str = Field(default="", example="NL34567654323456765432345", description="Value added tax number")
    coc_number: str = Field(default="", example="NLCOMPANYTEST42", description="Chamber of Commerce number")


class UserInformation(UserAddressInformation, UserContactInformation):
    pass


class OrderInformation(BaseModel):
    order_id: Optional[str] = Field(example="0209-1993-1234-1111")
    user_id: Optional[str] = Field(example="0209-1993-1234-1111")
    plan_type: str = Field(example="grow")
    gross_amount: str = Field(example=5000)
    tax_amount: str = Field(example=950)    
    net_amount: str = Field(example=4050)
    start_date: str = Field(example="69-69-69")
    end_date: str = Field(example="69-69-69")

