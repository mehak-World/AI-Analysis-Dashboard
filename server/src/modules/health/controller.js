const healthService = require("./service");

async function healthCheck(req, res, next) {
    try {
        const health = await healthService.getHealth();

        return res.status(200).json({
            success: true,
            data: health,
        });
    } catch (err) {
        next(err);
    }
}

module.exports = {
    healthCheck,
};