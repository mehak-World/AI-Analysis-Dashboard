// Auth routes
const router = require("express").Router();
const validate = require("../../middleware/validator");
const { authLimiter } = require("../../middleware/rateLimit/authLimiter");
const { registerSchema, loginSchema } = require("./validator");
const controller = require("./controller");
const { isAuthenticated } = require("./dependencies");

// Register user
router.post("/register", authLimiter, validate(registerSchema), controller.registerUser);

// Login User
router.post("/login", authLimiter, validate(loginSchema), controller.loginUser);

// Logout user
router.post("/logout", isAuthenticated, controller.logoutUser)

// Refresh token
router.get("/refresh", controller.refreshAccessToken)

// Get current user info
router.get("/me", isAuthenticated, (req, res) => {
    return res.status(200).json({
        success: true,  
        data: {
            id: req.user.id,
            email: req.user.email,
            username: req.user.username,
        }
    });
});

module.exports = router;