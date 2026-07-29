const mongoose = require("mongoose")
const env = require("./env")

async function dbConnect() {
  await mongoose.connect(env.MONGO_URL);
  console.log("Mongo Connected");
}

module.exports = dbConnect