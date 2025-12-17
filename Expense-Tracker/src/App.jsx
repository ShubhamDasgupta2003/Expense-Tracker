import { useState } from 'react'
import './App.css'
import Navbar  from './components/Navbar'
import Analyze from './pages/analyze'
import FileUpload from './components/FileUpload'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AddExpense from './pages/addExpense'

function App() {

  return (
    <div>
      <BrowserRouter>
      <Navbar></Navbar>
      <Routes>
        <Route path="/analyze" element={<Analyze/>}/>
        <Route path="/addExpense" element={<AddExpense/>}/>
      </Routes>
      </BrowserRouter>
      
      
    </div>

    
  )
}

export default App



