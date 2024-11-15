package com.example.filmcast.adapter

import android.content.Context
import android.content.SharedPreferences
import android.util.Log
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject

class InfoPerfilProvider(private val context: Context) {

    private val sharedPreferences: SharedPreferences =
        context.getSharedPreferences("app_preferences", Context.MODE_PRIVATE)

    private val TAG = "InfoPerfilProvider"  // Tag para los logs

    fun getActorProfiles(actorIds: List<String>, token: String, onComplete: (List<InfoPerfil>) -> Unit) {
        Log.d(TAG, "getActorProfiles: Iniciando la obtención de perfiles de actores.")

        val client = OkHttpClient()
        val actorProfiles = mutableListOf<InfoPerfil>()

        // Verificar si no hay actores guardados
        if (actorIds.isEmpty()) {
            Log.e(TAG, "getActorProfiles: No se encontraron IDs de actores.")
            return
        }

        // Recorrer los IDs de actores y obtener sus detalles
        for (actorId in actorIds) {
            Log.d(TAG, "getActorProfiles: Recuperando datos del actor con ID: $actorId")
            val request = Request.Builder()
                .url("https://model.cuspide.club/info_actor/$actorId")
                .addHeader("Authorization", "Bearer $token")
                .build()

            try {
                client.newCall(request).execute().use { response ->
                    if (response.isSuccessful) {
                        response.body?.string()?.let { responseBody ->
                            try {
                                val jsonResponse = JSONObject(responseBody)

                                // Extraer los datos que necesitas
                                val perfil = InfoPerfil(
                                    infoNombre = jsonResponse.getString("name"),
                                    infoGenero = jsonResponse.getString("gender"),
                                    infoPrecio = jsonResponse.getString("salary"),
                                    infoFilm = jsonResponse.getString("genre_specialization")
                                )
                                actorProfiles.add(perfil)
                                Log.d(TAG, "getActorProfiles: Perfil agregado para el actor ID: $actorId")
                            } catch (e: Exception) {
                                Log.e(TAG, "getActorProfiles: Error al parsear la respuesta para el actor ID: $actorId, Error: ${e.message}")
                            }
                        }
                    } else {
                        Log.e(TAG, "getActorProfiles: Error al obtener datos para el actor ID: $actorId. Código de respuesta: ${response.code}")
                    }
                }
            } catch (e: Exception) {
                Log.e(TAG, "getActorProfiles: Error en la solicitud para el actor ID: $actorId, Error: ${e.message}")
            }
        }

        // Enviar los perfiles al callback
        Log.d(TAG, "getActorProfiles: Enviando los datos de actores obtenidos al callback.")
        onComplete(actorProfiles)
    }
}
