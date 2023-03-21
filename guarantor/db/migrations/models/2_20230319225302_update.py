from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "payment_gateways" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "logo" TEXT,
    "currency" varchar[] NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "python_service" VARCHAR(32) NOT NULL
);;
        CREATE TABLE IF NOT EXISTS "user_corrects" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "amount" DECIMAL(12,2) NOT NULL,
    "currency" VARCHAR(4) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "user_corrects"."currency" IS 'RUB: RUB\nEUR: EUR\nUSD: USD\nUSDT: USDT';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "payment_gateways";
        DROP TABLE IF EXISTS "user_corrects";"""
