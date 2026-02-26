import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Design from "./pages/Design";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/design" element={<Design />} />
      </Routes>
    </Router>
  );
}

export default App;