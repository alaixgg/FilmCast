package com.example.filmcast.data.RetroFit

import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST

data class SeleccionData(
    val edad: String,
    val salario: String,
    val aniosAct: String,
    val likes: String,
    val belleza: String,
    val seguidores: String,
    val premios: String,
    val menciones: String,
    val tamañoPagina: String
)
interface ApiService {
    @POST("ruta_endpoint")
    fun enviarSeleccion(@Body data: SeleccionData): Call<Void>
}


data class Proyecto(
    val nombre: String,
    val descripcion: String,
    val genero: String,
    val fechaInicio: String,
    val fechaFin: String,
    val presupuesto: Double
)
interface enviarProyecto {
    @POST("ruta_endpoint")
    fun enviarSeleccion(@Body data: Proyecto): Call<Void>
}


data class RegistroRequest(
    val nombre: String,
    val clave: String,
    val des: String = "",
    val Pais: String = "",
    val telefono: String = "",
    val email: String = ""
)
interface RegistroApiService {
    @POST("/registro")
    suspend fun registrarUsuario(@Body request: RegistroRequest): Response<Void>
}

object RetrofitInstance {
    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl("https://db.cuspide.club/registro")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val api: ApiService by lazy {
        retrofit.create(ApiService::class.java)
    }
}


