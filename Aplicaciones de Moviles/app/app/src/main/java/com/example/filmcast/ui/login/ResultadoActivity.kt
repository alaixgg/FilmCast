package com.example.filmcast.ui.login

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import com.example.filmcast.adapter.InfoPerfil
import com.example.filmcast.adapter.InfoPerfilAdapter
import com.example.filmcast.adapter.InfoPerfilProvider

class ResultadoActivity : AppCompatActivity() {

    private val TAG = "ActivityActoresResultado"  // Definimos un tag para los logs

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_actores_resultado)

        Log.d(TAG, "onCreate: Actividad iniciada.")

        val recyclerView = findViewById<RecyclerView>(R.id.recyclerProfile)
        recyclerView.layoutManager = LinearLayoutManager(this)

        // Obtener el token de SharedPreferences
        val token = getSharedPreferences("app_preferences", MODE_PRIVATE).getString("token", null)
        Log.d(TAG, "onCreate: Token obtenido: $token")

        if (token != null) {
            Log.d(TAG, "onCreate: Token encontrado. Iniciando solicitud de perfiles.")
            val infoPerfilProvider = InfoPerfilProvider(this)
            infoPerfilProvider.getActorProfiles(token) { actorProfiles ->
                Log.d(TAG, "onCreate: Datos de actores recibidos. Cantidad de perfiles: ${actorProfiles.size}")

                // Actualizar el RecyclerView con la lista de perfiles
                runOnUiThread {
                    recyclerView.adapter = InfoPerfilAdapter(actorProfiles)
                    Log.d(TAG, "onCreate: Adaptador asignado al RecyclerView.")
                }
            }
        } else {
            Log.e(TAG, "onCreate: Token no encontrado.")
        }
    }
}