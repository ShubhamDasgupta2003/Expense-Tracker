import React,{useState} from "react";

function Table({expenses})
{
    if(!expenses || expenses.length === 0)
    {
        return <p>No expense added yet</p>;
    }

    return(
        <table className="ExpenseTable">
            <thead>
                <tr>
                    <th>Description</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
                {expenses.map((expense)=>(
                    <tr key={Date.now()}>
                        <td>{expense.description}</td>
                        <td>{expense.date}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default Table;