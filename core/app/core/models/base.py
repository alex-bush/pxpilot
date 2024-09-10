from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class BaseDbModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseIdDbModel(BaseDbModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
