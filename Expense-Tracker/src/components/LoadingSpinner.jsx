import React from 'react';
import styles from '../page_css/loading.module.css';

const LoadingSpinner = (props) => (
  <div className={styles['spinner-container']}>
    <div className={styles['loading-spinner']}></div>
    <label htmlFor="" id="loading-message">{props.message}</label>
  </div>
);

export default LoadingSpinner;
