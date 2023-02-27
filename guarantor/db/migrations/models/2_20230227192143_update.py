from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "deals" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(128) NOT NULL,
    "description" TEXT NOT NULL,
    "price" DECIMAL(12,2) NOT NULL,
    "currency" VARCHAR(3) NOT NULL  DEFAULT 'RUB',
    "status" VARCHAR(11) NOT NULL  DEFAULT 'unconfirmed',
    "customer_id" INT NOT NULL,
    "performer_id" INT NOT NULL,
    "deadline_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "api_client_id" INT NOT NULL REFERENCES "api_clients" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "deals"."currency" IS 'RUB: RUB\nEUR: EUR\nUSD: USD';
COMMENT ON COLUMN "deals"."status" IS 'UNCONFIRMED: unconfirmed\nCONFIRMED: confirmed\nCANCELLED: cancelled\nCOMPLETED: completed';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "deals";"""
