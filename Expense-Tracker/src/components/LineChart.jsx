import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// const data = [
//   { name: 'Page A', uv: 4000, pv: 2400 },
//   { name: 'Page B', uv: 3000, pv: 1398 },
//   { name: 'Page C', uv: 2000, pv: 9800 },
// ];

const MyLineChart = ({dataPoints}) => (
<div  style={{ 
    // transform: 'scale(0.7)',      // Scales to 80% of original size
    // transformOrigin: 'top left', // Ensures it stays anchored to the corner
    width: 'auto',  
    backgroundColor:'white',
    padding:'10px',
    borderRadius:'8px',
    boxShadow:'5px 5px 5px rgb(121, 121, 121)',         // Adjust container width to offset the scale
    }}>
    <ResponsiveContainer width={350} height={200} aspect={1.6}>
    <LineChart data={dataPoints}>
      <CartesianGrid strokeDasharray="1 1" />
      <XAxis dataKey="cat_code" interval={0} height={50} fontFamily='arial'
      tick={{ 
        angle: -45,       // Rotates text 45 degrees counter-clockwise
        textAnchor: 'end', // Aligns the end of the text to the tick mark
        fontSize:"0.6rem",
    }} />
      <YAxis tickCount={7} fontSize="0.6rem" fontFamily='arial'/>
      <Tooltip />
      <Legend verticalAlign='top' align='right'/>
      <Line type="monotone" dataKey="name" name="Category-wise exp" stroke="#5048e1ff" strokeWidth={2} />
    </LineChart>
  </ResponsiveContainer>
</div>
);

export default MyLineChart;
