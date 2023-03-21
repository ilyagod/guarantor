from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "payments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "status" VARCHAR(7) NOT NULL  DEFAULT 'waiting',
    "currency" VARCHAR(4) NOT NULL,
    "amount" DECIMAL(12,2) NOT NULL,
    "gateway_id" INT NOT NULL REFERENCES "payment_gateways" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "payments"."status" IS 'WAITING: waiting\nSUCCESS: success\nERROR: error';
COMMENT ON COLUMN "payments"."currency" IS 'RUB: RUB\nEUR: EUR\nUSD: USD\nUSDT: USDT';;
        CREATE TABLE IF NOT EXISTS "tron_wallets" (
    "wallet_id" SERIAL NOT NULL PRIMARY KEY,
    "address" TEXT NOT NULL,
    "private_key" TEXT NOT NULL,
    "public_key" TEXT NOT NULL,
    "status" VARCHAR(10) NOT NULL  DEFAULT 'waiting',
    "amount" DECIMAL(12,2) NOT NULL,
    "payment_id" INT NOT NULL UNIQUE REFERENCES "payments" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "tron_wallets"."status" IS 'WAITING: waiting\nRECEIVED: received\nTRANSFERED: transfered';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "payments";
        DROP TABLE IF EXISTS "tron_wallets";"""
