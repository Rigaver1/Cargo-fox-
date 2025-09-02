import React, { useEffect, useState } from 'react';

function CurrencyRatesDisplay() {
  const [rates, setRates] = useState({});
  const [lastUpdate, setLastUpdate] = useState(null);

  const fetchRates = async () => {
    try {
      const res = await fetch('/api/exchange_rates');
      if (res.ok) {
        const data = await res.json();
        setRates(data.rates);
        setLastUpdate(data.last_update);
      }
    } catch (err) {
      console.error('Failed to load rates', err);
    }
  };

  useEffect(() => {
    fetchRates();
  }, []);

  return (
    <div>
      <h2>Exchange Rates</h2>
      {lastUpdate && (
        <p>Last update: {new Date(lastUpdate).toLocaleString()}</p>
      )}
      <ul>
        {Object.entries(rates).map(([code, rate]) => (
          <li key={code}>{code}: {rate}</li>
        ))}
      </ul>
    </div>
  );
}

export default CurrencyRatesDisplay;
