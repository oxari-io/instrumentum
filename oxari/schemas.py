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
    user_id: str = Field(default="default", title="User Id", description="User ID", example="23456-23456-6543-3567")


class UserEmail(User):
    email: EmailStr = Field(title="Email", description="User e-mail address", example="o.hundogan@oxari.io")


class UserCredentials(UserEmail):
    password: str = Field(title="Password", description="User password", example="Password123!")


class UserIdentity(UserCredentials):
    username: str = Field(title="Username", description="Your user name", example="ZizekSlavoj")


class UserWithWallet(UserIdentity):
    n_credits: int = Field(title="Number of Credits", description="Your credit budget", example=100)


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
    customer_name: str = Field(example="John Doe")
    company_name: str = Field(default="", example="Doe Ltd.")
    phone: str = Field(example="+49 (0)176 666 42 69")
    email: EmailStr = Field(example="John@Doe.de")
    vat_number: str = Field(default="", example="NL34567654323456765432345", description="Value added tax number")
    coc_number: str = Field(default="", example="NLCOMPANYTEST42", description="Chamber of Commerce number")


class UserInformation(UserAddressInformation, UserContactInformation):
    pass


class OrderInformation(BaseModel):
    order_id: Optional[str] = Field(example="0209-1993-1234-1111")
    user_id: Optional[str] = Field(example="0209-1993-1234-1111")
    service: str = Field(example="grow")
    price: str = Field(example=5000)
    subtotal: str = Field(example=5000)
    netamount: str = Field(example=100)
    unitprice: str = Field(example=5000)
    startdate: str = Field(example="69-69-69")
    enddate: str = Field(example="69-69-69")