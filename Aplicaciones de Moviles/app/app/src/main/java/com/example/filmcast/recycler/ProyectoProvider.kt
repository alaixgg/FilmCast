package com.example.filmcast.recycler

import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import org.json.JSONArray
import java.io.IOException

class ProyectoProvider {

    companion object {
        private val client = OkHttpClient()
        private val url = "https://linkendpoint.com"

        fun obtenerProyecto(callback: (List<Proyecto>?) -> Unit) {
            val request = Request.Builder()
                .url(url)
                .build()

            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    e.printStackTrace()
                    callback(null) // Llama al callback con null en caso de error
                }

                override fun onResponse(call: Call, response: Response) {
                    if (response.isSuccessful) {
                        response.body?.let { responseBody ->
                            val jsonString = responseBody.string()
                            val jsonArray = JSONArray(jsonString)
                            val proyectosList = mutableListOf<Proyecto>()

                            for (i in 0 until jsonArray.length()) {
                                val jsonObject = jsonArray.getJSONObject(i)
                                val proyecto = Proyecto(
                                    tituloProyecto = jsonObject.getString("tituloProyecto"),
                                    fecha = jsonObject.getString("fecha"),
                                    ubicacion = jsonObject.getString("ubicacion"),
                                    mensaje = jsonObject.getString("mensajes")
                                )
                                proyectosList.add(proyecto)
                            }
                            callback(proyectosList)
                        } ?: callback(null)
                    } else {
                        callback(null)
                    }
                }
            })
        }
    }
}
