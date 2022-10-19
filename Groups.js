import axios from "axios";
import React, { useState } from "react";
import { useParams } from "react-router-dom";

const Groups = () => {
    const [value, setValue] = useState("");
    const [group, setGroup] = useState("")

    const user = useParams();
    console.log(user.user)
function handleButton(){
    axios.post(`http://127.0.0.1:5000/check_group`,{user:user.user, group}).then((res)=>{
    console.log(res) 
            {window.location.href=`/chat/${user.user}/${group}`}
    })
}
    return (
        <div>
            <input type="text" value={group} placeholder="enter group name" onChange={(e)=> setGroup(e.target.value)}/>
            <button onClick={()=>  {handleButton()}}>Enter</button>
        </div>
    )
}

export default Groups