import React, { useState, useEffect } from "react";
import axios from "axios";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

const SimulationDataGrid = () => {
  const [rowData, setRowData] = useState([]);
  const [columnDefs, setColumnDefs] = useState([
    // { headerName: "ID", field: "id" },
    // { headerName: "Evento", field: "evento" },
    // { headerName: "Llegada Aparato", field: "llegada_aparato" },
    // { headerName: "Fin Reparacion 1", field: "fin_reparacion_1" },
    // { headerName: "Fin Reparacion 2", field: "fin_reparacion_2" },
    // { headerName: "Fin Reparacion 3", field: "fin_reparacion_3" },
    // { headerName: "Monto Cobro", field: "monto_cobro" },
    // { headerName: "Reparador 1", field: "reparador_1" },
    // { headerName: "Reparador 2", field: "reparador_2" },
    // { headerName: "Reparador 3", field: "reparador_3" },
    // { headerName: "Cola", field: "cola" },
  ]);
  const [nextToken, setNextToken] = useState(null);
  const [totalRows, setTotalRows] = useState(0);
  const [loading, setLoading] = useState(false);

  const fetchSimulationData = async (token = null) => {
    setLoading(true);
    try {
      const result = await axios.get(`http://localhost:8000/simulacion`, {
        params: {
          token: token,
          limit: 10,
          horas: 1,
        },
      });
      const { total, vectors, next_token } = result.data;

      // If no columns are defined yet, generate them dynamically
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

  useEffect(() => {
    fetchSimulationData();
  }, []);

  const loadMoreData = () => {
    if (nextToken && !loading) {
      fetchSimulationData(nextToken);
    }
  };

  return (
    <div>
      <div className="ag-theme-alpine" style={{ height: 400, width: "100%" }}>
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

export default SimulationDataGrid;
