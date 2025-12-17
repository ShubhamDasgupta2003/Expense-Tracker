import React from 'react';
import FileUpload from '../components/FileUpload';
import styles from '../page_css/analyze.module.css'
import AskAI from '../components/AskAI';
function Analyze()
{
    return(
        <div>
        <div className={styles['container']}>
            <FileUpload></FileUpload>
        </div>
        <AskAI></AskAI>
        </div>
        
    );
}

export default Analyze;