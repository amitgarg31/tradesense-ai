import React, { useState, useEffect } from "react";
import {
  getLatestSummary,
  triggerSummaryGeneration,
  type Summary,
} from "../services/api";
import "./Insights.css";

const Insights: React.FC = () => {
  const [symbol, setSymbol] = useState("BTC-USD");
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadLatestSummary();
  }, []);

  const loadLatestSummary = async () => {
    setLoading(true);
    try {
      const data = await getLatestSummary();
      setSummary(data);
    } catch (error) {
      console.error("Failed to load summary:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSummary = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenerating(true);
    try {
      await triggerSummaryGeneration(symbol);
      alert("Summary generation triggered! Check back in a few moments.");
      setTimeout(loadLatestSummary, 5000);
    } catch (error) {
      console.error("Failed to trigger summary:", error);
      alert("Failed to trigger summary generation");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="insights">
      <div className="container">
        <div className="insights-header animate-fade-in">
          <h1>AI Insights</h1>
          <p>LLM-powered trading analysis and summaries</p>
        </div>

        <div className="generate-panel glass-card animate-fade-in">
          <h3>Generate New Summary</h3>
          <form onSubmit={handleGenerateSummary} className="generate-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="symbol">Symbol</label>
                <input
                  id="symbol"
                  type="text"
                  className="input"
                  placeholder="e.g., BTC-USD"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value)}
                  required
                />
              </div>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={generating}
              >
                {generating ? "Generating..." : "🧠 Generate Summary"}
              </button>
            </div>
          </form>
        </div>

        {loading ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading insights...</p>
          </div>
        ) : summary ? (
          <div className="summary-card glass-card animate-fade-in">
            <div className="summary-header">
              <div>
                <h3>{summary.symbol}</h3>
                <p className="summary-date">
                  {new Date(summary.timestamp).toLocaleString()}
                </p>
              </div>
              <span className="badge badge-success">AI Generated</span>
            </div>
            <div className="summary-content">
              <p>{summary.summary}</p>
            </div>
            <div className="summary-meta">
              <span className="meta-item">
                📊 Embedding Dimensions: {summary.embedding?.length || 0}
              </span>
            </div>
          </div>
        ) : (
          <div className="empty-state">
            <p>No summaries yet. Generate one to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Insights;
