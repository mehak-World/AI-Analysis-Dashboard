const env = require("./env")
const connectDB = require("./database")
const s3 = require("./aws")
const { connectRedis } = require("../infrastructure/redis/client")

module.exports = {
    env,
    connectDB,
    connectRedis,
    s3
}