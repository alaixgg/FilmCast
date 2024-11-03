package com.example.filmcast

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.adapter.ProyectoAdapter
import com.example.filmcast.recycler.ProyectoProvider
import com.example.filmcast.recycler.Proyecto

class MenuActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_menu)
        initRecyclerView()
    }

    private fun initRecyclerView() {
        val recyclerView = findViewById<RecyclerView>(R.id.recyclerProyectos)
        recyclerView.layoutManager = LinearLayoutManager(
            this,
            LinearLayoutManager.HORIZONTAL,
            false
        )

        ProyectoProvider.obtenerProyecto { proyectos ->
            if (proyectos != null) {
                recyclerView.adapter = ProyectoAdapter(proyectos)
            } else {
                println("Error al obtener proyectos")
            }
        }
    }
}
