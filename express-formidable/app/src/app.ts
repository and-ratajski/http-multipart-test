import * as dotenv from "dotenv";
import express, { Request, Response, Application } from "express";

dotenv.config();
const DEV_ENV = "development";
const PROD_ENV = "production";
const PORT = process.env.APP_PORT || 3000;

const app: Application = express();
app.use(express.json());
// app.use(express.static("public"));

let appHealth: boolean;

app.get("/", (req: Request, res: Response): void => {
  res.send("Hello World!");
});

app.get("/health", (req: Request, res: Response): void => {
  appHealth ? res.send("OK") : res.send("Not OK");
});

app.listen(PORT, (): void => {
  console.log(`Server Running here 👉 http://localhost:${PORT}`);
});
