const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const bcrypt = require('bcrypt');
const path = require('path');

const app = express();
app.use(express.json());
app.use(cors());
app.use(express.static(__dirname));

const connectionString = 'postgresql://neondb_owner:npg_dvcfk8pWS3Fs@ep-late-term-aiilpapy-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require';
const pool = new Pool({ connectionString });

pool.query(`
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    )
`).then(() => console.log('DB Users table ready'))
    .catch(e => console.error('DB Error:', e));

app.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;
        if (!username || !password) return res.status(400).json({ error: 'Missing fields' });

        const hash = await bcrypt.hash(password, 10);
        await pool.query('INSERT INTO users (username, password_hash) VALUES ($1, $2)', [username, hash]);
        res.json({ success: true });
    } catch (e) {
        if (e.code === '23505') return res.status(400).json({ error: 'Username already taken' });
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        const result = await pool.query('SELECT * FROM users WHERE username = $1', [username]);
        if (result.rows.length === 0) return res.status(400).json({ error: 'User not found' });

        const user = result.rows[0];
        const match = await bcrypt.compare(password, user.password_hash);
        if (!match) return res.status(400).json({ error: 'Invalid password' });

        res.json({ success: true, username: user.username });
    } catch (e) {
        res.status(500).json({ error: 'Server error' });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`[SERVER] Сервер запущен на порту ${PORT}`);
});
