import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import ExpenseForm from './components/ExpenseForm'
import Table from './components/ExpenseTable'

function App() {
  const [count, setCount] = useState(0);

  const DUMMY_EXPENSE=[
];

const [expenses,setExpenses] = useState(DUMMY_EXPENSE);

  return (
    <>
      <ExpenseForm></ExpenseForm>
      <Table expenses={expenses}></Table>
    </>
  )
}

export default App
