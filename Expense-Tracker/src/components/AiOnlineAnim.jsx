import React from "react";
import styles from "../page_css/aiLoader.module.css";

function ShowAiOnlineStatus()
{
    return(
        <div class={styles["ai-glow-container"]}>
            <p>🤖 Hi! I'm Dravina
            <br/>Your personal financial assistant to guide you with better financial planning</p>
        </div>

    );
}

export default ShowAiOnlineStatus;