import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = sa.create_engine('sqlite:///:memory:')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class TextItem(Base):
    __tablename__ = 'text_item'
    id = sa.Column(sa.Integer, primary_key=True)

    type = sa.Column(sa.Unicode(255))

    __mapper_args__ = {
        'polymorphic_on': type,
        'with_polymorphic': '*'
    }


class Article(TextItem):
    __tablename__ = 'article'
    id = sa.Column(
        sa.Integer, sa.ForeignKey(TextItem.id), primary_key=True
    )
    __mapper_args__ = {
        'polymorphic_identity': u'article'
    }


class Tag(Base):
    __tablename__ = 'tag'
    id = sa.Column(sa.Integer, primary_key=True)
    text_item_id = sa.Column(sa.Integer, sa.ForeignKey(TextItem.id))


TextItem.tag_count = sa.orm.column_property(
    sa.select(
        [
            sa.func.count('1')
        ],
    )
    .select_from(Tag.__table__)
    .where(Tag.__table__.c.text_item_id == Tag.__table__.c.id)
    .correlate(TextItem.__table__)
    .label('tag_count')
)


print session.query(TextItem).order_by(TextItem.tag_count)
