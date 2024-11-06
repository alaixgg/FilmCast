package com.example.filmcast.ui.login

import android.content.SharedPreferences
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import kotlinx.coroutines.*
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import org.json.JSONObject

class GuardadosActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var perfilAdapter: PerfilAdapter
    private val perfilList = mutableListOf<Map<String, String>>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_actores_lista)


        initRecyclerView()


        val token = getTokenFromPreferences()

        if (token != null) {

            fetchActorInfo(token)
        } else {
            Toast.makeText(this, "No se ha encontrado el token de sesión.", Toast.LENGTH_SHORT).show()
        }
    }

    private fun initRecyclerView() {
        recyclerView = findViewById(R.id.recyclerProfile)
        recyclerView.layoutManager = LinearLayoutManager(this)
        perfilAdapter = PerfilAdapter(perfilList)
        recyclerView.adapter = perfilAdapter
    }

    private fun fetchActorInfo(token: String) {
        val actorId = 1

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val client = OkHttpClient()
                val request = Request.Builder()
                    .url("https://db.cuspide.club/info_actor/$actorId")
                    .addHeader("Authorization", "Bearer $token")
                    .build()


                val response: Response = client.newCall(request).execute()

                if (response.isSuccessful) {
                    val responseBody = response.body?.string()
                    val actorInfo = parseActorInfo(responseBody)


                    withContext(Dispatchers.Main) {
                        perfilList.clear()
                        perfilList.add(actorInfo)
                        perfilAdapter.notifyDataSetChanged()
                    }
                } else {
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@GuardadosActivity, "Error al obtener los datos", Toast.LENGTH_SHORT).show()
                    }
                }

            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    Toast.makeText(this@GuardadosActivity, "Excepción: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    private fun parseActorInfo(responseBody: String?): Map<String, String> {
        val actorMap = mutableMapOf<String, String>()

        try {
            val json = JSONObject(responseBody)
            actorMap["name"] = json.optString("name", "N/A")
            actorMap["gender"] = json.optString("gender", "N/A")
            actorMap["price"] = json.optString("price", "N/A")
            actorMap["movieGenre"] = json.optString("movieGenre", "N/A")
        } catch (e: Exception) {
            e.printStackTrace()
        }

        return actorMap
    }

    private fun getTokenFromPreferences(): String? {
        val sharedPreferences = getSharedPreferences("app_preferences", MODE_PRIVATE)
        return sharedPreferences.getString("token", null)
    }

    inner class PerfilAdapter(private val perfilList: List<Map<String, String>>) : RecyclerView.Adapter<PerfilAdapter.PerfilViewHolder>() {

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PerfilViewHolder {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.item_perfil, parent, false)
            return PerfilViewHolder(view)
        }

        override fun onBindViewHolder(holder: PerfilViewHolder, position: Int) {
            val actor = perfilList[position]
            holder.bind(actor)
        }

        override fun getItemCount(): Int = perfilList.size

        inner class PerfilViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
            private val tvNombre: TextView = itemView.findViewById(R.id.tv_nombre)
            private val tvGenero: TextView = itemView.findViewById(R.id.tv_genero)
            private val tvPrecio: TextView = itemView.findViewById(R.id.tv_precio)
            private val tvGeneroPelicula: TextView = itemView.findViewById(R.id.tv_genero_pelicula)

            fun bind(actor: Map<String, String>) {
                tvNombre.text = actor["name"]
                tvGenero.text = actor["gender"]
                tvPrecio.text = actor["price"]
                tvGeneroPelicula.text = actor["movieGenre"]
            }
        }
    }
}
