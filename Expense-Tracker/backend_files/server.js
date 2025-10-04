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
    database: 'expenses',
     dateStrings: true,
});

// API endpoint for form submission
app.post('/submit-form', (req, res) => {
    const {description,date,selectedCategory,amount} = req.body;
    const sql = "INSERT INTO expense (description, date, cat_code, amount) VALUES (?, ?, ?, ?)";
    db.query(sql, [description, date, selectedCategory,amount], (err, result) => {
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
            res.status(200).json({result});
        }
    });

});

//API end-point to fetch expenses

app.get("/get-expense",(req,res)=>{
    const sql = "SELECT * FROM expense";
    db.query(sql,(err,result)=>{
        if(err){
            res.status(500).json({error:"error"+ err.sqlMessage});
        }
        else {
            res.status(200).json({result});
        }
    })
});

app.listen(port, () => {
    console.log(`Backend server running on port ${port}`);
});
