from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "deals" ALTER COLUMN "status" TYPE VARCHAR(19) USING "status"::VARCHAR(19);
        CREATE TABLE IF NOT EXISTS "disputes" (
    "dispute_id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(128) NOT NULL,
    "description" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deal_id" INT NOT NULL UNIQUE REFERENCES "deals" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "deals" ALTER COLUMN "status" TYPE VARCHAR(19) USING "status"::VARCHAR(19);
        DROP TABLE IF EXISTS "disputes";"""
