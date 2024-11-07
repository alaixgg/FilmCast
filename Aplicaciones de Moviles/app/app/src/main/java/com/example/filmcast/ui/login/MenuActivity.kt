package com.example.filmcast.ui.login

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import com.example.filmcast.adapter.ProyectoAdapter
import com.example.filmcast.recycler.ProyectoProvider

class MenuActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_menu)
        initRecyclerView()

        val menu_perfil = findViewById<ImageView>(R.id.menu_titulo_perfil)
        menu_perfil.setOnClickListener {
            val intent = Intent(this, PerfilActivity::class.java)
            startActivity(intent)
        }
        val menu_buscar = findViewById<Button>(R.id.menu_button_buscar)
        menu_buscar.setOnClickListener {
            val intent = Intent(this, ActivityBuscar::class.java)
            startActivity(intent)
        }
        val menu_gestionar = findViewById<Button>(R.id.menu_button_guardados)
        menu_gestionar.setOnClickListener {
            val intent = Intent(this, GuardadosActoresActivity::class.java)
            startActivity(intent)
        }

        val menu_crear_pr = findViewById<Button>(R.id.menu_button_crear_pr)
        menu_crear_pr.setOnClickListener {
            val intent = Intent(this, Crea_proyecto::class.java)
            startActivity(intent)
        }
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