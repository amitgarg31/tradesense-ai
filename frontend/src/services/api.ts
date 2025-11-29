import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface Trade {
  id: string;
  symbol: string;
  price: number;
  timestamp: string;
}

export interface Summary {
  id: string;
  symbol: string;
  summary: string;
  embedding: number[];
  timestamp: string;
}

// Ingestion API
export const ingestTrade = async (symbol: string, price: number) => {
  const response = await api.post("/ingest/", null, {
    params: { symbol, price },
  });
  return response.data;
};

// Query API
export const queryTrades = async (symbol: string, limit: number = 10) => {
  const response = await api.get("/query/", {
    params: { symbol, limit },
  });
  return response.data;
};

// Insights API
export const getLatestSummary = async (symbol?: string) => {
  const response = await api.get("/insights/latest", {
    params: symbol ? { symbol } : {},
  });
  return response.data;
};

export const triggerSummaryGeneration = async (symbol: string) => {
  const response = await api.post("/insights/trigger", null, {
    params: { symbol },
  });
  return response.data;
};

// WebSocket Connection
export class TradeWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000;

  constructor(
    private onMessage: (data: any) => void,
    private onError?: (error: Event) => void,
  ) {}

  connect() {
    const wsUrl = API_BASE_URL.replace("http", "ws") + "/ws/trades";

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log("✅ WebSocket connected");
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onMessage(data);
        } catch (error) {
          console.error("Failed to parse WebSocket message:", error);
        }
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        if (this.onError) {
          this.onError(error);
        }
      };

      this.ws.onclose = () => {
        console.log("WebSocket closed");
        this.attemptReconnect();
      };
    } catch (error) {
      console.error("Failed to create WebSocket:", error);
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(
        `Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`,
      );

      setTimeout(() => {
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    } else {
      console.error("Max reconnection attempts reached");
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }
}

export default api;
