package com.example.filmcast.data.RetroFit

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

data class SeleccionData(
    val edad: String,
    val generoCine: String,
    val educacion: String,
    val salario: String,
    val aniosAct: String,
    val genero: String,
    val likes: String,
    val belleza: String,
    val seguidores: String,
    val nacionalidad: String,
    val premios: String,
    val menciones: String,
    val tamañoPagina: String
)

interface ApiService {
    @POST("ruta_endpoint")
    fun enviarSeleccion(@Body data: SeleccionData): Call<Void>
}
