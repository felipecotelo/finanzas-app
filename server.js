const express = require('express');
const path    = require('path');
const fs      = require('fs');
const app     = express();

const BORRADORES_PATH = path.join(__dirname, '..', 'Estados de cuenta', 'borradores.json');

app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.sendStatus(204); return; }
  next();
});

app.use(express.json({ limit: '1mb' }));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/borradores', (req, res) => {
  try {
    const data = fs.existsSync(BORRADORES_PATH)
      ? JSON.parse(fs.readFileSync(BORRADORES_PATH, 'utf8'))
      : [];
    res.json(data);
  } catch { res.json([]); }
});

app.post('/api/borradores', (req, res) => {
  try {
    const list = Array.isArray(req.body) ? req.body : [];
    fs.writeFileSync(BORRADORES_PATH, JSON.stringify(list, null, 2));
    res.json({ ok: true, count: list.length });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Finanzas → http://localhost:${PORT}`));
