import { DataGrid } from "@mui/x-data-grid";
import { useEffect, useState } from "react";
import axios from "axios";

const Table = () => {
  const [vectorEstado, setVectorEstado] = useState([]);

  const rows = [
    { id: 1, llegada_aparato: "Hello", llegada_aparato: "World" },
    { id: 2, col1: "DataGridPro", col2: "is Awesome" },
    { id: 3, col1: "MUI", col2: "is Amazing" },
  ];

  const columns = [
    { field: "hora", headerName: "Hora", width: 50 },
    { field: "evento", headerName: "Evento", width: 60 },
    {
      field: "llegada_aparato_rnd",
      headerName: "Llegada Aparato RND",
      width: 160,
    },
    {
      field: "llegada_aparato",
      headerName: "Llegada Aparato",
      width: 120,
    },
    {
      field: "fin_reparacion_rnd",
      headerName: "Fin de Reparación RND",
      width: 170,
    },
    {
      field: "fin_reparacion",
      headerName: "Fin de Reparación",
      width: 150,
    },

    { field: "total_cobro_rnd", headerName: "Total a Cobrar RND", width: 160 },
    { field: "total_cobro", headerName: "Total a Cobrar", width: 110 },
    { field: "reparadores_1", headerName: "Reparador 1", width: 90 },
    { field: "reparadores_2", headerName: "Reparador 2", width: 90 },
    { field: "reparadores_3", headerName: "Reparador 3", width: 90 },
    { field: "reparadores_cola", headerName: "Cola", width: 50 },
    { field: "aparato_x", headerName: "Aparato X", width: 150 },
  ];

  useEffect(() => {
    const fetchData = () => {
      try {
        resizeBy = axios.get("http://localhost:8000");
        setVectorEstado(res.data);
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, []);

  return (
    <div style={{ height: 300, width: "100%" }}>
      <DataGrid rows={rows} columns={columns} />
    </div>
  );
};

export default Table;
