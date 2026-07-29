const { getRedisClient } = require("./client");

const redis = getRedisClient();

/**
 * Generic cache service.
 *
 * This file provides a clean abstraction over Redis.
 * Other parts of the application should use this
 * instead of calling Redis directly.
 */

const cache = {

    /**
     * Get a value from Redis.
     * Automatically parses JSON if possible.
     */
    async get(key) {
        const value = await redis.get(key);

        if (value === null) {
            return null;
        }

        try {
            return JSON.parse(value);
        } catch {
            return value;
        }
    },

    /**
     * Store a value.
     * Objects are automatically stringified.
     */
    async set(key, value, ttl = null) {
        const data =
            typeof value === "object"
                ? JSON.stringify(value)
                : String(value);

        if (ttl) {
            return redis.set(key, data, "EX", ttl);
        }

        return redis.set(key, data);
    },

    /**
     * Delete a key.
     */
    async del(key) {
        return redis.del(key);
    },

    /**
     * Check if key exists.
     */
    async exists(key) {
        return (await redis.exists(key)) === 1;
    },

    /**
     * Update expiry.
     */
    async expire(key, ttl) {
        return redis.expire(key, ttl);
    },

    /**
     * Remaining TTL.
     */
    async ttl(key) {
        return redis.ttl(key);
    },

    /**
     * Increment numeric value.
     */
    async increment(key) {
        return redis.incr(key);
    },

    /**
     * Decrement numeric value.
     */
    async decrement(key) {
        return redis.decr(key);
    },

    /**
     * Remove all keys.
     * Mainly for development/testing.
     */
    async flush() {
        return redis.flushdb();
    },

};

module.exports = cache;