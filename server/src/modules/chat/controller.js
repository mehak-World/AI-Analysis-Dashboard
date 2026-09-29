const chatService = require("./service");

const chat = async (req, res, next) => {
  try {
    const { sessionId } = req.params;
    const { question } = req.body;

    console.log("session id: ", sessionId);
    console.log("question: ", question);

    const result = await chatService.chat({
      sessionId,
      userId: req.user.id,
      question,
    });

    console.log("chat plan result: ", result)

    return res.status(200).json({
      success: true,
      data: result,
    });
  } catch (err) {
    next(err);
  }
};

module.exports = {
  chat,
};