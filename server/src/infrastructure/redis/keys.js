const RedisKeys = {

    /**
     * Refresh token for a specific user session.
     *
     * auth:refresh:<userId>:<sessionId>
     */
    AUTH_REFRESH(userId, sessionId) {
        return `auth:refresh:${userId}:${sessionId}`;
    },

    /**
     * Sorted set containing all active session IDs for a user.
     *
     * auth:sessions:<userId>
     */
    USER_SESSIONS(userId) {
        return `auth:sessions:${userId}`;
    },

    /**
     * Blacklisted access token (JWT ID).
     *
     * auth:blacklist:<jti>
     */
    ACCESS_BLACKLIST(jti) {
        return `auth:blacklist:${jti}`;
    },

    /**
     * Cache for AI analysis results.
     *
     * ai:analysis:<analysisId>
     */
    AI_ANALYSIS(analysisId) {
        return `ai:analysis:${analysisId}`;
    },

    /**
     * User profile cache.
     *
     * user:<userId>
     */
    USER(userId) {
        return `user:${userId}`;
    },

};

module.exports = RedisKeys;