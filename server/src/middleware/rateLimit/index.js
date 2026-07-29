const rateLimit = require("express-rate-limit");
const { RedisStore } = require("rate-limit-redis");
const { getRedisClient, connectRedis } = require("../../infrastructure/redis/client");

function createRateLimiter({
    windowMs,
    max,
    message,
    prefix,
}) {
    let store;

    try {
        const redisClient = getRedisClient();

        if (redisClient.status === "ready") {
            store = new RedisStore({
                sendCommand: (...args) => redisClient.call(...args),
                prefix,
            });
        } else {
            connectRedis().catch(() => {});
        }
    } catch (error) {
        console.warn("Redis store unavailable, falling back to memory store:", error.message);
    }

    return rateLimit({
        windowMs,
        max,
        standardHeaders: true,
        legacyHeaders: false,
        message,
        ...(store ? { store } : {}),
        skipSuccessfulRequests: false,
    });
}

module.exports = {
    createRateLimiter,
};