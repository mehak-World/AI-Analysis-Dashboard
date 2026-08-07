const express = require("express");

const controller = require("./controller");
const { isAuthenticated } = require("../auth/dependencies");

const router = express.Router();

router.post(
  "/:sessionId",
  isAuthenticated,
  controller.chat
);

module.exports = router;