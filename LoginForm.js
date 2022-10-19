import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const LoginForm = () => {
  const [user, setUser] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const [result, setResult] = useState({})

  const handleSubmit = () => {
    // const data = {"user": user, "password": password}
    // console.log(data)
   
    axios.post("http://127.0.0.1:5000/authorize_user", {user, password}).then((res)=> {setResult(res);
window.location.href=`/groups/${user}`}).catch((res)=> alert(res))

  };

  useEffect(()=> {
    console.log(result)
  },[result])

//   console.log(result)

  return (
    <div>
      <form>
        <label>name</label>
        <input
          value={user}
          type="text"
          id="user"
          name="user"
          placeholder="name"
          onChange={(event) => setUser(event.target.value)}
        />
        <label>password</label>
        <input
          value={password}
          type="password"
          id="password"
          name="password"
          placeholder="password"
          onChange={(event) => setPassword(event.target.value)}
        />
        <button onClick={() => handleSubmit()}>Submit</button>
      </form>
    </div>
  );
};

export default LoginForm;
