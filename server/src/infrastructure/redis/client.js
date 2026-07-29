const Redis = require("ioredis");
const env = require("../../config/env");

let redis = null;

/**
 * Creates (or returns) the singleton Redis client.
 * This does NOT connect to Redis automatically because
 * lazyConnect is enabled.
 */
function getRedisClient() {
    if (redis) {
        return redis;
    }

    redis = new Redis({
        host: env.REDIS_HOST || "127.0.0.1",
        port: Number(env.REDIS_PORT || 6379),
        username: env.REDIS_USERNAME || undefined,
        password: env.REDIS_PASSWORD || undefined,
        db: Number(env.REDIS_DB || 0),

        // We decide when to connect.
        lazyConnect: true,

        // Fail fast if Redis is unavailable.
        enableOfflineQueue: false,

        // Retry failed commands a limited number of times.
        maxRetriesPerRequest: null,

        // Reconnect automatically if the connection drops.
        retryStrategy(times) {
            return Math.min(times * 200, 2000);
        },
    });

    redis.on("connect", () => {
        console.log("🟡 Connecting to Redis...");
    });

    redis.on("ready", () => {
        console.log("✅ Redis is ready.");
    });

    redis.on("error", (error) => {
        console.error("❌ Redis Error:", error.message);
    });

    redis.on("close", () => {
        console.warn("🔌 Redis connection closed.");
    });

    redis.on("reconnecting", () => {
        console.log("♻️ Reconnecting to Redis...");
    });

    return redis;
}

/**
 * Establishes the Redis connection.
 * Should be called once during server startup.
 */
async function connectRedis() {
    const client = getRedisClient();

    if (client.status === "ready") {
        return client;
    }

    if (client.status === "connecting" || client.status === "connect" || client.status === "reconnecting") {
        return client;
    }

    try {
        await client.connect();

        if (client.status === "ready") {
            await client.ping();
        }

        return client;
    } catch (error) {
        console.error("❌ Failed to connect to Redis.");
        throw error;
    }
}

/**
 * Gracefully closes the Redis connection.
 */
async function disconnectRedis() {
    if (redis) {
        await redis.quit();
        redis = null;
    }
}

module.exports = {
    getRedisClient,
    connectRedis,
    disconnectRedis,
};