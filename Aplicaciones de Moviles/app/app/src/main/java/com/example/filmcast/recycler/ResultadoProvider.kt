package com.example.filmcast.recycler

import android.widget.Toast
import com.google.gson.Gson
import okhttp3.Call
import okhttp3.Callback
import okhttp3.Headers
import okhttp3.Headers.Companion.toHeaders
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import org.json.JSONException
import org.json.JSONObject
import java.io.IOException

class ResultadoProvider {
    companion object {
        private const val SERVER_URL = "https://db.cuspide.club/info_actor"
        private val client = OkHttpClient()

        // Lista local de perfiles
        var perfilList = mutableListOf<Perfil>()

        // Función para obtener la información de un actor
        fun getActorInfo(
            actorId: String,
            headers: Map<String, String>,
            onResult: (Perfil?) -> Unit,
            onError: (String) -> Unit
        ) {
            // Construir la solicitud GET con el actorId y los headers
            val request = Request.Builder()
                .url("$SERVER_URL/$actorId")
                .headers(headers.toHeaders())
                .build()

            // Ejecutar la solicitud
            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    onError("Error de red: ${e.message ?: "desconocido"}")
                }

                override fun onResponse(call: Call, response: Response) {
                    if (response.isSuccessful) {
                        response.body?.string()?.let { responseBody ->
                            val perfil = parseJsonToPerfil(responseBody)
                            if (perfil != null) {
                                // Añadir el perfil a la lista
                                perfilList.add(perfil)
                            }
                            onResult(perfil)
                        } ?: onError("Respuesta vacía del servidor")
                    } else {
                        onError("Error al obtener información del actor: ${response.message}")
                    }
                }
            })
        }

        // Función para convertir el JSON de respuesta en un objeto Perfil
        private fun parseJsonToPerfil(json: String): Perfil? {
            return try {
                val jsonObject = JSONObject(json)
                // Aquí extraemos los datos del JSON y los usamos para crear el objeto Perfil
                Perfil(
                    nombre = jsonObject.getString("nombre"),
                    genero = jsonObject.getString("genero"),
                    precio = jsonObject.getString("precio"),
                    generoCine = jsonObject.getString("generoCine")
                )
            } catch (e: JSONException) {
                null // Si hay un error en el parseo, devolvemos null
            }
        }
    }
}
