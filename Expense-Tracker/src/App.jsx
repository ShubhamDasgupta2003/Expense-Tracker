import { useState } from 'react'
import './App.css'
import Navbar  from './components/Navbar'
import Analyze from './pages/analyze'
import FileUpload from './components/FileUpload'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AddExpense from './pages/addExpense'
import Metrics from './pages/metrics'

function App() {

  return (
    <div>
      <BrowserRouter>
      <Navbar></Navbar>
      <Routes>
        <Route path="/analyze" element={<Analyze/>}/>
        <Route path="/addExpense" element={<AddExpense/>}/>
        <Route path="/metrics" element={<Metrics/>} />
      </Routes>
      </BrowserRouter>
      
      
    </div>

    
  )
}

export default App



