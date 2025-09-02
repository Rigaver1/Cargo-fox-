export async function fetchData(endpoint) {
  const res = await fetch(endpoint);
  if (!res.ok) throw new Error('API error');
  return res.json();
}
