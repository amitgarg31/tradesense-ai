import React from "react";
import "./TradeCard.css";

interface TradeCardProps {
  symbol: string;
  price: number;
  timestamp: string;
  isLive?: boolean;
}

const TradeCard: React.FC<TradeCardProps> = ({
  symbol,
  price,
  timestamp,
  isLive,
}) => {
  const formatTime = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  return (
    <div className={`trade-card glass-card ${isLive ? "live-pulse" : ""}`}>
      <div className="trade-header">
        <div className="trade-symbol">
          <span className="symbol-icon">💹</span>
          <span className="symbol-text">{symbol}</span>
        </div>
        {isLive && <span className="badge badge-success">LIVE</span>}
      </div>
      <div className="trade-price">
        $
        {price.toLocaleString("en-US", {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        })}
      </div>
      <div className="trade-time">{formatTime(timestamp)}</div>
    </div>
  );
};

export default TradeCard;
