import React, { useState } from 'react';
import CatDropdown from './CategoryDD';

const AddExpenseForm = () => {
  // State to hold the form input values for date and description
  const [formData, setFormData] = useState({
    description: '',
    date: new Date().toISOString().slice(0, 10), // Default to today's date
    amount: '',
  });
  const [selectedCategory,setSelectedCategory] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle changes to the input fields dynamically
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSelectedCategoryChange=(e)=>{
    setSelectedCategory(e.target.value);
  }

  const payload = {
    ...formData,
    selectedCategory,
  };

  // Handle the form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default page reload
    setLoading(true);
    setError(null);

    try {
      // Send a POST request to your backend endpoint
      const response = await fetch('http://localhost:3001/submit-form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Expense added successfully:', result);
      alert('Expense added successfully!');

      // Reset the form after successful submission
      setFormData({
        description: '',
        date: new Date().toISOString().slice(0, 10),
        amount: '',
      });

    } catch (err) {
      console.error('Error submitting form:', err);
      setError('Failed to add expense. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='container'>
    <form onSubmit={handleSubmit}>
      <h2>Add New Expense</h2>
      <div className='row'>
        <label htmlFor="amount">Amount</label>
        <input
          type="text"
          id="amount"
          name="amount"
          value={formData.amount}
          onChange={handleChange}
          required
        />
      </div>
      <div className='row'>
        <label htmlFor="description">Description</label>
        <input
          type="text"
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          required
        />
      </div>
      <div className='row'>
        <label htmlFor="date">Date</label>
        <input
          type="date"
          id="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
        />
      </div>
        <div className='row'>
         <label htmlFor="category">Category</label>
        <CatDropdown selectedCategory={selectedCategory}
        onCategoryChange={handleSelectedCategoryChange}></CatDropdown>
        </div>
      <button className="btn" type="submit" disabled={loading}>
        {loading ? 'Adding...' : 'Add Expense'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
    </div>
  );
};

export default AddExpenseForm;
