const { createRateLimiter } = require("./index");

const apiLimiter = createRateLimiter({
    windowMs: 60 * 1000,
    max: 150,
    prefix: "rl:api:",

    message: {
        success: false,
        message: "Too many requests."
    }
});

module.exports = {
    apiLimiter,
};