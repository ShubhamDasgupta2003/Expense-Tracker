import React, { useState } from "react";
import styles from '../page_css/askAi.module.css'
import { data } from "react-router-dom";

const AskAI = ()=>{

    const [query,setQuery] = useState('');
    const [answer, setAnswer] = useState('Your insights will appear here...');

    // Handle changes to the input fields dynamically
    const handleChange = (e) => {
        setQuery(e.target.value);
    };

    const handleSubmit = async (e)=>{
        e.preventDefault();
        setAnswer('Fetching insights');

        try{
            const response = await fetch("http://127.0.0.1:5000/api/ask",{
                method:'POST',
                headers: {
                'Content-Type': 'application/json', // This is the critical line
            },
            body:JSON.stringify({query:query})
            });

            if(!response.ok)
            {
                const err_data = await response.json();
                throw new Error(err_data || "Unable to generate insights");
            }

            const data = await response.json();
            setAnswer(data.answer || JSON.stringify(data));
            console.log(data);
        }
        catch(error)
        {
            throw new Error(error.message);
        }
    }

    return(
        <div className={styles['container']}>
            <div className={styles['query-container']}>
                <input type="text" name="query" id="query" placeholder="What do you want to know?" onChange={handleChange} value={query}/>
                <button onClick={handleSubmit} className={styles['animated-gradient-button']}>Generate<img src="/src/ai_symbol.png" alt="Description of the action" class="button-icon" width="35x"></img></button>
            </div>
            <textarea type="text" name="answer" id="answer" value={answer} className={styles['answer-cont']}/>
        </div>
    )
}

export default AskAI;