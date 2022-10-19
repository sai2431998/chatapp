import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const Messages = () => {
  const [content, setValue] = useState("");
  const [messages, setMessages] = useState("")
  const {user, grp} = useParams()

  useEffect(()=> {
    axios.get(`http://127.0.0.1:5000/get_group_message/?group_name=${grp}`).then((res)=>{
        setMessages(res.data)
    })
  }, [])
//   console.log(user)
const handleClick = () => {
    // setMessages(value)
    axios.post("http://127.0.0.1:5000/send_msg", {user, grp, content}).then((res)=> console.log(res))
}
  return (
    <div style={{display: "flex", flexDirection: "column"}}>
        {/* <div style={{display: "flex", flexGrow: 1}}>{messages.map((item)=> (<div>{item}</div>))}</div> */}
      
      <div style={{display: "flex", flexDirection: "row"}}>
      <input
        type="text"
        value={content}
        onChange={(e) => setValue(e.target.value)}
      />
      <button onClick={() => handleClick()}>Sent</button>
      <p>{messages}</p>
    
      </div></div>      
  );
};

export default Messages;