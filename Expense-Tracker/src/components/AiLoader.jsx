import React from "react";
import styles from '../page_css/aiLoader.module.css';

const MyAiLoader = (props)=>
(
    <div className={styles['container']} id="ai-loading" style={{display:'none'}}>
        <img src="/src/ai_symbol.png" alt="" />
        <div className={styles['status-text']}>Thinking...</div>
    </div>
);

export default MyAiLoader;