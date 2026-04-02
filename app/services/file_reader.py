from pathlib import Path
import fitz
import csv


class FileReaderService:
    @staticmethod
    def extract_text(file_path: Path) -> str:
        suffix = file_path.suffix.lower()

        if suffix == ".txt":
            return FileReaderService._read_txt(file_path)

        elif suffix == ".csv":
            return FileReaderService._read_csv(file_path)

        elif suffix == ".pdf":
            return FileReaderService._read_pdf(file_path)

        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    @staticmethod
    def _read_txt(file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    @staticmethod
    def _read_csv(file_path: Path) -> str:
        rows = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(", ".join(row))
        return "\n".join(rows)

    @staticmethod
    def _read_pdf(file_path: Path) -> str:
        text = []
        pdf = fitz.open(file_path)
        for page in pdf:
            text.append(page.get_text())
        pdf.close()
        return "\n".join(text)