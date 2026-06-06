import React, { useEffect, useState } from "react";

function fetchMetrics({onDataReceived,slider,genAnswer})
{
    const [data,setData] = useState(null);
    const [message,setMesssage] = useState("");
    // const [answer,setAnswer] = useState("");
    const [query,setQuery] = useState(null);
    useEffect(()=>{
        const fetchData = async()=>{
            try{
                const response = await fetch("http://127.0.0.1:5000/api/getmetrics",{
                method:'POST',
                headers:{
                'Content-Type': 'application/json', // This is the critical line
            },
            body:JSON.stringify({salary_slider:slider})
            });

            if(! response.ok)
            {
                throw new Error(`HTTP error status: ${response.status}`);
            }
            const result = await response.json();
            console.log(result);
            setData(result);
            
            onDataReceived(result);
            // console.log(result);
            }
            catch (error)
            {
                setMesssage(error.message);
            }

        }
        fetchData();
    },[]);
}

export default fetchMetrics;