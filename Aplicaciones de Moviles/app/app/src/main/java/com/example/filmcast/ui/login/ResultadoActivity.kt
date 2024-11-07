package com.example.filmcast.ui.login


import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import okhttp3.*
import com.google.gson.Gson
import java.io.IOException

class ResultadoActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var actorAdapter: ActorAdapter
    private val actorList = mutableListOf<ActorItem>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_actores_resultado)

        recyclerView = findViewById(R.id.recyclerProfile)
        recyclerView.layoutManager = LinearLayoutManager(this)
        actorAdapter = ActorAdapter(actorList)
        recyclerView.adapter = actorAdapter

        // Llamada a la API para obtener los datos
        getActorPredictionData()
    }

    private fun getActorPredictionData() {
        val client = OkHttpClient()

        // URL de la API que devuelve los datos de predicción
        val url = "https://db.cuspide.club/info_actor" // Cambia a la URL real de tu API

        val request = Request.Builder()
            .url(url)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e("GuardadosActivity", "Error al obtener los datos: ${e.message}")
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    val responseBody = response.body?.string()

                    // Parsear la respuesta de la API a objetos
                    responseBody?.let { parseResponse(it) }
                } else {
                    Log.e("GuardadosActivity", "Error en la respuesta de la API")
                }
            }
        })
    }

    private fun parseResponse(responseBody: String) {
        val json = Gson().fromJson(responseBody, Map::class.java)

        // Extraemos los datos de la predicción
        val prediccion = json["predecir"] as Map<String, List<String>>

        // Convertimos los valores del map a un formato adecuado para los items del RecyclerView
        val keys = listOf(
            "Age", "Years Active", "Beauty", "Skill Level", "Award Wins",
            "Media Mentions", "Social Media Followers", "Social Media Likes",
            "Network Size", "Income"
        )

        keys.forEach { key ->
            val values = prediccion[key]?.map { it.replace("[", "").replace("]", "") } ?: emptyList()
            if (values.isNotEmpty()) {
                val actorItem = ActorItem(
                    nombre = key,
                    valorMinimo = values[0],
                    valorMaximo = values.getOrElse(1) { "N/A" }
                )
                actorList.add(actorItem)
            }
        }

        // Duplicamos los datos como mencionaste
        val duplicatedList = actorList.toMutableList()
        actorList.addAll(duplicatedList) // Duplicamos los actores

        // Actualizamos el RecyclerView con los datos
        runOnUiThread {
            actorAdapter.notifyDataSetChanged()
        }
    }

    // Adapter para el RecyclerView
    inner class ActorAdapter(private val actorList: List<ActorItem>) : RecyclerView.Adapter<ActorAdapter.ActorViewHolder>() {

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ActorViewHolder {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.item_perfil, parent, false)
            return ActorViewHolder(view)
        }

        override fun onBindViewHolder(holder: ActorViewHolder, position: Int) {
            val actorItem = actorList[position]
            holder.bind(actorItem)
        }

        override fun getItemCount(): Int {
            return actorList.size
        }

        inner class ActorViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
            private val tvNombre: TextView = itemView.findViewById(R.id.tv_nombre)
            private val tvGenero: TextView = itemView.findViewById(R.id.tv_genero)

            fun bind(actorItem: ActorItem) {
                tvNombre.text = actorItem.nombre
                tvGenero.text = "Min: ${actorItem.valorMinimo}, Max: ${actorItem.valorMaximo}"
            }
        }
    }

    // Modelo de los datos de los actores, sin necesidad de crear una clase aparte
    data class ActorItem(val nombre: String, val valorMinimo: String, val valorMaximo: String)
}