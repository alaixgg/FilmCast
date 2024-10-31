package com.example.filmcast.ui.login

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R

class menuActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_menu)

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
            val intent = Intent(this, GuardadosActivity::class.java)
            startActivity(intent)
        }

    }
}