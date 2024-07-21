import { DataGrid } from "@mui/x-data-grid";
import { useEffect, useState } from "react";
import axios from "axios";

const PAGE_SIZE = 25;

const Table = () => {
  const [rows, setRows] = useState([]);
  const [page, setPage] = useState(0);

  const columns = [
    { field: "id", headerName: "Hora", width: 150 },
    { field: "evento", headerName: "Evento", width: 160 },
    {
      field: "llegada_aparato",
      headerName: "Llegada Aparato",
      width: 120,
    },
    {
      field: "fin_reparacion_1",
      headerName: "Fin de Reparación 1",
      width: 150,
    },
    {
      field: "fin_reparacion_2",
      headerName: "Fin de Reparación 2",
      width: 150,
    },
    {
      field: "fin_reparacion_3",
      headerName: "Fin de Reparación 3",
      width: 150,
    },
    { field: "monto_cobro", headerName: "Total a Cobrar", width: 110 },
    { field: "reparador_1", headerName: "Reparador 1", width: 90 },
    { field: "reparador_2", headerName: "Reparador 2", width: 90 },
    { field: "reparador_3", headerName: "Reparador 3", width: 90 },
    { field: "cola", headerName: "Cola", width: 50 },
    { field: "aparatos", headerName: "Aparatos", width: 200 },
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get("http://localhost:8000/simulacion", {
          params: { offset: page * PAGE_SIZE, limit: PAGE_SIZE, horas: 2 },
        });
        setRows(res.data);
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [page]);

  return (
    <div style={{ height: "100%", width: "100%" }}>
      <DataGrid rows={rows} columns={columns} />
    </div>
  );
};

export default Table;
