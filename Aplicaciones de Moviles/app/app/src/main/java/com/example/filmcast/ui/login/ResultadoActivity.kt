package com.example.filmcast.ui.login

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import com.example.filmcast.adapter.PerfilAdapter
import com.example.filmcast.recycler.ResultadoProvider
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ResultadoActivity : AppCompatActivity() {
    private lateinit var actorIds: List<String>
    private lateinit var token: String

    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_actores_resultado)

        token = "your_jwt_token_here"

        val actorId = intent.getIntExtra("ACTOR_ID", -1)
        if (actorId != -1){
            fetchActorInfo(actorId)
        }


        initRecyclerView()

        actorIds = intent.getStringArrayListExtra("ACTOR_IDS") ?: emptyList()

        val btnVolver = findViewById<Button>(R.id.resl_boton_volver)
        btnVolver.setOnClickListener {
            val intent = Intent(this, ActivityBuscar::class.java)
            startActivity(intent)
        }
    }

    private fun fetchActorInfo(actorId: Int) {
        val call = RetrofirInstace.api.getActorInfo(actorId, "Bearer $token")
        call.enqueue(object : Callback<ActorInfoResponse> {
            override fun onResponse(call: Call<ActorInfoResponse>, response: Response<ActorInfoResponse>) {
                if (response.isSuccessful) {
                    // Handle the actor information
                    val actorInfo = response.body()
                    actorInfo?.let {
                        // Update your UI with actor information
                        Toast.makeText(this@ResultadoActivity, "Actor: ${it.email}", Toast.LENGTH_LONG).show()
                    }
                } else {
                    // Handle the case where the actor is not found
                    Toast.makeText(this@ResultadoActivity, "Actor not found", Toast.LENGTH_LONG).show()
                }
            }

            override fun onFailure(call: Call<ActorInfoResponse>, t: Throwable) {
                // Handle failure in the network request
                Toast.makeText(this@ResultadoActivity, "Failed to fetch actor info", Toast.LENGTH_LONG).show()
            }
        })
    }

    private fun initRecyclerView() {
        val recyclerView = findViewById<RecyclerView>(R.id.recycler_profile)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = PerfilAdapter(ResultadoProvider.perfilList)
    }
}