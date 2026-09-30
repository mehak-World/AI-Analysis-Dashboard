const authService = require("./service");
const { REFRESH_TOKEN_TTL } = require("./dependencies");

const isProduction = process.env.NODE_ENV === "production";

const registerUser = async (req, res, next) => {
    try {
        const result = await authService.registerUser(req.body);

        if (!result) {
            return res.status(400).json({
                success: false,
                message: "User with that email already exists.",
            });
        }

        const { user, accessToken, refreshToken } = result;

        res.cookie("refreshToken", refreshToken, {
            httpOnly: true,
            secure: isProduction,
            sameSite: isProduction ? "None" : "Lax",
            maxAge: REFRESH_TOKEN_TTL,
        });

        return res.status(201).json({
            success: true,
            message: "User created successfully",
            data: {
                user,
                accessToken,
            },
        });
    } catch (err) {
        next(err);
    }
};

const loginUser = async (req, res, next) => {
    try {
        const result = await authService.loginUser(req.body);

        if (!result) {
            return res.status(401).json({
                success: false,
                message: "Invalid email or password.",
            });
        }

        const { user, accessToken, refreshToken } = result;

        res.cookie("refreshToken", refreshToken, {
            httpOnly: true,
            secure: isProduction,
            // secure: false,
            // sameSite: isProduction ? "None" : "Lax",
            sameSite: "Lax",
            maxAge: REFRESH_TOKEN_TTL,
        });

        return res.status(200).json({
            success: true,
            message: "User login successful",
            data: {
                user,
                accessToken,
            },
        });
    } catch (err) {
        next(err);
    }
};

const logoutUser = async (req, res, next) => {
    try {
        console.log("cookies: ", req.cookies)
        const refreshToken = req.cookies.refreshToken;
        const authHeader = req.headers.authorization;

        const accessToken = authHeader?.startsWith("Bearer ")
            ? authHeader.split(" ")[1]
            : null;

        if (!refreshToken || !accessToken) {
            return res.status(400).json({
                success: false,
                message: "Missing authentication tokens.",
            });
        }

        await authService.logout(
            req.user,
            accessToken,
            refreshToken
        );

        res.clearCookie("refreshToken");

        return res.json({
            success: true,
            message: "Logged out successfully."
        });

    } catch (err) {
        next(err);
    }
};


const refreshAccessToken = async (req, res) => {
    try {
        const refreshToken = req.cookies.refreshToken;
        console.log("Refresh token from cookie: ", refreshToken);

        if (!refreshToken) {
            return res.status(401).json({
                success: false,
                message: "Refresh token not found.",
            });
        }

        const accessToken = await authService.generateNewAccessToken(refreshToken);

        return res.status(200).json({
            success: true,
            data: {
                accessToken
            },
        });

    } catch (err) {
        return res.status(401).json({
            success: false,
            message: err.message || "Unable to refresh access token.",
        });
    }
};



module.exports = {
    registerUser,
    loginUser,
    logoutUser,
    refreshAccessToken
};