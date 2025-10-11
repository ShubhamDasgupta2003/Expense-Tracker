import React from 'react'; // You will create this file for styling

function Navbar() {
  return (
    <nav className="navbar">
      <a href="/" className="logo">MyBrand</a>
      <ul className="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/services">Services</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  );
}

export default Navbar;
