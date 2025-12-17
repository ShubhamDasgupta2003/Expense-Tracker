import React, { useState } from "react";
import styles from '../page_css/analyze.module.css'
import LoadingSpinner from "./LoadingSpinner";
function FileUpload()
{
    const [file,setFile] = useState(null);
    const [message,setMessage] = useState("");
    const [isLoading,setIsLoading] = useState(false);

    const handleFileChange = (event)=>{
        setFile(event.target.files[0]);
    };

    const handleFileUpload = async ()=>{
        if(!file)
        {
            setMessage('Please select a file')
            setIsLoading(false);
        }

        setMessage('Uploading and processing...');
        setIsLoading(true);
        const formData = new FormData();
        formData.append('file',file);

        try{
            const response = await fetch('http://127.0.0.1:5000/api/upload',{
                method:'POST',
                body: formData
            });

            if(!response.ok)
            {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Upload failed');
                setIsLoading(false);
            }

            const data = await response.json();
            setMessage("File uploaded successfully");
            setIsLoading(false);
            setFile(null);
        }
        catch (error){
            setMessage(`Error: ${error.message}`);
            setIsLoading(false);
        }
    };

    return(
        <div className={styles['upload-container']}>
            {
                isLoading ? (<LoadingSpinner message={message}></LoadingSpinner>) : ("")
            }

            <input type="file" onChange={handleFileChange}/>
            <button onClick={handleFileUpload} className={styles['upload-btn']} disabled={!file}>Upload</button>
            <input type="text" className={styles['message-cont']} value={message}/>
        </div>
    );
}

export default FileUpload;