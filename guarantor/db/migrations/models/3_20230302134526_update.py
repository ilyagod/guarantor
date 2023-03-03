from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "deals" ALTER COLUMN "status" TYPE VARCHAR(23) USING "status"::VARCHAR(23);
        ALTER TABLE "deals" ALTER COLUMN "status" TYPE VARCHAR(23) USING "status"::VARCHAR(23);
        CREATE TABLE IF NOT EXISTS "disputes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(128) NOT NULL,
    "description" TEXT NOT NULL,
    "status" VARCHAR(15) NOT NULL  DEFAULT 'open',
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deal_id" INT NOT NULL UNIQUE REFERENCES "deals" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "disputes"."status" IS 'OPEN: open\nCLOSED_SUCCESS: closed_success\nCLOSED_REJECTED: closed_rejected';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "deals" ALTER COLUMN "status" TYPE VARCHAR(11) USING "status"::VARCHAR(11);
        ALTER TABLE "deals" ALTER COLUMN "status" TYPE VARCHAR(11) USING "status"::VARCHAR(11);
        DROP TABLE IF EXISTS "disputes";"""
