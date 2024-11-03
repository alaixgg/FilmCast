package com.example.filmcast.recycler

import okhttp3.*
import org.json.JSONArray
import java.io.IOException



class PerfilProvider {
    companion object{
        private const val SERVER_URL = "direccion.com"
        private val client = OkHttpClient()
        var perfilList = mutableListOf<Perfil>()

        fun fetchPerfiles(onResult: (List<Perfil>) -> Unit, onError: (String) -> Unit){
            val request = Request.Builder()
                .url(SERVER_URL)
                .build()

            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    onError(e.message ?: "Error de red")
                }

                override fun onResponse(call: Call, response: Response) {
                    response.body?.string()?.let { responseBody ->
                        val perfiles = parseJsonToPerfilList(responseBody)
                        perfilList.clear()
                        perfilList.addAll(perfiles)
                        onResult(perfilList)
                    } ?: onError("Error en la respuesta del servidor")
                }
            })
        }

        private fun parseJsonToPerfilList(json: String): List<Perfil>{
            val perfiles = mutableListOf<Perfil>()
            val jsonArray = JSONArray(json)

            for (i in 0 until jsonArray.length()) {
                val jsonObject = jsonArray.getJSONObject(i)
                val perfil = Perfil(
                    nombre = jsonObject.getString("nombre"),
                    genero = jsonObject.getString("genero"),
                    precio = jsonObject.getString("precio"),
                    generoCine = jsonObject.getString("generoCine"),
                    foto = jsonObject.getString("foto")
                )
                perfiles.add(perfil)
            }
            return perfiles
        }

    }
}