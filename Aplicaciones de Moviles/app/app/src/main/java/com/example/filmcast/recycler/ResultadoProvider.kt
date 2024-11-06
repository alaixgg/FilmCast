package com.example.filmcast.recycler

import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import org.json.JSONObject
import java.io.IOException

class ResultadoProvider {
    companion object {
        private const val SERVER_URL = "https://db.cuspide.club/info_actor" // Endpoint para obtener la info del actor
        private val client = OkHttpClient()
        var perfilList = mutableListOf<Perfil>()

        // Esta función obtiene los detalles de los actores usando sus IDs
        fun fetchActorDetails(actorIds: List<String>, onResult: (List<Perfil>) -> Unit, onError: (String) -> Unit) {
            val requestBuilder = Request.Builder()

            // Iteramos sobre los IDs de los actores y realizamos una solicitud por cada uno
            for (actorId in actorIds) {
                val request = requestBuilder
                    .url("$SERVER_URL$actorId") // Concatenamos el ID del actor con el URL base
                    .build()

                client.newCall(request).enqueue(object : Callback {
                    override fun onFailure(call: Call, e: IOException) {
                        onError("Error de red al obtener los detalles del actor $actorId: ${e.message}")
                    }

                    override fun onResponse(call: Call, response: Response) {
                        if (response.isSuccessful) {
                            val responseData = response.body?.string()
                            val perfil = parseJsonToPerfil(responseData)

                            // Si el actor es válido, lo agregamos a la lista
                            if (perfil != null) {
                                perfilList.add(perfil)
                            }

                            // Llamamos a onResult después de obtener todos los actores
                            if (actorIds.size == perfilList.size) {
                                onResult(perfilList)
                            }
                        } else {
                            onError("Error al obtener el detalle del actor $actorId: ${response.message}")
                        }
                    }
                })
            }
        }

        // Esta función es para parsear la respuesta JSON a un objeto Perfil
        private fun parseJsonToPerfil(json: String?): Perfil? {
            if (json.isNullOrEmpty()) return null

            try {
                val jsonObject = JSONObject(json)
                return Perfil(
                    nombre = jsonObject.getString("nombre"),
                    genero = jsonObject.getString("genero"),
                    precio = jsonObject.getString("precio"),
                    generoCine = jsonObject.getString("generoCine")
                )
            } catch (e: Exception) {
                return null
            }
        }
    }
}