import { useEffect, useState } from "react";

type ServiceStatus = "ok" | "down" | "unknown";

interface Health {
  status: "ok" | "degraded";
  services: Record<string, ServiceStatus>;
}

const POLL_MS = 5000;

export function HealthPanel() {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // AbortController cancels an in-flight request when the component
    // unmounts, so we never call setState on an unmounted component.
    const controller = new AbortController();

    const load = async () => {
      try {
        const res = await fetch("/api/health/", { signal: controller.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        setHealth(await res.json());
        setError(null);
      } catch (e) {
        if (controller.signal.aborted) return;
        setError(e instanceof Error ? e.message : String(e));
      }
    };

    load();
    const timer = setInterval(load, POLL_MS);
    return () => {
      controller.abort();
      clearInterval(timer);
    };
  }, []);

  return (
    <section className="panel">
      <h2>System health</h2>
      {error && <p className="error">Backend unreachable: {error}</p>}
      {health && (
        <ul className="health-list">
          {Object.entries(health.services).map(([name, status]) => (
            <li key={name}>
              <span className={`dot dot-${status}`} aria-hidden />
              <span className="service-name">{name}</span>
              <span className="service-status">{status}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
