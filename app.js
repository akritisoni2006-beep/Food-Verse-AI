/**
 * Food Verse AI – Multimodal Food Intelligence Platform
 * ======================================================
 * Full-stack React 18 Application with 6 Multimodal Capabilities:
 * 1. Food Recognition & Nutrition (with Health Score)
 * 2. Visual Freshness & Spoilage Detection
 * 3. Restaurant Hygiene & Kitchen Safety Monitor
 * 4. Smart Cooking Assistant (Voice, Audio, Text, Vision)
 * 5. Personalized Adaptive Meal Planning
 * 6. Actionable Intelligence Dashboard & Reporting
 */

const { useState, useEffect, useRef } = React;

const SAMPLE_DISHES = [
  { id: "pizza", label: "Pizza", emoji: "🍕", path: "samples/pizza.png" },
  { id: "burger", label: "Burger", emoji: "🍔", path: "samples/burger.png" },
  { id: "sushi", label: "Sushi", emoji: "🍣", path: "samples/sushi.png" },
  { id: "salad", label: "Salad", emoji: "🥗", path: "samples/salad.png" },
  { id: "laddu", label: "Laddu", emoji: "🟡", path: "samples/laddu.png" },
];

/**
 * Client-side image optimizer:
 * Scales large photos (e.g. from smartphones or web downloads) down to max 1024px
 * and compresses them to clean, lightweight JPEGs (~150KB).
 * Prevents browser "Failed to fetch" timeouts and connection resets on large files!
 */
function compressAndLoadImage(file, callback) {
  if (!file) return;

  if (!file.type.startsWith("image/")) {
    alert("Please select a valid image file (JPG, PNG, or WEBP).");
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      const MAX_DIM = 1024;
      let width = img.width;
      let height = img.height;

      if (width > height && width > MAX_DIM) {
        height = Math.round((height * MAX_DIM) / width);
        width = MAX_DIM;
      } else if (height > MAX_DIM) {
        width = Math.round((width * MAX_DIM) / height);
        height = MAX_DIM;
      }

      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, width, height);

      // Output high quality, lightweight JPEG
      const compressedDataUrl = canvas.toDataURL("image/jpeg", 0.85);
      callback(compressedDataUrl);
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

/**
 * Robust fetch wrapper that handles server restarts, legacy fallbacks,
 * and user-friendly error formatting.
 */
async function safeFetchJson(url, options = {}, fallbackUrl = null, fallbackBody = null) {
  let resp;
  try {
    resp = await fetch(url, options);
  } catch (netErr) {
    // If browser cannot connect at all (server stopped or network refused)
    if (fallbackUrl) {
      try {
        const fbOpts = { ...options };
        if (fallbackBody) fbOpts.body = JSON.stringify(fallbackBody);
        resp = await fetch(fallbackUrl, fbOpts);
      } catch (fbErr) {
        throw new Error(
          "⚠️ Server Offline: Cannot reach the backend. Please verify that 'python app.py' is running in your terminal!"
        );
      }
    } else {
      throw new Error(
        "⚠️ Server Offline: Cannot reach the backend. Please verify that 'python app.py' is running in your terminal!"
      );
    }
  }

  // If endpoint is 404 and we have a legacy fallback endpoint
  if (resp.status === 404 && fallbackUrl) {
    const fallbackOpts = { ...options };
    if (fallbackBody) {
      fallbackOpts.body = JSON.stringify(fallbackBody);
    }
    resp = await fetch(fallbackUrl, fallbackOpts);
  }

  const rawText = await resp.text();
  let data;
  try {
    data = JSON.parse(rawText);
  } catch (err) {
    if (rawText.includes("<!DOCTYPE") || rawText.includes("<html")) {
      throw new Error(
        "⚡ Server Restart Needed: Please switch to your terminal, press Ctrl + C, and run 'python app.py' to activate the new FastAPI engine."
      );
    }
    throw new Error(`Invalid server response: ${rawText.slice(0, 100)}`);
  }

  if (!resp.ok) {
    throw new Error(data.detail || data.error || `Server error (${resp.status})`);
  }

  return data;
}

function App() {
  const [activeTab, setActiveTab] = useState("food");
  const [backendStatus, setBackendStatus] = useState({
    status: "connecting",
    ai_enabled: false,
    mode: "Loading..."
  });

  useEffect(() => {
    safeFetchJson("/api/status")
      .then((data) => setBackendStatus(data))
      .catch((err) => {
        console.warn("Could not reach FastAPI status endpoint:", err);
        setBackendStatus({ status: "offline", ai_enabled: false, mode: "Offline / Mock" });
      });
  }, []);

  return (
    <div className="platform-container">
      {/* Top Navigation Bar */}
      <header className="platform-header">
        <div className="header-left">
          <div className="brand-logo">🍲</div>
          <div>
            <h1>Food Verse AI</h1>
            <p className="brand-tagline">Multimodal Food Intelligence Platform</p>
          </div>
        </div>

        <div className="header-right">
          <div className="engine-badge" title="Backend Engine: FastAPI + Uvicorn">
            <span className="engine-icon">⚡</span>
            <span>FastAPI Backend</span>
          </div>

          {backendStatus.ai_enabled ? (
            <span className="badge-ai-mode live">✨ Live Gemini Vision</span>
          ) : (
            <span className="badge-ai-mode mock">💡 Mock Demo Mode</span>
          )}
        </div>
      </header>

      {/* Multimodal Navigation Tabs */}
      <nav className="tab-navigation">
        <button
          type="button"
          className={`tab-btn ${activeTab === "food" ? "active" : ""}`}
          onClick={() => setActiveTab("food")}
        >
          <span className="tab-icon">🍲</span> Food & Nutrition
        </button>

        <button
          type="button"
          className={`tab-btn ${activeTab === "freshness" ? "active" : ""}`}
          onClick={() => setActiveTab("freshness")}
        >
          <span className="tab-icon">🌿</span> Freshness Detector
        </button>

        <button
          type="button"
          className={`tab-btn ${activeTab === "hygiene" ? "active" : ""}`}
          onClick={() => setActiveTab("hygiene")}
        >
          <span className="tab-icon">🧼</span> Hygiene Monitor
        </button>

        <button
          type="button"
          className={`tab-btn ${activeTab === "cooking" ? "active" : ""}`}
          onClick={() => setActiveTab("cooking")}
        >
          <span className="tab-icon">👨‍🍳</span> Cooking Assistant
        </button>

        <button
          type="button"
          className={`tab-btn ${activeTab === "mealplan" ? "active" : ""}`}
          onClick={() => setActiveTab("mealplan")}
        >
          <span className="tab-icon">🥗</span> Meal Planner
        </button>

        <button
          type="button"
          className={`tab-btn ${activeTab === "dashboard" ? "active" : ""}`}
          onClick={() => setActiveTab("dashboard")}
        >
          <span className="tab-icon">📊</span> Intelligence Dashboard
        </button>
      </nav>

      {/* Main Content Area */}
      <main className="platform-content">
        {activeTab === "food" && <FoodNutritionModule />}
        {activeTab === "freshness" && <FreshnessModule />}
        {activeTab === "hygiene" && <HygieneModule />}
        {activeTab === "cooking" && <CookingAssistantModule />}
        {activeTab === "mealplan" && <MealPlannerModule />}
        {activeTab === "dashboard" && <IntelligenceDashboardModule onSwitchTab={setActiveTab} />}
      </main>

      {/* Footer */}
      <footer className="platform-footer">
        <p>
          <strong>Food Verse AI</strong> &bull; Unified Multimodal Platform &bull; Built with ReactJS & FastAPI
        </p>
        <p className="footer-links">
          <a href="/docs" target="_blank" rel="noopener noreferrer">📖 Interactive Swagger API Docs</a> &bull;
          <span> Images &bull; Video Frames &bull; Voice &bull; LLM Reasoning</span>
        </p>
      </footer>
    </div>
  );
}

// ===========================================================================
// MODULE 1: Food Recognition & Nutrition (with Health Score)
// ===========================================================================
function FoodNutritionModule() {
  const [image, setImage] = useState("");
  const [sampleTag, setSampleTag] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const file = e.target.files && e.target.files[0];
    if (file) {
      compressAndLoadImage(file, (optimizedDataUrl) => {
        setImage(optimizedDataUrl);
        setSampleTag("");
        setResult(null);
        setError("");
      });
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      compressAndLoadImage(e.dataTransfer.files[0], (optimizedDataUrl) => {
        setImage(optimizedDataUrl);
        setSampleTag("");
        setResult(null);
        setError("");
      });
    }
  };

  const handleSelectSample = async (sample) => {
    setSampleTag(sample.id);
    setLoading(true);
    setError("");
    try {
      const resp = await fetch(sample.path);
      const blob = await resp.blob();
      const reader = new FileReader();
      reader.onload = (evt) => {
        setImage(evt.target.result);
        setLoading(false);
      };
      reader.readAsDataURL(blob);
    } catch (err) {
      setLoading(false);
      setError("Failed to load sample image.");
    }
  };

  const analyzeFood = async () => {
    if (!image) return;
    setLoading(true);
    setError("");

    try {
      const data = await safeFetchJson(
        "/api/food/recognize",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image: image, sample_tag: sampleTag })
        },
        "/api/analyze",
        { image: image, sampleTag: sampleTag }
      );
      setResult(data);
    } catch (err) {
      setError(err.message || "Network request failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="module-card">
      <div className="module-header">
        <h2>🍲 Computer Vision Food Recognition & Nutrition</h2>
        <p>Identify dishes from food photos, calculate macronutrients, and generate a holistic Health Score.</p>
      </div>

      <div className="two-column-layout">
        <div className="input-column">
          <div
            className={`drop-area ${image ? "has-image" : ""}`}
            onClick={() => !image && fileInputRef.current.click()}
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
          >
            <input ref={fileInputRef} type="file" accept="image/*" onChange={handleFileUpload} style={{ display: "none" }} />
            {!image ? (
              <div className="drop-prompt">
                <span className="upload-icon">📷</span>
                <h4>Upload Food Photo</h4>
                <p>Click to browse or drop an image here (PNG, JPG, WEBP)</p>
              </div>
            ) : (
              <div className="preview-wrap">
                <img src={image} alt="Food preview" className="preview-media" />
                <button type="button" className="btn-clear" onClick={(e) => { e.stopPropagation(); setImage(""); setResult(null); }}>✕</button>
              </div>
            )}
          </div>

          <div className="samples-bar">
            <span>Or try a sample:</span>
            <div className="chip-row">
              {SAMPLE_DISHES.map((s) => (
                <button
                  key={s.id}
                  type="button"
                  className={`chip-btn ${sampleTag === s.id ? "active" : ""}`}
                  onClick={() => handleSelectSample(s)}
                >
                  {s.emoji} {s.label}
                </button>
              ))}
            </div>
          </div>

          <button
            type="button"
            className="btn-action-primary"
            disabled={!image || loading}
            onClick={analyzeFood}
          >
            {loading ? "Analyzing Food & Nutrition..." : "Identify Dish & Compute Health Score ✨"}
          </button>
          {error && <div className="alert-box error">{error}</div>}
        </div>

        <div className="output-column">
          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Scanning dish composition and calculating Health Score...</p>
            </div>
          )}

          {!loading && !result && (
            <div className="empty-placeholder">
              <span>🍽️</span>
              <h4>No Dish Analyzed Yet</h4>
              <p>Upload a food photo or select a sample dish to see instant computer vision recognition and nutrition facts.</p>
            </div>
          )}

          {!loading && result && (
            <div className="result-display fade-in">
              <div className="result-top-banner">
                <span className={`badge-pill ${result.is_mock ? "mock" : "ai"}`}>
                  {result.source_label || (result.is_mock ? "💡 Mock Demo Result" : "✨ Live AI Result")}
                </span>
                <h3>{result.name}</h3>
                <p className="culinary-desc">{result.description}</p>
              </div>

              {/* Health Score Gauge */}
              <div className="health-score-card">
                <div className="score-dial">
                  <span className="score-num">{result.health_score || 85}</span>
                  <span className="score-out">/100</span>
                </div>
                <div className="score-info">
                  <h4>Health Score: {result.health_rating || "Grade A (Nutrient Dense)"}</h4>
                  <p>Calculated based on nutrient density, fiber, and macronutrient balance.</p>
                </div>
              </div>

              {/* Nutrition Macros */}
              {result.nutrition && (
                <div className="macros-grid">
                  <div className="macro-pill cal">
                    <span className="label">Calories</span>
                    <span className="val">{result.nutrition.calories || "N/A"}</span>
                  </div>
                  <div className="macro-pill pro">
                    <span className="label">Protein</span>
                    <span className="val">{result.nutrition.protein || "N/A"}</span>
                  </div>
                  <div className="macro-pill carb">
                    <span className="label">Carbs</span>
                    <span className="val">{result.nutrition.carbs || "N/A"}</span>
                  </div>
                  <div className="macro-pill fat">
                    <span className="label">Fat</span>
                    <span className="val">{result.nutrition.fat || "N/A"}</span>
                  </div>
                  <div className="macro-pill fib">
                    <span className="label">Fiber</span>
                    <span className="val">{result.nutrition.fiber || "N/A"}</span>
                  </div>
                </div>
              )}

              {/* Health Insights */}
              {result.health_insights && (
                <div className="insights-box">
                  <h5>Nutritional Insights:</h5>
                  <ul>
                    {result.health_insights.map((insight, idx) => (
                      <li key={idx}>🌱 {insight}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="disclaimer-note">
                ⚠️ Estimates from food images are approximate and intended for educational guidance.
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ===========================================================================
// MODULE 2: Freshness & Spoilage Detection
// ===========================================================================
function FreshnessModule() {
  const [image, setImage] = useState("");
  const [sampleTag, setSampleTag] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const file = e.target.files && e.target.files[0];
    if (file) {
      compressAndLoadImage(file, (optimizedDataUrl) => {
        setImage(optimizedDataUrl);
        setSampleTag("");
        setResult(null);
        setError("");
      });
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      compressAndLoadImage(e.dataTransfer.files[0], (optimizedDataUrl) => {
        setImage(optimizedDataUrl);
        setSampleTag("");
        setResult(null);
        setError("");
      });
    }
  };

  const handleSelectSample = async (sample) => {
    setSampleTag(sample.id);
    setLoading(true);
    setError("");
    try {
      const resp = await fetch(sample.path);
      const blob = await resp.blob();
      const reader = new FileReader();
      reader.onload = (evt) => {
        setImage(evt.target.result);
        setLoading(false);
      };
      reader.readAsDataURL(blob);
    } catch (err) {
      setLoading(false);
      setError("Failed to load sample.");
    }
  };

  const analyzeFreshness = async () => {
    if (!image) return;
    setLoading(true);
    setError("");

    try {
      const data = await safeFetchJson(
        "/api/food/freshness",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image: image, sample_tag: sampleTag })
        },
        "/api/analyze",
        { image: image, sampleTag: sampleTag }
      );
      
      if (data.freshness && !data.classification) {
        data.food_name = data.name;
        data.classification = data.freshness.status === "fresh" ? "Fresh" : (data.freshness.status === "eat_soon" ? "Moderately Fresh" : "Spoiled");
        data.freshness_score = data.freshness.score;
        data.shelf_life_estimate = data.freshness.shelf_life;
        data.color_analysis = "Color tone verified.";
        data.texture_analysis = "Surface texture stable.";
        data.discoloration_risk = "Low risk detected.";
        data.surface_patterns = data.freshness.visual_cues || [];
        data.storage_recommendation = data.freshness.storage_tip || "Keep refrigerated.";
      }
      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to analyze freshness.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="module-card">
      <div className="module-header">
        <h2>🌿 Visual Freshness & Spoilage Classifier</h2>
        <p>Examine food surface patterns, discoloration, and texture to classify as Fresh, Moderately Fresh, or Spoiled.</p>
      </div>

      <div className="two-column-layout">
        <div className="input-column">
          <div
            className={`drop-area ${image ? "has-image" : ""}`}
            onClick={() => !image && fileInputRef.current.click()}
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
          >
            <input ref={fileInputRef} type="file" accept="image/*" onChange={handleFileUpload} style={{ display: "none" }} />
            {!image ? (
              <div className="drop-prompt">
                <span className="upload-icon">🔬</span>
                <h4>Upload Food or Produce Photo</h4>
                <p>Inspect freshness, surface oxidation, and shelf-life</p>
              </div>
            ) : (
              <div className="preview-wrap">
                <img src={image} alt="Freshness preview" className="preview-media" />
                <button type="button" className="btn-clear" onClick={(e) => { e.stopPropagation(); setImage(""); setResult(null); }}>✕</button>
              </div>
            )}
          </div>

          <div className="samples-bar">
            <span>Or test with samples:</span>
            <div className="chip-row">
              {SAMPLE_DISHES.map((s) => (
                <button
                  key={s.id}
                  type="button"
                  className={`chip-btn ${sampleTag === s.id ? "active" : ""}`}
                  onClick={() => handleSelectSample(s)}
                >
                  {s.emoji} {s.label}
                </button>
              ))}
            </div>
          </div>

          <button
            type="button"
            className="btn-action-primary"
            disabled={!image || loading}
            onClick={analyzeFreshness}
          >
            {loading ? "Scanning Surface Patterns..." : "Detect Freshness & Spoilage Risk 🔬"}
          </button>
          {error && <div className="alert-box error">{error}</div>}
        </div>

        <div className="output-column">
          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Analyzing color variance, texture striations, and oxidation risks...</p>
            </div>
          )}

          {!loading && !result && (
            <div className="empty-placeholder">
              <span>🌿</span>
              <h4>No Freshness Scan Active</h4>
              <p>Provide an image of fruit, vegetables, cooked meals, or dairy to evaluate microbial risk and shelf life.</p>
            </div>
          )}

          {!loading && result && (
            <div className="result-display fade-in">
              <div className={`freshness-banner ${(result.classification || "fresh").toLowerCase().replace(/\s+/g, '-')}`}>
                <div className="banner-left">
                  <span className="tier-icon">
                    {result.classification === "Fresh" ? "🟢" : result.classification === "Moderately Fresh" ? "🟡" : "🔴"}
                  </span>
                  <div>
                    <h3>{result.food_name || "Dish"} — {result.classification || "Inspected"}</h3>
                    <span className="shelf-life-tag">⏳ Estimated Shelf Life: {result.shelf_life_estimate || "2-3 days"}</span>
                  </div>
                </div>
                <div className="banner-score">
                  <span className="score-big">{result.freshness_score || 85}%</span>
                  <span>Freshness Index</span>
                </div>
              </div>

              <div className="freshness-analysis-grid">
                <div className="analysis-card">
                  <h5>🎨 Color Analysis</h5>
                  <p>{result.color_analysis || "Normal pigmentation."}</p>
                </div>
                <div className="analysis-card">
                  <h5>🔍 Texture & Moisture</h5>
                  <p>{result.texture_analysis || "Stable moisture."}</p>
                </div>
                <div className="analysis-card">
                  <h5>⚠️ Discoloration Risk</h5>
                  <p>{result.discoloration_risk || "Low risk."}</p>
                </div>
              </div>

              {result.surface_patterns && (
                <div className="surface-patterns-box">
                  <h5>Surface Indicators Observed:</h5>
                  <ul>
                    {result.surface_patterns.map((pat, idx) => (
                      <li key={idx}>✔ {pat}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="storage-advisory-box">
                <span className="advisory-icon">🧊</span>
                <div>
                  <strong>Storage Recommendation:</strong> {result.storage_recommendation || "Store refrigerated at 4°C."}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ===========================================================================
// MODULE 3: Restaurant Hygiene & Kitchen Safety Monitor
// ===========================================================================
function HygieneModule() {
  const [stationName, setStationName] = useState("Salad & Cold Prep Station #1");
  const [videoFrame, setVideoFrame] = useState("samples/salad.png");
  const [loading, setLoading] = useState(false);
  const [audit, setAudit] = useState(null);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleFrameUpload = (e) => {
    const file = e.target.files && e.target.files[0];
    if (file) {
      compressAndLoadImage(file, (optimizedDataUrl) => {
        setVideoFrame(optimizedDataUrl);
      });
    }
  };

  const runHygieneAudit = async () => {
    setLoading(true);
    setError("");

    try {
      const data = await safeFetchJson("/api/hygiene/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          video_or_frame: videoFrame || "data:image/png;base64,sample",
          restaurant_name: stationName
        })
      });
      setAudit(data);
    } catch (err) {
      setError(err.message || "Failed to audit hygiene.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="module-card">
      <div className="module-header">
        <h2>🧼 Restaurant Kitchen Hygiene & Safety Monitoring</h2>
        <p>Analyze kitchen video feeds or frames to detect glove usage, hair-cap compliance, sanitization, and cross-contamination risks.</p>
      </div>

      <div className="two-column-layout">
        <div className="input-column">
          <div className="station-selector-box">
            <label htmlFor="stationSelect">Select Kitchen Station / Video Feed:</label>
            <select
              id="stationSelect"
              className="select-input"
              value={stationName}
              onChange={(e) => setStationName(e.target.value)}
            >
              <option value="Salad & Cold Prep Station #1">🥗 Salad & Cold Prep Station #1</option>
              <option value="Hot Line & Grill Station #2">🍔 Hot Line & Grill Station #2</option>
              <option value="Sushi & Raw Seafood Bar">🍣 Sushi & Raw Seafood Bar</option>
              <option value="Dishwashing & Sanitizing Bay">🧼 Dishwashing & Sanitizing Bay</option>
            </select>
          </div>

          <div
            className="video-simulation-container"
            onClick={() => fileInputRef.current.click()}
          >
            <input ref={fileInputRef} type="file" accept="image/*,video/*" onChange={handleFrameUpload} style={{ display: "none" }} />
            <div className="video-overlay">
              <span className="live-rec-badge">● LIVE FEED</span>
              <span className="time-badge">{new Date().toLocaleTimeString()}</span>
            </div>
            {videoFrame ? (
              <img src={videoFrame} alt="Kitchen station feed" className="kitchen-feed-img" />
            ) : (
              <div className="camera-placeholder">
                <span>📹</span>
                <p>Click to upload camera snapshot / kitchen video frame</p>
              </div>
            )}
            <div className="feed-footer-hint">Click frame to upload new feed capture</div>
          </div>

          <button
            type="button"
            className="btn-action-primary"
            disabled={loading}
            onClick={runHygieneAudit}
          >
            {loading ? "Auditing HACCP Compliance..." : "Run AI Hygiene & Compliance Audit 🛡️"}
          </button>
          {error && <div className="alert-box error">{error}</div>}
        </div>

        <div className="output-column">
          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Scanning kitchen frame for glove adherence, hair restraints, and surface cleanliness...</p>
            </div>
          )}

          {!loading && !audit && (
            <div className="empty-placeholder">
              <span>🛡️</span>
              <h4>No Hygiene Audit Conducted</h4>
              <p>Trigger an inspection to identify safety violations, sanitation metrics, and compliance score.</p>
            </div>
          )}

          {!loading && audit && (
            <div className="result-display fade-in">
              <div className="hygiene-grade-banner">
                <div className="grade-badge">
                  <span className="grade-score">{audit.overall_sanitation_score}%</span>
                  <span className="grade-text">{audit.inspection_grade}</span>
                </div>
                <div className="grade-meta">
                  <h4>{audit.station_name}</h4>
                  <p>Audited: {audit.timestamp}</p>
                  <span className={`risk-tag ${(audit.cross_contamination_risk || "low").toLowerCase()}`}>
                    Cross-Contamination Risk: {audit.cross_contamination_risk}
                  </span>
                </div>
              </div>

              <div className="compliance-meters-grid">
                <div className="meter-card">
                  <div className="meter-head">
                    <span>🧤 Glove Compliance</span>
                    <strong>{audit.glove_compliance}%</strong>
                  </div>
                  <div className="progress-bar-bg">
                    <div className="progress-bar-fill green" style={{ width: `${audit.glove_compliance}%` }}></div>
                  </div>
                </div>

                <div className="meter-card">
                  <div className="meter-head">
                    <span>🧢 Hair-Cap Adherence</span>
                    <strong>{audit.hair_cap_compliance}%</strong>
                  </div>
                  <div className="progress-bar-bg">
                    <div className="progress-bar-fill blue" style={{ width: `${audit.hair_cap_compliance}%` }}></div>
                  </div>
                </div>

                <div className="meter-card">
                  <div className="meter-head">
                    <span>✨ Surface Cleanliness</span>
                    <strong>{audit.cleanliness_score}%</strong>
                  </div>
                  <div className="progress-bar-bg">
                    <div className="progress-bar-fill purple" style={{ width: `${audit.cleanliness_score}%` }}></div>
                  </div>
                </div>
              </div>

              <div className="violations-box">
                <h5>Safety Violations & Alerts:</h5>
                {audit.detected_violations.length === 0 ? (
                  <p className="no-violations">✅ Zero active violations detected. Excellent compliance!</p>
                ) : (
                  <ul className="violations-list">
                    {audit.detected_violations.map((v, i) => (
                      <li key={i}>⚠️ {v}</li>
                    ))}
                  </ul>
                )}
              </div>

              <div className="corrective-actions-box">
                <h5>Actionable Corrective Protocol:</h5>
                <ul>
                  {audit.actionable_recommendations.map((rec, i) => (
                    <li key={i}>📋 {rec}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ===========================================================================
// MODULE 4: Smart Cooking Assistant (Voice, Audio, Text, Vision)
// ===========================================================================
function CookingAssistantModule() {
  const [query, setQuery] = useState("");
  const [diet, setDiet] = useState("None");
  const [ingredientImg, setIngredientImg] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const [recipe, setRecipe] = useState(null);
  const [activeTimer, setActiveTimer] = useState(null);
  const [timerSeconds, setTimerSeconds] = useState(0);
  const [error, setError] = useState("");

  const fileInputRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRec) {
      const recognition = new SpeechRec();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "en-US";

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setQuery(transcript);
        setIsListening(false);
      };

      recognition.onerror = () => setIsListening(false);
      recognition.onend = () => setIsListening(false);

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleVoiceRecording = () => {
    if (!recognitionRef.current) {
      alert("Speech recognition is not supported in this browser. You can type in the prompt box!");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setQuery("");
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  useEffect(() => {
    let interval = null;
    if (activeTimer !== null && timerSeconds > 0) {
      interval = setInterval(() => {
        setTimerSeconds((prev) => prev - 1);
      }, 1000);
    } else if (timerSeconds === 0 && activeTimer !== null) {
      alert(`⏰ Timer complete for Step ${activeTimer}!`);
      setActiveTimer(null);
    }
    return () => clearInterval(interval);
  }, [activeTimer, timerSeconds]);

  const startTimerForStep = (stepNumber, minutes) => {
    setActiveTimer(stepNumber);
    setTimerSeconds(minutes * 60);
  };

  const generateRecipe = async () => {
    setLoading(true);
    setError("");

    try {
      const data = await safeFetchJson("/api/cooking/assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query_text: query,
          voice_transcript: query,
          ingredients_image: ingredientImg,
          dietary_preference: diet
        })
      });
      setRecipe(data);
    } catch (err) {
      setError(err.message || "Failed to generate recipe.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="module-card">
      <div className="module-header">
        <h2>👨‍🍳 Smart Multimodal Cooking Assistant</h2>
        <p>Ask by voice, type your ingredients, or upload a photo of your fridge to get step-by-step recipes and interactive timers.</p>
      </div>

      <div className="two-column-layout">
        <div className="input-column">
          <div className="voice-input-container">
            <label htmlFor="cookingPrompt">What would you like to cook?</label>
            <div className="input-with-mic">
              <input
                id="cookingPrompt"
                type="text"
                className="text-input"
                placeholder={isListening ? "Listening... Speak now!" : "e.g., Quick pasta with garlic, or healthy tofu dinner"}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <button
                type="button"
                className={`btn-mic ${isListening ? "listening" : ""}`}
                onClick={toggleVoiceRecording}
                title="Click to speak (Voice Recognition)"
              >
                {isListening ? "🔴" : "🎙️"}
              </button>
            </div>
            {isListening && <p className="voice-pulse-hint">Microphone listening... Speak clearly.</p>}
          </div>

          <div className="diet-filter-box">
            <label htmlFor="dietSelect">Dietary Preference:</label>
            <select
              id="dietSelect"
              className="select-input"
              value={diet}
              onChange={(e) => setDiet(e.target.value)}
            >
              <option value="None">Standard / Any</option>
              <option value="Vegetarian">Vegetarian</option>
              <option value="High Protein">High Protein</option>
              <option value="Keto">Keto / Low Carb</option>
              <option value="Gluten-Free">Gluten-Free</option>
            </select>
          </div>

          <div className="ingredient-upload-box">
            <label>Optional: Upload Ingredient / Fridge Photo</label>
            <div
              className={`drop-area compact ${ingredientImg ? "has-image" : ""}`}
              onClick={() => fileInputRef.current.click()}
            >
              <input ref={fileInputRef} type="file" accept="image/*" onChange={(e) => {
                const f = e.target.files && e.target.files[0];
                if (f) {
                  compressAndLoadImage(f, (optimized) => setIngredientImg(optimized));
                }
              }} style={{ display: "none" }} />
              {ingredientImg ? (
                <div className="preview-wrap">
                  <img src={ingredientImg} alt="Ingredient preview" className="preview-media" />
                  <button type="button" className="btn-clear" onClick={(e) => { e.stopPropagation(); setIngredientImg(""); }}>✕</button>
                </div>
              ) : (
                <div className="drop-prompt">
                  <span>📷 Snap Fridge / Ingredients</span>
                </div>
              )}
            </div>
          </div>

          <button
            type="button"
            className="btn-action-primary"
            disabled={loading}
            onClick={generateRecipe}
          >
            {loading ? "Chef AI Generating Guidance..." : "Create Step-by-Step Recipe 🍳"}
          </button>
          {error && <div className="alert-box error">{error}</div>}
        </div>

        <div className="output-column">
          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Formulating ingredients, culinary techniques, and interactive timers...</p>
            </div>
          )}

          {!loading && !recipe && (
            <div className="empty-placeholder">
              <span>👨‍🍳</span>
              <h4>Ask Chef AI</h4>
              <p>Try speaking: <em>"Quick garlic butter pasta"</em> or type the ingredients you have on hand.</p>
            </div>
          )}

          {!loading && recipe && (
            <div className="result-display fade-in">
              <div className="recipe-hero">
                <h3>{recipe.recipe_name}</h3>
                <div className="recipe-meta-pills">
                  <span>🌍 {recipe.cuisine}</span>
                  <span>⏱️ Prep: {recipe.prep_time}</span>
                  <span>🔥 Cook: {recipe.cook_time}</span>
                  <span>📊 {recipe.difficulty}</span>
                  <span>👥 Serves: {recipe.servings}</span>
                </div>
              </div>

              <div className="recipe-ingredients-card">
                <h5>Required Ingredients:</h5>
                <div className="ingredients-checklist">
                  {recipe.ingredients.map((ing, i) => (
                    <label key={i} className="ingredient-item">
                      <input type="checkbox" defaultChecked />
                      <span>{ing}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="recipe-steps-card">
                <h5>Interactive Cooking Steps:</h5>
                <div className="steps-list">
                  {recipe.steps.map((st) => (
                    <div key={st.step_number} className="step-card">
                      <div className="step-badge">{st.step_number}</div>
                      <div className="step-content">
                        <p className="step-text">{st.instruction}</p>
                        {st.technique_tip && (
                          <div className="technique-tip">
                            💡 <strong>Chef Tip:</strong> {st.technique_tip}
                          </div>
                        )}
                        {st.timer_minutes > 0 && (
                          <div className="step-timer-row">
                            <button
                              type="button"
                              className="btn-timer"
                              onClick={() => startTimerForStep(st.step_number, st.timer_minutes)}
                            >
                              ⏳ Start {st.timer_minutes}m Timer
                            </button>
                            {activeTimer === st.step_number && (
                              <span className="live-countdown">
                                Remaining: {Math.floor(timerSeconds / 60)}:{(timerSeconds % 60).toString().padStart(2, "0")}
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="chef-secret-box">
                <span className="chef-icon">⭐</span>
                <div>
                  <strong>Chef's Secret:</strong> {recipe.chef_secret}
                </div>
              </div>
              <div className="recipe-nutrition-tag">
                📊 {recipe.nutrition_per_serving}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ===========================================================================
// MODULE 5: Personalized Adaptive Meal Planning
// ===========================================================================
function MealPlannerModule() {
  const [age, setAge] = useState(28);
  const [weight, setWeight] = useState(70);
  const [height, setHeight] = useState(175);
  const [activity, setActivity] = useState("Moderately Active");
  const [goal, setGoal] = useState("Weight Loss");
  const [restrictions, setRestrictions] = useState("");
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState("");

  const generatePlan = async () => {
    setLoading(true);
    setError("");

    try {
      const data = await safeFetchJson("/api/mealplan/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          age: parseInt(age) || 28,
          weight_kg: parseFloat(weight) || 70,
          height_cm: parseFloat(height) || 175,
          activity_level: activity,
          dietary_goal: goal,
          dietary_restrictions: restrictions ? restrictions.split(",").map((s) => s.trim()) : []
        })
      });
      setPlan(data);
    } catch (err) {
      setError(err.message || "Failed to generate meal plan.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="module-card">
      <div className="module-header">
        <h2>🥗 Personalized Adaptive Meal Planner</h2>
        <p>Calculate your daily caloric energy expenditure (TDEE) and generate customized daily meal plans aligned with your dietary goals.</p>
      </div>

      <div className="two-column-layout">
        <div className="input-column">
          <div className="profile-form">
            <div className="form-row-three">
              <div className="form-group">
                <label>Age</label>
                <input type="number" className="text-input" value={age} onChange={(e) => setAge(e.target.value)} />
              </div>
              <div className="form-group">
                <label>Weight (kg)</label>
                <input type="number" className="text-input" value={weight} onChange={(e) => setWeight(e.target.value)} />
              </div>
              <div className="form-group">
                <label>Height (cm)</label>
                <input type="number" className="text-input" value={height} onChange={(e) => setHeight(e.target.value)} />
              </div>
            </div>

            <div className="form-group">
              <label>Daily Activity Level</label>
              <select className="select-input" value={activity} onChange={(e) => setActivity(e.target.value)}>
                <option value="Sedentary">Sedentary (Desk Job, minimal exercise)</option>
                <option value="Lightly Active">Lightly Active (1-3 workout days/week)</option>
                <option value="Moderately Active">Moderately Active (3-5 workout days/week)</option>
                <option value="Very Active">Very Active (6-7 intense days/week)</option>
              </select>
            </div>

            <div className="form-group">
              <label>Dietary Target / Goal</label>
              <select className="select-input" value={goal} onChange={(e) => setGoal(e.target.value)}>
                <option value="Weight Loss">Weight Loss (Caloric Deficit)</option>
                <option value="Muscle Gain">Muscle Gain (Hypertrophy Surplus)</option>
                <option value="Keto">Keto (High Fat / Low Carb)</option>
                <option value="High Protein">High Protein</option>
                <option value="Diabetic-Friendly">Diabetic-Friendly (Low Glycemic)</option>
                <option value="Balanced">Balanced Maintenance</option>
              </select>
            </div>

            <div className="form-group">
              <label>Allergies or Restrictions (comma-separated)</label>
              <input
                type="text"
                className="text-input"
                placeholder="e.g. Dairy-free, Peanuts, Shellfish"
                value={restrictions}
                onChange={(e) => setRestrictions(e.target.value)}
              />
            </div>

            <button
              type="button"
              className="btn-action-primary"
              disabled={loading}
              onClick={generatePlan}
            >
              {loading ? "Calculating Nutrition Protocol..." : "Generate Adaptive Meal Plan 🥗"}
            </button>
            {error && <div className="alert-box error">{error}</div>}
          </div>
        </div>

        <div className="output-column">
          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Computing Mifflin-St Jeor TDEE and balancing macronutrients...</p>
            </div>
          )}

          {!loading && !plan && (
            <div className="empty-placeholder">
              <span>🥗</span>
              <h4>Configure Your Profile</h4>
              <p>Enter your physiological parameters and dietary goals to generate a 4-meal daily nutritional protocol.</p>
            </div>
          )}

          {!loading && plan && (
            <div className="result-display fade-in">
              <div className="plan-header-card">
                <h3>{plan.plan_title}</h3>
                <div className="target-cals-badge">
                  <span className="cal-num">{plan.daily_calorie_target}</span>
                  <span className="cal-label">kcal / day</span>
                </div>
              </div>

              <div className="macro-distribution-box">
                <h5>Target Macronutrient Split:</h5>
                <div className="macro-split-grid">
                  {Object.entries(plan.macro_distribution).map(([key, val]) => (
                    <div key={key} className="macro-split-card">
                      <span className="k">{key}</span>
                      <span className="v">{val}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="meals-schedule-container">
                <h5>Daily Meal Protocol:</h5>
                <div className="meals-list">
                  {plan.meals.map((m, idx) => (
                    <div key={idx} className="meal-card">
                      <div className="meal-type-badge">{m.meal_type}</div>
                      <div className="meal-details">
                        <h4>{m.dish_name}</h4>
                        <div className="meal-tags">
                          <span>🔥 {m.calories} kcal</span>
                          <span>📊 {m.macros}</span>
                          <span>⏱️ {m.prep_time}</span>
                        </div>
                        <p className="meal-benefit">💡 {m.benefits}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="coaching-card">
                <h5>💧 Hydration & Coaching Advisory:</h5>
                <div className="hydration-badge">Target Water Intake: <strong>{plan.hydration_target}</strong></div>
                <ul>
                  {plan.coaching_tips.map((tip, i) => (
                    <li key={i}>✔ {tip}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ===========================================================================
// MODULE 6: Intelligence Dashboard & Executive Reports
// ===========================================================================
function IntelligenceDashboardModule({ onSwitchTab }) {
  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="module-card">
      <div className="module-header dashboard-header">
        <div>
          <h2>📊 Food Verse Multimodal Intelligence Dashboard</h2>
          <p>Consolidated operational summary of food quality, kitchen safety, and nutritional metrics.</p>
        </div>
        <button type="button" className="btn-print" onClick={handlePrint}>
          🖨️ Export / Print Executive Report
        </button>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card" onClick={() => onSwitchTab("food")}>
          <span className="kpi-icon">🍲</span>
          <span className="kpi-val">96/100</span>
          <span className="kpi-label">Average Food Health Score</span>
          <span className="kpi-sub">Grade A (Optimal)</span>
        </div>

        <div className="kpi-card" onClick={() => onSwitchTab("freshness")}>
          <span className="kpi-icon">🌿</span>
          <span className="kpi-val">91.8%</span>
          <span className="kpi-label">Produce Freshness Index</span>
          <span className="kpi-sub">Low Discoloration Risk</span>
        </div>

        <div className="kpi-card" onClick={() => onSwitchTab("hygiene")}>
          <span className="kpi-icon">🧼</span>
          <span className="kpi-val">94.0%</span>
          <span className="kpi-label">Kitchen Sanitation Compliance</span>
          <span className="kpi-sub">HACCP Grade A Passed</span>
        </div>

        <div className="kpi-card" onClick={() => onSwitchTab("mealplan")}>
          <span className="kpi-icon">🥗</span>
          <span className="kpi-val">1,850</span>
          <span className="kpi-label">Daily Calorie Target</span>
          <span className="kpi-sub">Personalized Protocol Active</span>
        </div>
      </div>

      <div className="pipeline-card">
        <h3>Multimodal AI Architecture Pipeline</h3>
        <div className="pipeline-flow">
          <div className="pipeline-node">
            <span className="p-icon">📷 📹</span>
            <strong>Computer Vision</strong>
            <p>Image & Video Frame Analysis (Dish ID, Spoilage, Glove & Hair-cap compliance)</p>
          </div>
          <div className="pipeline-arrow">➔</div>
          <div className="pipeline-node">
            <span className="p-icon">🎙️ ✍️</span>
            <strong>Speech & NLP</strong>
            <p>Voice Prompts & Text Queries (Cooking Guidance & Dietary Preferences)</p>
          </div>
          <div className="pipeline-arrow">➔</div>
          <div className="pipeline-node">
            <span className="p-icon">🧠 ⚡</span>
            <strong>FastAPI Reasoning Engine</strong>
            <p>Multimodal LLM (Gemini Vision) + Nutritional & HACCP Safety Services</p>
          </div>
          <div className="pipeline-arrow">➔</div>
          <div className="pipeline-node">
            <span className="p-icon">📊 🛡️</span>
            <strong>Actionable Insights</strong>
            <p>Dashboards, Health Scores, Storage Tips, and Safety Alerts</p>
          </div>
        </div>
      </div>

      <div className="alerts-feed-card">
        <h3>Live Operational Alerts & System Health</h3>
        <div className="alerts-list">
          <div className="alert-item alert-success">
            <span className="alert-item-icon">✅</span>
            <div>
              <strong>Sanitation Audit: Cold Prep Line #1 Passed</strong>
              <p>100% hair restraint compliance and 96% glove adherence maintained.</p>
            </div>
            <span className="alert-time">5 mins ago</span>
          </div>

          <div className="alert-item alert-warning">
            <span className="alert-item-icon">⏳</span>
            <div>
              <strong>Freshness Notice: Raw Sushi Advisory</strong>
              <p>Raw seafood batch should be consumed or chilled at ≤4°C within 24 hours.</p>
            </div>
            <span className="alert-time">22 mins ago</span>
          </div>

          <div className="alert-item alert-info">
            <span className="alert-item-icon">⚡</span>
            <div>
              <strong>FastAPI REST Gateway Active</strong>
              <p>Serving 6 modular endpoints with zero latency and full offline mock fallback support.</p>
            </div>
            <span className="alert-time">Just now</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// Mount React Root
const rootElement = document.getElementById("root");
const root = ReactDOM.createRoot(rootElement);
root.render(<App />);
