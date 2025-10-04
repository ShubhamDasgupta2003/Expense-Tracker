import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import ExpenseForm from './components/ExpenseForm'
import Table from './components/ExpenseTable'

function App() {

  return (
    <>
      <ExpenseForm></ExpenseForm>
      <Table></Table>
    </>
  )
}

export default App
