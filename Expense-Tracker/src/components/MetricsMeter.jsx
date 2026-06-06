import React from "react";
import CircularSlider from '@fseehawer/react-circular-slider';

function CircularMeter(prop)
{
    return(
        <div>
        <CircularSlider
        key={prop.value}
        dataIndex={prop.value} 
        width={100}
        label=""
        labelColor= {prop.textColor}
        valueFontSize="1.4rem"
        verticalOffset="0.5rem"
        max={100000}
        // value={prop.value}
        onChange={value => console.log(value)}
        progressColorFrom={prop.colorFrom}
        progressColorTo={prop.colorTo}
        hideKnob
        knobDraggable={false}
/>
        </div>
    );
}


export default CircularMeter;