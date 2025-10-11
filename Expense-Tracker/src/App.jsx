import { useState } from 'react'
import './App.css'
import ExpenseForm from './components/ExpenseForm'
import Table from './components/ExpenseTable'
import Navbar  from './components/Navbar'

function App() {

  return (
    <div>
      <Navbar></Navbar>
      <div className='parent-container'>
        <ExpenseForm></ExpenseForm>
        <Table></Table>
      </div>
    </div>

    
  )
}

export default App
