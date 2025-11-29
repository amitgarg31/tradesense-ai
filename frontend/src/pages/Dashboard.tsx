import React, { useState, useEffect } from "react";
import { TradeWebSocket, ingestTrade, type Trade } from "../services/api";
import MetricCard from "../components/MetricCard";
import TradeCard from "../components/TradeCard";
import "./Dashboard.css";

const Dashboard: React.FC = () => {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [wsConnected, setWsConnected] = useState(false);
  const [symbol, setSymbol] = useState("BTC-USD");
  const [price, setPrice] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const ws = new TradeWebSocket(
      (data) => {
        if (data.symbol && data.price) {
          const newTrade: Trade = {
            id: Math.random().toString(36),
            symbol: data.symbol,
            price: data.price,
            timestamp: data.timestamp || new Date().toISOString(),
          };
          setTrades((prev) => [newTrade, ...prev].slice(0, 20));
        }
      },
      (error) => {
        console.error("WebSocket error:", error);
        setWsConnected(false);
      },
    );

    ws.connect();
    setWsConnected(true);

    return () => {
      ws.disconnect();
    };
  }, []);

  const handleIngest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!symbol || !price) return;

    setLoading(true);
    try {
      await ingestTrade(symbol, parseFloat(price));
      setPrice("");
    } catch (error) {
      console.error("Failed to ingest trade:", error);
    } finally {
      setLoading(false);
    }
  };

  const avgPrice =
    trades.length > 0
      ? trades.reduce((sum, t) => sum + t.price, 0) / trades.length
      : 0;

  const latestPrice = trades.length > 0 ? trades[0].price : 0;
  const priceChange =
    trades.length > 1
      ? ((latestPrice - trades[1].price) / trades[1].price) * 100
      : 0;

  return (
    <div className="dashboard">
      <div className="container">
        <div className="dashboard-header">
          <div>
            <h1 className="animate-fade-in">Real-Time Dashboard</h1>
            <p>Monitor live trading data and key metrics</p>
          </div>
          <div className="connection-status">
            <span
              className={`status-indicator ${wsConnected ? "connected" : "disconnected"}`}
            ></span>
            <span>{wsConnected ? "Connected" : "Disconnected"}</span>
          </div>
        </div>

        <div className="grid grid-4 animate-fade-in">
          <MetricCard title="Total Trades" value={trades.length} icon="📊" />
          <MetricCard
            title="Latest Price"
            value={`$${latestPrice.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
            change={priceChange}
            icon="💰"
          />
          <MetricCard
            title="Average Price"
            value={`$${avgPrice.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
            icon="📈"
          />
          <MetricCard
            title="Active Symbols"
            value={new Set(trades.map((t) => t.symbol)).size}
            icon="🎯"
          />
        </div>

        <div className="dashboard-content">
          <div className="ingest-panel glass-card">
            <h3>Ingest New Trade</h3>
            <form onSubmit={handleIngest} className="ingest-form">
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
                <label htmlFor="price">Price</label>
                <input
                  id="price"
                  type="number"
                  step="0.01"
                  className="input"
                  placeholder="e.g., 50000.00"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  required
                />
              </div>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? "Ingesting..." : "Ingest Trade"}
              </button>
            </form>
          </div>

          <div className="trades-panel">
            <h3>Live Trade Feed</h3>
            {trades.length === 0 ? (
              <div className="empty-state">
                <p>No trades yet. Ingest some data to get started!</p>
              </div>
            ) : (
              <div className="trades-grid">
                {trades.map((trade, index) => (
                  <TradeCard
                    key={trade.id}
                    symbol={trade.symbol}
                    price={trade.price}
                    timestamp={trade.timestamp}
                    isLive={index === 0}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
