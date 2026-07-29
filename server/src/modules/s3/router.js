// configure the s3 routes
const express = require("express")
const router = express.Router()
const upload = require("../../middleware/multer")
const controller = require("./controller")

// upload file
router.post("/upload", upload.single("file"), controller.uploadFile);

router.get("/", controller.getFile);

module.exports = router