import React, { useState } from "react";
import styles from "../page_css/metrics.module.css";
import Filter from "../components/Filter"
import CircularMeter from "../components/MetricsMeter";
import DataFetcher from "../components/DataFetcher";
import MyLineChart from "../components/LineChart";
import Barchart from "../components/BarChart";
import MyPieChart from "../components/PieChart";
import MyAiLoader from "../components/AiLoader";
import ShowAiOnlineStatus from "../components/AiOnlineAnim";

function Metrics()
{
    const [data,setData] = useState(null);
    const [answer, setAnswer] = useState("");
    const [ansBoxVisible,setAnsboxVisible] = useState(false);

    const onAiThumbnailClicked = ()=>{
        const newStatus = !ansBoxVisible;
        setAnsboxVisible(newStatus);
    }

    return(
        <div className={styles['container']}>
            <DataFetcher onDataReceived={setData} slider={20000}></DataFetcher>
            <div className={styles['filter-navbar']}>
                <Filter updatedData={setData} genAnswer={setAnswer}></Filter>
            </div>
            <div className={styles['row']}>
                <div className={styles['metrics-cont']}>
                    <CircularMeter value={data?.total||0} colorFrom={"orange"} colorTo={"red"} textColor={"red"}/>
                    
                    <label htmlFor="">Total Expenditure</label>
                </div>

                <div className={styles['metrics-cont']}>
                    <CircularMeter value={data?.savings||0} colorFrom={"#0502ab"} colorTo={"#ffffff"} textColor={"#040191"} className={styles['meter']}/>
                    
                    <label htmlFor="">Savings</label>
                </div>

                <div className={styles['metrics-cont']}>
                    <CircularMeter value={data?.essential||0} colorFrom={"green"} colorTo={"white"} textColor={"green"} className={styles['meter']}/>
                    
                    <label htmlFor="">Investments</label>
                </div>
            </div>
            
            <div className={styles['row']}>
                <div className={styles['chart-cont']}>
                    <MyLineChart dataPoints={data?.group||[]}></MyLineChart>
                </div>
                <div className={styles['chart-cont']}>
                    <Barchart dataPoints={(data?.desc_sort || []).slice(0,5)}></Barchart>
                </div>
            </div>
            <div className={styles['row']}>
                <div className={styles['chart-cont']}>
                    <MyPieChart dataPoints={data?.pie_chart || []}></MyPieChart>
                </div>

                <div>
                    {/* <textarea name="answer-box" id={styles['answer-box']} className={styles['textbox-animated']} readOnly value={answer}></textarea> */}
                    <div contentEditable="true" className={!ansBoxVisible? styles.ansBoxHide:styles.ansBoxShow} name="answer-box" id={styles['answer-box']}>{answer}<MyAiLoader></MyAiLoader><ShowAiOnlineStatus></ShowAiOnlineStatus></div>
                </div>
            </div>

            <button className={styles['agent-thumbnail']} onClick={onAiThumbnailClicked}></button>
            
        </div>
    );
}

export default Metrics;