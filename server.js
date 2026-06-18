require("dotenv").config();
const express = require("express");
const cors = require("cors");

const connectDB = require("./src/config/db");

const app = express();

app.use(cors());
app.use(express.json());

// conectar banco
connectDB();

app.get("/", (req, res) => {
  res.send("Clinio rodando 🚀");
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log("Servidor rodando na porta " + PORT);
});