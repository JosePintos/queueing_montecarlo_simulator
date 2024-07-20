import "./Input.css";
import { MdOutlineTimer } from "react-icons/md";
import { RiMoneyDollarCircleFill } from "react-icons/ri";

const Input = () => {
  return (
    <div className="questions section container">
      <div className="secContainer grid">
        <div className="form">
          <div className="secHeading">
            <h3>Ingrese los parametros de la simulación</h3>
          </div>
          <div className="formContent flex">
            <div className="inputContainer">
              <MdOutlineTimer className="icon" />
              <input
                type="text"
                className="inputIcon"
                placeholder="horas a simular"
              />
            </div>
            <div className="inputContainer">
              <RiMoneyDollarCircleFill className="icon" />
              <input
                type="text"
                className="inputIcon"
                placeholder="min precio"
              />
            </div>
            <div className="inputContainer">
              <RiMoneyDollarCircleFill className="icon" />
              <input
                type="text"
                className="inputIcon"
                placeholder="max precio"
              />
            </div>

            <button className="btn">Simular</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Input;
