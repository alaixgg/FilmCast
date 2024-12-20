package com.example.filmcast.ui.login

import ActoresAdapter
import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import com.example.filmcast.adapter.InfoPerfil
import com.example.filmcast.adapter.InfoPerfilAdapter
import okhttp3.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

class GuardadosActoresActivity : AppCompatActivity() {
    private lateinit var sharedPreferences: SharedPreferences
    private lateinit var token: String
    private lateinit var recyclerView: RecyclerView  // RecyclerView para mostrar los actores
    private lateinit var infoPerfilAdapter: InfoPerfilAdapter  // Adaptador para el RecyclerView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_actores_guardados)

        val res_perfil = findViewById<ImageView>(R.id.PA_perfil)
        res_perfil.setOnClickListener {
            val intent = Intent(this, PerfilActivity::class.java)
            startActivity(intent)
        }
        val res_menu = findViewById<ImageView>(R.id.Pa_menu)
        res_menu.setOnClickListener {
            val intent = Intent(this, PerfilActivity::class.java)
            startActivity(intent)
        }
        val resl_boton_volver = findViewById<Button>(R.id.resl_boton_volver)
        resl_boton_volver.setOnClickListener {
            val intent = Intent(this, ActivityBuscar::class.java)
            startActivity(intent)
        }



        // Inicializar RecyclerView
        recyclerView = findViewById(R.id.recyclerProfile)
        recyclerView.layoutManager = LinearLayoutManager(this)  // Usamos un LinearLayoutManager
        infoPerfilAdapter = InfoPerfilAdapter(emptyList())  // Inicializamos el adaptador vacío
        recyclerView.adapter = infoPerfilAdapter  // Asignamos el adaptador al RecyclerView

        // Obtener SharedPreferences
        sharedPreferences = getSharedPreferences("app_preferences", MODE_PRIVATE)
        Log.d("ActivityResultado", "SharedPreferences cargados correctamente.")

        // Recuperar los índices de los actores más cercanos
        val closestIndices = sharedPreferences.getStringSet("closest_indices", emptySet())
        Log.d("ActivityResultado", "Índices recuperados: $closestIndices")

        // Recuperar el token
        token = getTokenFromPreferences().toString()
        Log.d("ActivityResultado", "Token recuperado: $token")

        // Verificar que los datos son válidos antes de enviar
        if (token != null && closestIndices != null && closestIndices.isNotEmpty()) {
            Log.d("ActivityResultado", "Datos válidos para enviar: token y closestIndices no son nulos.")
            // Realizamos una petición por cada actor_id
            val actorProfiles = mutableListOf<InfoPerfil>()
            for (actorIdString in closestIndices) {
                val actorId = actorIdString.toIntOrNull()  // Convertir cada ID a entero
                if (actorId != null) {
                    Log.d("ActivityResultado", "Enviando solicitud para el actor con ID: $actorId")
                    obtenerInfoActor(actorId, token) { perfil ->
                        actorProfiles.add(perfil)  // Agregar el perfil al listado
                        // Actualizar el adaptador con los datos nuevos
                        infoPerfilAdapter = InfoPerfilAdapter(actorProfiles)
                        recyclerView.adapter = infoPerfilAdapter
                    }  // Llamada a la API para cada actor
                } else {
                    Log.e("ActivityResultado", "ID de actor inválido: $actorIdString")
                }
            }
        } else {
            Log.e("ActivityResultado", "Error: Token o closestIndices son nulos o vacíos.")
            Toast.makeText(this, "Datos incompletos. No se puede enviar la solicitud.", Toast.LENGTH_SHORT).show()
        }
    }

    // Método para obtener el token desde SharedPreferences
    private fun getTokenFromPreferences(): String? {
        val token = sharedPreferences.getString("token", null)
        Log.d("ActivityResultado", "Token recuperado de SharedPreferences: $token")
        return token
    }

    // Método para obtener la información de un actor por su ID
    private fun obtenerInfoActor(actorId: Int, token: String, onComplete: (InfoPerfil) -> Unit) {
        val url = "https://db.cuspide.club/info_actor/$actorId" // URL de la API con el actor_id
        Log.d("ActivityResultado", "Preparando solicitud para el actor ID: $actorId en la URL: $url")

        val client = OkHttpClient()

        // Crear la solicitud con el encabezado de autorización
        val request = Request.Builder()
            .url(url)
            .get()  // Usamos GET para obtener los datos del actor
            .addHeader("Authorization", "Bearer $token")  // Agregar el token al encabezado
            .build()

        Log.d("ActivityResultado", "Solicitud configurada. Enviando a la API para actor ID: $actorId.")

        // Enviar la solicitud
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e("ActivityResultado", "Error al enviar solicitud para el actor ID $actorId: ${e.message}")
                runOnUiThread {
                    Toast.makeText(this@GuardadosActoresActivity, "Error en la conexión para el actor $actorId: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    val responseData = response.body?.string()
                    Log.d("ActivityResultado", "Respuesta de la API para actor ID $actorId: $responseData")

                    // Aquí procesamos la respuesta de la API
                    try {
                        val jsonResponse = JSONObject(responseData)
                        val perfil = InfoPerfil(
                            infoNombre = jsonResponse.getString("name"),
                            infoGenero = jsonResponse.getString("gender"),
                            infoPrecio = jsonResponse.getString("income"),
                            infoFilm = jsonResponse.getString("genre_specialization")
                        )

                        // Pasamos el perfil al callback
                        runOnUiThread {
                            onComplete(perfil)  // Llamamos al callback con el perfil
                        }
                    } catch (e: Exception) {
                        Log.e("ActivityResultado", "Error al procesar los datos para el actor ID $actorId: ${e.message}")
                    }
                } else {
                    Log.e("ActivityResultado", "Error en la respuesta de la API para actor ID $actorId: ${response.message}")
                    runOnUiThread {
                        Toast.makeText(this@GuardadosActoresActivity, "Error en la API para actor $actorId", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }
}
