from database import Base
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Text, Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

note_tag_association = Table(
    "Note_Tag",
    Base.metadata,
    Column("note_id", String(36), ForeignKey("Note.id")),
    Column("tag_id", String(36), ForeignKey("Tag.id")),
)

class Note(Base):
    __tablename__ = "Note"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    memo_date = Column(String(8), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # back_populates: 태그 객체를 가져올 때 연관된 노트 객체도 모두 가져온다
    tags = relationship("Tag", secondary=note_tag_association, back_populates="notes", lazy="joined")
    
class Tag(Base):
    __tablename__ = "Tag"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # back_populates: 노트 객체를 가져올 때 연관된 태그 객체도 모두 가져온다
    notes = relationship("Note", secondary=note_tag_association, back_populates="tags", lazy="joined")
    
    # back_populates: 모델 간의 양방향 관계를 설정할 때 사용되는 옵션.
    # 두 테이블 간의 관계를 양방향으로 쿼리할 때 사용되며, 한쪽에서 쿼리할 때 다른 쪽의 관련 정보를 쉽게 얻을 수 있다.
    