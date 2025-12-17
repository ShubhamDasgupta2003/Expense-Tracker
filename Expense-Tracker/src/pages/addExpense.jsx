import React from 'react';
import ExpenseForm from '../components/ExpenseForm'
import Table from '../components/ExpenseTable'
import styles from '../page_css/addExpense.module.css'
function AddExpense()
{
    return(
        <div className='parent-container'>
        <ExpenseForm></ExpenseForm>
        <Table></Table>
      </div>
    );
}

export default AddExpense;