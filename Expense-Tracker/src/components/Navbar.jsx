import React from 'react'; // You will create this file for styling
import ExpenseForm from './ExpenseForm';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <button className='btn btn-green'><Link to="/addExpense">New Expense</Link></button>
      <Link to="/analyze">Analyzer</Link>
    </nav>
  );
}

export default Navbar;
