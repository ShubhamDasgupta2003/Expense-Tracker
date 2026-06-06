import React from 'react'; // You will create this file for styling
import ExpenseForm from './ExpenseForm';
import { Link } from 'react-router-dom';
import styles from '../page_css/navbar.module.css'
function Navbar() {
  return (
    <nav className={styles['navbar']}>
      <Link to="/addExpense" className={styles['nav-link']}>New Expense</Link>
      <Link to="/analyze" className={styles['nav-link']}>Analyzer</Link>
      <Link to="/metrics" className={styles['nav-link']}>Metrics</Link>
    </nav>
  );
}

export default Navbar;
