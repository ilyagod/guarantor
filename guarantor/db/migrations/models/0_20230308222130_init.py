from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "external_id" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "deals" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(128) NOT NULL,
    "description" TEXT NOT NULL,
    "price" DECIMAL(12,2) NOT NULL,
    "currency" VARCHAR(4) NOT NULL  DEFAULT 'RUB',
    "status" VARCHAR(19) NOT NULL  DEFAULT 'created',
    "deal_type" VARCHAR(6) NOT NULL  DEFAULT 'common',
    "deadline_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "customer_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "performer_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "deals"."currency" IS 'RUB: RUB\nEUR: EUR\nUSD: USD\nUSDT: USDT';
COMMENT ON COLUMN "deals"."status" IS 'CREATED: created\nDENY_PERFORMER: deny_performer\nIN_PROCESS: in_process\nCLOSE: close\nARB_CLOSE_CUSTOMER: arb_close_customer\nARB_CLOSE_PERFORMER: arb_close_performer';
COMMENT ON COLUMN "deals"."deal_type" IS 'COMMON: common';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
