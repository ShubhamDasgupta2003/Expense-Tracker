import React, { useState } from "react";
import styles from "../page_css/slider.module.css"

function Filter({updatedData,genAnswer})
{

    const [slider,setSlider] = useState(20000);
    const [essenSlider,setEssenSlider] = useState(1000);
    const [shopSlider,setShopSlider] = useState(1000);
    const [flatpg,setFlatpg] = useState("Paying Guest");
    const [occup,setOccup] = useState("2");
    const ai_loading_element = document.getElementById("ai-loading");

    function onResetClick()
    {
        setSlider(20000);
        setEssenSlider(1000);
        setShopSlider(1000);
    }


    const onUpdateClick = async (e)=>{
        e.preventDefault()

        try{
            const response = await fetch("http://127.0.0.1:5000/api/getmetrics",{
                method:'POST',
                headers:{
                'Content-Type': 'application/json', // This is the critical line
            },
            body:JSON.stringify({salary_slider:Number(slider),pg_flat:flatpg,occupancy:occup})
            });

            if(! response.ok)
            {
                throw new Error("Unable to fetch response");
            }
            const data = await response.json();
            updatedData(data);
            console.log(data);

            const newQuery = `My current expenditure pattern looks like this. My monthly salary is ${slider}. My total expenditure is ${data?.total || 0} and my savings is ${data?.savings || 0}. The percentage of my expenses in sorted categorically is as follows: Essential expenses is ${data.pie_chart[0].amount}%, Discreations expenses is ${data.pie_chart[1].amount}% and my savings is ${data.pie_chart[2].amount}%. Give me suggestions on my spending and point out where I'm over spending and what can I do to prevent it. Also list best 5 ${flatpg} for ${occup} persons near Kondapur,Hyderabad under 18000/- and provide link to the sources`;
            

            // console.log(result);
            // 2nd Api call for text generation using RAG
            genAnswer("");
            ai_loading_element.style.display = "flex";
            const response_second = await fetch("http://127.0.0.1:5000/api/ask",{
                method:'POST',
                headers: {
                'Content-Type': 'application/json', // This is the critical line
            },
            body:JSON.stringify({query:newQuery})
            });

            if(!response_second.ok)
            {
                const err_data = await response_second.json();
                throw new Error(err_data || "Unable to generate insights");
            }

            const result = await response_second.json();
            genAnswer(result.answer || JSON.stringify(result));
            console.log(result);
        }
        catch(error)
        {
            throw new Error(error.message);
        }
        finally
        {
            ai_loading_element.style.display = "none";
        }
    }
    const onSliderChange = (e)=>{
        setSlider(e.target.value);
    }

    // A simple formatting utility function might help:
    const formatCurrency = (value) => {
    if (value === null || value === undefined) return '';
    return `₹${Number(value).toLocaleString('en-IN')}`; // Formats with India locale commas
    };

    return(
        <div className={styles['container']}>

            <div className={styles['row']}>
                <label htmlFor="" className={styles['slider-label']}>Salary:</label>
                <input type="text" name="salary" value={formatCurrency(slider)} onChange={onSliderChange} className={styles['display-box']} readOnly />
            </div>
            <input type="range" min="10000" max="100000" value={slider} onChange={onSliderChange} name="salary-slider" id="salary-slider" step="1" className={[styles['salary-slider'], styles['slider']].join(' ')}/>

            <div className={styles['row']}>
                <label htmlFor="" className={styles['slider-label']}>Essentials:</label>
                <input type="text" name="salary" value={formatCurrency(essenSlider)} onChange={(e)=>{
            setGrocSlider(e.target.value);
            }} className={styles['display-box']} readOnly />
            </div>
            <input type="range" min="100" max="20000" value={essenSlider} onChange={(e)=>{
            setEssenSlider(e.target.value);
            }} name="essential-slider" id="essential-slider" step="1" className={[styles['groc-slider'], styles['slider']].join(' ')}/>


            <div className={styles['row']}>
                <label htmlFor="" className={styles['slider-label']}>Discreations:</label>
                <input type="text" name="shop" value={formatCurrency(shopSlider)} onChange={(e)=>{
            setShopSlider(e.target.value);
            }} className={styles['display-box']} readOnly />
            </div>
            <input type="range" min="100" max="100000" value={shopSlider} onChange={(e)=>{
            setShopSlider(e.target.value);
            }} name="shop-slider" id="shop-slider" step="1" className={[styles['shop-slider'], styles['slider']].join(' ')}/>

            <div className={styles['row']}>
                <label htmlFor="" className={styles['slider-label']}>Flat/PG</label>
                <select name="flat-bhk"  value={flatpg} id="flat-bhk" onChange={(e)=>{
                    const newValue = e.target.value;
                    setFlatpg(newValue);
                    console.log(newValue);
                }}>
                    <option value="1-BHK">1-BHK</option>
                    <option value="2-BHK">2-BHK</option>
                    <option value="3-BHK">3-BHK</option>
                    <option value="Paying Guest">PG</option>
                </select>
            </div>

            <div className={styles['row']}>
                <label htmlFor="" className={styles['slider-label']}>Occupancy</label>
                <select value={occup} name="occupancy" id="occupancy" onChange={(e)=>{
                    const newValue = e.target.value;
                    setOccup(newValue);
                    console.log(newValue);
                }}>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5 or more">5+</option>
                </select>
            </div>

            <div className={styles['row']}>
                <button onClick={onUpdateClick}>Update</button>
                <button onClick={onResetClick}>Reset</button>
            </div>
        </div>
    );
}

export default Filter;
