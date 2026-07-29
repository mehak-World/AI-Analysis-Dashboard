const crypto = require("crypto");

const User = require("./model");

const {
    hashPassword,
    verifyPassword,
    generateTokens,
    REFRESH_TOKEN_TTL,
    verifyRefreshToken,
    verifyAccessToken
} = require("./dependencies");

const cache = require("../../infrastructure/redis/cache");
const CACHE_KEYS = require("../../infrastructure/redis/keys");

const sanitizeUser = (user) => ({
    id: user._id.toString(),
    email: user.email,
    username: user.username,
});

const createSession = async (user) => {
    const sessionId = crypto.randomUUID();
    const { accessToken, refreshToken } = generateTokens(
        user,
        sessionId
    );
    await cache.set(
        CACHE_KEYS.AUTH_REFRESH(user._id.toString(), sessionId),
        refreshToken,
        Math.floor(REFRESH_TOKEN_TTL / 1000)
    );

    return {
        accessToken,
        refreshToken,
    };
};

const registerUser = async ({
    username,
    email,
    password,
}) => {
    const existingUser = await User.findOne({ email });
    if (existingUser) {
        return null;
    }
    const hashedPassword = await hashPassword(password);
    const user = new User({
        username,
        email,
        password: hashedPassword,
    });
    await user.save();
    const tokens = await createSession(user);
    return {
        user: sanitizeUser(user),
        ...tokens,
    };
};

const loginUser = async ({email, password}) => {
    const user = await User.findOne({ email });
    if (!user) {
        return null;
    }

    const isValid = await verifyPassword(
        password,
        user.password
    );

    if (!isValid) {
        return null;
    }

    const tokens = await createSession(user);
    return {
        user: sanitizeUser(user),
        ...tokens,
    };
};

const logout = async (user, accessToken, refreshToken) => {
    const refreshPayload = verifyRefreshToken(refreshToken);
    const accessPayload = verifyAccessToken(accessToken);

    const sessionId = refreshPayload.sessionId;
    const jti = accessPayload.jti;

    // Remove refresh token
    await cache.del(
        CACHE_KEYS.AUTH_REFRESH(user.id, sessionId)
    );

    // Blacklist access token until it expires
    const ttl = accessPayload.exp - Math.floor(Date.now() / 1000);

    if (ttl > 0) {
        await cache.set(
            CACHE_KEYS.ACCESS_BLACKLIST(jti),
            true,
            ttl
        );
    }

};

const generateNewAccessToken = async (refreshToken) => {
    const refreshPayload = verifyRefreshToken(refreshToken);
    const { id, sessionId } = refreshPayload;

    // Check session exists
    const storedRefreshToken = await cache.get(
        CACHE_KEYS.AUTH_REFRESH(id, sessionId)
    );

    if (!storedRefreshToken) {
        throw new Error("Session expired.");
    }

    // Detect refresh token reuse
    if (storedRefreshToken !== refreshToken) {
        await cache.del(CACHE_KEYS.AUTH_REFRESH(id, sessionId));
        throw new Error("Refresh token reuse detected.");
    }

    const user = await User.findById(id);

    if (!user) {
        throw new Error("User not found.");
    }

    const { accessToken } = generateTokens(user, sessionId);
    return accessToken;
};


module.exports = {
    registerUser,
    loginUser,
    logout,
    generateNewAccessToken
};