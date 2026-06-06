import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Barchart = ({ dataPoints }) => (

  <div  style={{ 
    // transform: 'scale(0.7)',      // Scales to 80% of original size
    // transformOrigin: 'top left', // Ensures it stays anchored to the corner
    width: 'auto',  
    backgroundColor:'white',
    padding:'10px',
    borderRadius:'8px',
    boxShadow:'5px 5px 5px rgb(121, 121, 121)',
    margin:'0px'         // Adjust container width to offset the scale
    }}>

        <ResponsiveContainer width={300} height={30} aspect={1.5}>
    <BarChart data={dataPoints}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="cat_code" fontFamily='arial' interval={0} height={40} fontSize="0.8rem" width="50px" 
      tick={{ 
        angle: -35,       // Rotates text 45 degrees counter-clockwise
        textAnchor: 'end', // Aligns the end of the text to the tick mark
        fontSize:"0.6rem"}}/>
      <YAxis fontFamily='arial' fontSize="0.8rem"/>
      <Tooltip />
      <Legend verticalAlign='top' align='right'/>
      {/* dataKey must match the numerical value from your Python backend */}
      <Bar dataKey="exp_id" name="Most repeated expenses" fill="#d4004aff" radius={[4, 4, 0, 0]} />
    </BarChart>
  </ResponsiveContainer>
    </div>

);

export default Barchart;