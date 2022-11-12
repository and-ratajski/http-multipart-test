import * as dotenv from "dotenv";
import express, { Request, Response, Application, NextFunction } from "express";
import formidable from "formidable";

dotenv.config();
const DEV_ENV = "development";
const PROD_ENV = "production";
const PORT = process.env.APP_PORT || 3000;
const UPLOAD_DIR = process.env.UPLOAD_DIR || "/uploads";

const app: Application = express();
app.use(express.json());
app.use(express.static("public"));

app.get("/", (req: Request, res: Response): void => {
  res.redirect("/form.html");
});

app.post("/upload", (req: Request, res: Response, next: NextFunction): void => {
  const form = formidable({
    uploadDir: UPLOAD_DIR,
    maxFileSize: 5 * 1024 * 1024 * 1024, // 5Gb
  });
  form.parse(req, (err, _, files) => {
    if (err) {
      next(err);
      return;
    }
    res.sendFile((files["upload-file"] as any)["filepath"], null, (err) => {
      if (err) {
        return res.end("Error while downloading file.");
      }
    });
  });
});

app.get("/info", (req: Request, res: Response): void => {
  const content = {
    service: process.env.APP_NAME,
    serviceVersion: process.env.APP_VERSION,
    environment:
      process.env.NODE_ENV !== PROD_ENV ? process.env.NODE_ENV : undefined,
  };
  res.status(200).json(content);
});

app.listen(PORT, (): void => {
  console.log(`Server Running here 👉 http://localhost:${PORT}`);
});
