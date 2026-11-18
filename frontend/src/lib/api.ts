export async function getHealth() {
  const res = await fetch('/api/health');
  if (!res.ok) {
    throw new Error('Backend error: ' + res.status);
  }
  return res.json();
}

// fetch data from the backend API