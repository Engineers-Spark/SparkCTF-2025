const crypto    = require("crypto");

const secret_id = crypto.randomBytes(64).toString("hex");
const todo = db.getSiblingDB('todo');

const ADMIN_PASSWORD = crypto.randomBytes(64).toString("hex");
const DEV_PASSWORD = crypto.randomBytes(64).toString("hex");

const FLAG = process.env.FLAG || "SparkCTF{redacted}"

todo.users.insertOne({ username: "admin@spark.tech", password: ADMIN_PASSWORD });
todo.users.insertOne({ username: "dev@spark.tech", password: DEV_PASSWORD });

todo.notes.insertOne(
    {
        _id: secret_id,
        title: "flag",
        owner: "admin@spark.tech",
        content: FLAG,
        protected: 1
    });

todo.notes.insertMany([
    {
        title: "Trash",
        owner: "dev@spark.tech",
        content: "Take the trash out at 8pm tomorrow",
        protected: 0
    },
    {
        title: "Groceries",
        owner: "dev@spark.tech",
        content: "Buy groceries for next week",
        protected: 0
    }
]);

todo.notes.insertOne(
    {
        title: "My password",
        owner: "dev@spark.tech",
        content: "I keep forgetting my password so I save it here for the meantime, my password is : "+DEV_PASSWORD,
        protected: 1
    }
);
