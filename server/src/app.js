const express = require("express");
const helmet = require("helmet");
const cors = require("cors");
const compression = require("compression");
const morgan = require("morgan");
const cookieParser = require("cookie-parser")

const healthRoutes = require("./modules/health/routes");
const s3Routes = require("./modules/s3/router")
const authRoutes = require("./modules/auth/routes")
const analysisRoutes = require("./modules/analysis/routes")

const { apiLimiter } = require("./middleware/rateLimit/apiLimiter");

const app = express();

/**
 * Security
 */
app.use(
    helmet({
        crossOriginResourcePolicy: false,
    })
);

// cors config
app.use(
    cors({
        origin: true,
        credentials: true,
    })
);

// compress request
app.use(compression());

// body parsers
app.use(express.json({ limit: "20mb" }));
app.use(express.urlencoded({ extended: true }));

app.use(cookieParser())

// req logger
app.use(morgan("dev"));

// rate limiting
app.use("/", apiLimiter);

// check app health
app.use("/health", healthRoutes);
app.use("/s3", s3Routes)
app.use("/auth", authRoutes)
app.use("/analyze", analysisRoutes)

// NOT FOUND route -> always at end
app.use((req, res) => {
    return res.status(404).json({
        success: false,
        message: "Route not found",
    });
});

// error handler
app.use((err, req, res, next) => {
    console.error(err);

    return res.status(err.status || 500).json({
        success: false,
        message: err.message || "Internal Server Error",
    });
});

module.exports = app;