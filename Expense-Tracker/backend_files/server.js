const express = require('express');
const mysql = require('mysql');
const cors = require('cors');

const app = express();
const port = 3001;

// Middleware
app.use(express.json());
app.use(cors());

// Database connection
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'expenses'
});

// API endpoint for form submission
app.post('/submit-form', (req, res) => {
    const {description,date,selectedCategory} = req.body;
    const sql = "INSERT INTO expense (description, date, cat_code) VALUES (?, ?, ?)";
    db.query(sql, [description, date, selectedCategory], (err, result) => {
        if (err) {
            res.status(500).json({ error: "error"+ err.sqlMessage });
        } else {
            res.status(200).json({ message: 'Data inserted successfully!' });
        }
    });
});

//API end-point for fetching all categories
app.get('/get-category',(req,res)=>{
    const sql = "SELECT * FROM category";
    db.query(sql,(err,result)=>{
        if(err){
            res.status(500).json({error:"error"+ err.sqlMessage});
        }
        else {
            res.status(200);
        }
    });

})
app.listen(port, () => {
    console.log(`Backend server running on port ${port}`);
});
