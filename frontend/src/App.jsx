import { useMemo, useRef, useState } from "react";
import { uploadImage } from "./api";

const MAX_FILE_SIZE = 5 * 1024 * 1024;

function readableSize(size) {
  return `${(size / (1024 * 1024)).toFixed(2)} MB`;
}

function qualityFromSeverity(score) {
  if (typeof score !== "number") {
    return { label: "Unknown", tone: "neutral" };
  }

  if (score <= 0.25) {
    return { label: "Excellent", tone: "good" };
  }

  if (score <= 0.55) {
    return { label: "Moderate", tone: "fair" };
  }

  return { label: "Needs Attention", tone: "poor" };
}

export default function App() {
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const inputRef = useRef(null);

  const quality = useMemo(() => qualityFromSeverity(result?.severity_score), [result]);
  const confidence = useMemo(() => {
    if (typeof result?.severity_score !== "number") {
      return 0;
    }

    const normalized = Math.max(0, Math.min(1, 1 - result.severity_score));
    return Math.round(normalized * 100);
  }, [result]);

  const onSelectFile = async (file) => {
    if (!file) {
      return;
    }

    if (!file.type.startsWith("image/")) {
      setError("Please upload a valid image file.");
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError(`File is ${readableSize(file.size)}. Max allowed size is 5 MB.`);
      return;
    }

    setError("");
    setResult(null);
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setIsLoading(true);

    try {
      const payload = await uploadImage(file);
      setResult(payload);
    } catch (uploadError) {
      setError(uploadError.message || "Unable to process image right now.");
    } finally {
      setIsLoading(false);
    }
  };

  const onDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    const file = event.dataTransfer.files?.[0];
    onSelectFile(file);
  };

  return (
    <div className="shell">
      <div className="mesh" />
      <main className="layout">
        <section className="hero panel">
          <p className="eyebrow">TrustLens AI</p>
          <h1>Product Verification That Looks Premium And Works Fast</h1>
          <p className="lead">
            Upload a product image and get instant damage analysis, severity score, and price guidance from the Flask + YOLO backend.
          </p>
        </section>

        <section className="panel uploader">
          <div
            className={`dropzone ${isDragging ? "is-dragging" : ""}`}
            onClick={() => inputRef.current?.click()}
            onDragOver={(event) => {
              event.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={onDrop}
          >
            <input
              ref={inputRef}
              type="file"
              accept="image/*"
              onChange={(event) => onSelectFile(event.target.files?.[0])}
              hidden
            />
            <h2>Drop your image here</h2>
            <p>or click to browse • JPG, PNG, JPEG • max 5 MB</p>
          </div>

          <div className="preview-wrap">
            {previewUrl ? <img src={previewUrl} alt="Uploaded product preview" /> : <p className="muted">No image selected yet.</p>}
            {selectedFile && (
              <div className="meta">
                <span>{selectedFile.name}</span>
                <span>{readableSize(selectedFile.size)}</span>
              </div>
            )}
          </div>
        </section>

        <section className="panel result">
          <div className="result-head">
            <h2>Analysis Result</h2>
            {isLoading && <span className="badge loading">Analyzing...</span>}
            {!isLoading && result && <span className={`badge ${quality.tone}`}>{quality.label}</span>}
          </div>

          {error && <p className="error">{error}</p>}

          {!error && !result && !isLoading && <p className="muted">Upload an image to view verification details.</p>}

          {result && !isLoading && (
            <>
              <div className="stats">
                <article>
                  <label>Damage Type</label>
                  <strong>{result.damage_type || "Not detected"}</strong>
                </article>
                <article>
                  <label>Severity Score</label>
                  <strong>{typeof result.severity_score === "number" ? result.severity_score.toFixed(2) : "N/A"}</strong>
                </article>
                <article>
                  <label>Recommended Price</label>
                  <strong>INR {result.recommended_price ?? "N/A"}</strong>
                </article>
                <article>
                  <label>Confidence</label>
                  <strong>{confidence}%</strong>
                </article>
              </div>

              <div className="bar-block">
                <label>Condition Confidence</label>
                <div className="bar">
                  <div className="bar-fill" style={{ width: `${confidence}%` }} />
                </div>
              </div>

              <div className="explanation">
                <h3>Model Explanation</h3>
                <p>{result.explanation || "No explanation returned from backend."}</p>
              </div>

              {Array.isArray(result.detections) && result.detections.length > 0 && (
                <div className="detections">
                  <h3>Detections</h3>
                  <ul>
                    {result.detections.map((detection, index) => (
                      <li key={`${detection.class}-${index}`}>
                        <span>{detection.class}</span>
                        <span>{Math.round((detection.confidence || 0) * 100)}%</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}
        </section>
      </main>
    </div>
  );
}
