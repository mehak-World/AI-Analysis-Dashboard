const { Queue } = require("bullmq");

const { getRedisClient } = require("../../infrastructure/redis/client");

const analysisQueue = new Queue("analysis", {
    connection: getRedisClient(),

    defaultJobOptions: {
        attempts: 3,

        backoff: {
            type: "exponential",
            delay: 5000,
        },

        removeOnComplete: {
            age: 3600, // 1 hour
            count: 1000,
        },

        removeOnFail: {
            age: 86400, // 24 hours
            count: 1000,
        },
    },
});

module.exports = analysisQueue;