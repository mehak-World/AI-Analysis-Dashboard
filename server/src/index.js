const app = require("./app");

const { env, connectDB, connectRedis } = require("./config");

async function startServer() {

    try {

        await connectDB();
        await connectRedis();

        // Start BullMQ worker
        require("./modules/analysis/worker");

        app.listen(env.PORT, () => {

            console.log(`
======================================
🚀 AI Analysis Server Started
======================================
Environment : ${env.NODE_ENV}
Port        : ${env.PORT}
======================================
            `);

        });

    } catch (error) {

        console.error("Failed to start server");

        console.error(error);

        process.exit(1);

    }

}

startServer();