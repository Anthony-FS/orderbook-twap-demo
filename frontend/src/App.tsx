import { HealthPanel } from "./components/HealthPanel";

// Step 1: just the health panel. The order book, chart and TWAP panel
// arrive in steps 4, 5 and 7.
export default function App() {
  return (
    <main className="app">
      <header className="app-header">
        <h1>Order Book + TWAP</h1>
      </header>
      <HealthPanel />
    </main>
  );
}
