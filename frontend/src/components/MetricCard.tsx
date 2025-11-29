import React from "react";
import "./MetricCard.css";

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: number;
  icon?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  change,
  icon,
}) => {
  const isPositive = change !== undefined && change >= 0;

  return (
    <div className="metric-card glass-card">
      <div className="metric-header">
        <span className="metric-icon">{icon || "📊"}</span>
        <h4 className="metric-title">{title}</h4>
      </div>
      <div className="metric-value">{value}</div>
      {change !== undefined && (
        <div
          className={`metric-change ${isPositive ? "positive" : "negative"}`}
        >
          {isPositive ? "↑" : "↓"} {Math.abs(change).toFixed(2)}%
        </div>
      )}
    </div>
  );
};

export default MetricCard;
