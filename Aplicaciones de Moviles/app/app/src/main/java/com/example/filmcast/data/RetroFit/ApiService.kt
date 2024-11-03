package com.example.filmcast.data.RetroFit

import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST

// Data class para la selección de actor
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

// Data class para la creación de proyectos
data class Proyecto(
    val nombre: String,
    val descripcion: String,
    val genero: String,
    val fechaInicio: String,
    val fechaFin: String,
    val presupuesto: Double
)

// Data class para el registro de usuario
data class RegistroRequest(
    val nombre: String,
    val clave: String,
    val des: String = "",
    val Pais: String = "",
    val telefono: String = "",
    val email: String = ""
)

// Data class para guardar perfil
data class PerfilRequest(
    val nombre: String,
    val descripcion: String,
    val telefono: String,
    val nacionalidad: String,
    val email: String
)

// Interfaz principal de la API
interface ApiService {

    // Endpoint para buscar actor
    @POST("ruta_endpoint_seleccion") // Cambia esta ruta
    fun enviarSeleccion(@Body data: SeleccionData): Call<Void>

    // Endpoint para crear proyecto
    @POST("ruta_endpoint_proyecto") // Cambia esta ruta
    fun enviarProyecto(@Body proyecto: Proyecto): Call<Void>

    // Endpoint para registro
    @POST("/registro")
    suspend fun registrarUsuario(@Body request: RegistroRequest): Response<Void>

    // Endpoint para guardar perfil
    @POST("ruta/de/la/api") // Cambia esta ruta
    fun guardarPerfil(@Body perfil: PerfilRequest): Call<Void>
}

// Objeto de instancia de Retrofit
object RetrofitInstance {
    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl("https://db.cuspide.club/") // Cambia la URL base según tu configuración
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val api: ApiService by lazy {
        retrofit.create(ApiService::class.java)
    }
}
