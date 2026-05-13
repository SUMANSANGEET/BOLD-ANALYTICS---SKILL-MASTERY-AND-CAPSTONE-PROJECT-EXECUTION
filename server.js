const express = require('express');
const cors = require('cors');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Get paginated and filtered villages
app.get('/api/villages', (req, res) => {
    const { page = 1, limit = 20, q = '', state = '', district = '' } = req.query;
    
    const offset = (page - 1) * limit;
    const params = [];
    let whereClause = 'WHERE 1=1';
    
    if (q) {
        whereClause += ' AND village_name LIKE ?';
        params.push(`%${q}%`);
    }
    if (state) {
        whereClause += ' AND state = ?';
        params.push(state);
    }
    if (district) {
        whereClause += ' AND district = ?';
        params.push(district);
    }
    
    const countSql = `SELECT COUNT(*) as total FROM villages ${whereClause}`;
    const dataSql = `SELECT * FROM villages ${whereClause} LIMIT ? OFFSET ?`;
    
    db.get(countSql, params, (err, countRow) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        
        const dataParams = [...params, parseInt(limit), parseInt(offset)];
        db.all(dataSql, dataParams, (err, rows) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            
            res.json({
                data: rows,
                total: countRow.total,
                page: parseInt(page),
                totalPages: Math.ceil(countRow.total / limit)
            });
        });
    });
});

// Get overall statistics
app.get('/api/stats/summary', (req, res) => {
    const sql = `
        SELECT 
            COUNT(*) as total_villages,
            SUM(population) as total_population,
            AVG(literacy_rate) as avg_literacy_rate,
            SUM(area_hectares) as total_area
        FROM villages
    `;
    
    db.get(sql, [], (err, row) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(row);
    });
});

// Get distinct states and districts for dropdowns
app.get('/api/locations', (req, res) => {
    db.all(`SELECT DISTINCT state FROM villages ORDER BY state`, [], (err, states) => {
        if (err) return res.status(500).json({ error: err.message });
        
        db.all(`SELECT DISTINCT state, district FROM villages ORDER BY district`, [], (err, districts) => {
            if (err) return res.status(500).json({ error: err.message });
            
            const locationMap = {};
            states.forEach(s => {
                locationMap[s.state] = districts.filter(d => d.state === s.state).map(d => d.district);
            });
            
            res.json(locationMap);
        });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
