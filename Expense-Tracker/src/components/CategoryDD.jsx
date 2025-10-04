import { useEffect,useState } from "react";

const categoryDropdown=({selectedCategory,onCategoryChange})=>{
    const [category,setCategory] = useState([]);
    // const [selectedCategory,setSelectedCategory] = useState('');

    useEffect(()=>{
        //Fetch data from api-endpoint

        fetch("http://localhost:3001/get-category")
        .then(response=>{
            //Check for successfull response
            if(!response.ok)
            {
                throw new Error('Network response was not ok: ${response.statusText}');
            }
            return response.json();
        })
        .then(data=>{setCategory(data.result);
        })

        .catch(err=>{
            console.log(err.message);
        })

    },[])

    return(
        <div>
            <select name="" id="categoryChoice" value={selectedCategory} onChange={onCategoryChange}>
                <option value="">--Please choose an option--</option>
                {category.map(cat=>(
                    <option key={cat.cat_code} value={cat.cat_code}>{cat.cat_desc}</option>
                ))}
            </select>
        </div>
    )
}

export default categoryDropdown;

