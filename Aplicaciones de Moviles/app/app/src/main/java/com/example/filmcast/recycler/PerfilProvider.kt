package com.example.filmcast.recycler

import okhttp3.*
import org.json.JSONArray
import java.io.IOException



class PerfilProvider {
    companion object {
        private const val SERVER_URL = "https://db.cuspide.club/mis_favoritos"
        private val client = OkHttpClient()
        var perfilList = mutableListOf<Perfil>()

        fun fetchFavoritos(token: String, onResult: (List<Perfil>) -> Unit, onError: (String) -> Unit) {
            // Crear solicitud GET con el token en el encabezado de autorización
            val request = Request.Builder()
                .url(SERVER_URL)
                .addHeader("Authorization", "Bearer $token")
                .build()

            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    onError(e.message ?: "Error de red")
                }

                override fun onResponse(call: Call, response: Response) {
                    response.body?.string()?.let { responseBody ->
                        if (response.isSuccessful) {
                            val favoritos = parseJsonToPerfilList(responseBody)
                            perfilList.clear()
                            perfilList.addAll(favoritos)
                            onResult(perfilList)
                        } else {
                            onError("Error al obtener favoritos: ${response.message}")
                        }
                    } ?: onError("Error en la respuesta del servidor")
                }
            })
        }

        private fun parseJsonToPerfilList(json: String): List<Perfil> {
            val perfiles = mutableListOf<Perfil>()
            val jsonArray = JSONArray(json)

            for (i in 0 until jsonArray.length()) {
                val jsonObject = jsonArray.getJSONObject(i)
                val perfil = Perfil(
                    nombre = jsonObject.getString("nombre"),
                    genero = jsonObject.getString("genero"),
                    precio = jsonObject.getString("precio"),
                    generoCine = jsonObject.getString("generoCine")
                )
                perfiles.add(perfil)
            }
            return perfiles
        }
    }
}
