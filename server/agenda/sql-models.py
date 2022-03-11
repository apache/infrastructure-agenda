class TimeStampMixin(object):
    created_on = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.utcnow())
    updated_on = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow())


class SubmitterMixin(object):
    submitter = db.relationship('User')


class VoteState:
    YAY = 1
    NAY = -1
    ABSTAIN = 0


class ItemBase(TimeStampMixin, SubmitterMixin, db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)  # this should be a fk to ci stuff? (PMC or officer)
    text = db.Column(db.Text)


class Approval(TimeStampMixin, SubmitterMixin, db.Model):
    __tablename__ = "approvals"

    id = db.Column(db.Integer, primary_key=True)
    # item_id = ??  # this needs to be a FK to anything that inheris from ItemBase
                    # Concrete Inheritance: https://docs.sqlalchemy.org/en/14/orm/inheritance.html#relationships-with-concrete-inheritance


class Vote(TimeStampMixin, SubmitterMixin, db.model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)


class Comment(TimeStampMixin, SubmitterMixin, db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    submitter = db.relationship('User')
    text = db.Column(db.Text)
    #item_id = ??  # same as above

class Report(ItemBase):
    __tablename__ = "reports"
    
    shepherd = db.relationship('User')  # this needs to be fleshed out more
    flagged = db.Column(db.Boolean)
    #approvals = db.relationship('Approval')
    #comments = db.relationship('Comment')


class Resolution(ItemBase):
    __tablename__ = "resolutions"

    #comments = db.relationship('Comment')
    #votes = db.relationship('Vote')
    # links/commentary  # not sure how this is different from just comments


class TLPResolution(Resolution):
    __tablename__ = "tlp_resolutions"


class AtticTLPResolution(Resolution):
    __tablename__ = "attic_tlp_resolutions"


class ChairChangeResolution(Resolution):
    __tablename__ = "chair_change_resolutions"


class DiscussionItem(ItemBase):
    __tablename__ = "discussion_items"

    # status = ??  # comments
    # carryover ??


class ActionItem(ItemBase):
    __tablename__ = "action_items"

    owner = db.relationship('User')
    report = db.relationship('Report')
    # status = ??  # comments, etc...
