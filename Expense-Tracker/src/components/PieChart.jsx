import { PieChart, Pie, Tooltip, ResponsiveContainer, Cell, Legend } from 'recharts';

const MyPieChart = ({dataPoints}) =>{
    const chartData = dataPoints ? Object.values(dataPoints) : [];
    const formatLegendText = (value, entry) => {
  return <span style={{fontSize:'0.6rem', fontFamily:'arial'}}>{value}</span>;
};
    return (

      <div  style={{ 
    // transform: 'scale(0.7)',      // Scales to 80% of original size
    // transformOrigin: 'top left', // Ensures it stays anchored to the corner
    width: 'auto',  
    backgroundColor:'white',
    padding:'10px',
    borderRadius:'8px',
    boxShadow:'5px 5px 5px rgb(121, 121, 121)',         // Adjust container width to offset the scale
    }}>

      <ResponsiveContainer width={300} height={200} aspect={1.4}>
    <PieChart>
      <Pie
        data={dataPoints}
        dataKey="amount" // Required: specifies the field for slice size
        nameKey="name"  // Specifies the field for labels
        cx="50%"        // X-coordinate of the center
        cy="50%"        // Y-coordinate of the center
        outerRadius={70} 
        innerRadius={35}
        label ={{
          fontSize: '14px',
          fontFamily: 'Arial, sans-serif',
          fontWeight: 'bold'
        }}          // Set to true for simple labels
      >
      {chartData.map((entry,index)=>(
        <Cell key={`cell-${index}`} fill={entry.color}/>
      ))
      }
      </Pie>
      <Tooltip />
      
      <Legend layout='vertical' verticalAlign='top' align='right' formatter={formatLegendText}/>
    </PieChart>
  </ResponsiveContainer>
    </div>

);
}

export default MyPieChart;
