package com.example.filmcast.ui.login

import ActoresAdapter
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import okhttp3.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

class GuardadosActoresActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var actoresAdapter: ActoresAdapter
    private val client = OkHttpClient()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_actores_guardados)

        recyclerView = findViewById(R.id.recyclerProfile)
        recyclerView.layoutManager = LinearLayoutManager(this)

        // Realiza la consulta a la API
        fetchActoresData()
    }

    // Método para hacer la solicitud a la API y obtener los datos
    private fun fetchActoresData() {
        val url = "https://tu-api.com/actores_guardados"  // Cambia esta URL por la URL real de tu API
        val request = Request.Builder().url(url).build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    Toast.makeText(this@GuardadosActoresActivity, "Error de red: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    val jsonResponse = response.body?.string()
                    runOnUiThread {
                        parseActoresData(jsonResponse)
                    }
                } else {
                    runOnUiThread {
                        Toast.makeText(this@GuardadosActoresActivity, "Error al obtener datos", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }

    // Método para parsear la respuesta JSON y actualizar el RecyclerView
    private fun parseActoresData(jsonResponse: String?) {
        val actoresList = mutableListOf<Map<String, Any>>()

        try {
            val jsonArray = JSONArray(jsonResponse)
            for (i in 0 until jsonArray.length()) {
                val actorJson = jsonArray.getJSONObject(i)
                val actor = mapOf(
                    "id" to actorJson.getString("id"),
                    "nombre" to actorJson.getString("nombre"),
                    "imagen" to actorJson.getString("imagen")
                )
                actoresList.add(actor)
            }

            actoresAdapter = ActoresAdapter(actoresList) { actor ->
                // Aquí lanzamos el Intent para abrir el perfil del actor
                val intent = Intent(this, ActorActivity::class.java).apply {
                    putExtra("ACTOR_ID", actor["id"] as String)
                }
                startActivity(intent)
            }

            recyclerView.adapter = actoresAdapter

        } catch (e: Exception) {
            Log.e("GuardadosActoresActivity", "Error al parsear datos: ${e.message}")
        }
    }
}

