"""create_subscriptions

Revision ID: 1fab66265d7f
Revises: 
Create Date: 2022-07-08 15:12:56.249569

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "1fab66265d7f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "subscriptions",
        sa.Column("user_id", sa.String(10)),
        sa.Column("feed_url", sa.String(2048)),
        sa.Column("last_check", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "feed_url"),
    )


def downgrade() -> None:
    op.drop_table("subscriptions")
