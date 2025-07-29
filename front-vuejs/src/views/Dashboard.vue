<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Lucymar_App</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">


      <!--Esto es el Menú: es una lista !!)-->
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Link</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Dropdown
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Action</a></li>
            <li><a class="dropdown-item" href="#">Another action</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <a class="nav-link" aria-disabled="true"></a>
        </li>
      </ul>
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"/>
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>

<footer>
  
</footer>


    <main class="grid-container">
      <div class="cuadrante" id="gastos">
        <GuardarGasto />
      </div>
      <div class="cuadrante" id="resultados">
        <EstadoResultados />
      </div>
      <div class="cuadrante" id="ingresos">
        <GuardarIngreso />
      </div>
      <div class="cuadrante" id="estadisticas">
        <Estadisticas />
      </div>
    </main>
  

  </template>
  
  <script setup>

  import GuardarGasto from './dashboard/GuardarGasto.vue'
  import EstadoResultados from './dashboard/EstadoResultados.vue'
  import GuardarIngreso from './dashboard/GuardarIngreso.vue'
  import Estadisticas from './dashboard/Estadisticas.vue'
  

  </script>
  