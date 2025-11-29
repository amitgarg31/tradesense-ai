import React, { useState } from "react";
import { queryTrades, type Trade } from "../services/api";
import TradeCard from "../components/TradeCard";
import "./Analytics.css";

const Analytics: React.FC = () => {
  const [symbol, setSymbol] = useState("BTC-USD");
  const [limit, setLimit] = useState(10);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(false);

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await queryTrades(symbol, limit);
      setTrades(data.recent_trades || []);
    } catch (error) {
      console.error("Failed to query trades:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analytics">
      <div className="container">
        <div className="analytics-header animate-fade-in">
          <h1>Analytics</h1>
          <p>Query and analyze historical trading data</p>
        </div>

        <div className="query-panel glass-card animate-fade-in">
          <h3>Query Historical Trades</h3>
          <form onSubmit={handleQuery} className="query-form">
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
              <div className="form-group">
                <label htmlFor="limit">Limit</label>
                <input
                  id="limit"
                  type="number"
                  className="input"
                  placeholder="10"
                  value={limit}
                  onChange={(e) => setLimit(parseInt(e.target.value))}
                  min="1"
                  max="100"
                  required
                />
              </div>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? "Querying..." : "Query"}
              </button>
            </div>
          </form>
        </div>

        <div className="results-section">
          {trades.length > 0 && (
            <>
              <h3>Results ({trades.length} trades)</h3>
              <div className="trades-grid">
                {trades.map((trade) => (
                  <TradeCard
                    key={trade.id}
                    symbol={trade.symbol}
                    price={trade.price}
                    timestamp={trade.timestamp}
                  />
                ))}
              </div>
            </>
          )}
          {!loading && trades.length === 0 && (
            <div className="empty-state">
              <p>No results. Try querying for a different symbol.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Analytics;
