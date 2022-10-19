import "./App.css";
import LoginForm from "./LoginForm";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Messages from "./Messages";
import Groups from "./Groups";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route path="/chat/:user/:grp" element={<Messages />} />
        <Route path="/groups/:user" element={<Groups />} />
      </Routes>
    </div>
  );
}

export default App;