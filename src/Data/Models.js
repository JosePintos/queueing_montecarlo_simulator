class Aparato {
  static #lastId = 0;

  #id;
  #estado;
  #tiempo_llegada;

  constructor(estado, tiempo_llegada) {
    this.#id = ++Aparato.#lastId;
    this.#estado = estado;
    this.#tiempo_llegada = tiempo_llegada;
  }

  getId() {
    return this.#id;
  }

  getEstado() {
    return this.#estado;
  }

  setEstado(value) {
    this.#estado = value;
  }

  getTiempoLlegada() {
    return this.#tiempo_llegada;
  }

  setTiempoLlegada(value) {
    this.#tiempo_llegada = value;
  }
}

class Reparador {
  static #cola = 0;
  static #lastId = 0;
  #estado;
  #id;

  constructor(estado, id) {
    this.#estado = estado;
    this.#id = ++Reparador.#lastId;
  }

  getEstado() {
    return this.#estado;
  }
  setEstado(value) {
    this.#estado = value;
  }

  getId() {
    return this.#id;
  }

  static getCola() {
    return Reparador.#cola;
  }
  static setCola(value) {
    Reparador.#cola = value;
  }
}
