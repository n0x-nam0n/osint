import React, { useState } from "react";
import axios from "axios";

function App() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState(null);

    const handleSearch = async () => {
        const res = await axios.post("http://127.0.0.1:5000/search", { query });
        setResults(res.data);
    };

    return (
        <div className="p-5">
            <input
                className="border p-2"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter email or domain"
            />
            <button className="ml-2 bg-blue-500 text-white p-2" onClick={handleSearch}>Search</button>

            {results && <pre>{JSON.stringify(results, null, 2)}</pre>}
        </div>
    );
}

export default App;
