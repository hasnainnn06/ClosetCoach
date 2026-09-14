import express from "express";
import cors from "cors";

const app = express();
app.use(cors());           // VERY IMPORTANT
app.use(express.json());

app.get("/api/health", (req, res) => {
  res.json({ status: "Backend is connected successfully" });
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
