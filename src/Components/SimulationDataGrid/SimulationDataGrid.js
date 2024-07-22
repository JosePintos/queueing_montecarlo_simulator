import React, { useState } from "react";
import axios from "axios";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import Input from "../Input/Input";

const App = () => {
  const [rowData, setRowData] = useState([]);
  const [columnDefs, setColumnDefs] = useState([]);
  const [nextToken, setNextToken] = useState(null);
  const [totalRows, setTotalRows] = useState(0);
  const [loading, setLoading] = useState(false);
  const [queryParams, setQueryParams] = useState({});

  const fetchSimulationData = async (params, token = null) => {
    setLoading(true);
    try {
      const result = await axios.get(`http://localhost:8000/simulacion`, {
        params: {
          ...params,
          token: token,
          limit: 25,
        },
      });
      const { total, vectors, next_token } = result.data;

      if (vectors.length > 0) {
        const dynamicColumns = generateDynamicColumns(vectors);
        setColumnDefs(dynamicColumns);
      }

      setRowData((prevData) => [...prevData, ...vectors]);
      setTotalRows(total);
      setNextToken(next_token);
    } catch (error) {
      console.error("Error fetching simulation data:", error);
    } finally {
      setLoading(false);
    }
  };

  const generateDynamicColumns = (data) => {
    const columns = {};
    data.forEach((item) => {
      Object.keys(item).forEach((key) => {
        if (!columns[key]) {
          columns[key] = {
            headerName:
              key.charAt(0).toUpperCase() + key.slice(1).replace("_", " "),
            field: key,
          };
        }
      });
    });
    return Object.values(columns);
  };

  const handleSimulate = (params) => {
    setRowData([]);
    setNextToken(null);
    setQueryParams(params);
    fetchSimulationData(params);
  };

  const loadMoreData = () => {
    if (nextToken && !loading) {
      fetchSimulationData(queryParams, nextToken);
    }
  };

  return (
    <div>
      <Input onSimulate={handleSimulate} />
      <div className="ag-theme-alpine" style={{ height: 600, width: "100%" }}>
        <AgGridReact
          rowData={rowData}
          columnDefs={columnDefs}
          pagination={false}
        />
      </div>
      {nextToken && (
        <button onClick={loadMoreData} disabled={loading}>
          {loading ? "Loading..." : "Load More"}
        </button>
      )}
    </div>
  );
};

export default App;
