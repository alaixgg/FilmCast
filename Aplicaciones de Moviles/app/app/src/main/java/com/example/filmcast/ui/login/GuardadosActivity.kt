package com.example.filmcast.ui.login

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import com.example.filmcast.adapter.PerfilAdapter
import com.example.filmcast.recycler.PerfilProvider

class GuardadosActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_actores_lista)
        initRecyclerView()

        val btnBuscar = findViewById<Button>(R.id.menu_button_buscar)

        btnBuscar.setOnClickListener {
            val intent = Intent(this, ActivityBuscar::class.java)
            startActivity(intent)
        }

        val btnVolver = findViewById<Button>(R.id.GA_boton_volver)


    }

    private fun initRecyclerView(){
        val recyclerView = findViewById<RecyclerView>(R.id.recyclerProfile)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = PerfilAdapter(PerfilProvider.perfilList)
    }


}
