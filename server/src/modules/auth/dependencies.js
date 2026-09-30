const jwt = require("jsonwebtoken");
const env = require("../../config/env");
const bcrypt = require("bcrypt");
const crypto = require("crypto");
const { ACCESS_BLACKLIST } = require("../../infrastructure/redis/keys");
const cache = require("../../infrastructure/redis/cache");
const CACHE_KEYS = require("../../infrastructure/redis/keys")

const ACCESS_TOKEN_TTL = "15m";
const REFRESH_TOKEN_TTL = 30 * 24 * 60 * 60 * 1000;

const generateTokens = (user, sessionId) => {
    const jti = crypto.randomUUID();
    const payload = {
        id: user._id.toString(),
        email: user.email,
        username: user.username,
        jti
    };

    const refreshPayload = {
        id: user._id.toString(),
        email: user.email,
        username: user.username,
        sessionId
    }

    const accessToken = jwt.sign(payload, env.JWT_SECRET, {
        expiresIn: ACCESS_TOKEN_TTL,
    });

    const refreshToken = jwt.sign(refreshPayload, env.JWT_SECRET, {
        expiresIn: "30d",
    });

    return { accessToken, refreshToken };
};

const hashPassword = async (password) => {
    return bcrypt.hash(password, 10);
};

const verifyPassword = async (plainPassword, hashed) => {
    return bcrypt.compare(plainPassword, hashed);
};

const verifyRefreshToken = (token) => {
    return jwt.verify(token, env.JWT_SECRET)
}

const verifyAccessToken = (token) => {
    return jwt.verify(token, env.JWT_SECRET);
};

const isAuthenticated = async (req, res, next) => {
    try {
        const authHeader = req.headers.authorization;

        if (!authHeader?.startsWith("Bearer ")) {
            return res.status(401).json({
                success: false,
                message: "Authentication required.",
            });
        }

        const accessToken = authHeader.split(" ")[1];
        const payload = verifyAccessToken(accessToken);
        const isBlacklisted = await cache.exists(
            CACHE_KEYS.ACCESS_BLACKLIST(payload.jti)
        );

        if (isBlacklisted) {
            return res.status(401).json({
                success: false,
                message: "Authentication required.",
            });
        }

        req.user = {
            id: payload.id,
            email: payload.email,
            username: payload.username,
            jti: payload.jti,
        };

        next();

    } catch (err) {

        return res.status(401).json({
            success: false,
            message: "Authentication required.",
        });
    }
};


module.exports = {
    generateTokens,
    ACCESS_TOKEN_TTL,
    REFRESH_TOKEN_TTL,
    hashPassword,
    verifyPassword,
    verifyRefreshToken,
    verifyAccessToken,
    isAuthenticated
};