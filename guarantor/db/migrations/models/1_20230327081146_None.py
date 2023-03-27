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
    "price" DOUBLE PRECISION NOT NULL,
    "currency" VARCHAR(4) NOT NULL  DEFAULT 'USDT',
    "status" VARCHAR(19) NOT NULL  DEFAULT 'created',
    "deal_type" VARCHAR(6) NOT NULL  DEFAULT 'common',
    "chat_id" UUID NOT NULL,
    "deadline_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "customer_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "performer_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "deals"."currency" IS 'USDT: USDT';
COMMENT ON COLUMN "deals"."status" IS 'CREATED: created\nDENY_PERFORMER: deny_performer\nWAITING_FOR_PAYMENT: waiting_for_payment\nCONFIRM_PERFORMER: confirm_performer\nCLOSE: close\nARB_CLOSE_CUSTOMER: arb_close_customer\nARB_CLOSE_PERFORMER: arb_close_performer';
COMMENT ON COLUMN "deals"."deal_type" IS 'COMMON: common';
CREATE TABLE IF NOT EXISTS "disputes" (
    "dispute_id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(128) NOT NULL,
    "description" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deal_id" INT NOT NULL UNIQUE REFERENCES "deals" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "payment_gateways" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "logo" TEXT,
    "currency" varchar[] NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "python_service" VARCHAR(32) NOT NULL
);
CREATE TABLE IF NOT EXISTS "payments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "status" VARCHAR(7) NOT NULL  DEFAULT 'waiting',
    "currency" VARCHAR(4) NOT NULL,
    "amount" DECIMAL(12,2) NOT NULL,
    "gateway_id" INT NOT NULL REFERENCES "payment_gateways" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "payments"."status" IS 'WAITING: waiting\nSUCCESS: success\nERROR: error';
COMMENT ON COLUMN "payments"."currency" IS 'USDT: USDT';
CREATE TABLE IF NOT EXISTS "user_corrects" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "amount" DECIMAL(12,2) NOT NULL,
    "currency" VARCHAR(4) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "user_corrects"."currency" IS 'USDT: USDT';
CREATE TABLE IF NOT EXISTS "tron_wallets" (
    "wallet_id" SERIAL NOT NULL PRIMARY KEY,
    "address" TEXT NOT NULL,
    "private_key" TEXT NOT NULL,
    "public_key" TEXT NOT NULL,
    "status" VARCHAR(10) NOT NULL  DEFAULT 'waiting',
    "amount" DECIMAL(12,2) NOT NULL,
    "payment_id" INT NOT NULL UNIQUE REFERENCES "payments" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "tron_wallets"."status" IS 'WAITING: waiting\nRECEIVED: received\nTRANSFERED: transfered';
CREATE TABLE IF NOT EXISTS "chat_messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "message" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deal_id" INT NOT NULL REFERENCES "deals" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
