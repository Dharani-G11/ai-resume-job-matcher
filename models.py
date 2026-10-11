from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))

    resumes: Mapped[list["Resume"]] = relationship(
        back_populates="user"
    )


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable = True
    )

    user: Mapped["User"] = relationship(
        back_populates="resumes"
    )


class Job(Base):
    __tablename__ = "jobs"

    id:Mapped[int] = mapped_column(primary_key = True)
    title:Mapped[str] = mapped_column(String(255))
    description:Mapped[str]
    user_id:Mapped[int |None] = mapped_column(
        ForeignKey("users.id"),
        nullable = True
    )

class Analysis(Base):
    __tablename__= "analysis"

    id:Mapped[int]=mapped_column(primary_key=True)
    resume_id:Mapped[int]=mapped_column(
        ForeignKey("resumes.id")
    )
    job_id:Mapped[int]=mapped_column(
        ForeignKey("jobs.id")
    )
    result:Mapped[str]