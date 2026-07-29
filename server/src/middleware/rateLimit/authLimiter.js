const { createRateLimiter } = require("./index");

const authLimiter = createRateLimiter({
    windowMs: 15 * 60 * 1000,
    max: 5,
    prefix: "rl:auth:",

    message: {
        success: false,
        message: "Too many login attempts."
    }
});

module.exports = {
    authLimiter,
};