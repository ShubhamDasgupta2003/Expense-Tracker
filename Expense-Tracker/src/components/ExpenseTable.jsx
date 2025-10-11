import React,{useEffect, useState} from "react";

function Table()
{
    const [expenses,setExpenses] = useState('');

    useEffect(()=>{
        fetch("http://localhost:3001/get-expense")
            .then(response=>{
        //Check for invalid response
            if(!response.ok)
            {
                throw new Error('Network response was not ok: ${response.statusText}');
            }
            return response.json();
    })
    .then(data=>{setExpenses(data.result)
    })

    .catch(err=>{
            console.log(err.message);
        });

    },[])

    if(!expenses || expenses.length === 0)
    {
        return <p>No expense added yet</p>;
    }

    return(
        <div className="table-cont">
        <table className="ExpenseTable">
            <thead>
                <tr>
                    <th>Description</th>
                    <th>Category</th>
                    <th>Amount</th>
                    <th colSpan={2}>Date</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {expenses.map((expense)=>{
                    return (
                    <tr key={expense.exp_id}>
                        <td>{expense.Description}</td>
                        <td>{expense.cat_code}</td>
                        <td>{expense.amount}</td>
                        <td>{expense.Date.slice(0,10).split('-').reverse().join('/')}</td>
                        <td><button className="btn btn-green" id={expense.exp_id}>Edit</button></td>
                        <td><button className="btn btn-red">Delete</button></td>
                    </tr>
                )})}
            </tbody>
        </table>
        </div>
    );
};

export default Table;