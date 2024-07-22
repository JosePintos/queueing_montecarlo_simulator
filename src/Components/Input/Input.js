import React, { useState } from "react";
import "./Input.css";
import { MdOutlineTimer } from "react-icons/md";
import { RiMoneyDollarCircleFill } from "react-icons/ri";
import { IoHourglassOutline, IoEnter } from "react-icons/io5";

const Input = ({ onSimulate }) => {
  const [formData, setFormData] = useState({
    horas: 8,
    maxPrecio: "",
    minPrecio: "",
    minTiempo: "",
    maxTiempo: "",
    media: "",
  });

  const [errors, setErrors] = useState({});

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const validateInputs = () => {
    const newErrors = {};
    if (!formData.horas || isNaN(formData.horas)) {
      newErrors.horas = "Ingrese un número";
    }
    if (formData.maxPrecio && isNaN(formData.maxPrecio)) {
      newErrors.maxPrecio = "Ingrese un número";
    }
    if (formData.minPrecio && isNaN(formData.minPrecio)) {
      newErrors.minPrecio = "Ingrese un número";
    }
    if (formData.minTiempo && isNaN(formData.minTiempo)) {
      newErrors.minTiempo = "Ingrese un número";
    }
    if (formData.maxTiempo && isNaN(formData.maxTiempo)) {
      newErrors.maxTiempo = "Ingrese un número";
    }
    if (formData.media && isNaN(formData.media)) {
      newErrors.media = "Ingrese un número";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSimulate = () => {
    if (validateInputs()) {
      onSimulate({
        horas: parseFloat(formData.horas),
        precio_min: formData.minPrecio
          ? parseFloat(formData.minPrecio)
          : undefined,
        precio_max: formData.maxPrecio
          ? parseFloat(formData.maxPrecio)
          : undefined,
        tiempo_min: formData.minTiempo
          ? parseFloat(formData.minTiempo)
          : undefined,
        tiempo_max: formData.maxTiempo
          ? parseFloat(formData.maxTiempo)
          : undefined,
        media: formData.media ? parseFloat(formData.media) : undefined,
      });
    }
  };
  return (
    <div className="questions section container">
      <div className="secContainer grid">
        <div className="form">
          <div className="secHeading">
            <h3>Ingrese los parametros de la simulación</h3>
          </div>
          <div className="formContent flex">
            <div className="horaSimulacion">
              <div className="inputContainer">
                <MdOutlineTimer className="icon" />
                <input
                  type="text"
                  className="inputIcon"
                  name="horas"
                  placeholder="horas a simular"
                  value={formData.horas}
                  onChange={handleInputChange}
                />
                {errors.horas && <span className="error">{errors.horas}</span>}
              </div>
            </div>
            <div className="precioSimulacion">
              <div className="inputContainer">
                <RiMoneyDollarCircleFill className="icon" />
                <input
                  type="text"
                  className="inputIcon"
                  name="minPrecio"
                  placeholder="min precio"
                  value={formData.minPrecio}
                  onChange={handleInputChange}
                />
                {errors.minPrecio && (
                  <span className="error">{errors.minPrecio}</span>
                )}
              </div>
              <div className="inputContainer">
                <RiMoneyDollarCircleFill className="icon" />
                <input
                  type="text"
                  className="inputIcon"
                  name="maxPrecio"
                  placeholder="max precio"
                  value={formData.maxPrecio}
                  onChange={handleInputChange}
                />
                {errors.maxPrecio && (
                  <span className="error">{errors.maxPrecio}</span>
                )}
              </div>
            </div>
            <div className="reparacionFin">
              <div className="inputContainer">
                <IoHourglassOutline className="icon" />
                <input
                  type="text"
                  className="inputIcon"
                  name="minTiempo"
                  placeholder="tiempo min reparacion"
                  value={formData.minTiempo}
                  onChange={handleInputChange}
                />
                {errors.minTiempo && (
                  <span className="error">{errors.minTiempo}</span>
                )}
              </div>
              <div className="inputContainer">
                <IoHourglassOutline className="icon" />
                <input
                  type="text"
                  className="inputIcon"
                  name="maxTiempo"
                  placeholder="tiempo max reparacion"
                  value={formData.maxTiempo}
                  onChange={handleInputChange}
                />
                {errors.maxTiempo && (
                  <span className="error">{errors.maxTiempo}</span>
                )}
              </div>
            </div>
            <div className="mediaLlegada">
              <div className="inputContainer">
                <IoEnter className="icon" />
                <input
                  type="text"
                  className="inputIcon"
                  name="media"
                  placeholder="llegada media"
                  value={formData.media}
                  onChange={handleInputChange}
                />
                {errors.media && <span className="error">{errors.media}</span>}
              </div>
            </div>
            <button className="btn" onClick={handleSimulate}>
              Simular
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Input;
