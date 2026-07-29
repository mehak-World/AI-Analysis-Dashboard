const express = require("express");
const controller = require("./controller");
const upload = require("../../middleware/multer")
const { isAuthenticated } = require("../auth/dependencies")

const router = express.Router();

// Upload file
router.post("/upload", isAuthenticated, upload.single("file"), controller.handleUploadAndAnalyze)

// Get analysis status
router.get("/:sessionId", isAuthenticated, controller.getAnalysis);

module.exports = router;