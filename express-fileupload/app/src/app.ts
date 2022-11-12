import * as dotenv from "dotenv";
import express, { Request, Response, Application } from "express";
import fileUpload, { UploadedFile } from "express-fileupload";

dotenv.config();
const DEV_ENV = "development";
const PROD_ENV = "production";
const PORT = process.env.APP_PORT || 3000;
const UPLOAD_DIR = process.env.UPLOAD_DIR || "/uploads";

const app: Application = express();
app.use(express.json());
app.use(express.static("public"));
app.use(
  fileUpload({
    limits: {
      fileSize: 5 * 1024 * 1024 * 1024, // 5Gb
    },
  })
);

app.get("/", (req: Request, res: Response): void => {
  res.redirect("/form.html");
});

app.post("/upload", (req: Request, res: Response): void => {
  if (!req.files) {
    res.status(400).send("No files were uploaded.");
  }
  const file = req.files!.uploadFile as UploadedFile;

  file.mv(`${UPLOAD_DIR}/${file.name}`, (err) => {
    if (err) {
      console.log(err);
      return res.end("Error while uploading file.");
    }
    // Return uploaded file
    res.sendFile(`${UPLOAD_DIR}/${file.name}`, null, (err) => {
      if (err) {
        console.log(err);
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
